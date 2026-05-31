# LINQ: GetDashboardStats (statystyki)

| Atrybut | Wartość |
|---|---|
| ID | LINQ-03 |
| Serwis | `DocumentService.GetDashboardStats()` |
| Endpoint | `GET /api/Document/GetDashboardStats/{year}/{documentType}` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Agregowanie danych statystycznych dla dashboardu — liczniki i miesięczne sumy.

## Zapytania LINQ (szacowane)

### Liczniki globalne

```csharp
var totalDocuments = await _context.Documents
    .CountAsync(d => d.UserFirmId == userFirmId);

var totalClients = await _context.UserFirms
    .Where(uf => uf.Id == userFirmId)
    .SelectMany(uf => uf.ClientFirms)
    .CountAsync();

var totalProducts = await _context.Products
    .CountAsync(p => p.UserFirmId == userFirmId);

var totalBankAccounts = await _context.BankAccounts
    .CountAsync(ba => ba.UserFirmId == userFirmId);
```

### Miesięczne sumy

```csharp
var monthlyTotals = await _context.Documents
    .Where(d => d.UserFirmId == userFirmId
             && d.DocumentTypeId == documentTypeId
             && d.IssueDate.Year == year)
    .GroupBy(d => d.IssueDate.Month)
    .Select(g => new MonthlyTotalDto {
        Month = g.Key,
        InvoiceAmount = g.Sum(d => d.TotalPrice),
        IncomeAmount = g.Where(d => d.DocumentStatusId == 2) // Platita
                        .Sum(d => d.TotalPrice)
    })
    .ToListAsync();
```

## Anomalie

| # | Anomalia |
|---|---|
| LQ03-01 | Miesięczne sumy zawierają tylko miesiące z dokumentami — miesiące puste pomijane; frontend musi uzupełniać 0 |
| LQ03-02 | Wiele osobnych zapytań do DB (N+1 potencjalne); brak jednego aggregate query |
| LQ03-03 | `DocumentStatusId == 2` hardkodowane — zakłada że "Platita" to zawsze status 2 |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
