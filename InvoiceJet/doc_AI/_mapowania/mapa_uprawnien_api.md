# Mapa: Uprawnienia ↔ endpointy API (M-08)

| Pole | Wartość |
|---|---|
| ID dokumentu | M-08 |
| Typ dokumentu | mapa krzyżowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Mapa wiąże 12 uprawnień logicznych (UPR-01..UPR-12) z konkretnymi endpointami API i ich mechanizmem autoryzacji. InvoiceJet ma jedną rolę (`User`) — granularność uprawnień jest logiczna, nie techniczna; każde UPR odpowiada grupie powiązanych operacji.

## Tabela mapowań

| ID Uprawnienia | Uprawnienie | Endpointy | Metoda HTTP | JWT wymagany | Rola | Mechanizm autoryzacji |
|---|---|---|---|---|---|---|
| UPR-01 | Rejestracja | API-01 | POST | Nie | Brak | Endpoint publiczny — brak `[Authorize]` |
| UPR-02 | Logowanie | API-02 | POST | Nie | Brak | Endpoint publiczny — brak `[Authorize]` |
| UPR-03 | Zarządzanie własną firmą | API-03 (`isClient=false`), API-05, API-06 | POST, PUT, GET | Tak | User | `[Authorize(Roles = "User")]` na kontrolerze |
| UPR-04 | Zarządzanie klientami | API-03 (`isClient=true`), API-07, API-08, API-09 | POST, GET, PUT | Tak | User | `[Authorize(Roles = "User")]` na kontrolerze |
| UPR-05 | Pobieranie danych z ANAF | API-04 | GET | Tak | User | `[Authorize(Roles = "User")]` + proxy do ANAF |
| UPR-06 | Zarządzanie produktami | API-10, API-11, API-12, API-13 | GET, POST, PUT | Tak | User | `[Authorize(Roles = "User")]` na kontrolerze |
| UPR-07 | Zarządzanie kontami bankowymi | API-14, API-15, API-16, API-17 | GET, POST, PUT | Tak | User | `[Authorize(Roles = "User")]` na kontrolerze |
| UPR-08 | Zarządzanie seriami dokumentów | API-18, API-19, API-20, API-21 | GET, POST, PUT | Tak | User | `[Authorize(Roles = "User")]` na kontrolerze |
| UPR-09 | Zarządzanie dokumentami | API-22, API-23, API-24, API-25, API-26 | POST, PUT, GET | Tak | User | `[Authorize(Roles = "User")]` na kontrolerze |
| UPR-10 | Generowanie PDF | API-27, API-28, API-29 | GET, POST | Tak | User | `[Authorize(Roles = "User")]` na kontrolerze |
| UPR-11 | Statystyki dashboardu | API-30 | GET | Tak | User | `[Authorize(Roles = "User")]` na kontrolerze |
| UPR-12 | Konwersja na storno | API-31 | PUT | Tak | User | `[Authorize(Roles = "User")]` na kontrolerze |

## Izolacja danych (per użytkownik)

Pomimo jednej roli, dane użytkowników są izolowane przez claim `userId` w JWT — każde zapytanie LINQ filtruje po `userId`:

| Zasób | Filtr LINQ |
|---|---|
| Firmy | `WHERE UserFirm.UserId = @userId` |
| Produkty | `WHERE Product.UserId = @userId` |
| Konta bankowe | `WHERE BankAccount.FirmId IN (firmy użytkownika)` |
| Serie dokumentów | `WHERE DocumentSeries.UserId = @userId` |
| Dokumenty | `WHERE Document.UserId = @userId` |

## Uwagi

- Brak granularnej kontroli dostępu per zasób (UPR-BRAK-01 z `lista_uprawnien.md`): rola `User` daje dostęp do wszystkich chronionych operacji.
- API-03 obsługuje zarówno UPR-03 jak i UPR-04 — rozróżnienie przez parametr `{isClient}` w URL.
- API-07 i API-08 to ten sam fizyczny endpoint (duplikat numeracji).
- Brak roli administratora (UPR-BRAK-03).
- Brak refresh token (UPR-BRAK-04) — po wygaśnięciu JWT wymagane ponowne logowanie.
- Źródło: [lista_uprawnien.md](../06_role_i_uprawnienia/lista_uprawnien.md)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
