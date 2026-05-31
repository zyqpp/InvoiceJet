# Inwentaryzacja ról i uprawnień

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Źródło | `InvoiceJetAPI/InvoiceJet.Presentation/Controllers/`, `AuthController.cs`, `AuthMiddleware` |

## 1. Lista ról (1)

| ID | Rola | Opis | Dokument | Status |
|---|---|---|---|---|
| ROLA-01 | `User` | Zalogowany użytkownik systemu. Jedyna rola w aplikacji. | [link](../06_role_i_uprawnienia/User.md) | szkic |

## 2. Mechanizm autoryzacji

- **Technologia:** JWT Bearer Token (HmacSha512)
- **Przechowywanie:** `localStorage` po stronie klienta Angular (`authToken`)
- **Przekazywanie:** nagłówek `Authorization: Bearer {token}` — dodawany przez `AuthInterceptor`
- **Walidacja po stronie API:** `[Authorize]` na metodach kontrolera (ASP.NET Core middleware)
- **Wygaśnięcie:** sprawdzane przez `JwtHelperService.isTokenExpired()` w Angular `AuthGuard` i `AuthInterceptor`
- **Payload JWT (zdekodowany):** `userId`, `firstName`, `lastName`, `email`

## 3. Macierz endpointów × rola

| Endpoint | Publiczny | User |
|---|---|---|
| `POST /api/Auth/register` | ✅ | ✅ |
| `POST /api/Auth/login` | ✅ | ✅ |
| Wszystkie pozostałe 29 endpointów | ❌ | ✅ |

> **Uwaga:** Brak ról administracyjnych, brak ról wielopoziomowych. Wszyscy zalogowani użytkownicy mają identyczne uprawnienia do wszystkich chronionych zasobów. Izolacja danych realizowana jest przez `userId` z JWT — każdy zapytanie filtruje rekordy po ID zalogowanego użytkownika (przez `ActiveUserFirmId` w tabeli `User`).

## 4. Izolacja danych między użytkownikami

Mimo braku ról, system zapewnia izolację danych:

| Mechanizm | Opis |
|---|---|
| `User.ActiveUserFirmId` | FK do aktywnej firmy użytkownika; wszystkie zasoby (Firm, Product, BankAccount, Document, DocumentSeries) powiązane przez `UserFirm.UserId` |
| `ClaimTypes.NameIdentifier` | UserId z JWT przekazywany do serwisów przez `IHttpContextAccessor` |
| Filtrowanie w serwisach | Każde zapytanie do DB zawiera filtr po `userId` lub `userFirmId` |

## 5. Anomalie

| # | Anomalia |
|---|---|
| ROL-A01 | Brak podziału na role (np. Admin / User) — jeden poziom dostępu dla wszystkich |
| ROL-A02 | `TokenExpiredDialogComponent` w Angular — dialog "session expired" otwierany ręcznie; interceptor obsługuje 401 przez toastr.error + logout, bez dialogu |
| ROL-A03 | `AuthService.options` — pole `private options: any = { observe: "response", responseType: "text" }` zdefiniowane, nieużywane w żadnej metodzie |
| ROL-A04 | `UserService.getUserByEmail()` wstrzykiwana w `AuthService` jako `public userService` — sugeruje planowaną funkcję (np. sprawdzanie czy email istnieje przy rejestracji), nigdy niezaimplementowaną |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Inwentaryzacja — 1 rola, mechanizm JWT, macierz uprawnień. |
