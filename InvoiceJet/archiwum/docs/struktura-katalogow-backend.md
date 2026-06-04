# Struktura katalogowa — backend (InvoiceJetAPI)

Katalog główny projektu: `InvoiceJet/InvoiceJetAPI/`

Spis wygenerowany na podstawie struktury plików i folderów w repozytorium. Pominięto katalogi generowane lokalnie (`bin`, `obj`, `.vs`), pliki migracji z katalogu `obj` oraz katalog `docs` (dokumentacja AOS).

---

## Drzewo katalogów i plików

```
InvoiceJetAPI/
├── global.json
├── InvoiceJet.sln
│
├── InvoiceJet.Presentation/          ← Warstwa prezentacji (Web API host)
│   ├── InvoiceJet.Presentation.csproj
│   ├── Program.cs
│   ├── appsettings.json
│   ├── appsettings.Development.json
│   │
│   ├── Properties/
│   │   └── launchSettings.json
│   │
│   ├── Controllers/
│   │   ├── AuthController.cs
│   │   ├── BankAccountController.cs
│   │   ├── DocumentController.cs
│   │   ├── DocumentSeriesController.cs
│   │   ├── FirmController.cs
│   │   └── ProductController.cs
│   │
│   ├── Middleware/
│   │   └── ExceptionMiddleware.cs
│   │
│   └── Seeders/
│       └── DbSeeder.cs
│
├── InvoiceJet.Application/            ← Warstwa aplikacyjna (logika biznesowa, DTO, mapowania)
│   ├── InvoiceJet.Application.csproj
│   │
│   ├── DTOs/
│   │   ├── BankAccountDto.cs
│   │   ├── DashboardStatsDto.cs
│   │   ├── DocumentAutofillDto.cs
│   │   ├── DocumentProductRequestDto.cs
│   │   ├── DocumentRequestDto.cs
│   │   ├── DocumentSeriesDto.cs
│   │   ├── DocumentStatusDto.cs
│   │   ├── DocumentStreamDto.cs
│   │   ├── DocumentTableRecordDto.cs
│   │   ├── FirmDto.cs
│   │   ├── MonthlyTotalDto.cs
│   │   ├── ProductDto.cs
│   │   ├── UserLoginDto.cs
│   │   └── UserRegisterDto.cs
│   │
│   ├── MappingProfiles/
│   │   ├── BankAccountProfile.cs
│   │   ├── DocumentProductProfile.cs
│   │   ├── DocumentProfile.cs
│   │   ├── DocumentSeriesProfile.cs
│   │   ├── DocumentStatusProfile.cs
│   │   ├── FirmProfile.cs
│   │   └── ProductProfile.cs
│   │
│   └── Services/
│       ├── IAuthService.cs
│       ├── IBankAccountService.cs
│       ├── IDocumentSeriesService.cs
│       ├── IDocumentService.cs
│       ├── IFirmService.cs
│       ├── IPdfGenerationService.cs
│       ├── IProductService.cs
│       ├── IUserService.cs
│       │
│       └── Impl/
│           ├── AuthService.cs
│           ├── BankAccountService.cs
│           ├── DocumentSeriesService.cs
│           ├── DocumentService.cs
│           ├── FirmService.cs
│           ├── ProductService.cs
│           └── UserService.cs
│
├── InvoiceJet.Domain/                 ← Warstwa domenowa (modele, wyjątki, interfejsy)
│   ├── InvoiceJet.Domain.csproj
│   │
│   ├── Enums/
│   │   ├── Currency.cs
│   │   ├── DocumentStatus.cs
│   │   └── DocumentType.cs
│   │
│   ├── Exceptions/
│   │   ├── AnafFirmNotFoundException.cs
│   │   ├── BankAccountAssociatedWithDocuments.cs
│   │   ├── FirmAssociatedWithDocumentException.cs
│   │   ├── IncorrectPasswordException.cs
│   │   ├── InvalidPasswordException.cs
│   │   ├── NoBankAccountAddedException.cs
│   │   ├── PasswordMismatchException.cs
│   │   ├── ProductAssociatedWithInvoiceException.cs
│   │   ├── ProductWithSameNameExistsException.cs
│   │   ├── UserAlreadyExistsException.cs
│   │   ├── UserHasNoAssociatedFirmException.cs
│   │   └── UserNotFoundException.cs
│   │
│   ├── Interfaces/
│   │   ├── IUnitOfWork.cs
│   │   │
│   │   └── Repositories/
│   │       ├── IBankAccountRepository.cs
│   │       ├── IDocumentProductRepository.cs
│   │       ├── IDocumentRepository.cs
│   │       ├── IDocumentSeriesRepository.cs
│   │       ├── IDocumentStatusRepository.cs
│   │       ├── IDocumentTypeRepository.cs
│   │       ├── IFirmRepository.cs
│   │       ├── IGenericRepository.cs
│   │       ├── IProductRepository.cs
│   │       ├── IUserFirmRepository.cs
│   │       └── IUserRepository.cs
│   │
│   └── Models/
│       ├── BankAccount.cs
│       ├── BaseEntity.cs
│       ├── Document.cs
│       ├── DocumentProduct.cs
│       ├── DocumentSeries.cs
│       ├── DocumentStatus.cs
│       ├── DocumentType.cs
│       ├── Firm.cs
│       ├── Product.cs
│       ├── User.cs
│       └── UserFirm.cs
│
└── InvoiceJet.Infrastructure/         ← Warstwa infrastruktury (EF Core, repozytoria, PDF, fabryki)
    ├── InvoiceJet.Infrastructure.csproj
    │
    ├── Factories/
    │   ├── IDocumentFactory.cs
    │   ├── IDocumentFactoryProvicer.cs        ← [UWAGA: literówka w nazwie pliku — "Provicer" zamiast "Provider"]
    │   │
    │   └── Impl/
    │       ├── InvoiceDocumentFactory.cs
    │       ├── ProformaDocumentFactory.cs
    │       └── StornoDocumentFactory.cs
    │
    ├── Migrations/
    │   ├── 20240624165318_InitialCreate.cs
    │   ├── 20240624165318_InitialCreate.Designer.cs
    │   └── InvoiceJetDbContextModelSnapshot.cs
    │
    ├── Persistence/
    │   ├── InvoiceJetDbContext.cs
    │   ├── UnitOfWork.cs
    │   │
    │   └── Repositories/
    │       ├── GenericRepository.cs
    │       ├── BankAccountRepository.cs
    │       ├── DocumentProductRepository.cs
    │       ├── DocumentRepository.cs
    │       ├── DocumentSeriesRepository.cs
    │       ├── DocumentStatusRepository.cs
    │       ├── DocumentTypeRepository.cs
    │       ├── FirmRepository.cs
    │       ├── ProductRepository.cs
    │       ├── UserFirmRepository.cs
    │       └── UserRepository.cs
    │
    └── Services/
        ├── PdfGenerationService.cs
        │
        └── IQuestPDFDocument/
            ├── Invoice.cs
            ├── ProformaInvoice.cs
            ├── StornoInvoice.cs
            │
            └── Component/
                └── AddressComponent.cs
```

