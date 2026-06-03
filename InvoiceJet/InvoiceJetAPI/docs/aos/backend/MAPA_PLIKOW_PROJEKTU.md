# Mapa plików projektu — InvoiceJetAPI

**Data aktualizacji:** 2026-05-30
**Cel:** Szybka nawigacja po plikach źródłowych — dla agentów i developerów.
**Zasada:** Każdy nowy plik dodany do projektu musi być tu wpisany.
**Ścieżki:** względem katalogu `InvoiceJet/InvoiceJetAPI/` (bez prefiksu projektu).

---

## 1. Warstwa Presentation

### 1.1 Konfiguracja startowa

| Plik | Klasa / zawartość | Rola |
|---|---|---|
| `InvoiceJet.Presentation/Program.cs` | `WebApplication` builder | DI, middleware, JWT, CORS, seeder, QuestPDF |
| `InvoiceJet.Presentation/Seeders/DbSeeder.cs` | `DbSeeder.SeedDocumentTypes` | Seed `DocumentType` i `DocumentStatus` przy starcie |
| `InvoiceJet.Presentation/Middleware/ExceptionMiddleware.cs` | `ExceptionMiddleware.Invoke` | Globalny handler wyjątków → HTTP status |

### 1.2 Kontrolery

| Plik | Klasa | Route base | Endpointy (metoda HTTP + akcja) |
|---|---|---|---|
| `InvoiceJet.Presentation/Controllers/AuthController.cs` | `AuthController` | `/api/Auth` | `POST register`, `POST login` |
| `InvoiceJet.Presentation/Controllers/FirmController.cs` | `FirmController` | `/api/Firm` | `POST AddFirm/{isClient}`, `GET fromAnaf/{cui}`, `PUT EditFirm/{isClient}`, `GET GetUserActiveFirm`, `GET GetUserClientFirms`, `PUT DeleteFirms` |
| `InvoiceJet.Presentation/Controllers/BankAccountController.cs` | `BankAccountController` | `/api/BankAccount` | `GET GetUserFirmBankAccounts`, `POST AddUserFirmBankAccount`, `PUT EditUserFirmBankAccount`, `PUT DeleteUserFirmBankAccounts` |
| `InvoiceJet.Presentation/Controllers/ProductController.cs` | `ProductController` | `/api/Product` | `GET GetAllProductsForUserId`, `POST AddProduct`, `PUT EditProduct`, `PUT DeleteProducts` |
| `InvoiceJet.Presentation/Controllers/DocumentSeriesController.cs` | `DocumentSeriesController` | `/api/DocumentSeries` | `GET GetAllDocumentSeriesForUserId`, `POST AddDocumentSeries`, `PUT UpdateDocumentSeries`, `PUT DeleteDocumentSeries` |
| `InvoiceJet.Presentation/Controllers/DocumentController.cs` | `DocumentController` | `/api/Document` | `POST AddDocument`, `PUT EditDocument`, `GET GetDocumentTableRecords/{documentTypeId}`, `GET GetDocumentById/{documentId}`, `PUT DeleteDocuments`, `GET GetDocumentAutofillInfo/{documentTypeId}`, `POST GenerateDocumentPdf`\*, `POST GetInvoicePdfStream`, `GET GetDashboardStats/{year}/{documentType}`, `PUT TransformToStorno` |

> \* `GenerateDocumentPdf` ma własny `try/catch` w kontrolerze (zwraca `BadRequest` zamiast przechodzić przez `ExceptionMiddleware`).

---

## 2. Warstwa Application

### 2.1 Interfejsy serwisów

