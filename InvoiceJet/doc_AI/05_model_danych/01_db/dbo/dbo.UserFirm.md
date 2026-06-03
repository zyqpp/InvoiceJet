# Tabela `dbo.UserFirm`

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Klasa domenowa | `InvoiceJet.Domain.Models.UserFirm` |

## Opis

Tabela łącząca (junction table) między `User` a `Firm`. Pełni podwójną rolę:
1. Rejestruje przynależność firmy do użytkownika
2. Flaga `IsClient` odróżnia własną firmę użytkownika (`IsClient=false`) od klientów (`IsClient=true`)

Ponadto `UserFirm` jest **węzłem agregującym** — do `UserFirmId` podłączone są `BankAccount`, `Product`, `DocumentSeries`, `Document`.

## Kolumny

| Kolumna | Typ SQL | Nullable | PK/FK | Uwagi |
|---|---|---|---|---|
| `UserFirmId` | `int` IDENTITY | NOT NULL | **PK** | Autoincrement |
| `UserId` | `uniqueidentifier` | NOT NULL | FK → `User.Id` CASCADE | Właściciel |
| `FirmId` | `int` | NOT NULL | FK → `Firm.Id` CASCADE | Firma |
| `IsClient` | `bit` | NOT NULL | — | `false` = firma własna, `true` = klient |

## Indeksy

| Indeks | Kolumna | Unikalny |
|---|---|---|
| `IX_UserFirm_FirmId` | `FirmId` | NIE |
| `IX_UserFirm_UserId` | `UserId` | NIE |

## Relacje

| Kierunek | Relacja | Szczegóły |
|---|---|---|
| `UserFirm` → `User` | N:1 wymagana | CASCADE |
| `UserFirm` → `Firm` | N:1 wymagana | CASCADE |
| `UserFirm` ← `BankAccount` | 1:N | `BankAccount.UserFirmId → UserFirmId`; CASCADE |
| `UserFirm` ← `Product` | 1:N | `Product.UserFirmId → UserFirmId`; bez CASCADE |
| `UserFirm` ← `DocumentSeries` | 1:N | `DocumentSeries.UserFirmId → UserFirmId`; bez CASCADE |
| `UserFirm` ← `Document` | 1:N | `Document.UserFirmId → UserFirmId`; bez CASCADE |
| `User.ActiveUserFirmId` → `UserFirm` | N:0..1 | wskaźnik aktywnej firmy; bez CASCADE |

## Dane seedowane

Brak.

## Uwagi

- Brak unikalnego indeksu na `(UserId, FirmId)` — możliwe duplikaty (ten sam user + ta sama firma)
- `IsClient=false` — może być tylko jedna taka firma per user (logicznie; brak ograniczenia DB)
- Usunięcie `User` kaskaduje do `UserFirm`, co kaskaduje do `BankAccount` → potencjalnie niebezpieczna kaskada

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Karta tabeli na podstawie ModelSnapshot. |
