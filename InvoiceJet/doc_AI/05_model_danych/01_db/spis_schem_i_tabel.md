# Spis schematów i tabel

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Źródło | `InvoiceJetDbContextModelSnapshot.cs`, EF Core 8.0.6 |

## Ogólne informacje

| Parametr | Wartość |
|---|---|
| Silnik DB | Microsoft SQL Server |
| ORM | Entity Framework Core 8.0.6 |
| Strategia | Code First z migracjami |
| Schema | `dbo` (jedyna schema; domyślna SQL Server) |
| Liczba tabel | 10 |
| Identity columns | SQL Server IDENTITY (autoincrement) na wszystkich kolumnach PK poza `User.Id` (GUID) |

## Lista tabel (10)

| # | Tabela | PK | PK Typ | Wiersze seedowane | Dokument |
|---|---|---|---|---|---|
| 1 | `User` | `Id` | `uniqueidentifier` (GUID) | — | [link](dbo/dbo.User.md) |
| 2 | `Firm` | `Id` | `int` IDENTITY | — | [link](dbo/dbo.Firm.md) |
| 3 | `UserFirm` | `UserFirmId` | `int` IDENTITY | — | [link](dbo/dbo.UserFirm.md) |
| 4 | `BankAccount` | `Id` | `int` IDENTITY | — | [link](dbo/dbo.BankAccount.md) |
| 5 | `Product` | `Id` | `int` IDENTITY | — | [link](dbo/dbo.Product.md) |
| 6 | `DocumentType` | `Id` | `int` IDENTITY | 3 (seeded) | [link](dbo/dbo.DocumentType.md) |
| 7 | `DocumentStatus` | `Id` | `int` IDENTITY | 2 (seeded) | [link](dbo/dbo.DocumentStatus.md) |
| 8 | `DocumentSeries` | `Id` | `int` IDENTITY | — | [link](dbo/dbo.DocumentSeries.md) |
| 9 | `Document` | `Id` | `int` IDENTITY | — | [link](dbo/dbo.Document.md) |
| 10 | `DocumentProduct` | `Id` | `int` IDENTITY | — | [link](dbo/dbo.DocumentProduct.md) |

## Relacje (FK) — zestawienie

| FK | Od tabeli.Kolumna | Do tabeli.Kolumna | Wymagany | OnDelete |
|---|---|---|---|---|
| FK-01 | `UserFirm.UserId` | `User.Id` | TAK | CASCADE |
| FK-02 | `UserFirm.FirmId` | `Firm.Id` | TAK | CASCADE |
| FK-03 | `User.ActiveUserFirmId` | `UserFirm.UserFirmId` | NIE | — |
| FK-04 | `BankAccount.UserFirmId` | `UserFirm.UserFirmId` | TAK | CASCADE |
| FK-05 | `Product.UserFirmId` | `UserFirm.UserFirmId` | NIE | — |
| FK-06 | `DocumentSeries.UserFirmId` | `UserFirm.UserFirmId` | NIE | — |
| FK-07 | `DocumentSeries.DocumentTypeId` | `DocumentType.Id` | NIE | — |
| FK-08 | `Document.UserFirmId` | `UserFirm.UserFirmId` | NIE | — |
| FK-09 | `Document.BankAccountId` | `BankAccount.Id` | TAK | CASCADE |
| FK-10 | `Document.ClientId` | `Firm.Id` | NIE | — |
| FK-11 | `Document.DocumentStatusId` | `DocumentStatus.Id` | NIE | — |
| FK-12 | `Document.DocumentTypeId` | `DocumentType.Id` | NIE | — |
| FK-13 | `DocumentProduct.DocumentId` | `Document.Id` | NIE | — |
| FK-14 | `DocumentProduct.ProductId` | `Product.Id` | NIE | — |

## Indeksy — zestawienie

| Tabela | Kolumna(y) | Typ indeksu | Uwagi |
|---|---|---|---|
| `BankAccount` | `UserFirmId` | Non-unique | FK lookup |
| `Document` | `BankAccountId` | Non-unique | FK lookup |
| `Document` | `ClientId` | Non-unique | FK lookup |
| `Document` | `DocumentStatusId` | Non-unique | FK lookup |
| `Document` | `DocumentTypeId` | Non-unique | FK lookup |
| `Document` | `UserFirmId` | Non-unique | FK lookup |
| `DocumentProduct` | `DocumentId` | Non-unique | FK lookup |
| `DocumentProduct` | `ProductId` | Non-unique | FK lookup |
| `DocumentSeries` | `DocumentTypeId` | Non-unique | FK lookup |
| `DocumentSeries` | `UserFirmId` | Non-unique | FK lookup |
| `Product` | `Name` | **UNIQUE** | `nvarchar(450)` — unikalna nazwa produktu |
| `Product` | `UserFirmId` | Non-unique | FK lookup |
| `User` | `ActiveUserFirmId` | Non-unique | FK lookup |
| `UserFirm` | `FirmId` | Non-unique | FK lookup |
| `UserFirm` | `UserId` | Non-unique | FK lookup |

## Uwagi

- Brak timestampów audytowych (`CreatedAt`, `UpdatedAt`) we wszystkich tabelach
- `Product.Name` UNIQUE jest globalny (nie per UserFirm) — dwa różnych użytkowników nie mogą mieć produktu o tej samej nazwie
- Usuwanie konta bankowego (`BankAccount`) kasuje kaskadowo wszystkie dokumenty powiązane z tym kontem (FK-09 CASCADE)
- Usuwanie firmy (`Firm`) kasuje kaskadowo rekordy `UserFirm` (FK-02 CASCADE)
- Usuwanie użytkownika (`User`) kasuje kaskadowo rekordy `UserFirm` (FK-01 CASCADE)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Spis tabel i relacji na podstawie ModelSnapshot. |