| Plik | Interfejs | Opis |
|---|---|---|
| `InvoiceJet.Application/Services/IAuthService.cs` | `IAuthService` | `RegisterUser`, `LoginUser` |
| `InvoiceJet.Application/Services/IFirmService.cs` | `IFirmService` | operacje na firmach + ANAF |
| `InvoiceJet.Application/Services/IBankAccountService.cs` | `IBankAccountService` | CRUD kont bankowych |
| `InvoiceJet.Application/Services/IProductService.cs` | `IProductService` | CRUD produktów |
| `InvoiceJet.Application/Services/IDocumentSeriesService.cs` | `IDocumentSeriesService` | CRUD serii dokumentów |
| `InvoiceJet.Application/Services/IDocumentService.cs` | `IDocumentService` | dokumenty: dodaj/edytuj/lista/szczegóły/usuń/stats/pdf/storno |
| `InvoiceJet.Application/Services/IPdfGenerationService.cs` | `IPdfGenerationService` | generowanie PDF przez QuestPDF |
| `InvoiceJet.Application/Services/IUserService.cs` | `IUserService` | `GetCurrentUserId()` — odczyt z JWT claim |

### 2.2 Implementacje serwisów

| Plik | Klasa | Komentarz |
|---|---|---|
| `InvoiceJet.Application/Services/Impl/AuthService.cs` | `AuthService` | `RegisterUser`, `LoginUser`, `CreateToken` (private) |
| `InvoiceJet.Application/Services/Impl/FirmService.cs` | `FirmService` | integracja ANAF (`HttpClient` bez IHttpClientFactory) |
| `InvoiceJet.Application/Services/Impl/BankAccountService.cs` | `BankAccountService` | `DeactivateOtherBankAccounts` (private) |
| `InvoiceJet.Application/Services/Impl/ProductService.cs` | `ProductService` | — |
| `InvoiceJet.Application/Services/Impl/DocumentSeriesService.cs` | `DocumentSeriesService` | `AddInitialDocumentSeries` (wywoływana z P-03, P-05) |
| `InvoiceJet.Application/Services/Impl/DocumentService.cs` | `DocumentService` | `UpdateDocumentProducts`, `IncreaseDocumentSeriesNumber`, `GetTotalDocumentsAsync`, `GetMonthlyTotalsAsync` (private) |
| `InvoiceJet.Application/Services/Impl/UserService.cs` | `UserService` | `GetCurrentUserId()` z `IHttpContextAccessor` |

### 2.3 DTO

| Plik | Klasa | Kierunek | Używany przez |
|---|---|---|---|
| `InvoiceJet.Application/DTOs/UserRegisterDto.cs` | `UserRegisterDto` | wejście | `AuthController.Register` → `AuthService.RegisterUser` |
| `InvoiceJet.Application/DTOs/UserLoginDto.cs` | `UserLoginDto` | wejście | `AuthController.Login` → `AuthService.LoginUser` |
| `InvoiceJet.Application/DTOs/FirmDto.cs` | `FirmDto` | wejście/wyjście | `FirmController` |
| `InvoiceJet.Application/DTOs/BankAccountDto.cs` | `BankAccountDto` | wejście/wyjście | `BankAccountController` |
| `InvoiceJet.Application/DTOs/ProductDto.cs` | `ProductDto` | wejście/wyjście | `ProductController` |
| `InvoiceJet.Application/DTOs/DocumentSeriesDto.cs` | `DocumentSeriesDto` | wejście/wyjście | `DocumentSeriesController` |
| `InvoiceJet.Application/DTOs/DocumentRequestDto.cs` | `DocumentRequestDto` | wejście/wyjście | `DocumentController.AddDocument`, `EditDocument`, `GenerateDocumentPdf`, `GetInvoicePdfStream` |
| `InvoiceJet.Application/DTOs/DocumentProductRequestDto.cs` | `DocumentProductRequestDto` | wejście | zagnieżdżone w `DocumentRequestDto` |
| `InvoiceJet.Application/DTOs/DocumentTableRecordDto.cs` | `DocumentTableRecordDto` | wyjście | `DocumentController.GetDocumentTableRecords` |
| `InvoiceJet.Application/DTOs/DocumentAutofillDto.cs` | `DocumentAutofillDto` | wyjście | `DocumentController.GetDocumentAutofillInfo` |
| `InvoiceJet.Application/DTOs/DocumentStatusDto.cs` | `DocumentStatusDto` | wyjście | zagnieżdżony w `DocumentAutofillDto` |
| `InvoiceJet.Application/DTOs/DocumentStreamDto.cs` | `DocumentStreamDto` | wejście | `DocumentController.GetInvoicePdfStream` |
| `InvoiceJet.Application/DTOs/DashboardStatsDto.cs` | `DashboardStatsDto` | wyjście | `DocumentController.GetDashboardStats` |
| `InvoiceJet.Application/DTOs/MonthlyTotalDto.cs` | `MonthlyTotalDto` | wyjście | zagnieżdżone w `DashboardStatsDto` |

