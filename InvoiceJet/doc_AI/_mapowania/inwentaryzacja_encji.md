# Inwentaryzacja encji DB

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Źródło | `InvoiceJetAPI/InvoiceJet.Infrastructure/Migrations/InvoiceJetDbContextModelSnapshot.cs` |

## Lista encji

| Nazwa encji | Tabela DB | Lokalizacja klasy | Dokument | Status |
|---|---|---|---|---|
| `User` | `User` | `InvoiceJetAPI/InvoiceJet.Domain/Models/User.cs` | [`../05_model_danych/01_db/dbo/dbo.User.md`](../05_model_danych/01_db/dbo/dbo.User.md) | szkic |
| `Firm` | `Firm` | `InvoiceJetAPI/InvoiceJet.Domain/Models/Firm.cs` | [`../05_model_danych/01_db/dbo/dbo.Firm.md`](../05_model_danych/01_db/dbo/dbo.Firm.md) | szkic |
| `BankAccount` | `BankAccount` | `InvoiceJetAPI/InvoiceJet.Domain/Models/BankAccount.cs` | [`../05_model_danych/01_db/dbo/dbo.BankAccount.md`](../05_model_danych/01_db/dbo/dbo.BankAccount.md) | szkic |
| `UserFirm` | `UserFirm` | `InvoiceJetAPI/InvoiceJet.Domain/Models/UserFirm.cs` | [`../05_model_danych/01_db/dbo/dbo.UserFirm.md`](../05_model_danych/01_db/dbo/dbo.UserFirm.md) | szkic |
| `Product` | `Product` | `InvoiceJetAPI/InvoiceJet.Domain/Models/Product.cs` | [`../05_model_danych/01_db/dbo/dbo.Product.md`](../05_model_danych/01_db/dbo/dbo.Product.md) | szkic |
| `DocumentType` | `DocumentType` | `InvoiceJetAPI/InvoiceJet.Domain/Models/DocumentType.cs` | [`../05_model_danych/01_db/dbo/dbo.DocumentType.md`](../05_model_danych/01_db/dbo/dbo.DocumentType.md) | szkic |
| `DocumentSeries` | `DocumentSeries` | `InvoiceJetAPI/InvoiceJet.Domain/Models/DocumentSeries.cs` | [`../05_model_danych/01_db/dbo/dbo.DocumentSeries.md`](../05_model_danych/01_db/dbo/dbo.DocumentSeries.md) | szkic |
| `Document` | `Document` | `InvoiceJetAPI/InvoiceJet.Domain/Models/Document.cs` | [`../05_model_danych/01_db/dbo/dbo.Document.md`](../05_model_danych/01_db/dbo/dbo.Document.md) | szkic |
| `DocumentProduct` | `DocumentProduct` | `InvoiceJetAPI/InvoiceJet.Domain/Models/DocumentProduct.cs` | [`../05_model_danych/01_db/dbo/dbo.DocumentProduct.md`](../05_model_danych/01_db/dbo/dbo.DocumentProduct.md) | szkic |
| `DocumentStatus` | `DocumentStatus` | `InvoiceJetAPI/InvoiceJet.Domain/Models/DocumentStatus.cs` | [`../05_model_danych/01_db/dbo/dbo.DocumentStatus.md`](../05_model_danych/01_db/dbo/dbo.DocumentStatus.md) | szkic |

## Dodatkowe informacje

- Wszystkie encje w jednej schemie `dbo` (SQL Server domyślna).
- `DbContext`: `InvoiceJetDbContext` (`InvoiceJetAPI/InvoiceJet.Infrastructure/Persistence/InvoiceJetDbContext.cs`).
- EF Core wersja: 8.0.6 (z snapshot).
- Jawna konfiguracja w `OnModelCreating`:
  - `User.ActiveUserFirmId` → nullable FK do `UserFirm`
  - `Product.Name` → unikalny indeks
- Dane seedowane: `DocumentType` (3 rekordy), `DocumentStatus` (2 rekordy) — przez `DbSeeder` przy starcie.
