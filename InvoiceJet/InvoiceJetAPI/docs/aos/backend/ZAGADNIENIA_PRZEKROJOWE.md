# Zagadnienia przekrojowe — InvoiceJetAPI

**Data aktualizacji:** 2026-05-31

---

## 1. Uwierzytelnianie i autoryzacja (JWT)

Kotwica: `Program.cs`, `AuthService.cs › AuthService.CreateToken`

| Element | Wartość |
|---|---|
| Schemat | `JwtBearerDefaults.AuthenticationScheme` |
| Klucz podpisu | `AppSettings:Token` (z `appsettings.json`) — klucz symetryczny |
| Algorytm podpisu | `HmacSha512Signature` |
| Walidacja podpisu | `ValidateIssuerSigningKey = true` |
| Walidacja issuer | `ValidateIssuer = false` |
| Walidacja audience | `ValidateAudience = false` |
| Walidacja czasu życia | `ValidateLifetime = true` |
| Tolerancja zegara | `ClockSkew = TimeSpan.Zero` (zero — token wygasa dokładnie po 10 min) |
| Mapowanie roszczeń | `MapInboundClaims = false` (claimy odczytywane po oryginalnych nazwach) |
| Czas ważności | `DateTime.UtcNow.AddMinutes(10)` |

Claimy w tokenie (`AuthService.cs › AuthService.CreateToken`):

| Typ roszczenia | Wartość | Źródło |
|---|---|---|
| `userId` | `User.Id.ToString()` (Guid jako string) | `User.Id` |
| `firstName` | `User.FirstName` | `User.FirstName` |
| `lastName` | `User.LastName` | `User.LastName` |
| `email` | `User.Email` | `User.Email` |
| `ClaimTypes.Role` | `"User"` (stała) | hardcoded |

```csharp
// AuthService.cs › AuthService.CreateToken
var claims = new List<Claim>
{
    new("userId", user.Id.ToString()),
    new("firstName", user.FirstName),
    new("lastName", user.LastName),
    new("email", user.Email),
    new(ClaimTypes.Role, "User")
};
var token = new JwtSecurityToken(
    claims: claims,
    expires: DateTime.UtcNow.AddMinutes(10),
    signingCredentials: credentials
);
```

Autoryzacja w kontrolerach: atrybut `[Authorize(Roles = "User")]` na poziomie klasy lub metody. Endpointy auth (`/api/Auth/register`, `/api/Auth/login`) nie mają atrybutu `[Authorize]` — są publiczne.

Tożsamość bieżącego użytkownika w serwisach: `IUserService.GetCurrentUserId()` (odczyt claima `userId` z `HttpContext.User`). Rejestracja: `builder.Services.AddHttpContextAccessor()` (`Program.cs`).

### Hashowanie haseł (BCrypt)

Kotwica: `AuthService.cs › AuthService.RegisterUser`, `AuthService.LoginUser`

| Element | Wartość |
|---|---|
| Biblioteka | `BCrypt.Net.BCrypt` (alias `BC`) |
| Hashowanie | `BC.HashPassword(userDto.Password)` — sól generowana wewnętrznie |
| Weryfikacja | `BC.Verify(userDto.Password, user.PasswordHash)` |
| Przechowywanie | kolumna `User.PasswordHash` (SQL `nvarchar(max)`) |

Hasło jawne **nigdzie nie jest zapisywane ani logowane** — wyłącznie hash BCrypt trafia do bazy.

### Wymagania dotyczące siły hasła

Kotwica: `AuthService.cs › AuthService.RegisterUser`

```csharp
var passwordRules = new Regex(@"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$");
```

| Wymaganie | Opis |
|---|---|
| Minimalna długość | ≥ 8 znaków |
| Mała litera | co najmniej jedna (`a–z`) |
| Duża litera | co najmniej jedna (`A–Z`) |
| Cyfra | co najmniej jedna (`0–9`) |
| Znak specjalny | co najmniej jeden — **wyłącznie** z zestawu `@ $ ! % * ? &` |
| Dozwolone znaki | `A–Z`, `a–z`, `0–9`, `@$!%*?&` — inne znaki (np. `#`, `^`) są **niedozwolone** |

