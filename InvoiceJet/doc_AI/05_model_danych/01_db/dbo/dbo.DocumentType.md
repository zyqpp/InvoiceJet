# Tabela `dbo.DocumentType`

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Klasa domenowa | `InvoiceJet.Domain.Models.DocumentType` |

## Kolumny

| Kolumna | Typ SQL | Nullable | PK/FK | Uwagi |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | NOT NULL | **PK** | Autoincrement |
| `Name` | `nvarchar(max)` | NOT NULL | — | Nazwa typu dokumentu |

## Indeksy

Brak (poza PK).

## Relacje

| Kierunek | Relacja | Szczegóły |
|---|---|---|
| `Document.DocumentTypeId` → `DocumentType` | N:0..1 nullable | — |
| `DocumentSeries.DocumentTypeId` → `DocumentType` | N:0..1 nullable | — |

## Dane seedowane

Seedowane przez `DbSeeder.SeedDocumentTypes()` przy starcie aplikacji:

| Id | Name |
|---|---|
| 1 | `Factura` |
| 2 | `Factura Proforma` |
| 3 | `Factura Storno` |

**Enum odpowiadający:**
```csharp
// DocumentTypeEnum.cs
enum DocumentTypeEnum { Invoice = 1, ProformaInvoice = 2, StornoInvoice = 3 }
```

## Uwagi

- Tabela słownikowa — dane niezmienne po seedowaniu
- `Document.DocumentTypeId` jest nullable mimo że logicznie każdy dokument musi mieć typ

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Karta tabeli na podstawie ModelSnapshot. |