### 2.4 Profile AutoMapper

| Plik | Klasa | Mapowanie |
|---|---|---|
| `InvoiceJet.Application/MappingProfiles/BankAccountProfile.cs` | `BankAccountProfile` | `BankAccount` ↔ `BankAccountDto` |
| `InvoiceJet.Application/MappingProfiles/DocumentProductProfile.cs` | `DocumentProductProfile` | `DocumentProduct` ↔ `DocumentProductRequestDto` |
| `InvoiceJet.Application/MappingProfiles/DocumentProfile.cs` | `DocumentProfile` | `Document` ↔ `DocumentRequestDto`, `DocumentTableRecordDto` |
| `InvoiceJet.Application/MappingProfiles/DocumentSeriesProfile.cs` | `DocumentSeriesProfile` | `DocumentSeries` ↔ `DocumentSeriesDto` |
| `InvoiceJet.Application/MappingProfiles/DocumentStatusProfile.cs` | `DocumentStatusProfile` | `DocumentStatus` ↔ `DocumentStatusDto` |
| `InvoiceJet.Application/MappingProfiles/FirmProfile.cs` | `FirmProfile` | `Firm` ↔ `FirmDto` |
| `InvoiceJet.Application/MappingProfiles/ProductProfile.cs` | `ProductProfile` | `Product` ↔ `ProductDto` |

---

## 3. Warstwa Domain

### 3.1 Encje (modele)

| Plik | Klasa | Tabela DB | Komentarz |
|---|---|---|---|
| `InvoiceJet.Domain/Models/BaseEntity.cs` | `BaseEntity` (abstract) | — | `int Id` — baza dla większości encji |
| `InvoiceJet.Domain/Models/User.cs` | `User` | `User` | `Guid Id` (nie dziedziczy `BaseEntity`), `ActiveUserFirmId` nullable FK |
| `InvoiceJet.Domain/Models/Firm.cs` | `Firm` | `Firm` | dane firmy: `Name`, `Cui`, `RegCom`, `Address`, `City`, `County` |
| `InvoiceJet.Domain/Models/UserFirm.cs` | `UserFirm` | `UserFirm` | powiązanie User ↔ Firm, `IsClient` flag |
| `InvoiceJet.Domain/Models/BankAccount.cs` | `BankAccount` | `BankAccount` | `IsActive`, `Currency` (enum), FK → `UserFirm` |
| `InvoiceJet.Domain/Models/Product.cs` | `Product` | `Product` | `Name` (unikalne IX), `Price` decimal, `TvaValue`, `ContainsTva`, `UnitOfMeasurement` |
| `InvoiceJet.Domain/Models/DocumentType.cs` | `DocumentType` | `DocumentType` | lookup: `Name` (Factura/Factura Proforma/Factura Storno) — seeded |
| `InvoiceJet.Domain/Models/DocumentSeries.cs` | `DocumentSeries` | `DocumentSeries` | `SeriesName`, `CurrentNumber`, `FirstNumber`, `IsDefault`, FK → `UserFirm`, `DocumentType` |
| `InvoiceJet.Domain/Models/DocumentStatus.cs` | `DocumentStatus` | `DocumentStatus` | lookup: `Status` (Unpaid/Paid) — seeded |
| `InvoiceJet.Domain/Models/Document.cs` | `Document` | `Document` | `DocumentNumber`, `IssueDate`, `DueDate`, `UnitPrice`, `TotalPrice`, FKs → `BankAccount`, `Firm`, `DocumentType`, `DocumentStatus`, `UserFirm` |
| `InvoiceJet.Domain/Models/DocumentProduct.cs` | `DocumentProduct` | `DocumentProduct` | pozycja faktury: `Quantity`, `UnitPrice`, `TotalPrice`, FK → `Document`, `Product` |

