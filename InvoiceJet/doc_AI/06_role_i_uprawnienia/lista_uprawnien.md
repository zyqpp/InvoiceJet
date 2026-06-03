# Lista uprawnień — InvoiceJet

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| Autor | Agent Claudiusz Sonte 4.6 max |
| Wersja | 1.0 |
| Data | 2026-05-31 |
| Status | Obowiązujący |
| Liczba uprawnień | 12 |
| Liczba ról | 1 (User) |

## Streszczenie

System InvoiceJet ma jedną rolę (`User`) i prosty model uprawnień oparty na JWT. Nie istnieje granularna kontrola dostępu per zasób — użytkownik z rolą `User` ma dostęp do wszystkich chronionych operacji, przy czym izolacja danych jest realizowana przez claim `userId` zawarty w tokenie (każdy użytkownik widzi wyłącznie własne dane).

## Model uprawnień

### Mechanizm autoryzacji

| Warstwa | Mechanizm |
|---|---|
| Backend | Atrybut `[Authorize(Roles = "User")]` na klasach kontrolerów; JWT middleware weryfikuje podpis i ważność tokenu |
| Backend — izolacja danych | Claim `userId` wyekstrahowany z tokenu JWT jest używany we wszystkich zapytaniach LINQ do filtrowania danych per użytkownik |
| Frontend — routing | `AuthGuard.canActivate()` sprawdza `authService.isLoggedIn()` i przekierowuje na `/login` jeśli brak sesji |
| Frontend — HTTP | `AuthInterceptor` dodaje nagłówek `Authorization: Bearer <token>` do każdego żądania; przy odpowiedzi HTTP 401 wywołuje `authService.logout()` |

### Cykl życia tokenu

Token JWT jest wydawany przez endpoint `POST /api/Auth/login` i zawiera:
- claim `userId` — identyfikator użytkownika w bazie danych
- claim `role` — wartość `"User"`
- standardowe claimy: `exp` (czas wygaśnięcia), `iat` (czas wydania)

Token jest przechowywany po stronie frontendu (localStorage lub sessionStorage) i nie jest odświeżany automatycznie — po wygaśnięciu wymagane jest ponowne logowanie.

## Tabela uprawnień

| ID | Uprawnienie | Opis | Wymagany JWT | Wymagana rola | Endpointy |
|---|---|---|---|---|---|
| UPR-01 | Rejestracja | Tworzenie nowego konta użytkownika | Nie | Brak | API-01 |
| UPR-02 | Logowanie | Uzyskanie tokenu JWT | Nie | Brak | API-02 |
| UPR-03 | Zarządzanie własną firmą | CRUD firmy użytkownika (dodanie, edycja, podgląd) | Tak | User | API-03, API-05, API-06 |
| UPR-04 | Zarządzanie klientami | CRUD firm klientów (dodanie przez `isClient=true`, podgląd listy, usunięcie) | Tak | User | API-03 (`isClient=true`), API-07, API-08, API-09 |
| UPR-05 | Pobieranie danych z ANAF | Autouzupełnienie danych firmy po numerze CUI z zewnętrznego API ANAF | Tak | User | API-04 |
| UPR-06 | Zarządzanie produktami | CRUD produktów użytkownika (lista, dodanie, edycja, usunięcie) | Tak | User | API-10, API-11, API-12, API-13 |
| UPR-07 | Zarządzanie kontami bankowymi | CRUD kont bankowych firmy użytkownika | Tak | User | API-14, API-15, API-16, API-17 |
| UPR-08 | Zarządzanie seriami dokumentów | CRUD serii numeracyjnych dokumentów | Tak | User | API-18, API-19, API-20, API-21 |
| UPR-09 | Zarządzanie dokumentami | CRUD dokumentów (faktura, proforma, storno): dodanie, edycja, lista, szczegóły, usunięcie | Tak | User | API-22, API-23, API-24, API-25, API-26 |
| UPR-10 | Generowanie PDF | Eksport dokumentu do formatu PDF; pobieranie strumienia PDF | Tak | User | API-27, API-28, API-29 |
| UPR-11 | Statystyki dashboardu | Podgląd statystyk dokumentów per rok i typ dokumentu | Tak | User | API-30 |
| UPR-12 | Konwersja na storno | Zmiana typu dokumentu na storno (operacja nieodwracalna) | Tak | User | API-31 |

## Izolacja danych między użytkownikami

Pomimo że wszyscy zalogowani użytkownicy mają tę samą rolę `User`, dane są izolowane na poziomie bazy danych. Każde zapytanie LINQ filtruje rekordy po `UserId` wyekstrahowanym z JWT. Nie istnieje mechanizm administracyjny pozwalający jednemu użytkownikowi na dostęp do danych innego.

| Zasób | Mechanizm izolacji |
|---|---|
| Firmy | `WHERE UserFirm.UserId = @userId` |
| Produkty | `WHERE Product.UserId = @userId` (pośrednio przez firmę) |
| Konta bankowe | `WHERE BankAccount.FirmId IN (firmy użytkownika)` |
| Serie dokumentów | `WHERE DocumentSeries.UserId = @userId` |
| Dokumenty | `WHERE Document.UserId = @userId` |

## Wątpliwości i braki

| ID | Brak / wątpliwość | Wpływ |
|---|---|---|
| UPR-BRAK-01 | Brak autoryzacji granularnej (per zasób) | Użytkownik z rolą `User` ma dostęp do wszystkich operacji — nie można zablokować np. eksportu PDF dla wybranych kont |
| UPR-BRAK-02 | Brak modelu multi-tenant / organizacji | Nie istnieje pojęcie organizacji — każdy użytkownik jest izolowaną wyspą danych |
| UPR-BRAK-03 | Brak roli administratora | Nie ma możliwości administracji użytkownikami, przeglądania danych innych użytkowników ani zarządzania systemem przez panel admina |
| UPR-BRAK-04 | Brak mechanizmu refresh token | Po wygaśnięciu JWT użytkownik jest wylogowywany — brak silent refresh |
| UPR-BRAK-05 | Brak audytu operacji | System nie loguje kto, kiedy i jaką operację wykonał (brak audit trail) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny — 12 uprawnień, model JWT, tabela izolacji danych. |
