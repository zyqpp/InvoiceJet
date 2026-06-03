# Inwentaryzacja DTO — obiekty transferu danych

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Źródło | `InvoiceJetAPI/InvoiceJet.Application/DTOs/` |

## Lista DTO (14)

| ID | Klasa DTO | Plik | Kierunek | Używane w | Dokument | Status |
|---|---|---|---|---|---|---|
| DTO-01 | `UserLoginDto` | `UserLoginDto.cs` | Request → API | `AuthController.Login` | [link](../05_model_danych/03_dto/DTO-01_UserLoginDto.md) | szkic |
| DTO-02 | `UserRegisterDto` | `UserRegisterDto.cs` | Request → API | `AuthController.Register` | [link](../05_model_danych/03_dto/DTO-02_UserRegisterDto.md) | szkic |
| DTO-03 | `FirmDto` | `FirmDto.cs` | Obustronny | `FirmController`, `DocumentRequestDto` | [link](../05_model_danych/03_dto/DTO-03_FirmDto.md) | szkic |
| DTO-04 | `BankAccountDto` | `BankAccountDto.cs` | Obustronny | `BankAccountController`, `DocumentRequestDto` | [link](../05_model_danych/03_dto/DTO-04_BankAccountDto.md) | szkic |
| DTO-05 | `ProductDto` | `ProductDto.cs` | Obustronny | `ProductController` | [link](../05_model_danych/03_dto/DTO-05_ProductDto.md) | szkic |
| DTO-06 | `DocumentSeriesDto` | `DocumentSeriesDto.cs` | Obustronny | `DocumentSeriesController`, `DocumentAutofillDto` | [link](../05_model_danych/03_dto/DTO-06_DocumentSeriesDto.md) | szkic |
| DTO-07 | `DocumentStatusDto` | `DocumentStatusDto.cs` | API → Response | `DocumentAutofillDto`, `DocumentTableRecordDto` | [link](../05_model_danych/03_dto/DTO-07_DocumentStatusDto.md) | szkic |
| DTO-08 | `DocumentProductRequestDto` | `DocumentProductRequestDto.cs` | Request → API | `DocumentRequestDto` (lista produktów) | [link](../05_model_danych/03_dto/DTO-08_DocumentProductRequestDto.md) | szkic |
| DTO-09 | `DocumentRequestDto` | `DocumentRequestDto.cs` | Obustronny | `DocumentController.AddDocument`, `EditDocument`, `GenerateDocumentPdf`, `GetInvoicePdfStream` | [link](../05_model_danych/03_dto/DTO-09_DocumentRequestDto.md) | szkic |
| DTO-10 | `DocumentTableRecordDto` | `DocumentTableRecordDto.cs` | API → Response | `DocumentController.GetDocumentTableRecords` | [link](../05_model_danych/03_dto/DTO-10_DocumentTableRecordDto.md) | szkic |
| DTO-11 | `DocumentAutofillDto` | `DocumentAutofillDto.cs` | API → Response | `DocumentController.GetDocumentAutofillInfo` | [link](../05_model_danych/03_dto/DTO-11_DocumentAutofillDto.md) | szkic |
| DTO-12 | `DocumentStreamDto` | `DocumentStreamDto.cs` | API → Response | `DocumentController.GetInvoicePdfStream` | [link](../05_model_danych/03_dto/DTO-12_DocumentStreamDto.md) | szkic |
| DTO-13 | `DashboardStatsDto` | `DashboardStatsDto.cs` | API → Response | `DocumentController.GetDashboardStats` | [link](../05_model_danych/03_dto/DTO-13_DashboardStatsDto.md) | szkic |
| DTO-14 | `MonthlyTotalDto` | `MonthlyTotalDto.cs` | API → Response | `DashboardStatsDto` (lista miesięczna) | [link](../05_model_danych/03_dto/DTO-14_MonthlyTotalDto.md) | szkic |

## Szczegóły pól każdego DTO

### DTO-01 `UserLoginDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `Email` | `string` | nie | brak inicjalizacji domyślnej |
| `Password` | `string` | nie | brak inicjalizacji domyślnej |

### DTO-02 `UserRegisterDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `Id` | `Guid?` | tak | opcjonalny |
| `FirstName` | `string` | nie | — |
| `LastName` | `string` | nie | — |
| `Email` | `string` | nie | — |
| `Password` | `string` | nie | — |
| `PasswordConfirmation` | `string` | nie | walidacja po stronie serwisu |

### DTO-03 `FirmDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `Id` | `int` | nie | — |
| `Name` | `string` | nie | `string.Empty` |
| `Cui` | `string` | nie | numer identyfikacji podatkowej (Rumunia) |
| `RegCom` | `string?` | tak | numer rejestracji handlowej |
| `Address` | `string` | nie | `string.Empty` |
| `County` | `string` | nie | województwo/okręg |
| `City` | `string` | nie | `string.Empty` |

### DTO-04 `BankAccountDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `Id` | `int` | nie | — |
| `BankName` | `string` | nie | `string.Empty` |
| `Iban` | `string` | nie | `string.Empty` |
| `Currency` | `CurrencyEnum` | nie | enum: `Ron=0`, `Eur=1` |
| `IsActive` | `bool` | nie | — |

### DTO-05 `ProductDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `Id` | `int` | nie | — |
| `Name` | `string` | nie | `string.Empty` |
| `Price` | `decimal` | nie | `[Column(TypeName = "decimal(18,2)")]` |
| `ContainsTva` | `bool` | nie | domyślnie `false` |
| `UnitOfMeasurement` | `string?` | tak | `string.Empty` |
| `TvaValue` | `int` | nie | domyślnie `19` (procent VAT) |

