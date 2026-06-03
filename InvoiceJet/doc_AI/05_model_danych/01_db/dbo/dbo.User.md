# Tabela `dbo.User`

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Klasa domenowa | `InvoiceJet.Domain.Models.User` |

## Kolumny

| Kolumna | Typ SQL | Nullable | PK/FK | Uwagi |
|---|---|---|---|---|
| `Id` | `uniqueidentifier` | NOT NULL | **PK** | GUID generowany przez EF Core; jedyne PK GUID w projekcie |
| `FirstName` | `nvarchar(max)` | NOT NULL | — | Imię |
| `LastName` | `nvarchar(max)` | NOT NULL | — | Nazwisko |
| `Email` | `nvarchar(max)` | NOT NULL | — | Unikalność egzekwowana przez serwis (nie indeks DB) |
| `PasswordHash` | `nvarchar(max)` | NOT NULL | — | BCrypt hash (z wbudowanym salt) |
| `Role` | `nvarchar(max)` | NOT NULL | — | Wartość hardcoded: `"User"` |
| `ActiveUserFirmId` | `int` | **NULL** | FK → `UserFirm.UserFirmId` | Aktywna firma; nullable — user może nie mieć firmy |

## Indeksy

| Indeks | Kolumna | Unikalny |
|---|---|---|
| `IX_User_ActiveUserFirmId` | `ActiveUserFirmId` | NIE |

## Relacje

| Kierunek | Relacja | Szczegóły |
|---|---|---|
| `User` → `UserFirm` | Nullable FK | `User.ActiveUserFirmId → UserFirm.UserFirmId`; brak OnDelete |
| `UserFirm` → `User` | Wymagany FK | `UserFirm.UserId → User.Id`; OnDelete CASCADE |

## Dane seedowane

Brak.

## Uwagi

- `Email` nie ma indeksu UNIQUE na poziomie bazy — unikalność sprawdzana w `AuthService.RegisterUser()` przez `FirstOrDefaultAsync`
- `Role` zawsze `"User"` — hardcoded w `AuthService.CreateToken()` i przy tworzeniu obiektu User
- `Id` jako GUID zamiast `int` — niespójne z pozostałymi tabelami
- `PasswordHash` przechowuje cały hash BCrypt (zawiera salt i work factor)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Karta tabeli na podstawie ModelSnapshot. |
