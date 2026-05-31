# Komponent: DbSeeder (Inicjalizacja bazy danych)

| Atrybut | Wartość |
|---|---|
| Plik | `InvoiceJet.Infrastructure/Data/DbSeeder.cs` (szacowane) |
| Wywołanie | `Program.cs` przy starcie aplikacji |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Inicjalizacja bazy danych danymi słownikowymi przy pierwszym uruchomieniu. Tworzy wymagane rekordy w tabelach referencyjnych jeśli są puste.

## Dane seedowane

### DocumentType

| Id | Name |
|---|---|
| 1 | Factura |
| 2 | Factura Proforma |
| 3 | Factura Storno |

### DocumentStatus

Dokładne wartości wymagają weryfikacji z kodem źródłowym `DbSeeder.cs`. Prawdopodobne statusy:

| Id | Name (rumuński) | Znaczenie |
|---|---|---|
| 1 | Trimisa | Wysłana |
| 2 | Platita | Zapłacona |
| 3 | Anulata | Anulowana |
| 4 | Refuzata | Odrzucona |

## Wywołanie w Program.cs

```csharp
// Program.cs (po zbudowaniu aplikacji)
using (var scope = app.Services.CreateScope())
{
    var seeder = scope.ServiceProvider.GetRequiredService<DbSeeder>();
    await seeder.SeedAsync();
}
```

## Logika seedowania

```csharp
// Szacowana logika
public async Task SeedAsync()
{
    if (!await _context.DocumentTypes.AnyAsync())
    {
        await _context.DocumentTypes.AddRangeAsync(
            new DocumentType { Id = 1, Name = "Factura" },
            new DocumentType { Id = 2, Name = "Factura Proforma" },
            new DocumentType { Id = 3, Name = "Factura Storno" }
        );
        await _context.SaveChangesAsync();
    }

    if (!await _context.DocumentStatuses.AnyAsync())
    {
        // Dodaj statusy...
        await _context.SaveChangesAsync();
    }
}
```

## Uwagi

- Seed nie tworzy użytkowników ani firm — dane biznesowe wprowadzane przez UI
- Idempotentny — wywołanie wielokrotne nie duplikuje danych (`AnyAsync()` check)
- Uruchamiany przy każdym starcie aplikacji (niska wydajność przy cold start)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