### DTO-06 `DocumentSeriesDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `Id` | `int` | nie | — |
| `SeriesName` | `string` | nie | `string.Empty` |
| `FirstNumber` | `int` | nie | — |
| `CurrentNumber` | `int` | nie | inkrementowany przy każdym dokumencie |
| `IsDefault` | `bool` | nie | — |
| `DocumentTypeId` | `int?` | tak | FK do `DocumentType` |
| `DocumentType` | `DocumentType?` | tak | encja domenowa (nie DTO) — anomalia |

> **Uwaga (DTO-06-A):** `DocumentSeriesDto.DocumentType` jest typem domenowym `DocumentType`, nie DTO — naruszenie separacji warstw.

### DTO-07 `DocumentStatusDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `Id` | `int` | nie | — |
| `Status` | `string` | nie | `string.Empty` |

### DTO-08 `DocumentProductRequestDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `Id` | `int` | nie | — |
| `Name` | `string` | nie | `string.Empty` |
| `UnitPrice` | `decimal` | nie | cena jednostkowa |
| `TotalPrice` | `decimal` | nie | cena całkowita (z VAT lub bez) |
| `ContainsTva` | `bool` | nie | domyślnie `false` |
| `UnitOfMeasurement` | `string` | nie | `string.Empty` |
| `TvaValue` | `int` | nie | domyślnie `19` |
| `Quantity` | `int` | nie | — |

### DTO-09 `DocumentRequestDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `Id` | `int` | nie | — |
| `DocumentNumber` | `string?` | tak | null → generuje serwis |
| `Seller` | `FirmDto?` | tak | firma wystawiająca |
| `Client` | `FirmDto` | nie (null!) | klient — pole `null!` (wymagane) |
| `IssueDate` | `DateTime` | nie | data wystawienia |
| `DueDate` | `DateTime?` | tak | termin płatności |
| `BankAccount` | `BankAccountDto?` | tak | konto bankowe |
| `DocumentSeries` | `DocumentSeriesDto?` | tak | seria dokumentu |
| `DocumentType` | `DocumentType?` | tak | encja domenowa (anomalia) |
| `DocumentStatus` | `DocumentStatus?` | tak | encja domenowa (anomalia) |
| `Products` | `List<DocumentProductRequestDto>` | nie (null!) | — |

> **Uwaga (DTO-09-A):** `DocumentRequestDto.DocumentType` i `.DocumentStatus` to typy domenowe, nie DTO — naruszenie separacji warstw.

### DTO-10 `DocumentTableRecordDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `Id` | `int` | nie | — |
| `DocumentNumber` | `string` | nie | `string.Empty` |
| `ClientName` | `string` | nie | `string.Empty` — mapowane z `Document.Client.Name` |
| `IssueDate` | `DateTime` | nie | — |
| `DueDate` | `DateTime?` | tak | — |
| `TotalValue` | `decimal` | nie | mapowane z `Document.TotalPrice` |
| `DocumentStatus` | `DocumentStatus?` | tak | encja domenowa (anomalia) |

> **Uwaga (DTO-10-A):** `DocumentTableRecordDto.DocumentStatus` to typ domenowy, nie DTO.

### DTO-11 `DocumentAutofillDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `Clients` | `List<FirmDto>` | nie (null!) | lista klientów |
| `DocumentSeries` | `List<DocumentSeriesDto>` | nie (null!) | serie dokumentów |
| `DocumentStatuses` | `List<DocumentStatusDto>` | nie (null!) | statusy |
| `Products` | `List<ProductDto>` | nie (null!) | produkty |

### DTO-12 `DocumentStreamDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `DocumentNumber` | `string` | nie | `string.Empty` |
| `PdfContent` | `byte[]` | nie | `Array.Empty<byte>()` — zawartość PDF |

### DTO-13 `DashboardStatsDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `TotalDocuments` | `int` | nie | domyślnie `0` |
| `TotalClients` | `int` | nie | domyślnie `0` |
| `TotalProducts` | `int` | nie | domyślnie `0` |
| `TotalBankAccounts` | `int` | nie | domyślnie `0` |
| `MonthlyTotals` | `List<MonthlyTotalDto>?` | tak | lista 12 miesięcy |

### DTO-14 `MonthlyTotalDto`

| Pole | Typ C# | Nullable | Uwagi |
|---|---|---|---|
| `Month` | `int` | nie | 1–12 |
| `InvoiceAmount` | `decimal` | nie | suma wartości faktur w miesiącu |
| `IncomeAmount` | `decimal` | nie | suma przychodów w miesiącu |

## Anomalie DTO

| # | Anomalia |
|---|---|
| DTO-A01 | `DocumentSeriesDto.DocumentType` — typ domenowy `DocumentType`, nie DTO |
| DTO-A02 | `DocumentRequestDto.DocumentType` — typ domenowy `DocumentType`, nie DTO |
| DTO-A03 | `DocumentRequestDto.DocumentStatus` — typ domenowy `DocumentStatus`, nie DTO |
| DTO-A04 | `DocumentTableRecordDto.DocumentStatus` — typ domenowy `DocumentStatus`, nie DTO |
| DTO-A05 | `UserLoginDto` i `UserRegisterDto` — pola bez domyślnych wartości (brak `= string.Empty`), mogą powodować NullReferenceException |
| DTO-A06 | Brak DTO dla odpowiedzi z Auth endpointów (token JWT zwracany prawdopodobnie jako anonymous object lub string) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Inwentaryzacja wszystkich 14 DTO z polami. |
