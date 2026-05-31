# Diagram Clean Architecture — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Warstwy projektu

```mermaid
graph TD
    subgraph PRESENTATION["🌐 InvoiceJet.Presentation"]
        PC[Program.cs<br/>DI + Middleware + CORS + JWT]
        EX[ExceptionMiddleware.cs]
        AC[AuthController]
        FC[FirmController]
        BC[BankAccountController]
        PROD[ProductController]
        DSC[DocumentSeriesController]
        DC[DocumentController]
    end

    subgraph APPLICATION["⚙️ InvoiceJet.Application"]
        subgraph SERVICES["Services"]
            AS[AuthService]
            FS[FirmService]
            BAS[BankAccountService]
            PS[ProductService]
            DSS[DocumentSeriesService]
            DOCS[DocumentService]
        end
        subgraph DTOS["DTOs (14)"]
            D1[RegisterUserDto]
            D2[FirmRequestDto]
            D3[DocumentRequestDto]
            D4[...12 innych]
        end
        subgraph MAPPERS["AutoMapper Profiles (7)"]
            M1[AuthProfile]
            M2[FirmProfile]
            M3[DocumentProfile]
            M4[...4 innych]
        end
    end

    subgraph DOMAIN["🏛️ InvoiceJet.Domain"]
        subgraph ENTITIES["Entities (10)"]
            E1[User]
            E2[Firm]
            E3[UserFirm]
            E4[BankAccount]
            E5[Product]
            E6[DocumentSeries]
            E7[Document]
            E8[DocumentProduct]
            E9[DocumentType]
            E10[DocumentStatus]
        end
        subgraph EXCEPTIONS["Exceptions (9)"]
            EX1[UserAlreadyExistsException]
            EX2[UserNotFoundException]
            EX3[FirmNotFoundException]
            EX4[...6 innych]
        end
        subgraph INTERFACES["Repository Interfaces"]
            I1[IUserRepository]
            I2[IFirmRepository]
            I3[IDocumentRepository]
            I4[...inne]
            IUoW[IUnitOfWork]
        end
    end

    subgraph INFRASTRUCTURE["🗄️ InvoiceJet.Infrastructure"]
        subgraph DB["Database"]
            CTX[InvoiceJetDbContext<br/>EF Core 8]
            MIG[Migrations]
        end
        subgraph REPOS["Repositories"]
            R1[UserRepository]
            R2[FirmRepository]
            R3[DocumentRepository]
            R4[...inne]
        end
        UoW[UnitOfWork<br/>CompleteAsync = SaveChangesAsync]
        SEED[DbSeeder<br/>DocumentType + DocumentStatus]
    end

    %% Dependencies
    PRESENTATION --> APPLICATION
    APPLICATION --> DOMAIN
    INFRASTRUCTURE --> DOMAIN
    PRESENTATION --> INFRASTRUCTURE

    style PRESENTATION fill:#4A90D9,color:#fff
    style APPLICATION fill:#7B68EE,color:#fff
    style DOMAIN fill:#2ECC71,color:#fff
    style INFRASTRUCTURE fill:#E67E22,color:#fff
```

## HTTP Request Pipeline

```
HTTP Request
    ↓
[HTTPS Redirection]
    ↓
[CORS: localhost:4200]
    ↓
[Authentication: JwtBearer]
    ↓
[Authorization: [Authorize]]
    ↓
[ExceptionMiddleware] ← przechwytuje wszystkie wyjątki
    ↓
[Controller] → [Service] → [Repository] → [DB]
    ↓
HTTP Response (200/201/400/401/404/409/500)
```

## Dependency Injection (Program.cs)

```
Scoped:
  IUnitOfWork → UnitOfWork
  IAuthService → AuthService
  IFirmService → FirmService
  IBankAccountService → BankAccountService
  IProductService → ProductService
  IDocumentSeriesService → DocumentSeriesService
  IDocumentService → DocumentService

Singleton:
  AutoMapper (AddAutoMapper)
  
HttpClient:
  IHttpClientFactory (dla ANAF API)
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
