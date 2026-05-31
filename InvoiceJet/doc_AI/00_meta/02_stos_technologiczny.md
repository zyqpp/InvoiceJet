# Stos technologiczny

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Źródło | `InvoiceJet.Presentation.csproj`, `InvoiceJet.Infrastructure.csproj`, `InvoiceJetUI/package.json` |

## 1. Backend — InvoiceJetAPI

### Runtime i framework

| Technologia | Wersja | Rola |
|---|---|---|
| .NET | 8.0 | Runtime |
| ASP.NET Core | 8.0 | Web API framework |
| Target Framework | `net8.0` | — |
| Nullable | `enable` | — |
| ImplicitUsings | `enable` | — |

### Pakiety NuGet

| Pakiet | Wersja | Rola |
|---|---|---|
| `AutoMapper` | 13.0.1 | Mapowanie obiektów (Encja ↔ DTO) |
| `AutoMapper.Collection` | 10.0.0 | Rozszerzenie AutoMapper dla kolekcji |
| `BCrypt.Net-Next` | 4.0.3 | Hashowanie i weryfikacja haseł |
| `Microsoft.AspNetCore.Authentication.JwtBearer` | 8.0.6 | Walidacja JWT Bearer Token |
| `Microsoft.AspNetCore.OpenApi` | 8.0.6 | OpenAPI/Swagger wsparcie |
| `Microsoft.Data.SqlClient` | 5.2.1 | Sterownik SQL Server |
| `Microsoft.EntityFrameworkCore` | 8.0.6 | ORM — Code First |
| `Microsoft.EntityFrameworkCore.SqlServer` | 8.0.6 | Provider SQL Server dla EF Core |
| `Microsoft.EntityFrameworkCore.Tools` | 8.0.6 | Migracje (CLI) |
| `Newtonsoft.Json` | 13.0.3 | Deserializacja JSON (m.in. odpowiedzi ANAF) |
| `QuestPDF` | 2024.3.10 | Generowanie dokumentów PDF (licencja Community) |
| `Swashbuckle.AspNetCore` | 6.6.2 | Swagger UI |
| `Swashbuckle.AspNetCore.Filters` | 7.0.12 | Filtry Swagger (JWT security) |

### Baza danych

| Technologia | Szczegóły |
|---|---|
| Silnik | Microsoft SQL Server |
| Connection string | `ProdConnection` (appsettings — tylko produkcyjny) |
| Schema | `dbo` (domyślna) |
| ORM | EF Core 8 Code First |
| Migracje | EF Core Migrations |

---

## 2. Frontend — InvoiceJetUI

### Runtime i framework

| Technologia | Wersja | Rola |
|---|---|---|
| Node.js | (kompatybilny z Angular 16) | Runtime budowania |
| Angular CLI | 16.2.12 | Framework SPA |
| TypeScript | — | Język |
| Package name | `facturila-ui` | Nazwa pakietu npm |

### Kluczowe zależności npm

| Pakiet | Wersja | Rola |
|---|---|---|
| `@angular/core` | ~16.2.12 | Framework Angular |
| `@angular/material` | ~16.2.12 | Komponenty Material Design (tabele, dialogi, formularze) |
| `@angular/cdk` | ~16.2.12 | Angular CDK |
| `@angular/forms` | ~16.2.12 | Reaktywne formularze |
| `@angular/router` | ~16.2.12 | Routing SPA |
| `@auth0/angular-jwt` | — | Dekodowanie i weryfikacja JWT po stronie klienta |
| `ng2-charts` | — | Wykresy (Chart.js wrapper dla Angular) |
| `chart.js` | — | Biblioteka wykresów |
| `ngx-toastr` | — | Powiadomienia toast |
| `rxjs` | ~7.8.0 | Programowanie reaktywne |

---

## 3. Hosting i infrastruktura

| Element | Szczegóły |
|---|---|
| API (produkcja) | Azure App Service — `invoicejetapi.azurewebsites.net` |
| API (lokalne) | `https://localhost:7229` |
| Frontend (lokalne) | `http://localhost:4200` |
| CORS | Polityka "NgOrigins": `localhost:4200`, `https://localhost:4200` |
| JWT walidacja Issuer | `false` (pomijana) |
| JWT walidacja Audience | `false` (pomijana) |
| JWT ClockSkew | `TimeSpan.Zero` (brak tolerancji na różnicę czasu) |

---

## 4. Architektura rozwiązania

```
InvoiceJet.sln
├── InvoiceJetAPI/                    ← Backend (.NET 8)
│   ├── InvoiceJet.Presentation/     ← Warstwa prezentacji (ASP.NET Core Web API)
│   ├── InvoiceJet.Application/      ← Warstwa aplikacyjna (serwisy, DTO, profile)
│   ├── InvoiceJet.Domain/           ← Warstwa domenowa (modele, interfejsy, wyjątki)
│   └── InvoiceJet.Infrastructure/   ← Warstwa infrastrukturalna (EF Core, repozytoria, PDF)
│
└── InvoiceJetUI/                     ← Frontend (Angular 16)
    └── src/app/
        ├── components/               ← Komponenty Angular (24 szt.)
        ├── services/                 ← Serwisy HTTP (8 szt.)
        ├── models/                   ← Interfejsy TypeScript
        └── guards/                   ← AuthGuard
```

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Inwentaryzacja stosu na podstawie plików csproj i package.json. |
