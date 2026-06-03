# Tabela `dbo.DocumentSeries`

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Klasa domenowa | `InvoiceJet.Domain.Models.DocumentSeries` |

## Kolumny

| Kolumna | Typ SQL | Nullable | PK/FK | Uwagi |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | NOT NULL | **PK** | Autoincrement |
| `SeriesName` | `nvarchar(max)` | NOT NULL | — | Prefiks serii (np. "FV", "PRO", "STORNO") |
| `FirstNumber` | `int` | NOT NULL | — | Pierwsza wartość numeracji (zazwyczaj 1) |
| `CurrentNumber` | `int` | NOT NULL | — | Bieżący numer — inkrementowany po każdym wystawieniu dokumentu |
| `IsDefault` | `bit` | NOT NULL | — | Czy seria domyślna dla danego typu |
| `DocumentTypeId` | `int` | **NULL** | FK → `DocumentType.Id` | Typ dokumentu dla tej serii |
| `UserFirmId` | `int` | **NULL** | FK → `UserFirm.UserFirmId` | Właściciel — firma użytkownika |

## Indeksy

| Indeks | Kolumna | Unikalny |
|---|---|---|
| `IX_DocumentSeries_DocumentTypeId` | `DocumentTypeId` | NIE |
| `IX_DocumentSeries_UserFirmId` | `UserFirmId` | NIE |

## Relacje

| Kierunek | Relacja | Szczegóły |
|---|---|---|
| `DocumentSeries` → `UserFirm` | N:0..1 nullable | bez CASCADE |
| `DocumentSeries` → `DocumentType` | N:0..1 nullable | bez CASCADE |

## Dane seedowane

Brak.

## Uwagi

- Numer dokumentu generowany jako `SeriesName + CurrentNumber.ToString("D4")` (zero-padded do 4 cyfr)
- `CurrentNumber` inkrementowany po każdym zapisie dokumentu przez `IncreaseDocumentSeriesNumber()`
- Brak blokady (lock) na `CurrentNumber` — przy równoczesnym tworzeniu dokumentów możliwy race condition (zduplikowane numery)
- `IsDefault` — brak ograniczenia DB że tylko jedna seria na typ może być domyślna; logika aplikacji musi to egzekwować
- `FirstNumber` i `CurrentNumber` — `FirstNumber` ustawiany przy tworzeniu, `CurrentNumber` inkrementowany; `CurrentNumber` zawsze ≥ `FirstNumber` (logicznie)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Karta tabeli na podstawie ModelSnapshot. |
