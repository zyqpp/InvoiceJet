# Mapa: Pola DB ↔ DTO ↔ ekrany UI (M-02)

| Pole | Wartość |
|---|---|
| ID dokumentu | M-02 |
| Typ dokumentu | mapa krzyżowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Mapa śledzi przepływ kluczowych pól danych od kolumny w tabeli DB, przez pole DTO w warstwie aplikacji, aż do komponentu Angular wyświetlającego lub przyjmującego te dane. Skupia się na polach faktycznie używanych w UI — pomija pola czysto techniczne (np. `IsDeleted`, `CreatedAt`) niewidoczne dla użytkownika.

## Tabela mapowań

### Tabela: User

| Tabela DB | Kolumna | DTO | Pole DTO | Ekran (komponent) | Uwagi |
|---|---|---|---|---|---|
| `User` | `Id` (Guid) | `UserRegisterDto` | `Id` | EKRAN-02 `RegisterComponent` | Opcjonalne przy rejestracji |
| `User` | `FirstName` | `UserRegisterDto` | `FirstName` | EKRAN-02 `RegisterComponent` | Pole formularza rejestracji |
| `User` | `LastName` | `UserRegisterDto` | `LastName` | EKRAN-02 `RegisterComponent` | Pole formularza rejestracji |
| `User` | `Email` | `UserRegisterDto` / `UserLoginDto` | `Email` | EKRAN-01 `LoginComponent`, EKRAN-02 `RegisterComponent` | Używane do logowania i rejestracji |
| `User` | `PasswordHash` | `UserRegisterDto` / `UserLoginDto` | `Password` | EKRAN-01, EKRAN-02 | Hashowane BCrypt przed zapisem — pole `Password` to plaintext w DTO |
| `User` | `PasswordHash` | `UserRegisterDto` | `PasswordConfirmation` | EKRAN-02 `RegisterComponent` | Tylko walidacja — nie trafia do DB |

### Tabela: Firm

| Tabela DB | Kolumna | DTO | Pole DTO | Ekran (komponent) | Uwagi |
|---|---|---|---|---|---|
| `Firm` | `Id` | `FirmDto` | `Id` | EKRAN-04, EKRAN-05, DIALOG-01 | Identyfikator firmy/klienta |
| `Firm` | `Name` | `FirmDto` | `Name` | EKRAN-04 `FirmDetailsComponent`, EKRAN-05 `ClientsComponent`, DIALOG-01 | Nazwa firmy / klienta |
| `Firm` | `Cui` | `FirmDto` | `Cui` | EKRAN-04, DIALOG-01 | Numer identyfikacji podatkowej (Rumunia) |
| `Firm` | `RegCom` | `FirmDto` | `RegCom` | EKRAN-04, DIALOG-01 | Numer rejestracji handlowej (opcjonalny) |
| `Firm` | `Address` | `FirmDto` | `Address` | EKRAN-04, DIALOG-01 | Adres siedziby |
| `Firm` | `County` | `FirmDto` | `County` | EKRAN-04, DIALOG-01 | Okręg/województwo (Rumunia) |
| `Firm` | `City` | `FirmDto` | `City` | EKRAN-04, DIALOG-01 | Miasto |
| `Firm` | `Name` | `DocumentTableRecordDto` | `ClientName` | EKRAN-09 `InvoicesComponent`, EKRAN-11, EKRAN-13 | Mapowane z `Document.Client.Name` — wyświetlane w tabeli |

### Tabela: BankAccount

| Tabela DB | Kolumna | DTO | Pole DTO | Ekran (komponent) | Uwagi |
|---|---|---|---|---|---|
| `BankAccount` | `Id` | `BankAccountDto` | `Id` | EKRAN-06 `BankAccountsComponent`, DIALOG-02 | Identyfikator konta |
| `BankAccount` | `BankName` | `BankAccountDto` | `BankName` | EKRAN-06, DIALOG-02, EKRAN-10 (formularz faktury) | Nazwa banku — widoczna na fakturze |
| `BankAccount` | `Iban` | `BankAccountDto` | `Iban` | EKRAN-06, DIALOG-02, EKRAN-10 | Numer IBAN — widoczny na fakturze |
| `BankAccount` | `Currency` | `BankAccountDto` | `Currency` | EKRAN-06, DIALOG-02, EKRAN-10 | Enum: `Ron=0`, `Eur=1` |
| `BankAccount` | `IsActive` | `BankAccountDto` | `IsActive` | EKRAN-06 | Oznaczenie aktywnego konta |

