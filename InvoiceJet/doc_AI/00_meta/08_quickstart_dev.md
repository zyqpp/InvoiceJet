# Quickstart dla dewelopera — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Wymagania

| Narzędzie | Wersja | Do czego |
|---|---|---|
| .NET SDK | 8.0 | Backend ASP.NET Core |
| SQL Server / LocalDB | 2019+ | Baza danych |
| Node.js | 18+ | Frontend Angular |
| Angular CLI | 16.x | `ng serve` |
| Visual Studio / VS Code | dowolna | IDE |

## Uruchomienie backendu

### 1. Konfiguracja `appsettings.json`

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=InvoiceJetDb;Trusted_Connection=True;"
  },
  "AppSettings": {
    "Token": "twój_sekretny_klucz_minimum_32_znaki_dla_HmacSha512",
    "AnafApiUrl": "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva"
  }
}
```

### 2. Migracje EF Core

```bash
cd InvoiceJetAPI/InvoiceJet.Presentation
dotnet ef database update
```

### 3. Uruchomienie

```bash
dotnet run
# API dostępne na: https://localhost:5001 lub http://localhost:5000
```

Swagger UI: `https://localhost:5001/swagger`

### 4. Seed danych

DbSeeder uruchamia się automatycznie przy starcie — tworzy `DocumentType` i `DocumentStatus`.

## Uruchomienie frontendu

```bash
cd InvoiceJet/src
npm install
ng serve
# Aplikacja dostępna na: http://localhost:4200
```

## Konfiguracja URL API (Angular)

```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  apiUrl: 'https://localhost:5001/api'
};

// src/environments/environment.prod.ts
export const environment = {
  production: true,
  apiUrl: 'https://invoicejetapi.azurewebsites.net/api'
};
```

## Kluczowe informacje dla dewelopera

### JWT w backendzie — odczyt userId

```csharp
// W każdym kontrolerze:
var userId = int.Parse(User.FindFirst("userId")!.Value);
```

### Wzorzec dostępu do danych (Unit of Work)

```csharp
// Wstrzykiwanie:
private readonly IUnitOfWork _unitOfWork;

// Użycie:
await _unitOfWork.Products.GetAllByUserFirmIdAsync(userFirmId);
await _unitOfWork.CompleteAsync(); // = SaveChangesAsync()
```

### Dodawanie nowego endpointu (szablon)

1. Dodaj metodę w `I{Nazwa}Service.cs`
2. Zaimplementuj w `{Nazwa}Service.cs`
3. Dodaj endpoint w `{Nazwa}Controller.cs`
4. Wyjątki domenowe → `ExceptionMiddleware.cs`
5. DTO jeśli potrzebne → `DTOs/` + profil AutoMapper

### Angular — wzorzec dostępu do API

```typescript
// Serwis Angular
getAll(): Observable<IProduct[]> {
    return this.http.get<IProduct[]>(`${environment.apiUrl}/Product/GetAll`);
}

// Komponent
ngOnInit() {
    this.productService.getAll().subscribe({
        next: (products) => this.products = products,
        error: (err) => this.toastr.error(err.error?.message)
    });
}
```

## Najważniejsze pliki

| Plik | Rola |
|---|---|
| `InvoiceJet.Presentation/Program.cs` | DI, middleware, JWT, CORS |
| `InvoiceJet.Infrastructure/Migrations/InvoiceJetDbContextModelSnapshot.cs` | Pełny schemat DB |
| `src/app/app-routing.module.ts` | Routing Angular |
| `src/environments/environment.ts` | URL API (dev) |
| `src/app/helpers/jwt.interceptor.ts` | Dołączanie JWT do żądań |
| `src/app/helpers/auth.guard.ts` | Ochrona tras |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
