# ERD schematu dbo — InvoiceJet

| Pole | Wartość |
|---|---|
| ID dokumentu | ERD-DBO-01 |
| Typ dokumentu | Diagram ERD |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Opis

Skrócony diagram ERD dla schematu `dbo` projektu InvoiceJet. Zawiera wszystkie 10 tabel z kluczowymi relacjami (PK, FK). Pola nie będące kluczami głównie pominięte dla czytelności — szczegółowe definicje kolumn dostępne w plikach per-tabela.

## Diagram Mermaid

```mermaid
erDiagram
    User {
        int Id PK
        string FirstName
        string LastName
        string Email
        string PasswordHash
    }

    Firm {
        int Id PK
        string FirmName
        string CuiValue
        string RegCom
        string Address
        string County
        string City
    }

    UserFirm {
        int Id PK
        int UserId FK
        int FirmId FK
    }

    BankAccount {
        int Id PK
        int UserFirmId FK
        string BankName
        string Iban
        string Currency
    }

    Product {
        int Id PK
        int UserFirmId FK
        string Name
        string MeasureUnit
        decimal Price
        decimal VatRate
    }

    DocumentType {
        int Id PK
        string Name
    }

    DocumentSeries {
        int Id PK
        int UserFirmId FK
        int DocumentTypeId FK
        string SeriesName
        int CurrentNumber
    }

    DocumentStatus {
        int Id PK
        string Name
    }

    Document {
        int Id PK
        int UserFirmId FK
        int ClientId FK
        int BankAccountId FK
        int DocumentSeriesId FK
        int DocumentTypeId FK
        int DocumentStatusId FK
        string DocumentNumber
        datetime IssueDate
        datetime DueDate
        decimal TotalPrice
    }

    DocumentProduct {
        int Id PK
        int DocumentId FK
        int ProductId FK
        decimal Quantity
        decimal Price
        decimal VatRate
    }

    User ||--o{ UserFirm : "ma"
    Firm ||--o{ UserFirm : "ma"
    UserFirm ||--o{ BankAccount : "posiada"
    UserFirm ||--o{ Product : "posiada"
    UserFirm ||--o{ DocumentSeries : "posiada"
    UserFirm ||--o{ Document : "wystawia (jako sprzedawca)"
    Firm ||--o{ Document : "jest nabywca"
    DocumentType ||--o{ Document : "klasyfikuje"
    DocumentType ||--o{ DocumentSeries : "typizuje"
    DocumentStatus ||--o{ Document : "ma status"
    Document ||--o{ DocumentProduct : "ma pozycje"
    Product ||--o{ DocumentProduct : "wystepuje w"
    BankAccount ||--o{ Document : "powiazane z"
    DocumentSeries ||--o{ Document : "numeruje"
```

## Uwagi do diagramu

- `UserFirm` to tabela pośrednicząca User–Firm (wystawiający fakturę). Relacja User:UserFirm = 1:1 praktycznie (jeden użytkownik ma jedną aktywną firmę).
- `Firm` jest reużywana zarówno jako firma własna (poprzez `UserFirm.FirmId`) jak i firma klienta (poprzez `Document.ClientId`).
- `DocumentProduct` to tabela junction między `Document` a `Product` — przechowuje snapshot wartości produktu w chwili wystawienia.
- Tabele `DocumentType` i `DocumentStatus` są tabelami słownikowymi — wypełniane przez `DbSeeder` przy starcie.
- Relacja `UserFirm` ↔ klienci (`Firm`) jest relacją M:N przez dodatkową tabelę junction `UserFirm_Firm` (szczegóły w [dbo.UserFirm_relations.md](dbo.UserFirm_relations.md)).

## Powiązane dokumenty

| Dokument | Opis |
|---|---|
| [erd_globalny.md](../erd_globalny.md) | Rozszerzony ERD z pełną listą kolumn |
| [dbo.UserFirm_relations.md](dbo.UserFirm_relations.md) | Szczegóły relacji M:N UserFirm–Firm (klienci) |
| [dbo.Document.md](dbo.Document.md) | Tabela centralna — dokumenty finansowe |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — schemat dbo. |