---

## Podsumowanie — rozszerzenia plików

| Rozszerzenie | Liczba plików | Typ |
|---|---|---|
| `.cs` | 109 | C# — kontrolery, serwisy, repozytoria, modele, DTO, profile AutoMapper, wyjątki, fabryki, dokumenty QuestPDF |
| `.csproj` | 4 | Pliki projektów .NET (`Presentation`, `Application`, `Domain`, `Infrastructure`) |
| `.json` | 5 | Konfiguracja (`appsettings.json`, `appsettings.Development.json`, `launchSettings.json`, `global.json`) + `.sln` (1) |
| `.sln` | 1 | Plik solution Visual Studio |

**Łącznie plików źródłowych (bez `bin`, `obj`, `.vs`, `docs`):** ~119

---

## Rozkład plików `.cs` według warstwy

| Warstwa | Katalog | Liczba `.cs` |
|---|---|---|
| Presentation | `InvoiceJet.Presentation/` | 9 |
| Application | `InvoiceJet.Application/` | 36 |
| Domain | `InvoiceJet.Domain/` | 38 |
| Infrastructure | `InvoiceJet.Infrastructure/` | 26 |
| **Łącznie** | | **109** |

---

## Katalogi pomijane (nie w repozytorium / generowane)

Poniższe katalogi mogą pojawić się lokalnie, ale nie są częścią źródeł:

- `bin/` — skompilowane artefakty (`Debug`/`Release`)
- `obj/` — pliki pośrednie MSBuild i generowane przez kompilator
- `.vs/` — ustawienia lokalne Visual Studio
- `docs/` — dokumentacja AOS (oddzielny katalog z plikami `.md`)
