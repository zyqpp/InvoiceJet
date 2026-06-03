# LINQ: GetDocumentById (pełny dokument z pozycjami)

| Atrybut | Wartość |
|---|---|
| ID | LINQ-01 |
| Serwis | `DocumentService.GetDocumentById()` |
| Endpoint | `GET /api/Document/GetDocumentById/{id}` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Pobranie pełnego dokumentu z wszystkimi zagnieżdżonymi danymi potrzebnymi do formularza edycji.

## Zapytanie LINQ (szacowane)

```csharp
var document = await _context.Documents
    .Include(d => d.Client)                          // Firma klienta
    .Include(d => d.BankAccount)                     // Konto bankowe
    .Include(d => d.DocumentSeries)                  // Seria numeracji
    .Include(d => d.DocumentStatus)                  // Status dokumentu
    .Include(d => d.UserFirm)                        // Powiązanie z firmą wystawiającego
        .ThenInclude(uf => uf.Firm)                  // Dane firmy wystawiającego (Seller)
    .Include(d => d.DocumentProducts)                // Pozycje dokumentu
        .ThenInclude(dp => dp.Product)               // Dane produktu dla każdej pozycji
    .FirstOrDefaultAsync(d => d.Id == id);
```

## Includowane tabele

| Include | Tabela docelowa | Użycie |
|---|---|---|
| `Client` | `Firm` | Dane klienta w formularzu |
| `BankAccount` | `BankAccount` | Konto bankowe |
| `DocumentSeries` | `DocumentSeries` | Seria (SeriesName, CurrentNumber) |
| `DocumentStatus` | `DocumentStatus` | Status dokumentu |
| `UserFirm → Firm` | `UserFirm` + `Firm` | Dane sprzedawcy (Seller) |
| `DocumentProducts → Product` | `DocumentProduct` + `Product` | Pozycje z danymi produktu |

## SQL generowane przez EF Core

EF Core generuje jedno zapytanie SQL z JOIN dla wszystkich Include, lub multiple queries zależnie od konfiguracji `AsSplitQuery()`.

## Anomalie

| # | Anomalia |
|---|---|
| LQ01-01 | `dp.Product!.Name` w AutoMapper profilu — jeśli `ThenInclude(dp => dp.Product)` jest pominięty, rzuca `NullReferenceException` |
| LQ01-02 | Brak `AsNoTracking()` — EF Core śledzi encję co może powodować problemy z detached entities przy aktualizacji |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
