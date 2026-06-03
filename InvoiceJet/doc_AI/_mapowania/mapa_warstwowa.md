# Mapa warstwowa: UC → ekran → API → serwis → repo → DB (M-05)

| Pole | Wartość |
|---|---|
| ID dokumentu | M-05 |
| Typ dokumentu | mapa krzyżowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Mapa śledzi 8 kluczowych flow funkcjonalnych przez wszystkie warstwy Clean Architecture: od przypadku użycia i ekranu UI, przez endpoint API, serwis aplikacji i repozytorium, aż do tabel bazy danych. Pozwala szybko zidentyfikować pełny stos dla dowolnej funkcji biznesowej.

## Tabela mapowań warstwowych

| UC / Funkcja | Ekran (komponent) | Endpoint API | Kontroler | Serwis | Repozytorium | Tabele DB |
|---|---|---|---|---|---|---|
| Rejestracja użytkownika | EKRAN-02 `RegisterComponent` | `POST /api/Auth/register` (API-01) | `AuthController.Register` | `AuthService.Register()` | `UserRepository` | `User` |
| Logowanie | EKRAN-01 `LoginComponent` | `POST /api/Auth/login` (API-02) | `AuthController.Login` | `AuthService.Login()` | `UserRepository` | `User` |
| Zarządzanie danymi firmy | EKRAN-04 `FirmDetailsComponent` | `GET /api/Firm/GetUserActiveFirm` (API-06) + `PUT /api/Firm/EditFirm` (API-05) | `FirmController` | `FirmService.GetUserActiveFirm()` + `FirmService.EditFirm()` | `FirmRepository` | `Firm`, `UserFirm` |
| Autouzupełnienie z ANAF | EKRAN-04 `FirmDetailsComponent`, DIALOG-01 | `GET /api/Firm/GetFirmFromAnaf` (API-04) | `FirmController.GetFirmDataFromAnaf` | `FirmService.GetFirmFromAnaf()` → ANAF HTTP | *(brak repo — HTTP zewnętrzny)* | *(brak — ANAF API)* |
| Zarządzanie klientami | EKRAN-05 `ClientsComponent` + DIALOG-01 | `GET /api/Firm/GetUserClientFirms` (API-07) + `POST /api/Firm/AddFirm/{isClient=true}` (API-03) + `PUT /api/Firm/DeleteFirms` (API-09) | `FirmController` | `FirmService.GetUserClientFirms()` + `FirmService.AddFirm()` | `FirmRepository` | `Firm`, `UserFirm` |
| Zarządzanie produktami | EKRAN-07 `ProductsComponent` + DIALOG-03 | `GET /api/Product/GetAll` (API-10) + `POST /api/Product/AddProduct` (API-11) + `PUT /api/Product/EditProduct` (API-12) + `PUT /api/Product/DeleteProducts` (API-13) | `ProductController` | `ProductService` | `ProductRepository` | `Product` |
| Zarządzanie kontami bankowymi | EKRAN-06 `BankAccountsComponent` + DIALOG-02 | `GET /api/BankAccount/GetAll` (API-14) + `POST /api/BankAccount/AddBankAccount` (API-15) + `PUT /api/BankAccount/EditBankAccount` (API-16) + `PUT /api/BankAccount/DeleteBankAccounts` (API-17) | `BankAccountController` | `BankAccountService` | `BankAccountRepository` | `BankAccount` |
| Zarządzanie seriami dokumentów | EKRAN-08 `DocumentSeriesComponent` + DIALOG-04 | `GET /api/DocumentSeries/GetAll` (API-18) + `POST /api/DocumentSeries/AddDocumentSeries` (API-19) + `PUT /api/DocumentSeries/UpdateDocumentSeries` (API-20) + `PUT /api/DocumentSeries/DeleteDocumentSeries` (API-21) | `DocumentSeriesController` | `DocumentSeriesService` | `DocumentSeriesRepository` | `DocumentSeries`, `DocumentType` |
| Wystawienie faktury | EKRAN-10 `AddOrEditInvoiceComponent` (BASE-01 `BaseInvoiceComponent`) | `GET /api/Document/GetDocumentAutofillInfo` (API-27) + `POST /api/Document/AddDocument` (API-22) | `DocumentController` | `DocumentService.GetDocumentAutofillInfo()` + `DocumentService.AddDocument()` | `DocumentRepository` | `Document`, `DocumentProduct`, `DocumentSeries`, `Firm`, `BankAccount`, `DocumentType`, `DocumentStatus` |
| Edycja / podgląd faktury | EKRAN-10 `AddOrEditInvoiceComponent` | `GET /api/Document/GetById/{id}` (API-25) + `PUT /api/Document/EditDocument` (API-23) | `DocumentController` | `DocumentService.GetDocumentById()` (LINQ-01) + `DocumentService.EditDocument()` | `DocumentRepository` | `Document`, `DocumentProduct`, `Firm`, `BankAccount`, `DocumentSeries`, `DocumentType`, `DocumentStatus` |
| Generowanie PDF faktury | EKRAN-10 `AddOrEditInvoiceComponent`, DIALOG-05 `PdfViewerComponent` | `POST /api/Document/GetPdfStream` (API-29) + `POST /api/Document/GenerateInvoicePdf` (API-28) | `DocumentController` | `PdfGenerationService.GenerateInvoicePdf()` (QuestPDF) | *(brak repo — in-memory)* | *(brak)* |
| Lista faktur | EKRAN-09 `InvoicesComponent` | `GET /api/Document/GetTableRecords` (API-24, `documentTypeId=1`) | `DocumentController` | `DocumentService.GetDocumentTableRecords()` (LINQ-02) | `DocumentRepository` | `Document`, `Firm` |
| Konwersja na storno | EKRAN-09 `InvoicesComponent` | `PUT /api/Document/TransformToStorno` (API-31) | `DocumentController` | `DocumentService.TransformToStorno()` | `DocumentRepository` | `Document`, `DocumentType` |
| Statystyki dashboardu | EKRAN-03 `DashboardComponent` | `GET /api/Document/GetDashboardStats` (API-30) | `DocumentController` | `DocumentService.GetDashboardStats()` (LINQ-03) | `DocumentRepository` | `Document` |

