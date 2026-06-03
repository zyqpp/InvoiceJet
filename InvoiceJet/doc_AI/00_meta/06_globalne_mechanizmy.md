# Globalne mechanizmy techniczne

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Źródło | `Program.cs`, `ExceptionMiddleware.cs`, `AuthInterceptor.ts`, `ErrorInterceptor.ts`, `AuthService.cs`, `AuthGuard.ts` |

## 1. Autentykacja i autoryzacja

### Backend — JWT Bearer

```
Konfiguracja (Program.cs):
  Algorithm:  HmacSha512Signature
  Expiry:     DateTime.UtcNow.AddMinutes(10)
  ClockSkew:  TimeSpan.Zero  (brak tolerancji)
  ValidateIssuer:   false
  ValidateAudience: false
  ValidateLifetime: true
  MapInboundClaims: false
```

**Payload tokenu (Claims):**
| Klucz claimu | Źródło |
|---|---|
| `"userId"` | `User.Id.ToString()` |
| `"firstName"` | `User.FirstName` |
| `"lastName"` | `User.LastName` |
| `"email"` | `User.Email` |
| `ClaimTypes.Role` | `"User"` (stałe) |

**Pobieranie userId w serwisach:**
```csharp
// UserService.cs › GetCurrentUserId()
// Odczytuje userId z HttpContext.User.FindFirst("userId")
```

**Weryfikacja na endpointach:** atrybut `[Authorize]` — 29 z 31 endpointów.

---

### Frontend — AuthInterceptor + AuthGuard

**AuthInterceptor** (`auth.interceptor.ts`):
- Przechwytuje każde wychodzące żądanie HTTP
- Jeśli `localStorage.getItem("authToken")` nie jest null → dodaje nagłówek `Authorization: Bearer {token}`
- Przy odpowiedzi 401 → `authService.logout()` + `router.navigate(["/login"])`

**AuthGuard** (`auth.guard.ts`):
- Implementuje `CanActivate`
- Sprawdza `authService.isLoggedIn()` = `token istnieje && !jwtHelper.isTokenExpired(token)`
- Jeśli wygasły/brak → `authService.logout()` + redirect do `/login`
- Wszystkie trasy `/dashboard/**` są chronione

---

## 2. Obsługa błędów

### Backend — ExceptionMiddleware

```csharp
// ExceptionMiddleware.cs — top-level middleware, otacza całe żądanie
try { await _next(context); }
catch (SpecificException ex) { response.StatusCode = mappedCode; ... }
catch (Exception ex) { response.StatusCode = 500; ... }
```

**Mapowanie wyjątków:**

| Klasa wyjątku | HTTP | Komunikat |
|---|---|---|
| `UserAlreadyExistsException` | 409 | (z wyjątku) |
| `UserNotFoundException` | 404 | (z wyjątku) |
| `InvalidPasswordException` | 400 | (z wyjątku) |
| `PasswordMismatchException` | 400 | (z wyjątku) |
| `IncorrectPasswordException` | 400 | (z wyjątku) |
| `UserHasNoAssociatedFirmException` | 400 | (z wyjątku) |
| `NoBankAccountAddedException` | 400 | (z wyjątku) |
| Wszystkie pozostałe | 500 | (message wyjątku) |

> **Uwaga:** `DocumentController.GenerateDocument` (API-28) i `DocumentSeriesController.AddDocumentSeries` (API-19) mają własne try/catch — omijają ExceptionMiddleware. Błędy z API-19 zwracane jako plain string, nie JSON.

---

### Frontend — ErrorInterceptor

```typescript
// error.interceptor.ts — globalny interceptor błędów HTTP
catchError(error => {
    switch(error.status) {
        case 400: toastr.error(message, "Error"); break;
        case 401: toastr.error("Session has expired", "Unauthorized"); break;
        case 404: toastr.error(message, "Not Found"); break;
        case 500: toastr.error(message, "Error"); break;
        default:  toastr.error("An unexpected error has occurred.", "Unexpected Error");
    }
    return throwError(error);
})
```

---

## 3. Izolacja danych między użytkownikami

Każdy użytkownik widzi wyłącznie swoje dane. Mechanizm:

1. **JWT → userId** — po zalogowaniu userId zapisany w tokenie
2. **UserService.GetCurrentUserId()** — odczytuje `userId` z `HttpContext.User`
3. **ActiveUserFirmId** — klucz `User.ActiveUserFirmId` wskazuje aktywną firmę; serwisy pobierają `userFirmId` przez `UnitOfWork.Users.GetUserFirmIdAsync(userId)`
4. **Filtrowanie w każdym zapytaniu** — WHERE `UserFirmId = {userFirmId}` dla Firm, Product, BankAccount, Document, DocumentSeries

Brak separacji na poziomie ról — wszyscy zalogowani mają identyczne uprawnienia do operacji, ale dane są izolowane przez `userId`/`userFirmId`.

---

## 4. Seed danych startowych

**Klasa:** `DbSeeder` (`InvoiceJet.Presentation/Seeders/DbSeeder.cs`)  
**Wywołanie:** `await DbSeeder.SeedDocumentTypes(app);` w `Program.cs` — przed startem serwera

**Dane seedowane:**

`DocumentType`:
| Id | Name |
|---|---|
| 1 | `Factura` |
| 2 | `Factura Proforma` |
| 3 | `Factura Storno` |

`DocumentStatus`:
| Id | Status |
|---|---|
| 1 | `Unpaid` |
| 2 | `Paid` |

---

## 5. Unit of Work Pattern

**Interfejs:** `IUnitOfWork` (`InvoiceJet.Domain/Interfaces/`)  
**Implementacja:** `UnitOfWork` (`InvoiceJet.Infrastructure/Persistence/`)

```
IUnitOfWork
├── Users:           IUserRepository
├── Firms:           IFirmRepository
├── BankAccounts:    IBankAccountRepository
├── Products:        IProductRepository
├── DocumentSeries:  IDocumentSeriesRepository
├── Documents:       IDocumentRepository
├── DocumentProducts: IDocumentProductRepository
├── DocumentStatuses: IGenericRepository<DocumentStatus>
└── CompleteAsync()  ← = DbContext.SaveChangesAsync()
```

**Rejestracja DI (Program.cs):**
```csharp
builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();
builder.Services.AddScoped(typeof(IGenericRepository<>), typeof(GenericRepository<>));
```

---

## 6. CORS

**Polityka:** `"NgOrigins"`

```csharp
policy.WithOrigins("http://localhost:4200", "https://localhost:4200")
      .AllowAnyMethod()
      .AllowAnyHeader();
```

> **Uwaga:** Polityka CORS nie obejmuje produkcyjnej domeny frontendu (jeśli frontend hostowany publicznie, wymagana aktualizacja).

---

## 7. Generowanie PDF

**Licencja:** QuestPDF Community (`QuestPDF.Settings.License = LicenseType.Community;`)  
**Dwa tryby generowania:**

| Tryb | Endpoint | Metoda | Wynik |
|---|---|---|---|
| Zapis na dysk | API-28 | `GenerateInvoicePdf()` | Plik PDF na dysku serwera; klient nie dostaje pliku |
| Strumień | API-29 | `GetInvoicePdfStream()` | `byte[]` zwracany do klienta, wyświetlany w `PdfViewerComponent` |

**Anomalia:** `GenerateInvoicePdf()` hardcodes `new InvoiceDocument()` — zawsze faktura zwykła, niezależnie od `DocumentType`.

---

## 8. Integracja z ANAF (zewnętrzne API)

**ANAF** = Agenția Națională de Administrare Fiscală (rumuński urząd skarbowy)

**Endpoint:** `GET /api/Firm/fromAnaf/{cui}`  
**Cel:** Pobiera dane firmy (nazwa, adres) na podstawie numeru CUI (Cod Unic de Înregistrare).

> [UWAGA: Dokładny URL i parametry ANAF API do weryfikacji z kodem `FirmService.cs`]

---

## 9. Middleware pipeline (kolejność)

```
1. ExceptionMiddleware           ← przechwytuje WSZYSTKIE wyjątki
2. Swagger UI (tylko Development)
3. DbSeeder (seed at startup)
4. CORS ("NgOrigins")
5. HTTPS Redirection
6. Authentication (JWT Bearer)
7. Authorization ([Authorize])
8. MapControllers → Kontrolery
```

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokumentacja mechanizmów globalnych na podstawie kodu źródłowego. |