### Tabela: Product

| Tabela DB | Kolumna | DTO | Pole DTO | Ekran (komponent) | Uwagi |
|---|---|---|---|---|---|
| `Product` | `Id` | `ProductDto` | `Id` | EKRAN-07 `ProductsComponent`, DIALOG-03 | |
| `Product` | `Name` | `ProductDto` | `Name` | EKRAN-07, DIALOG-03, EKRAN-10/12 (wiersze faktury) | Unikalna nazwa produktu (indeks unikalny w DB) |
| `Product` | `Price` | `ProductDto` | `Price` | EKRAN-07, DIALOG-03, EKRAN-10/12 | Cena jednostkowa `decimal(18,2)` |
| `Product` | `ContainsTva` | `ProductDto` | `ContainsTva` | DIALOG-03, EKRAN-10/12 | Czy cena zawiera VAT |
| `Product` | `TvaValue` | `ProductDto` | `TvaValue` | DIALOG-03, EKRAN-10/12 | Stawka VAT w % (domyślnie 19) |
| `Product` | `UnitOfMeasurement` | `ProductDto` | `UnitOfMeasurement` | DIALOG-03, EKRAN-10/12 | Jednostka miary (opcjonalna) |

### Tabela: DocumentSeries

| Tabela DB | Kolumna | DTO | Pole DTO | Ekran (komponent) | Uwagi |
|---|---|---|---|---|---|
| `DocumentSeries` | `Id` | `DocumentSeriesDto` | `Id` | EKRAN-08 `DocumentSeriesComponent`, DIALOG-04 | |
| `DocumentSeries` | `SeriesName` | `DocumentSeriesDto` | `SeriesName` | EKRAN-08, DIALOG-04, EKRAN-10/12 (wybór serii) | Prefiks serii (np. „FV") |
| `DocumentSeries` | `FirstNumber` | `DocumentSeriesDto` | `FirstNumber` | DIALOG-04 | Numer startowy |
| `DocumentSeries` | `CurrentNumber` | `DocumentSeriesDto` | `CurrentNumber` | EKRAN-08 | Aktualny numer (inkrementowany przy każdym dok.) |
| `DocumentSeries` | `IsDefault` | `DocumentSeriesDto` | `IsDefault` | EKRAN-08, DIALOG-04 | Czy seria domyślna dla danego typu |
| `DocumentSeries` | `DocumentTypeId` | `DocumentSeriesDto` | `DocumentTypeId` | DIALOG-04 | FK do `DocumentType` |

### Tabela: Document

| Tabela DB | Kolumna | DTO | Pole DTO | Ekran (komponent) | Uwagi |
|---|---|---|---|---|---|
| `Document` | `Id` | `DocumentRequestDto` / `DocumentTableRecordDto` | `Id` | EKRAN-09/11/13 (tabela), EKRAN-10/12/14 (formularz) | Identyfikator dokumentu |
| `Document` | `DocumentNumber` | `DocumentRequestDto` / `DocumentTableRecordDto` | `DocumentNumber` | EKRAN-09/11/13, EKRAN-10/12/14 | Numer dokumentu — generowany przez serwis jeśli null |
| `Document` | `IssueDate` | `DocumentRequestDto` / `DocumentTableRecordDto` | `IssueDate` | EKRAN-09/11/13, EKRAN-10/12/14 | Data wystawienia |
| `Document` | `DueDate` | `DocumentRequestDto` / `DocumentTableRecordDto` | `DueDate` | EKRAN-09/11/13 (opcjonalnie), EKRAN-10/12/14 | Termin płatności (nullable) |
| `Document` | `TotalPrice` | `DocumentTableRecordDto` | `TotalValue` | EKRAN-09/11/13 | Suma wartości — mapowane z `Document.TotalPrice` |
| `Document` | `ClientId` (FK) | `DocumentRequestDto` | `Client` (FirmDto) | EKRAN-10/12/14 | Klient — zagnieżdżony FirmDto |
| `Document` | `BankAccountId` (FK) | `DocumentRequestDto` | `BankAccount` (BankAccountDto) | EKRAN-10/12/14 | Konto bankowe na fakturze |
| `Document` | `DocumentSeriesId` (FK) | `DocumentRequestDto` | `DocumentSeries` (DocumentSeriesDto) | EKRAN-10/12/14 | Seria dokumentu |
| `Document` | `DocumentTypeId` (FK) | `DocumentRequestDto` | `DocumentType` | EKRAN-10/12/14 | Typ dokumentu (anomalia: typ domenowy, nie DTO) |
| `Document` | `DocumentStatusId` (FK) | `DocumentRequestDto` / `DocumentTableRecordDto` | `DocumentStatus` | EKRAN-09/11/13, EKRAN-10/12/14 | Status dokumentu (anomalia: typ domenowy, nie DTO) |

### Tabela: DocumentProduct

| Tabela DB | Kolumna | DTO | Pole DTO | Ekran (komponent) | Uwagi |
|---|---|---|---|---|---|
| `DocumentProduct` | `Name` | `DocumentProductRequestDto` | `Name` | EKRAN-10/12/14 (wiersze tabeli produktów w formularzu) | Nazwa pozycji na fakturze |
| `DocumentProduct` | `UnitPrice` | `DocumentProductRequestDto` | `UnitPrice` | EKRAN-10/12/14 | Cena jednostkowa |
| `DocumentProduct` | `TotalPrice` | `DocumentProductRequestDto` | `TotalPrice` | EKRAN-10/12/14 | Cena całkowita |
| `DocumentProduct` | `Quantity` | `DocumentProductRequestDto` | `Quantity` | EKRAN-10/12/14 | Ilość |
| `DocumentProduct` | `TvaValue` | `DocumentProductRequestDto` | `TvaValue` | EKRAN-10/12/14 | Stawka VAT w % |
| `DocumentProduct` | `ContainsTva` | `DocumentProductRequestDto` | `ContainsTva` | EKRAN-10/12/14 | Czy cena zawiera VAT |
| `DocumentProduct` | `UnitOfMeasurement` | `DocumentProductRequestDto` | `UnitOfMeasurement` | EKRAN-10/12/14 | Jednostka miary |

### Tabela: DocumentStatus (dane seedowane)

| Tabela DB | Kolumna | DTO | Pole DTO | Ekran (komponent) | Uwagi |
|---|---|---|---|---|---|
| `DocumentStatus` | `Id` | `DocumentStatusDto` | `Id` | EKRAN-10/12 (wybór statusu) | Seedowane 2 wartości przy starcie |
| `DocumentStatus` | `Status` | `DocumentStatusDto` | `Status` | EKRAN-10/12, EKRAN-09/11/13 (tabela) | Np. „Paid" / „Unpaid" |

### Tabele pomocnicze (bez bezpośredniego UI)

| Tabela DB | Kolumna | DTO | Pole DTO | Ekran (komponent) | Uwagi |
|---|---|---|---|---|---|
| `UserFirm` | `UserId` + `FirmId` | *(brak DTO)* | *(brak)* | *(brak — relacja wewnętrzna)* | Tabela łącząca User ↔ Firm; używana w LINQ-04, LINQ-05 |
| `DocumentType` | `Id` + `Type` | *(brak osobnego DTO)* | `DocumentType` w `DocumentSeriesDto` | EKRAN-08 (typ serii), EKRAN-10/12/14 | Seedowane 3 typy: Faktura, Proforma, Storno; anomalia: typ domenowy w DTO |

## Uwagi

- Pola techniczne (`IsDeleted`, `CreatedAt`, `UpdatedAt`, `PasswordHash`) pominięte — niewidoczne w UI.
- `DocumentRequestDto.DocumentType` i `.DocumentStatus` to typy domenowe bezpośrednio w DTO (anomalie DTO-A02, DTO-A03) — naruszenie Clean Architecture.
- `DocumentTableRecordDto.DocumentStatus` jest typem domenowym (DTO-A04).
- `DocumentSeriesDto.DocumentType` jest typem domenowym (DTO-A01).
- `DashboardStatsDto` i `MonthlyTotalDto` są używane tylko przez EKRAN-03 Dashboard — nie mają bezpośredniego odpowiednika w tabelach DB (dane agregowane przez LINQ-03).
- `DocumentStreamDto` (`PdfContent`, `DocumentNumber`) jest używane tylko przez DIALOG-05 PdfViewer — dane generowane in-memory przez QuestPDF.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — kluczowe pola z 9 tabel DB przez 14 DTO do 14 ekranów. |