## Diagram warstw (Clean Architecture)

```
UI (Angular 16)
    └── Komponent (*.component.ts)
        └── Serwis Angular (*.service.ts)
            │  HTTP Request (Bearer JWT)
            ▼
Presentation (ASP.NET Core 8)
    └── Controller ([Authorize(Roles="User")])
        └── Wywołanie serwisu aplikacji
            ▼
Application
    └── Service (IXxxService → XxxService)
        └── Wywołanie repozytorium lub HTTP (ANAF)
            ▼
Infrastructure
    └── Repository (IXxxRepository → XxxRepository)
        └── EF Core DbContext (LINQ)
            ▼
Database (SQL Server)
    └── Tabele: User, Firm, UserFirm, BankAccount, Product,
               DocumentType, DocumentSeries, Document,
               DocumentProduct, DocumentStatus
```

## Uwagi

- Nazwy klas serwisów i repozytoriów są konwencjonalne (np. `DocumentService`, `DocumentRepository`) — dokładne nazwy należy zweryfikować w kodzie źródłowym `InvoiceJetAPI/InvoiceJet.Application/Services/` i `InvoiceJet.Infrastructure/Persistence/Repositories/`.
- `PdfGenerationService` działa in-memory z biblioteką QuestPDF — nie korzysta z repozytorium ani bazy danych.
- `FirmService.GetFirmFromAnaf()` wywołuje zewnętrzne API ANAF zamiast repozytorium DB.
- LINQ-01 (GetDocumentById) stosuje eager loading z 6 Include() — najdroższe zapytanie w projekcie.
- Soft-delete: wszystkie operacje usunięcia ustawiają `IsDeleted = true` (brak fizycznego DELETE).

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — 14 flow przez wszystkie warstwy. |