### 3.2 Enumy

| Plik | Enum | Wartości |
|---|---|---|
| `InvoiceJet.Domain/Enums/Currency.cs` | `CurrencyEnum` | `Ron = 0`, `Euro = 1` |
| `InvoiceJet.Domain/Enums/DocumentStatus.cs` | `DocumentStatusEnum` | `Unpaid = 1`, `Paid = 2` |
| `InvoiceJet.Domain/Enums/DocumentType.cs` | `DocumentTypeEnum` | `Invoice = 1`, `ProformaInvoice = 2`, `StornoInvoice = 3` |

### 3.3 Wyjątki domenowe

| Plik | Klasa | Komunikat wyświetlany użytkownikowi | Zmapowany w middleware? | HTTP |
|---|---|---|---|---|
| `InvoiceJet.Domain/Exceptions/AnafFirmNotFoundException.cs` | `AnafFirmNotFoundException` | `Firm with CUI {cui} not found in ANAF database.` | ✅ tak | `404` |
| `InvoiceJet.Domain/Exceptions/BankAccountAssociatedWithDocuments.cs` | `BankAccountAssociatedWithDocumentsException` | `Can't delete. Bank account is associated with documents.` | ✅ tak | `400` |
| `InvoiceJet.Domain/Exceptions/FirmAssociatedWithDocumentException.cs` | `FirmAssociatedWithDocumentException` | `Can't delete. Firm {firmName} is associated with a document.` | ❌ **nie** ⚠️ | `500` (catch-all) |
| `InvoiceJet.Domain/Exceptions/IncorrectPasswordException.cs` | `IncorrectPasswordException` | `Password is incorrect.` | ✅ tak | `400` |
| `InvoiceJet.Domain/Exceptions/InvalidPasswordException.cs` | `InvalidPasswordException` | `Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.` | ❌ **nie** ⚠️ | `500` (catch-all) |
| `InvoiceJet.Domain/Exceptions/NoBankAccountAddedException.cs` | `NoBankAccountAddedException` | `Please add a bank account, before generating a document.` | ✅ tak | `400` |
| `InvoiceJet.Domain/Exceptions/PasswordMismatchException.cs` | `PasswordMismatchException` | `Password confirmation doesn't match.` | ✅ tak | `400` |
| `InvoiceJet.Domain/Exceptions/ProductAssociatedWithInvoiceException.cs` | `ProductAssociatedWithInvoiceException` | `Can't delete. Product {productName} is associated with an invoice.` | ✅ tak | `400` |
| `InvoiceJet.Domain/Exceptions/ProductWithSameNameExistsException.cs` | `ProductWithSameNameExistsException` | `Product with name {productName} already exists.` | ❌ **nie** ⚠️ | `500` (catch-all) |
| `InvoiceJet.Domain/Exceptions/UserAlreadyExistsException.cs` | `UserAlreadyExistsException` | `User with email {email} already exists.` | ✅ tak | `400` |
| `InvoiceJet.Domain/Exceptions/UserHasNoAssociatedFirmException.cs` | `UserHasNoAssociatedFirmException` | `User has no associated firm. Add a firm in Firm Details page.` | ✅ tak | `400` |
| `InvoiceJet.Domain/Exceptions/UserNotFoundException.cs` | `UserNotFoundException` | `User with email {email} not found.` | ✅ tak | `400` |

> ⚠️ Trzy wyjątki domenowe **niezmapowane** w `ExceptionMiddleware` → `500` catch-all:
> `FirmAssociatedWithDocumentException`, `InvalidPasswordException`, `ProductWithSameNameExistsException`.
> Szczegóły i lista napraw: `KATALOG_WYJATKOW.md § 5`.

### 3.4 Interfejsy repozytoriów i UoW

