# Mapa: Endpoint ↔ DTO ↔ LINQ ↔ tabela DB (M-03)

| Pole | Wartość |
|---|---|
| ID dokumentu | M-03 |
| Typ dokumentu | mapa krzyżowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Mapa łączy 31 endpointów API z obiektami DTO używanymi jako request/response, zapytaniami LINQ w warstwie infrastruktury oraz tabelami DB dotkniętymi przez każdą operację. Pozwala szybko znaleźć pełny przepływ danych dla dowolnego endpointu.

## Tabela mapowań

| ID | Endpoint | Metoda HTTP | Request DTO | Response DTO | LINQ | Tabele DB |
|---|---|---|---|---|---|---|
| API-01 | `/api/Auth/register` | POST | `UserRegisterDto` | string (JWT) | brak LINQ — EF Core SaveChanges | `User` |
| API-02 | `/api/Auth/login` | POST | `UserLoginDto` | string (JWT) | `_context.Users.FirstOrDefault(e == email)` | `User` |
| API-03 | `/api/Firm/AddFirm/{isClient}` | POST | `FirmDto` | `FirmDto` | `_context.Firms.Add()` + `UserFirm.Add()` | `Firm`, `UserFirm` |
| API-04 | `/api/Firm/GetFirmFromAnaf` | GET | *(CUI jako query param)* | `FirmDto` | brak — wywołanie zewnętrzne ANAF | *(brak — dane z ANAF)* |
| API-05 | `/api/Firm/EditFirm` | PUT | `FirmDto` | `FirmDto` | `_context.Firms.Update()` | `Firm` |
| API-06 | `/api/Firm/GetUserActiveFirm` | GET | *(brak body)* | `FirmDto` | LINQ-04: Include(UserFirm).Where(userId) | `Firm`, `UserFirm` |
| API-07 | `/api/Firm/GetUserClientFirms` | GET | *(brak body)* | `List<FirmDto>` | LINQ-05: Where(isClient + userId) | `Firm`, `UserFirm` |
| API-08 | `/api/Firm/GetUserClientFirms` | GET | *(wariant z paginacją)* | `List<FirmDto>` | LINQ-05 (tożsamy z API-07) | `Firm`, `UserFirm` |
| API-09 | `/api/Firm/DeleteFirms` | PUT | `int[]` *(ids)* | brak | `Where(id IN ids).Set(IsDeleted=true)` | `Firm`, `UserFirm` |
| API-10 | `/api/Product/GetAll` | GET | *(brak body)* | `List<ProductDto>` | `Where(userId).Where(!IsDeleted)` | `Product` |
| API-11 | `/api/Product/AddProduct` | POST | `ProductDto` | `ProductDto` | `_context.Products.Add()` | `Product` |
| API-12 | `/api/Product/EditProduct` | PUT | `ProductDto` | `ProductDto` | `_context.Products.Update()` | `Product` |
| API-13 | `/api/Product/DeleteProducts` | PUT | `int[]` *(ids)* | brak | `Where(id IN ids).Set(IsDeleted=true)` | `Product` |
| API-14 | `/api/BankAccount/GetAll` | GET | *(brak body)* | `List<BankAccountDto>` | `Where(firmId + !IsDeleted)` | `BankAccount` |
| API-15 | `/api/BankAccount/AddBankAccount` | POST | `BankAccountDto` | `BankAccountDto` | `_context.BankAccounts.Add()` | `BankAccount` |
| API-16 | `/api/BankAccount/EditBankAccount` | PUT | `BankAccountDto` | `BankAccountDto` | `_context.BankAccounts.Update()` | `BankAccount` |
| API-17 | `/api/BankAccount/DeleteBankAccounts` | PUT | `int[]` *(ids)* | brak | `Where(id IN ids).Set(IsDeleted=true)` | `BankAccount` |
| API-18 | `/api/DocumentSeries/GetAll` | GET | *(brak body)* | `List<DocumentSeriesDto>` | `Where(userId + !IsDeleted)` | `DocumentSeries`, `DocumentType` |
| API-19 | `/api/DocumentSeries/AddDocumentSeries` | POST | `DocumentSeriesDto` | `DocumentSeriesDto` | `_context.DocumentSeries.Add()` | `DocumentSeries` |
| API-20 | `/api/DocumentSeries/UpdateDocumentSeries` | PUT | `DocumentSeriesDto` | `DocumentSeriesDto` | `_context.DocumentSeries.Update()` | `DocumentSeries` |
| API-21 | `/api/DocumentSeries/DeleteDocumentSeries` | PUT | `int[]` *(ids)* | brak | `Where(id IN ids).Set(IsDeleted=true)` | `DocumentSeries` |
| API-22 | `/api/Document/AddDocument` | POST | `DocumentRequestDto` | `DocumentRequestDto` | SaveChanges: Document + DocumentProduct + DocumentSeries.CurrentNumber++ | `Document`, `DocumentProduct`, `DocumentSeries` |
| API-23 | `/api/Document/EditDocument` | PUT | `DocumentRequestDto` | `DocumentRequestDto` | Update Document + re-create DocumentProducts | `Document`, `DocumentProduct` |
| API-24 | `/api/Document/GetTableRecords` | GET | *(documentTypeId query param)* | `List<DocumentTableRecordDto>` | LINQ-02: Select projekcja bez Include | `Document`, `Firm` |
| API-25 | `/api/Document/GetById/{documentId}` | GET | *(id w URL)* | `DocumentRequestDto` | LINQ-01: Include(Client, BankAccount, DocSeries, DocProducts, DocType, DocStatus) | `Document`, `Firm`, `BankAccount`, `DocumentSeries`, `DocumentProduct`, `DocumentType`, `DocumentStatus` |
| API-26 | `/api/Document/DeleteDocument` | PUT | `int[]` *(ids)* | brak | `Where(id IN ids).Set(IsDeleted=true)` | `Document` |
| API-27 | `/api/Document/GetDocumentAutofillInfo` | GET | *(brak body)* | `DocumentAutofillDto` | Where(userId) na Clients, DocSeries, DocStatuses, Products | `Firm`, `DocumentSeries`, `DocumentStatus`, `Product` |
| API-28 | `/api/Document/GenerateInvoicePdf` | POST | `DocumentRequestDto` | *(plik PDF — application/pdf)* | brak LINQ — dane z request body | *(brak — generacja w pamięci)* |
| API-29 | `/api/Document/GetPdfStream` | POST | `DocumentRequestDto` | `DocumentStreamDto` | brak LINQ — dane z request body | *(brak — generacja w pamięci)* |
| API-30 | `/api/Document/GetDashboardStats` | GET | *(year + documentType query params)* | `DashboardStatsDto` | LINQ-03: GroupBy(Month) + Count() | `Document` |
| API-31 | `/api/Document/TransformToStorno` | PUT | `DocumentRequestDto` | `DocumentRequestDto` | Update Document.DocumentType → Storno | `Document`, `DocumentType` |

## Uwagi

- LINQ-01 do LINQ-05 są opisane w `inwentaryzacja_linq.md` — tylko 5 zapytań z pełną inwentaryzacją; pozostałe endpointy używają prostego EF Core (Add/Update/soft-delete).
- API-07 i API-08 to fizycznie ten sam endpoint (duplikat numeracji) — patrz anomalia A-02 w `inwentaryzacja_api.md`.
- API-09, API-13, API-17, API-21, API-26 używają `PUT` z tablicą `int[]` jako soft-delete; brak fizycznego DELETE — patrz anomalia A-01.
- API-28 zwraca zawsze typ dokumentu `InvoiceDocument` (bug A-06) — nie obsługuje proformy ani storna.
- `DocumentRequestDto.DocumentType` i `.DocumentStatus` są typami domenowymi (nie DTO) — anomalia DTO-A02, DTO-A03.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
