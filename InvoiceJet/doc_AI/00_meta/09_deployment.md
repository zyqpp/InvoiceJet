# Wdrożenie (Deployment) — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Środowiska

| Środowisko | Backend URL | Frontend URL |
|---|---|---|
| Produkcja | `https://invoicejetapi.azurewebsites.net` | Angular → Azure Static Web Apps (zakładane) |
| Lokalne (dev) | `https://localhost:5001` | `http://localhost:4200` |

## Hosting Backend — Azure App Service

- Platform: Azure App Service (Windows lub Linux)
- Runtime: .NET 8
- Connection String: Azure SQL Database

## Konfiguracja produkcyjna

### appsettings.Production.json (lub Azure App Settings)

| Klucz | Opis |
|---|---|
| `ConnectionStrings:DefaultConnection` | Azure SQL connection string |
| `AppSettings:Token` | Sekretny klucz JWT (min. 32 znaki) |
| `AppSettings:AnafApiUrl` | URL ANAF API |

### Krytyczne — CORS w produkcji (BUG)

```csharp
// Program.cs — OBECNY KOD (tylko dev):
builder.Services.AddCors(options => {
    options.AddPolicy("AllowAll", policy => {
        policy.WithOrigins("http://localhost:4200") // ← BUG! Brak produkcji
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});
```

**Do naprawy przed wdrożeniem produkcyjnym:**
```csharp
policy.WithOrigins(
    "http://localhost:4200",
    "https://twoja-aplikacja.azurestaticapps.net"  // ← DODAĆ
)
```

## CI/CD

Brak informacji o CI/CD pipeline w projekcie. Prawdopodobne wdrożenie ręczne przez:
- Visual Studio Publish → Azure App Service
- lub GitHub Actions

## Zmienne środowiskowe wymagane na Azure

| Nazwa | Opis |
|---|---|
| `ConnectionStrings__DefaultConnection` | SQL Server connection string |
| `AppSettings__Token` | JWT secret key |
| `AppSettings__AnafApiUrl` | URL ANAF API |

**Uwaga:** Separator `__` (double underscore) w Azure App Settings odpowiada `:` w appsettings.json.

## Angular — build produkcyjny

```bash
ng build --configuration production
# Generuje: dist/facturila-ui/
```

Pliki z `dist/facturila-ui/` wdrożone na Azure Static Web Apps lub dowolny hosting statyczny.

## Migracje bazy przy wdrożeniu

EF Core migracje powinny być uruchamiane przez pipeline CI/CD lub przy starcie aplikacji:

```csharp
// Program.cs (opcjonalne auto-migrate)
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<InvoiceJetDbContext>();
    db.Database.Migrate();
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
