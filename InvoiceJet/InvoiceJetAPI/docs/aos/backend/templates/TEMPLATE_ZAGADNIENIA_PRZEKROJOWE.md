<!--
SZABLON ZAGADNIENIA_PRZEKROJOWE — wiedza techniczna nie należąca do jednego procesu.
Plik docelowy: docs/aos/backend/ZAGADNIENIA_PRZEKROJOWE.md
ŹRÓDŁA: Program.cs, Middleware, UnitOfWork, AutoMapper, appsettings*.json, Infrastructure/Services/*, Factories/*.
-->

# Zagadnienia przekrojowe — InvoiceJetAPI

**Data aktualizacji:** RRRR-MM-DD

---

## 1. Uwierzytelnianie i autoryzacja (JWT)

| Element | Wartość / kotwica |
|---|---|
| Schemat | `JwtBearerDefaults.AuthenticationScheme` |
| Konfiguracja | `Program.cs` |
| Klucz podpisu | `AppSettings:Token` (`appsettings.json`) |
| Walidacja podpisu | `ValidateIssuerSigningKey = true` |
| Walidacja issuer/audience | `ValidateIssuer = false`, `ValidateAudience = false` |
| Walidacja czasu życia | `ValidateLifetime = true`, `ClockSkew = TimeSpan.Zero` |
| Mapowanie roszczeń | `MapInboundClaims = false` |
| Generowanie tokenu | `[AuthService.cs › AuthService.CreateToken]` |
| Czas ważności | `[X minut]` (sprawdź w `CreateToken`) |
| Claimy | `userId`, `firstName`, `lastName`, `email`, `ClaimTypes.Role` |

## 2. `ExceptionMiddleware`

- Plik: `Presentation/Middleware/ExceptionMiddleware.cs`
- Pełen rejestr wyjątek→HTTP: `KATALOG_WYJATKOW.md`
- Odpowiedź: `application/json` o kształcie `{ "message": "<exception.Message>" }`
- Uwaga: wyjątki niemapowane jawnie → `500 Internal Server Error`.

## 3. `IUnitOfWork` i transakcje

| Element | Opis |
|---|---|
| Plik | `Infrastructure/Persistence/UnitOfWork.cs` |
| Repozytoria | agregowane jako właściwości (`Users`, `Documents`, …) |
| `CompleteAsync()` | wykonuje `SaveChangesAsync` |
| Jawne transakcje | [czy są używane `BeginTransactionAsync`? — sprawdź i opisz] |
| Wzorzec wielokrotnego zapisu | wiele `CompleteAsync()` w jednym procesie — bez jawnej transakcji — [marker UWAGA jeżeli krytyczne] |

## 4. AutoMapper

| Element | Opis |
|---|---|
| Rejestracja | `Program.cs` → `AddAutoMapper(AppDomain.CurrentDomain.GetAssemblies())` |
| Lokalizacja profili | `Application/MappingProfiles/*` |
| Konwencja | profil per encja/DTO |

## 5. CORS

| Polityka | Wartość |
|---|---|
| Nazwa | `NgOrigins` |
| Origins | `http://localhost:4200`, `https://localhost:4200` |
| Metody | wszystkie |
| Nagłówki | wszystkie |

## 6. Baza danych i migracje

| Element | Wartość |
|---|---|
| Provider | SQL Server (`UseSqlServer`) |
| Connection string | `ConnectionStrings:ProdConnection` (`appsettings.json`) |
| `DbContext` | `Infrastructure/Persistence/InvoiceJetDbContext.cs` |
| Migracje | `Infrastructure/Migrations/*` |
| Snapshot | `InvoiceJetDbContextModelSnapshot.cs` (źródło prawdy dla `SLOWNIK_DANYCH`) |
| Seed | `Presentation/Seeders/DbSeeder.cs` |

## 7. Integracja ANAF (Rumuński rejestr firm)

| Element | Opis |
|---|---|
| Cel | Pobranie danych firmy po `CUI` |
| Proces | `P-05_GetFirmFromAnaf` |
| Kotwica | `[FirmService.cs › FirmService.[Method]]` |
| Wyjątek | `AnafFirmNotFoundException` → `404` (mapowany w `ExceptionMiddleware`) |
| URL / klucz API | [sprawdź `appsettings.json` i `FirmService`] |

## 8. Generowanie PDF (QuestPDF)

| Element | Opis |
|---|---|
| Licencja | `LicenseType.Community` (ustawiona w `Program.cs`) |
| Fabryki dokumentów | `Infrastructure/Factories/Impl/*DocumentFactory.cs` |
| Komponenty | `Infrastructure/Services/IQuestPDFDocument/*` |
| Serwis | `Infrastructure/Services/PdfGenerationService.cs` |
| Używane przez | `P-16_GenerateDocumentPdf`, `P-17_GetInvoicePdfStream` |

## 9. Konfiguracja (`appsettings*.json`)

| Sekcja | Pliki | Użycie |
|---|---|---|
| `ConnectionStrings:ProdConnection` | `appsettings.json` | DbContext |
| `AppSettings:Token` | `appsettings.json` | JWT |
| [inne] | — | — |
