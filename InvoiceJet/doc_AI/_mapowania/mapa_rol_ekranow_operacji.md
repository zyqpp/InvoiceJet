# Mapa: Rola × ekran × operacja (M-07)

| Pole | Wartość |
|---|---|
| ID dokumentu | M-07 |
| Typ dokumentu | mapa krzyżowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Mapa prezentuje dla każdego ekranu i operacji: wymaganą rolę użytkownika, wywoływany endpoint API oraz mechanizm autoryzacji. InvoiceJet ma jedną rolę (`User`) — ekrany publiczne (login, register) nie wymagają żadnej roli; wszystkie pozostałe chronione są przez `AuthGuard` (frontend) i `[Authorize(Roles = "User")]` (backend).

## Tabela mapowań

| Ekran (ID) | Komponent | Operacja | Wymagana rola | Endpoint (ID) | Autoryzacja backend | Uwagi |
|---|---|---|---|---|---|---|
| EKRAN-01 Login | `LoginComponent` | Zalogowanie | Brak | API-02 POST | Brak `[Authorize]` | Ekran publiczny, brak AuthGuard |
| EKRAN-01 Login | `LoginComponent` | Przejście do rejestracji | Brak | *(nawigacja)* | — | Link do `/register` |
| EKRAN-02 Register | `RegisterComponent` | Rejestracja | Brak | API-01 POST | Brak `[Authorize]` | Ekran publiczny, brak AuthGuard |
| EKRAN-02 Register | `RegisterComponent` | Przejście do logowania | Brak | *(nawigacja)* | — | Link do `/login` |
| EKRAN-03 Dashboard | `DashboardComponent` | Podgląd statystyk | User | API-30 GET | `[Authorize(Roles = "User")]` | Dane per rok i typ dokumentu |
| EKRAN-03 Dashboard | `DashboardComponent` | Wylogowanie | User | *(localStorage clear)* | — | Navbar: usuwa token, redirect → `/login` |
| EKRAN-04 Dane firmy | `FirmDetailsComponent` | Podgląd danych firmy | User | API-06 GET | `[Authorize(Roles = "User")]` | Aktywna firma użytkownika |
| EKRAN-04 Dane firmy | `FirmDetailsComponent` | Edycja danych firmy | User | API-05 PUT | `[Authorize(Roles = "User")]` | |
| EKRAN-04 Dane firmy | `FirmDetailsComponent` | Autouzupełnienie z ANAF | User | API-04 GET | `[Authorize(Roles = "User")]` | Proxy do ANAF po CUI |
| EKRAN-04 Dane firmy | `FirmDetailsComponent` | Dodaj klienta | User | API-03 POST (`isClient=true`) | `[Authorize(Roles = "User")]` | Anomalia UI-A01: niezaimplementowane |
| EKRAN-05 Klienci | `ClientsComponent` | Lista klientów | User | API-07 GET | `[Authorize(Roles = "User")]` | |
| EKRAN-05 Klienci | `ClientsComponent` | Dodaj klienta (modal) | User | API-03 POST (`isClient=true`) | `[Authorize(Roles = "User")]` | Otwiera DIALOG-01 |
| EKRAN-05 Klienci | `ClientsComponent` | Edytuj klienta (modal) | User | API-05 PUT | `[Authorize(Roles = "User")]` | Otwiera DIALOG-01 |
| EKRAN-05 Klienci | `ClientsComponent` | Usuń klientów | User | API-09 PUT | `[Authorize(Roles = "User")]` | Soft-delete, `int[]` ids |
| EKRAN-06 Konta bankowe | `BankAccountsComponent` | Lista kont | User | API-14 GET | `[Authorize(Roles = "User")]` | |
| EKRAN-06 Konta bankowe | `BankAccountsComponent` | Dodaj konto (modal) | User | API-15 POST | `[Authorize(Roles = "User")]` | Otwiera DIALOG-02 |
| EKRAN-06 Konta bankowe | `BankAccountsComponent` | Edytuj konto (modal) | User | API-16 PUT | `[Authorize(Roles = "User")]` | Otwiera DIALOG-02 |
| EKRAN-06 Konta bankowe | `BankAccountsComponent` | Usuń konta | User | API-17 PUT | `[Authorize(Roles = "User")]` | Soft-delete |
| EKRAN-07 Produkty | `ProductsComponent` | Lista produktów | User | API-10 GET | `[Authorize(Roles = "User")]` | |
| EKRAN-07 Produkty | `ProductsComponent` | Dodaj produkt (modal) | User | API-11 POST | `[Authorize(Roles = "User")]` | Otwiera DIALOG-03 |
| EKRAN-07 Produkty | `ProductsComponent` | Edytuj produkt (modal) | User | API-12 PUT | `[Authorize(Roles = "User")]` | Otwiera DIALOG-03 |
| EKRAN-07 Produkty | `ProductsComponent` | Usuń produkty | User | API-13 PUT | `[Authorize(Roles = "User")]` | Soft-delete |
| EKRAN-08 Serie dokumentów | `DocumentSeriesComponent` | Lista serii | User | API-18 GET | `[Authorize(Roles = "User")]` | |
| EKRAN-08 Serie dokumentów | `DocumentSeriesComponent` | Dodaj serię (modal) | User | API-19 POST | `[Authorize(Roles = "User")]` | Otwiera DIALOG-04 |
| EKRAN-08 Serie dokumentów | `DocumentSeriesComponent` | Edytuj serię (modal) | User | API-20 PUT | `[Authorize(Roles = "User")]` | Otwiera DIALOG-04 |
| EKRAN-08 Serie dokumentów | `DocumentSeriesComponent` | Usuń serie | User | API-21 PUT | `[Authorize(Roles = "User")]` | Soft-delete |
| EKRAN-09 Lista faktur | `InvoicesComponent` | Lista faktur | User | API-24 GET | `[Authorize(Roles = "User")]` | `documentTypeId=1` |
| EKRAN-09 Lista faktur | `InvoicesComponent` | Usuń faktury | User | API-26 PUT | `[Authorize(Roles = "User")]` | Soft-delete |
| EKRAN-09 Lista faktur | `InvoicesComponent` | Konwertuj na storno | User | API-31 PUT | `[Authorize(Roles = "User")]` | Operacja nieodwracalna |
| EKRAN-10 Formularz faktury | `AddOrEditInvoiceComponent` | Autouzupełnienie formularza | User | API-27 GET | `[Authorize(Roles = "User")]` | Klienci, serie, statusy, produkty |
| EKRAN-10 Formularz faktury | `AddOrEditInvoiceComponent` | Dodaj fakturę | User | API-22 POST | `[Authorize(Roles = "User")]` | |
| EKRAN-10 Formularz faktury | `AddOrEditInvoiceComponent` | Edytuj fakturę | User | API-23 PUT + API-25 GET | `[Authorize(Roles = "User")]` | GET przy ładowaniu, PUT przy zapisie |
| EKRAN-10 Formularz faktury | `AddOrEditInvoiceComponent` | Podgląd PDF | User | API-29 POST | `[Authorize(Roles = "User")]` | Otwiera DIALOG-05 (PdfViewer) |
| EKRAN-10 Formularz faktury | `AddOrEditInvoiceComponent` | Generuj PDF (pobierz) | User | API-28 POST | `[Authorize(Roles = "User")]` | Bug: hardcoded InvoiceDocument |
| EKRAN-11 Lista proform | `InvoiceProformasComponent` | Lista proform | User | API-24 GET | `[Authorize(Roles = "User")]` | `documentTypeId=2` |
| EKRAN-11 Lista proform | `InvoiceProformasComponent` | Usuń proformy | User | API-26 PUT | `[Authorize(Roles = "User")]` | Soft-delete |
| EKRAN-12 Formularz proformy | `AddOrEditInvoiceProformaComponent` | Autouzupełnienie | User | API-27 GET | `[Authorize(Roles = "User")]` | |
| EKRAN-12 Formularz proformy | `AddOrEditInvoiceProformaComponent` | Dodaj proformę | User | API-22 POST | `[Authorize(Roles = "User")]` | |
| EKRAN-12 Formularz proformy | `AddOrEditInvoiceProformaComponent` | Edytuj proformę | User | API-23 PUT + API-25 GET | `[Authorize(Roles = "User")]` | |
| EKRAN-12 Formularz proformy | `AddOrEditInvoiceProformaComponent` | Podgląd PDF | User | API-29 POST | `[Authorize(Roles = "User")]` | Otwiera DIALOG-05 |
| EKRAN-13 Lista storn | `InvoiceStornosComponent` | Lista storn | User | API-24 GET | `[Authorize(Roles = "User")]` | `documentTypeId=3` |
| EKRAN-13 Lista storn | `InvoiceStornosComponent` | Usuń storna | User | API-26 PUT | `[Authorize(Roles = "User")]` | Soft-delete |
| EKRAN-14 Formularz storna | `AddOrEditInvoiceStornosComponent` | Podgląd/edycja storna | User | API-25 GET + API-23 PUT | `[Authorize(Roles = "User")]` | Storno tworzone wyłącznie przez API-31 |
| EKRAN-14 Formularz storna | `AddOrEditInvoiceStornosComponent` | Podgląd PDF | User | API-29 POST | `[Authorize(Roles = "User")]` | |

## Uwagi

- InvoiceJet ma jedną rolę (`User`) — nie ma operacji dostępnych dla wielu różnych ról.
- Ekrany `/login` i `/register` są poza systemem AuthGuard — brak tokenu JWT.
- `AuthGuard` w Angular chroni wszystkie trasy `/dashboard/*` — przy braku tokenu redirect do `/login`.
- `AuthInterceptor` dodaje nagłówek `Authorization: Bearer` do każdego żądania i obsługuje HTTP 401.
- Soft-delete: brak fizycznego DELETE w API — wszystkie usunięcia przez `PUT` z `int[]` ids.
- Anomalia UI-A01: `addNewClient()` w `FirmDetailsComponent` — niezaimplementowana funkcja (tylko `console.log`).

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