| Plik | Interfejs | Kluczowe metody |
|---|---|---|
| `InvoiceJet.Domain/Interfaces/IUnitOfWork.cs` | `IUnitOfWork` | agreguje wszystkie `IXxxRepository`, `CompleteAsync()` = `SaveChangesAsync()` |
| `InvoiceJet.Domain/Interfaces/Repositories/IGenericRepository.cs` | `IGenericRepository<T>` | `GetByIdAsync`, `GetAllAsync`, `AddAsync`, `AddRangeAsync`, `UpdateAsync`, `RemoveAsync`, `RemoveRangeAsync`, `Query()` |
| `InvoiceJet.Domain/Interfaces/Repositories/IUserRepository.cs` | `IUserRepository` | `GetUserFirmIdAsync` (→ `int?`), `GetUserFirmAsync` (→ `UserFirm`), `GetUserByIdAsync` |
| `InvoiceJet.Domain/Interfaces/Repositories/IFirmRepository.cs` | `IFirmRepository` | `GetTotalClientsAsync` + metody `IGenericRepository` |
| `InvoiceJet.Domain/Interfaces/Repositories/IBankAccountRepository.cs` | `IBankAccountRepository` | `GetUserFirmBankAccountsAsync`, `GetTotalBankAccountsAsync` |
| `InvoiceJet.Domain/Interfaces/Repositories/IProductRepository.cs` | `IProductRepository` | `GetUserFirmProductsAsync`, `FindUserFirmProductByName`, `GetTotalProductsAsync` |
| `InvoiceJet.Domain/Interfaces/Repositories/IDocumentSeriesRepository.cs` | `IDocumentSeriesRepository` | `GetAllDocumentSeriesForActiveUserFirm` |
| `InvoiceJet.Domain/Interfaces/Repositories/IDocumentRepository.cs` | `IDocumentRepository` | `GetAllDocumentsByType`, `GetDocumentWithAllInfo` |
| `InvoiceJet.Domain/Interfaces/Repositories/IDocumentProductRepository.cs` | `IDocumentProductRepository` | `GetAllDocumentProductsForDocument`, `RemoveRangeAsync` |
| `InvoiceJet.Domain/Interfaces/Repositories/IDocumentStatusRepository.cs` | `IDocumentStatusRepository` | metody `IGenericRepository` |
| `InvoiceJet.Domain/Interfaces/Repositories/IDocumentTypeRepository.cs` | `IDocumentTypeRepository` | metody `IGenericRepository` |
| `InvoiceJet.Domain/Interfaces/Repositories/IUserFirmRepository.cs` | `IUserFirmRepository` | `GetUserFirmById`, `GetUserFirmClients` |

---

## 4. Warstwa Infrastructure

### 4.1 Persystencja

