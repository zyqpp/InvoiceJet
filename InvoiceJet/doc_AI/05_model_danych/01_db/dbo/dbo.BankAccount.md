# Tabela `dbo.BankAccount`

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Klasa domenowa | `InvoiceJet.Domain.Models.BankAccount` |

## Kolumny

| Kolumna | Typ SQL | Nullable | PK/FK | Uwagi |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | NOT NULL | **PK** | Autoincrement |
| `BankName` | `nvarchar(max)` | NOT NULL | — | Nazwa banku |
| `Iban` | `nvarchar(max)` | NOT NULL | — | Numer IBAN |
| `Currency` | `int` | NOT NULL | — | Enum: `Ron=0`, `Eur=1` |
| `IsActive` | `bit` | NOT NULL | — | Czy konto aktywne (używane do generowania dokumentów) |
| `UserFirmId` | `int` | NOT NULL | FK → `UserFirm.UserFirmId` CASCADE | Właściciel — firma użytkownika |

## Indeksy

| Indeks | Kolumna | Unikalny |
|---|---|---|
| `IX_BankAccount_UserFirmId` | `UserFirmId` | NIE |

## Relacje

| Kierunek | Relacja | Szczegóły |
|---|---|---|
| `BankAccount` → `UserFirm` | N:1 wymagana | CASCADE przy usunięciu `UserFirm` |
| `Document.BankAccountId` → `BankAccount` | N:1 wymagana | **CASCADE** — usunięcie konta kasuje dokumenty! |

## Dane seedowane

Brak.

## Uwagi

- Dokument wymaga konta bankowego (`Document.BankAccountId NOT NULL`). Przy tworzeniu dokumentu pobierane jest pierwsze aktywne konto (`WHERE IsActive=true`) → `NoBankAccountAddedException` jeśli brak
- **Ryzyko**: usunięcie `BankAccount` kaskaduje do `Document` (CASCADE delete) → utrata danych dokumentów
- `Currency` przechowywany jako `int` (enum) — brak czytelności na poziomie surowej DB

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Karta tabeli na podstawie ModelSnapshot. |
