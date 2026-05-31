# Tabela `dbo.Firm`

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Klasa domenowa | `InvoiceJet.Domain.Models.Firm` |

## Kolumny

| Kolumna | Typ SQL | Nullable | PK/FK | Uwagi |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | NOT NULL | **PK** | Autoincrement |
| `Name` | `nvarchar(max)` | NOT NULL | — | Nazwa firmy |
| `Cui` | `nvarchar(max)` | NOT NULL | — | Cod Unic de Înregistrare (rumuński NIP) |
| `RegCom` | `nvarchar(max)` | **NOT NULL** (snapshot) | — | Numer rejestracji handlowej; **UWAGA:** w DTO jako `string?` (nullable) |
| `Address` | `nvarchar(max)` | NOT NULL | — | Adres |
| `County` | `nvarchar(max)` | NOT NULL | — | Okręg/województwo (jud.) |
| `City` | `nvarchar(max)` | NOT NULL | — | Miasto |

## Indeksy

Brak (poza PK).

## Relacje

| Kierunek | Relacja | Szczegóły |
|---|---|---|
| `Firm` → `UserFirm` (kolekcja) | 1:N | `UserFirm.FirmId → Firm.Id`; OnDelete CASCADE |
| `Document.ClientId` → `Firm` | N:0..1 | Firma jako klient dokumentu; nullable |

## Dane seedowane

Brak.

## Uwagi

- Ta sama tabela `Firm` przechowuje zarówno **własne firmy użytkownika**, jak i **klientów** — rozróżnienie przez `UserFirm.IsClient`
- `RegCom` — niespójność: NOT NULL w snapshot, ale `FirmDto.RegCom` jako `string?`. Aplikacja może wysyłać `null` → potencjalny błąd przy zapisie
- Brak indeksu na `Cui` — wyszukiwanie po CUI (integracja ANAF) wykonywane bez indeksu

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Karta tabeli na podstawie ModelSnapshot. |
