# Drzewo projektu

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Uwaga | Pokazuje strukturę logiczną — pomija `bin/`, `obj/`, `node_modules/`, `.angular/` |

## Backend — InvoiceJetAPI

```
InvoiceJetAPI/
│
├── InvoiceJet.Presentation/                   ← Warstwa prezentacji (API)
│   ├── Controllers/
│   │   ├── AuthController.cs                  ← Register, Login
│   │   ├── FirmController.cs                  ← CRUD firm (własna + klienci) + ANAF
│   │   ├── BankAccountController.cs           ← CRUD kont bankowych
│   │   ├── ProductController.cs               ← CRUD produktów
│   │   ├── DocumentSeriesController.cs        ← CRUD serii dokumentów
│   │   └── DocumentController.cs             ← CRUD dokumentów + PDF + dashboard
│   ├── Middleware/
│   │   └── ExceptionMiddleware.cs             ← Globalny handler wyjątków
│   ├── Seeders/
│   │   └── DbSeeder.cs                        ← Seed: DocumentType, DocumentStatus
│   ├── Program.cs                             ← DI, middleware pipeline, CORS, JWT
│   └── InvoiceJet.Presentation.csproj
│
├── InvoiceJet.Application/                    ← Warstwa aplikacyjna
│   ├── DTOs/                                  ← 14 klas DTO
│   │   ├── UserLoginDto.cs
│   │   ├── UserRegisterDto.cs
│   │   ├── FirmDto.cs
│   │   ├── BankAccountDto.cs
│   │   ├── ProductDto.cs
│   │   ├── DocumentSeriesDto.cs
│   │   ├── DocumentStatusDto.cs
│   │   ├── DocumentProductRequestDto.cs
│   │   ├── DocumentRequestDto.cs
│   │   ├── DocumentTableRecordDto.cs
│   │   ├── DocumentAutofillDto.cs
│   │   ├── DocumentStreamDto.cs
│   │   ├── DashboardStatsDto.cs
│   │   └── MonthlyTotalDto.cs
│   ├── Services/
│   │   ├── IAuthService.cs
│   │   ├── IFirmService.cs
│   │   ├── IBankAccountService.cs
│   │   ├── IProductService.cs
│   │   ├── IDocumentSeriesService.cs
│   │   ├── IDocumentService.cs
│   │   ├── IPdfGenerationService.cs
│   │   ├── IUserService.cs
│   │   └── Impl/
│   │       ├── AuthService.cs
│   │       ├── FirmService.cs
│   │       ├── BankAccountService.cs
│   │       ├── ProductService.cs
│   │       ├── DocumentSeriesService.cs
│   │       ├── DocumentService.cs
│   │       └── UserService.cs
│   ├── MappingProfiles/                       ← 7 profili AutoMapper
│   │   ├── BankAccountProfile.cs
│   │   ├── FirmProfile.cs
│   │   ├── ProductProfile.cs
│   │   ├── DocumentStatusProfile.cs
│   │   ├── DocumentSeriesProfile.cs
│   │   ├── DocumentProductProfile.cs
│   │   └── DocumentProfile.cs
│   └── InvoiceJet.Application.csproj
│
├── InvoiceJet.Domain/                         ← Warstwa domenowa
│   ├── Models/                                ← 10 encji
│   │   ├── User.cs
│   │   ├── Firm.cs
│   │   ├── BankAccount.cs
│   │   ├── UserFirm.cs
│   │   ├── Product.cs
│   │   ├── DocumentType.cs
│   │   ├── DocumentSeries.cs
│   │   ├── Document.cs
│   │   ├── DocumentProduct.cs
│   │   └── DocumentStatus.cs
│   ├── Exceptions/                            ← Wyjątki domenowe
│   │   ├── UserAlreadyExistsException.cs
│   │   ├── UserNotFoundException.cs
│   │   ├── InvalidPasswordException.cs
│   │   ├── PasswordMismatchException.cs
│   │   ├── IncorrectPasswordException.cs
│   │   ├── UserHasNoAssociatedFirmException.cs
│   │   └── NoBankAccountAddedException.cs
│   ├── Interfaces/                            ← Kontrakty repozytoriów
│   │   ├── IUnitOfWork.cs
│   │   ├── IGenericRepository.cs
│   │   └── Repositories/
│   │       ├── IUserRepository.cs
│   │       ├── IFirmRepository.cs
│   │       ├── IBankAccountRepository.cs
│   │       ├── IProductRepository.cs
│   │       ├── IDocumentSeriesRepository.cs
│   │       ├── IDocumentRepository.cs
│   │       └── IDocumentProductRepository.cs
│   ├── Enums/
│   │   ├── DocumentStatusEnum.cs              ← Unpaid=1, Paid=2
│   │   ├── DocumentTypeEnum.cs                ← Invoice=1, Proforma=2, Storno=3
│   │   └── CurrencyEnum.cs                    ← Ron=0, Eur=1
│   └── InvoiceJet.Domain.csproj
│
└── InvoiceJet.Infrastructure/                 ← Warstwa infrastrukturalna
    ├── Persistence/
    │   ├── InvoiceJetDbContext.cs             ← EF Core DbContext
    │   ├── UnitOfWork.cs                      ← Unit of Work
    │   ├── Repositories/
    │   │   ├── GenericRepository.cs
    │   │   ├── UserRepository.cs
    │   │   ├── FirmRepository.cs
    │   │   ├── BankAccountRepository.cs
    │   │   ├── ProductRepository.cs
    │   │   ├── DocumentSeriesRepository.cs
    │   │   ├── DocumentRepository.cs
    │   │   └── DocumentProductRepository.cs
    │   └── Migrations/
    │       └── InvoiceJetDbContextModelSnapshot.cs
    ├── Services/
    │   └── PdfGenerationService.cs            ← QuestPDF implementacja
    ├── Factories/                             ← Zakomentowane w Program.cs
    │   ├── IDocumentFactory.cs
    │   └── Impl/
    │       ├── InvoiceDocumentFactory.cs
    │       ├── ProformaDocumentFactory.cs
    │       └── DocumentFactoryProvider.cs
    └── InvoiceJet.Infrastructure.csproj
```