| Plik | Klasa | Rola |
|---|---|---|
| `InvoiceJet.Infrastructure/Persistence/InvoiceJetDbContext.cs` | `InvoiceJetDbContext` | `DbContext`: 10 `DbSet<T>`, jawne konfiguracje w `OnModelCreating` |
| `InvoiceJet.Infrastructure/Persistence/UnitOfWork.cs` | `UnitOfWork` | implementacja `IUnitOfWork`, `CompleteAsync()` = `SaveChangesAsync()` |
| `InvoiceJet.Infrastructure/Persistence/Repositories/GenericRepository.cs` | `GenericRepository<T>` | bazowa implementacja `IGenericRepository<T>` |
| `InvoiceJet.Infrastructure/Persistence/Repositories/UserRepository.cs` | `UserRepository` | `GetUserFirmIdAsync`, `GetUserFirmAsync`, `GetUserByIdAsync` |
| `InvoiceJet.Infrastructure/Persistence/Repositories/FirmRepository.cs` | `FirmRepository` | `GetTotalClientsAsync` (zlicza po `UserId`, nie `UserFirmId`) |
| `InvoiceJet.Infrastructure/Persistence/Repositories/BankAccountRepository.cs` | `BankAccountRepository` | `GetUserFirmBankAccountsAsync`, `GetTotalBankAccountsAsync` |
| `InvoiceJet.Infrastructure/Persistence/Repositories/ProductRepository.cs` | `ProductRepository` | `GetUserFirmProductsAsync`, `FindUserFirmProductByName`, `GetTotalProductsAsync` |
| `InvoiceJet.Infrastructure/Persistence/Repositories/DocumentSeriesRepository.cs` | `DocumentSeriesRepository` | `GetAllDocumentSeriesForActiveUserFirm` |
| `InvoiceJet.Infrastructure/Persistence/Repositories/DocumentRepository.cs` | `DocumentRepository` | `GetAllDocumentsByType`, `GetDocumentWithAllInfo` |
| `InvoiceJet.Infrastructure/Persistence/Repositories/DocumentProductRepository.cs` | `DocumentProductRepository` | `GetAllDocumentProductsForDocument`, `RemoveRangeAsync` |
| `InvoiceJet.Infrastructure/Persistence/Repositories/DocumentStatusRepository.cs` | `DocumentStatusRepository` | metody `IGenericRepository` |
| `InvoiceJet.Infrastructure/Persistence/Repositories/DocumentTypeRepository.cs` | `DocumentTypeRepository` | metody `IGenericRepository` |
| `InvoiceJet.Infrastructure/Persistence/Repositories/UserFirmRepository.cs` | `UserFirmRepository` | `GetUserFirmById`, `GetUserFirmClients` |

### 4.2 Migracje

| Plik | Rola |
|---|---|
| `InvoiceJet.Infrastructure/Migrations/InvoiceJetDbContextModelSnapshot.cs` | **Źródło prawdy schematu** — typy kolumn, nullable, klucze, indeksy, kaskady |
| `InvoiceJet.Infrastructure/Migrations/20240624165318_InitialCreate.cs` | Migracja inicjalna |
| `InvoiceJet.Infrastructure/Migrations/20240624165318_InitialCreate.Designer.cs` | Designer (auto-generated) |

### 4.3 Fabryki PDF (QuestPDF)

| Plik | Klasa / Interfejs | Rola |
|---|---|---|
| `InvoiceJet.Infrastructure/Factories/IDocumentFactory.cs` | `IDocumentFactory` | interfejs fabryki dokumentów PDF |
| `InvoiceJet.Infrastructure/Factories/IDocumentFactoryProvicer.cs` | `IDocumentFactoryProvider` | interfejs providera fabryk |
| `InvoiceJet.Infrastructure/Factories/Impl/InvoiceDocumentFactory.cs` | `InvoiceDocumentFactory` | fabryka dla `Factura` (`DocumentTypeId=1`) |
| `InvoiceJet.Infrastructure/Factories/Impl/ProformaDocumentFactory.cs` | `ProformaDocumentFactory` | fabryka dla `Factura Proforma` (`DocumentTypeId=2`) |
| `InvoiceJet.Infrastructure/Factories/Impl/StornoDocumentFactory.cs` | `StornoDocumentFactory` | fabryka dla `Factura Storno` (`DocumentTypeId=3`) |
| `InvoiceJet.Infrastructure/Services/PdfGenerationService.cs` | `PdfGenerationService` | implementacja `IPdfGenerationService`; wewnętrzny `try/catch` połyka błędy QuestPDF ⚠️ |
| `InvoiceJet.Infrastructure/Services/IQuestPDFDocument/Invoice.cs` | `Invoice` | dokument PDF faktury |
| `InvoiceJet.Infrastructure/Services/IQuestPDFDocument/ProformaInvoice.cs` | `ProformaInvoice` | dokument PDF proformy |
| `InvoiceJet.Infrastructure/Services/IQuestPDFDocument/StornoInvoice.cs` | `StornoInvoice` | dokument PDF storna |
| `InvoiceJet.Infrastructure/Services/IQuestPDFDocument/Component/AddressComponent.cs` | `AddressComponent` | komponent adresu w PDF |

---

## 5. Dokumentacja AOS

### 5.1 Instrukcje dla agenta (BackendAgentAI)

