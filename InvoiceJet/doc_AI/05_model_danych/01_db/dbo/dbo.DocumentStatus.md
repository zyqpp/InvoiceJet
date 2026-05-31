# Tabela `dbo.DocumentStatus`

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Klasa domenowa | `InvoiceJet.Domain.Models.DocumentStatus` |

## Kolumny

| Kolumna | Typ SQL | Nullable | PK/FK | Uwagi |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | NOT NULL | **PK** | Autoincrement |
| `Status` | `nvarchar(max)` | NOT NULL | — | Nazwa statusu |

## Indeksy

Brak (poza PK).

## Relacje

| Kierunek | Relacja | Szczegóły |
|---|---|---|
| `Document.DocumentStatusId` → `DocumentStatus` | N:0..1 nullable | — |

## Dane seedowane

Seedowane przez `DbSeeder.SeedDocumentTypes()` przy starcie aplikacji:

| Id | Status |
|---|---|
| 1 | `Unpaid` |
| 2 | `Paid` |

**Enum odpowiadający:**
```csharp
// DocumentStatusEnum.cs
enum DocumentStatusEnum { Unpaid = 1, Paid = 2 }
```

## Uwagi

- Tabela słownikowa — dane niezmienne po seedowaniu
- Nowy dokument tworzony zawsze ze statusem `Unpaid` (Id=1): `DocumentStatusId = (int)DocumentStatusEnum.Unpaid`
- `Document.DocumentStatusId` jest nullable

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Karta tabeli na podstawie ModelSnapshot. |