---

## Frontend — InvoiceJetUI

```
InvoiceJetUI/
├── src/
│   ├── app/
│   │   ├── app.component.ts / .html / .scss
│   │   ├── app.module.ts
│   │   ├── app-routing.module.ts               ← 17 tras
│   │   │
│   │   ├── components/
│   │   │   ├── dashboard/
│   │   │   │   └── dashboard.component.ts
│   │   │   ├── login/
│   │   │   │   └── login.component.ts
│   │   │   ├── register/
│   │   │   │   └── register.component.ts
│   │   │   ├── navbar/
│   │   │   │   └── navbar.component.ts
│   │   │   ├── sidebar/
│   │   │   │   └── sidebar.component.ts
│   │   │   ├── pdf-viewer/
│   │   │   │   └── pdf-viewer.component.ts
│   │   │   ├── token-expired-dialog/
│   │   │   │   └── token-expired-dialog.component.ts
│   │   │   ├── firm/
│   │   │   │   ├── firm-details/firm-details.component.ts
│   │   │   │   ├── clients/clients.component.ts
│   │   │   │   ├── add-edit-client-dialog/add-edit-client-dialog.component.ts
│   │   │   │   └── bank-accounts/
│   │   │   │       ├── bank-accounts.component.ts
│   │   │   │       └── add-or-edit-bank-account-dialog/
│   │   │   │           └── add-or-edit-bank-account-dialog.component.ts
│   │   │   ├── products/
│   │   │   │   ├── products.component.ts
│   │   │   │   └── add-or-edit-product-dialog/
│   │   │   │       └── add-or-edit-product-dialog.component.ts
│   │   │   ├── document-series/
│   │   │   │   ├── document-series.component.ts
│   │   │   │   └── add-or-edit-document-series-dialog/
│   │   │   │       └── add-or-edit-document-series-dialog.component.ts
│   │   │   ├── invoices/
│   │   │   │   ├── invoices.component.ts
│   │   │   │   ├── base-invoice/base-invoice.component.ts  ← klasa abstrakcyjna
│   │   │   │   └── add-or-edit-invoice/add-or-edit-invoice.component.ts
│   │   │   ├── invoice-proformas/
│   │   │   │   ├── invoice-proformas.component.ts
│   │   │   │   └── add-or-edit-invoice-proforma/
│   │   │   │       └── add-or-edit-invoice-proforma.component.ts
│   │   │   └── invoice-stornos/
│   │   │       ├── invoice-stornos.component.ts
│   │   │       └── add-or-edit-invoice-stornos/
│   │   │           └── add-or-edit-invoice-stornos.component.ts
│   │   │
│   │   ├── services/
│   │   │   ├── auth.service.ts
│   │   │   ├── firm.service.ts
│   │   │   ├── bank-account.service.ts
│   │   │   ├── product.service.ts
│   │   │   ├── document-series.service.ts
│   │   │   ├── document.service.ts
│   │   │   ├── sidebar.service.ts
│   │   │   ├── user.service.ts
│   │   │   └── interceptor/
│   │   │       ├── auth.interceptor.ts
│   │   │       └── error.interceptor.ts
│   │   │
│   │   ├── models/
│   │   │   ├── IBankAccount.ts
│   │   │   ├── ICurrency.ts
│   │   │   ├── IDashboardStats.ts
│   │   │   ├── IDocument.ts
│   │   │   ├── IDocumentAutofill.ts
│   │   │   ├── IDocumentProduct.ts
│   │   │   ├── IDocumentProductRequest.ts
│   │   │   ├── IDocumentRequest.ts
│   │   │   ├── IDocumentSeries.ts
│   │   │   ├── IDocumentStatus.ts
│   │   │   ├── IDocumentTableRecord.ts
│   │   │   ├── IDocumentType.ts
│   │   │   ├── IFirm.ts
│   │   │   ├── ILoginUser.ts
│   │   │   ├── IMonthlyTotal.ts
│   │   │   ├── IProduct.ts
│   │   │   └── IRegisterUser.ts
│   │   │
│   │   └── guards/
│   │       └── auth.guard.ts
│   │
│   └── environments/
│       ├── environment.ts              ← apiUrl: localhost:7229
│       └── environment.prod.ts        ← apiUrl: invoicejetapi.azurewebsites.net
│
├── package.json
└── angular.json
```

