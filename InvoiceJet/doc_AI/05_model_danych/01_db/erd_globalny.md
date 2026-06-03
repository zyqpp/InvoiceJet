# ERD Globalny — diagram encji

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Źródło | `InvoiceJetDbContextModelSnapshot.cs` |

## Diagram Mermaid

```mermaid
erDiagram
    User {
        uniqueidentifier Id PK
        nvarchar         FirstName "NOT NULL"
        nvarchar         LastName "NOT NULL"
        nvarchar         Email "NOT NULL"
        nvarchar         PasswordHash "NOT NULL"
        nvarchar         Role "NOT NULL"
        int              ActiveUserFirmId "NULL, FK→UserFirm"
    }

    Firm {
        int      Id PK
        nvarchar Name "NOT NULL"
        nvarchar Cui "NOT NULL"
        nvarchar RegCom "NOT NULL (snapshot); nullable w DTO"
        nvarchar Address "NOT NULL"
        nvarchar County "NOT NULL"
        nvarchar City "NOT NULL"
    }

    UserFirm {
        int             UserFirmId PK
        uniqueidentifier UserId "NOT NULL, FK→User CASCADE"
        int             FirmId "NOT NULL, FK→Firm CASCADE"
        bit             IsClient "NOT NULL"
    }

    BankAccount {
        int      Id PK
        nvarchar BankName "NOT NULL"
        nvarchar Iban "NOT NULL"
        int      Currency "NOT NULL (enum: Ron=0, Eur=1)"
        bit      IsActive "NOT NULL"
        int      UserFirmId "NOT NULL, FK→UserFirm CASCADE"
    }

    Product {
        int      Id PK
        nvarchar Name "NOT NULL, UNIQUE (nvarchar(450))"
        decimal  Price "decimal(18,2) NOT NULL"
        bit      ContainsTva "NOT NULL"
        int      TvaValue "NOT NULL"
        nvarchar UnitOfMeasurement "NULL"
        int      UserFirmId "NULL, FK→UserFirm"
    }

    DocumentType {
        int      Id PK
        nvarchar Name "NOT NULL (seeded: Factura, Proforma, Storno)"
    }

    DocumentStatus {
        int      Id PK
        nvarchar Status "NOT NULL (seeded: Unpaid, Paid)"
    }

    DocumentSeries {
        int      Id PK
        nvarchar SeriesName "NOT NULL"
        int      FirstNumber "NOT NULL"
        int      CurrentNumber "NOT NULL"
        bit      IsDefault "NOT NULL"
        int      DocumentTypeId "NULL, FK→DocumentType"
        int      UserFirmId "NULL, FK→UserFirm"
    }

    Document {
        int      Id PK
        nvarchar DocumentNumber "NOT NULL"
        datetime IssueDate "NOT NULL"
        datetime DueDate "NULL"
        decimal  UnitPrice "decimal(18,2) NOT NULL"
        decimal  TotalPrice "decimal(18,2) NOT NULL"
        int      BankAccountId "NOT NULL, FK→BankAccount CASCADE"
        int      ClientId "NULL, FK→Firm"
        int      DocumentStatusId "NULL, FK→DocumentStatus"
        int      DocumentTypeId "NULL, FK→DocumentType"
        int      UserFirmId "NULL, FK→UserFirm"
    }

    DocumentProduct {
        int     Id PK
        decimal Quantity "decimal(18,2) NOT NULL"
        decimal UnitPrice "decimal(18,2) NOT NULL"
        decimal TotalPrice "decimal(18,2) NOT NULL"
        int     DocumentId "NULL, FK→Document"
        int     ProductId "NULL, FK→Product"
    }

    %% Relacje
    User          ||--o| UserFirm       : "ActiveUserFirmId (nullable)"
    UserFirm      }o--|| User           : "UserId (CASCADE)"
    UserFirm      }o--|| Firm           : "FirmId (CASCADE)"
    UserFirm      ||--o{ BankAccount    : "has"
    UserFirm      ||--o{ Product        : "has"
    UserFirm      ||--o{ DocumentSeries : "has"
    UserFirm      ||--o{ Document       : "has"
    Document      ||--o{ DocumentProduct : "contains"
    DocumentProduct }o--o| Product       : "references"
    Document      }o--|| BankAccount    : "BankAccountId (CASCADE)"
    Document      }o--o| Firm           : "ClientId (nullable)"
    Document      }o--o| DocumentStatus : "nullable"
    Document      }o--o| DocumentType   : "nullable"
    DocumentSeries }o--o| DocumentType  : "nullable"
```

## Legenda relacji

| Notacja | Znaczenie |
|---|---|
| `||--||` | jeden do jednego (obowiązkowy) |
| `||--o|` | jeden do zero-lub-jeden (nullable FK) |
| `||--o{` | jeden do wielu (obowiązkowy) |
| `}o--||` | wiele do jednego (wymagany FK) |
| `}o--o|` | wiele do zero-lub-jeden (nullable FK) |
| CASCADE | kasowanie rodzica kasuje dzieci |

## Kluczowe obserwacje

| # | Obserwacja |
|---|---|
| OBS-01 | `Document.BankAccountId` NOT NULL + CASCADE → usunięcie konta bankowego kasuje WSZYSTKIE powiązane dokumenty |
| OBS-02 | `Document.UserFirmId` jest nullable (int?) mimo że logicznie każdy dokument musi mieć firmę |
| OBS-03 | `Document.DocumentTypeId` i `DocumentStatusId` są nullable — dokument może być bez statusu/typu |
| OBS-04 | `Product.Name` — UNIQUE INDEX na `nvarchar(450)` — nazwy produktów muszą być unikalne globalnie (nie per UserFirm!) |
| OBS-05 | `Firm.RegCom` — w snapshot IsRequired (nvarchar(max)), ale w `FirmDto.RegCom` jest nullable string? — niespójność |
| OBS-06 | `UserFirm.IsClient` — flaga odróżniająca firmę własną od klienta; ta sama tabela `Firm` służy dla obu |
| OBS-07 | Brak jawnego `UpdatedAt`/`CreatedAt` — żadna tabela nie ma timestampów audytowych |
| OBS-08 | `User.Id` — `uniqueidentifier` (GUID), podczas gdy wszystkie inne klucze to `int` IDENTITY |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | ERD na podstawie ModelSnapshot EF Core. |