| Plik | Zawartość |
|---|---|
| `docs/BackendAgentAI/01_ZASADY_BACKEND_AOS.md` | 9 wymiarów, 3 odbiorcy, zasady ZB.1–ZB.10, styl |
| `docs/BackendAgentAI/02_SLOWNIK_BACKEND.md` | Terminologia, identyfikatory P-XX/API-XX/WAL-XX/TC-XX/DT-XX |
| `docs/BackendAgentAI/03_MARKERY_I_WERYFIKACJA.md` | Markery `[UWAGA]`, Definicja Ukończenia (DoD) per plik |
| `docs/BackendAgentAI/04_REGULY_DEKOMPOZYCJI.md` | Reguła „co jest procesem", numeracja, nazewnictwo |
| `docs/BackendAgentAI/05_KATALOGI_PRZEKROJOWE.md` | Spec 7 katalogów przekrojowych |
| `docs/BackendAgentAI/AOS_BACKEND_PROCESS_TEMPLATE.md` | Indeks 8 plików procesu, kolejność pracy |

### 5.2 Szablony procesów

| Plik | Szablon dla |
|---|---|
| `docs/aos/backend/templates/TEMPLATE_00_METADANE.md` | `00_METADANE.md` |
| `docs/aos/backend/templates/TEMPLATE_01_PRZEGLAD_PROCESU.md` | `01_PRZEGLAD_PROCESU.md` |
| `docs/aos/backend/templates/TEMPLATE_02_KONTRAKT_API.md` | `02_KONTRAKT_API.md` |
| `docs/aos/backend/templates/TEMPLATE_03_LOGIKA_APLIKACYJNA.md` | `03_LOGIKA_APLIKACYJNA.md` |
| `docs/aos/backend/templates/TEMPLATE_04_DANE_MODELE_MAPOWANIA.md` | `04_DANE_MODELE_MAPOWANIA.md` |
| `docs/aos/backend/templates/TEMPLATE_05_BLEDY_BEZPIECZENSTWO.md` | `05_BLEDY_BEZPIECZENSTWO.md` |
| `docs/aos/backend/templates/TEMPLATE_06_SCENARIUSZE_TESTOWE.md` | `06_SCENARIUSZE_TESTOWE.md` |
| `docs/aos/backend/templates/TEMPLATE_HISTORIA_ZMIAN.md` | `HISTORIA_ZMIAN.md` |

### 5.3 Szablony katalogów przekrojowych

| Plik | Katalog docelowy |
|---|---|
| `docs/aos/backend/templates/TEMPLATE_KATALOG_API.md` | `KATALOG_API.md` |
| `docs/aos/backend/templates/TEMPLATE_SLOWNIK_DANYCH.md` | `SLOWNIK_DANYCH.md` |
| `docs/aos/backend/templates/TEMPLATE_KATALOG_WYJATKOW.md` | `KATALOG_WYJATKOW.md` |
| `docs/aos/backend/templates/TEMPLATE_MODEL_DOMENY.md` | `MODEL_DOMENY.md` |
| `docs/aos/backend/templates/TEMPLATE_ZAGADNIENIA_PRZEKROJOWE.md` | `ZAGADNIENIA_PRZEKROJOWE.md` |
| `docs/aos/backend/templates/TEMPLATE_KATALOG_DANYCH_TESTOWYCH.md` | `KATALOG_DANYCH_TESTOWYCH.md` |
| `docs/aos/backend/templates/TEMPLATE_MAPA_FULLSTACK.md` | `MAPA_FULLSTACK.md` |

### 5.4 Katalogi przekrojowe (docelowe)