---

## Dokumentacja

```
InvoiceJet/
├── PLAN.md                            ← Plan dokumentowania (13 faz)
├── archiwum/                          ← Informacja o archiwizacji starej dokumentacji
├── wytyczne/                          ← Wytyczne frameworku AOS (7 plików)
└── doc_AI/                            ← NOWA dokumentacja systemu
    ├── README.md
    ├── 00_meta/                       ← Dokumenty fundacyjne (ten plik)
    ├── 01_ekrany/                     ← Dokumentacja ekranów Angular
    ├── 02_procesy/                    ← Dokumentacja procesów technicznych
    ├── 03_algorytmy/                  ← Dokumentacja algorytmów
    ├── 04_api_i_integracje/           ← Endpointy API
    ├── 05_model_danych/               ← Model DB, DTO, AutoMapper
    ├── 06_role_i_uprawnienia/         ← Role i macierz uprawnień
    ├── 07_use_case/                   ← Przypadki użycia
    ├── 08_model_biznesowy/            ← Kontekst biznesowy
    ├── 09_procesy_biznesowe/          ← BPMN/Mermaid procesy
    ├── 10_testy/                      ← Scenariusze testowe
    ├── _mapowania/                    ← Inwentaryzacje i mapy krzyżowe
    └── _szablony/                     ← Szablony dokumentów
```

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pełne drzewo projektu. |
