# Tabela `dbo.Document`

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Klasa domenowa | `InvoiceJet.Domain.Models.Document` |

## Kolumny

| Kolumna | Typ SQL | Nullable | PK/FK | Uwagi |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | NOT NULL | **PK** | Autoincrement |
| `DocumentNumber` | `nvarchar(max)` | NOT NULL | — | Wygenerowany numer (np. "FV0005") |
| `IssueDate` | `datetime2` | NOT NULL | — | Data wystawienia |
| `DueDate` | `datetime2` | **NULL** | — | Termin płatności (opcjonalny) |
| `UnitPrice` | `decimal(18,2)` | NOT NULL | — | Suma cen netto (bez VAT) pozycji × ilości |
| `TotalPrice` | `decimal(18,2)` | NOT NULL | — | Suma brutto (z VAT) wszystkich pozycji |
| `BankAccountId` | `int` | NOT NULL | FK → `BankAccount.Id` **CASCADE** | Konto bankowe — wymagane! |
| `ClientId` | `int` | **NULL** | FK → `Firm.Id` | Klient |
| `DocumentStatusId` | `int` | **NULL** | FK → `DocumentStatus.Id` | Status (Unpaid/Paid) |
| `DocumentTypeId` | `int` | **NULL** | FK → `DocumentType.Id` | Typ (Faktura/Proforma/Storno) |
| `UserFirmId` | `int` | **NULL** | FK → `UserFirm.UserFirmId` | Firma wystawiająca |

## Indeksy

| Indeks | Kolumna | Unikalny |
|---|---|---|
| `IX_Document_BankAccountId` | `BankAccountId` | NIE |
| `IX_Document_ClientId` | `ClientId` | NIE |
| `IX_Document_DocumentStatusId` | `DocumentStatusId` | NIE |
| `IX_Document_DocumentTypeId` | `DocumentTypeId` | NIE |
| `IX_Document_UserFirmId` | `UserFirmId` | NIE |

## Relacje

| Kierunek | Relacja | Szczegóły |
|---|---|---|
| `Document` → `BankAccount` | N:1 wymagana | **CASCADE** — usunięcie konta kasuje dokumenty |
| `Document` → `Firm` (Client) | N:0..1 nullable | bez CASCADE |
| `Document` → `DocumentStatus` | N:0..1 nullable | bez CASCADE |
| `Document` → `DocumentType` | N:0..1 nullable | bez CASCADE |
| `Document` → `UserFirm` | N:0..1 nullable | bez CASCADE |
| `Document` ← `DocumentProduct` | 1:N | `DocumentProduct.DocumentId → Document.Id` |

## Dane seedowane

Brak.

## Uwagi

- `DocumentNumber` — brak UNIQUE constraint; duplikaty możliwe przy race condition (patrz [dbo.DocumentSeries.md](dbo.DocumentSeries.md))
- `UserFirmId` nullable mimo że logicznie każdy dokument musi należeć do firmy
- `DocumentTypeId` nullable mimo że każdy dokument musi mieć typ
- `BankAccountId` NOT NULL + CASCADE delete — usunięcie konta bankowego kasuje WSZYSTKIE powiązane dokumenty (⚠️ niebezpieczne)
- `UnitPrice` = suma netto, `TotalPrice` = suma brutto — wyliczane w `UpdateDocumentProducts()` przy każdym zapisie
- Brak pola `SeriesId` — relacja z serią dokumentów zachowana tylko przez `DocumentNumber` (string)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Karta tabeli na podstawie ModelSnapshot. |