| Plik | Status | Zawartość |
|---|---|---|
| `docs/aos/backend/ZAGADNIENIA_PRZEKROJOWE.md` | ✅ gotowy | JWT, middleware, UoW, AutoMapper, CORS, DB, seed, ANAF, QuestPDF, pipeline |
| `docs/aos/backend/KATALOG_DANYCH_TESTOWYCH.md` | ✅ gotowy | Globalne fixture'y DT-01 – DT-08 |
| `docs/aos/backend/KATALOG_API.md` | ✅ gotowy | 31 endpointów API-01 – API-31, zgrupowane per kontroler |
| `docs/aos/backend/KATALOG_WYJATKOW.md` | ✅ gotowy | 9 zmapowanych + 6 niemapowanych (→500) z komunikatami |
| `docs/aos/backend/SLOWNIK_DANYCH.md` | ⏳ planowany | Schematy tabel, kolumny, enumy, seed |
| `docs/aos/backend/MODEL_DOMENY.md` | ⏳ planowany | Diagram ER, konfiguracje EF Core |
| `docs/aos/backend/MAPA_FULLSTACK.md` | 🚫 poza zakresem | Most do AOS frontendu — etap fullstack |

### 5.5 Procesy (dokumentacja aktywna)

| Katalog | Procesy |
|---|---|
| `docs/aos/backend/processes/Authentication/` | P-01 RegisterUser ✅, P-02 LoginUser ✅ |
| `docs/aos/backend/processes/FirmManagement/` | P-03 AddFirm ✅, P-04 GetFirmFromAnaf ✅, P-05 EditFirm ✅, P-06 GetUserActiveFirm ✅, P-07 GetUserClientFirms ✅, P-08 ManageClientFirms ✅ |
| `docs/aos/backend/processes/ProductManagement/` | P-09 ManageProducts ✅ |
| `docs/aos/backend/processes/BankAccountManagement/` | P-10 ManageBankAccounts ✅ |
| `docs/aos/backend/processes/DocumentSeriesManagement/` | P-11 ManageDocumentSeries ✅ |
| `docs/aos/backend/processes/DocumentManagement/` | P-12 AddDocument ✅, P-13 EditDocument ✅, P-14 GetDocuments ✅, P-15 DeleteDocuments ✅, P-16 GetDocumentAutofillInfo ✅, P-17 ManageDocumentPdf ✅, P-18 GetDashboardStats ✅, P-19 TransformToStorno ✅ |

Każdy proces zawiera **8 plików**: `00_METADANE`, `01_PRZEGLAD_PROCESU`, `02_KONTRAKT_API`, `03_LOGIKA_APLIKACYJNA`, `04_DANE_MODELE_MAPOWANIA`, `05_BLEDY_BEZPIECZENSTWO`, `06_SCENARIUSZE_TESTOWE`, `HISTORIA_ZMIAN`.

---

## 6. Szybkie mapowanie: Kontroler → Pliki do przeczytania

Przy dokumentowaniu procesu dla danego kontrolera przeczytaj:

| Kontroler | Serwis | DTO | Encje |
|---|---|---|---|
| `AuthController` | `AuthService` | `UserRegisterDto`, `UserLoginDto` | `User` |
| `FirmController` | `FirmService` | `FirmDto` | `Firm`, `UserFirm` |
| `BankAccountController` | `BankAccountService` | `BankAccountDto` | `BankAccount`, `UserFirm` |
| `ProductController` | `ProductService` | `ProductDto` | `Product`, `UserFirm` |
| `DocumentSeriesController` | `DocumentSeriesService` | `DocumentSeriesDto` | `DocumentSeries`, `DocumentType`, `UserFirm` |
| `DocumentController` | `DocumentService`, `PdfGenerationService` | `DocumentRequestDto`, `DocumentProductRequestDto`, `DocumentTableRecordDto`, `DocumentAutofillDto`, `DocumentStreamDto`, `DashboardStatsDto`, `MonthlyTotalDto` | `Document`, `DocumentProduct`, `DocumentSeries`, `BankAccount`, `Firm`, `DocumentType`, `DocumentStatus` |

**Zawsze** czytaj niezależnie od kontrolera:
- `InvoiceJet.Presentation/Middleware/ExceptionMiddleware.cs`
- `InvoiceJet.Infrastructure/Migrations/InvoiceJetDbContextModelSnapshot.cs` (sekcja dotycząca encji)
- `InvoiceJet.Infrastructure/Persistence/Repositories/<Repo>.cs` (repozytoria używane przez serwis)