> ⚠️ Komunikat błędu (`InvalidPasswordException`) mówi ogólnie „one special character", ale regex akceptuje tylko 7 konkretnych znaków. Użytkownik może być zdezorientowany próbując np. `#` lub `^`. Szczegóły: `KATALOG_WYJATKOW.md § 2`.

---

## 2. `ExceptionMiddleware`

Kotwica: `Presentation/Middleware/ExceptionMiddleware.cs › ExceptionMiddleware.Invoke`

Middleware przechwytuje wszystkie nieobsłużone wyjątki z pipeline'u i serializuje odpowiedź:

```csharp
// ExceptionMiddleware.cs › ExceptionMiddleware.HandleExceptionAsync
var response = new { message = exception.Message };
var payload = JsonSerializer.Serialize(response);
context.Response.ContentType = "application/json";
context.Response.StatusCode = (int)statusCode;
```

Format odpowiedzi błędu: `{ "message": "<exception.Message>" }`.

Mapa wyjątek → status HTTP (kolejność catch):

| Wyjątek | Status HTTP |
|---|---|
| `AnafFirmNotFoundException` | `404 Not Found` |
| `BankAccountAssociatedWithDocumentsException` | `400 Bad Request` |
| `UserHasNoAssociatedFirmException` | `400 Bad Request` |
| `ProductAssociatedWithInvoiceException` | `400 Bad Request` |
| `NoBankAccountAddedException` | `400 Bad Request` |
| `UserNotFoundException` | `400 Bad Request` |
| `IncorrectPasswordException` | `400 Bad Request` |
| `UserAlreadyExistsException` | `400 Bad Request` |
| `PasswordMismatchException` | `400 Bad Request` |
| `Exception` (catch-all) | `500 Internal Server Error` |

> Pełny rejestr z komunikatami: `KATALOG_WYJATKOW.md`.

> [UWAGA: `InvalidPasswordException` (rzucany w `AuthService.RegisterUser` gdy hasło nie spełnia regex) **nie jest jawnie mapowany** w `ExceptionMiddleware`. Trafia do catch-all → `500 Internal Server Error` zamiast `400 Bad Request` — WYMAGA WERYFIKACJI Z ZESPOŁEM]

Uwaga dodatkowa — kontrolery z własnym `try/catch` omijające middleware:

| Kontroler.Metoda | Efekt | Proces |
|---|---|---|
| `DocumentController.GenerateDocument` | `catch (Exception ex) → BadRequest(ex.Message)` — każdy wyjątek zwraca `400` (zamiast właściwego kodu) | P-17 `02_KONTRAKT_API.md § API-28` |
| `DocumentSeriesController.AddDocumentSeries` | `catch (Exception ex) → BadRequest(ex.Message)` — ciało odpowiedzi to **plain string** (nie JSON `{ "message": "..." }`) | P-11 `02_KONTRAKT_API.md § API-19` |

> ⚠️ Oba kontrolery przechwytują **wszystkie** wyjątki (`Exception`) — w tym domenowe, które normalnie miałyby konkretny kod HTTP. Efekt: `UserHasNoAssociatedFirmException` zwraca `400` przez lokalny catch, lecz z innym formatem body niż reszta API.

---

## 3. `IUnitOfWork` i transakcje

Kotwica: `Infrastructure/Persistence/UnitOfWork.cs › UnitOfWork`

| Element | Opis |
|---|---|
| Interfejs | `IUnitOfWork` |
| Implementacja | `UnitOfWork` (Primary Constructor z `InvoiceJetDbContext`) |
| `CompleteAsync()` | wywołuje `_context.SaveChangesAsync()` — zatwierdza zmiany EF Core tracking |
| Jawne transakcje | brak — `BeginTransactionAsync` nie jest używany w żadnym procesie |
| Lifetime | `Scoped` (`AddScoped<IUnitOfWork, UnitOfWork>()`) |

Repozytoria agregowane przez `IUnitOfWork`:

| Właściwość | Typ | Tabela |
|---|---|---|
| `Users` | `IUserRepository` | `User` |
| `Firms` | `IFirmRepository` | `Firm` |
| `BankAccounts` | `IBankAccountRepository` | `BankAccount` |
| `UserFirms` | `IUserFirmRepository` | `UserFirm` |
| `Products` | `IProductRepository` | `Product` |
| `DocumentTypes` | `IDocumentTypeRepository` | `DocumentType` |
| `DocumentSeries` | `IDocumentSeriesRepository` | `DocumentSeries` |
| `Documents` | `IDocumentRepository` | `Document` |
| `DocumentProducts` | `IDocumentProductRepository` | `DocumentProduct` |
| `DocumentStatuses` | `IDocumentStatusRepository` | `DocumentStatus` |

Wzorzec `GenericRepository<T>`: `GetByIdAsync`, `GetAllAsync`, `AddAsync`, `AddRangeAsync`, `UpdateAsync`, `RemoveAsync`, `RemoveRangeAsync`, `Query()` (zwraca `IQueryable<T>`). Kotwica: `GenericRepository.cs`.

> [UWAGA: Procesy wykonujące wiele `CompleteAsync()` (np. wystawienie faktury) nie oplatają zapisów jawną transakcją. Awaria między pierwszym a drugim `CompleteAsync()` może pozostawić bazę w stanie niespójnym — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 4. AutoMapper

| Element | Wartość |
|---|---|
| Rejestracja | `builder.Services.AddAutoMapper(AppDomain.CurrentDomain.GetAssemblies())` (`Program.cs`) |
| Lokalizacja profili | `Application/MappingProfiles/*.cs` |

Dostępne profile:

| Profil | Encja / DTO |
|---|---|
| `BankAccountProfile.cs` | `BankAccount` ↔ DTO |
| `DocumentProductProfile.cs` | `DocumentProduct` ↔ DTO |
| `DocumentProfile.cs` | `Document` ↔ DTO |
| `DocumentSeriesProfile.cs` | `DocumentSeries` ↔ DTO |
| `DocumentStatusProfile.cs` | `DocumentStatus` ↔ DTO |
| `FirmProfile.cs` | `Firm` ↔ DTO |
| `ProductProfile.cs` | `Product` ↔ DTO |

> Brak profilu dla encji `User` — procesy `P-01_RegisterUser` i `P-02_LoginUser` nie używają AutoMapper; mapowanie DTO→encja jest wykonywane ręcznie w `AuthService`.

---

## 5. CORS

Kotwica: `Program.cs`

| Element | Wartość |
|---|---|
| Nazwa polityki | `NgOrigins` |
| Dozwolone origins | `http://localhost:4200`, `https://localhost:4200` |
| Metody | wszystkie (`AllowAnyMethod()`) |
| Nagłówki | wszystkie (`AllowAnyHeader()`) |
| Kolejność w pipeline | przed `UseHttpsRedirection`, `UseAuthentication`, `UseAuthorization` |

---

## 6. Baza danych i migracje

Kotwica: `Program.cs`, `Infrastructure/Persistence/InvoiceJetDbContext.cs`, `Infrastructure/Migrations/`

| Element | Wartość |
|---|---|
| Provider | SQL Server (`UseSqlServer`) |
| Connection string | `ConnectionStrings:ProdConnection` (`appsettings.json`) |
| `DbContext` | `InvoiceJetDbContext` |
| EF Core wersja | `8.0.6` (snapshot: `HasAnnotation("ProductVersion", "8.0.6")`) |
| Snapshot | `InvoiceJetDbContextModelSnapshot.cs` — źródło prawdy schematu dla `SLOWNIK_DANYCH.md` |

Jawne konfiguracje EF Core w `OnModelCreating` (`InvoiceJetDbContext.cs`):

```csharp
// InvoiceJetDbContext.cs › InvoiceJetDbContext.OnModelCreating
modelBuilder.Entity<User>()
    .HasOne(u => u.ActiveUserFirm)
    .WithMany()
    .HasForeignKey(u => u.ActiveUserFirmId)
    .IsRequired(false);        // nullable FK — user bez firmy jest poprawny

modelBuilder.Entity<Product>()
    .HasIndex(p => p.Name)
    .IsUnique();               // unikalność nazwy produktu na poziomie DB
```

Encje (`DbSet<T>`) zarejestrowane w `InvoiceJetDbContext`:
`User`, `Firm`, `BankAccount`, `UserFirm`, `Product`, `DocumentType`, `DocumentSeries`, `Document`, `DocumentProduct`, `DocumentStatus`.

---

## 7. Seed startowy (`DbSeeder`)

Kotwica: `Presentation/Seeders/DbSeeder.cs › DbSeeder.SeedDocumentTypes`

`DbSeeder.SeedDocumentTypes` jest wywoływany przy starcie aplikacji (`Program.cs`: `await DbSeeder.SeedDocumentTypes(app)`).

Logika seeda:

```csharp
// DbSeeder.cs › DbSeeder.SeedDocumentTypes
context.Database.EnsureCreated();  // tworzy DB bez migracji jeśli nie istnieje
if (!context.DocumentType.Any())
{
    // seedy: Factura, Factura Proforma, Factura Storno
}
if (!context.DocumentStatus.Any())
{
    // seedy: Unpaid, Paid
}
```

Seedowane dane:

| Tabela | Wartości | ID (kolejność inserta) |
|---|---|---|
| `DocumentType` | `"Factura"`, `"Factura Proforma"`, `"Factura Storno"` | 1, 2, 3 |
| `DocumentStatus` | `"Unpaid"`, `"Paid"` | 1, 2 |

> [UWAGA: `EnsureCreated()` tworzy schemat bazy bez uruchamiania migracji EF Core. W środowisku deweloperskim może to prowadzić do rozbieżności między migracjami a rzeczywistym schematem — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 8. Integracja ANAF (rumuński rejestr firm)

| Element | Opis |
|---|---|
| Cel | Pobranie danych firmy na podstawie numeru CUI (rumuński NIP) |
| Wyjątek | `AnafFirmNotFoundException` → `404 Not Found` (mapowany w `ExceptionMiddleware`) |
| Serwis | `FirmService.cs` |
| Używany przez | proces pobrania firmy z ANAF (kontroler `FirmController`) |
| URL zewnętrzny | `https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva` (z `appsettings.json › AppSettings:AnafApiUrl`) |
| Klucz API | brak — endpoint ANAF jest publiczny, autoryzacja po stronie klienta nie jest wymagana |

---

## 9. Generowanie PDF (QuestPDF)

Kotwica: `Program.cs`, `Infrastructure/Services/PdfGenerationService.cs`, `Infrastructure/Factories/`

| Element | Opis |
|---|---|
| Licencja | `LicenseType.Community` (ustawiona w `Program.cs`: `QuestPDF.Settings.License = LicenseType.Community`) |
| Serwis | `PdfGenerationService` (zarejestrowany jako `IPdfGenerationService`, `Scoped`) |
| Fabryki dokumentów | `Infrastructure/Factories/Impl/*DocumentFactory.cs` |

> [UWAGA: Rejestracja fabryki dokumentów w `Program.cs` jest zakomentowana:
> ```csharp
> // builder.Services.AddSingleton<IDocumentFactory, InvoiceDocumentFactory>();
> // builder.Services.AddSingleton<IDocumentFactory, ProformaDocumentFactory>();
> // builder.Services.AddSingleton<DocumentFactoryProvider>();
> ```
> `PdfGenerationService` jest zarejestrowany, ale fabryki nie są wstrzykiwane przez DI.
> `GetInvoicePdfStream` (API-29) tworzy `DocumentFactoryProvider` bezpośrednio (`new DocumentFactoryProvider()`) i poprawnie wybiera fabrykę na podstawie `DocumentType.Id`.
> `GenerateInvoicePdf` (API-28) zawsze tworzy `new InvoiceDocument(invoiceData)` niezależnie od typu dokumentu — BUG ⚠️:
> ```csharp
> // PdfGenerationService.cs › PdfGenerationService.GenerateInvoicePdf
> IDocument document = new InvoiceDocument(invoiceData); // hardcoded — ignoruje DocumentType
> ```
> Dla Proformy i Storno API-28 generuje błędny layout faktury zwykłej. API-29 działa poprawnie.]

---

## 10. Kolejność middleware w pipeline

Na podstawie `Program.cs` (`app.*` w kolejności):

1. `app.UseMiddleware<ExceptionMiddleware>()` — jako pierwszy, przechwytuje wszystkie wyjątki
2. `app.UseSwagger()` / `app.UseSwaggerUI()` — tylko `Development`
3. `await DbSeeder.SeedDocumentTypes(app)` — seed przy starcie
4. `app.UseCors("NgOrigins")`
5. `app.UseHttpsRedirection()`
6. `app.UseAuthentication()`
7. `app.UseAuthorization()`
8. `app.MapControllers()`
