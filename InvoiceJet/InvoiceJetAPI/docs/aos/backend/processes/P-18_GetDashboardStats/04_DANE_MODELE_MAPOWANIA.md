# Statystyki dashboardu — Dane, modele i mapowania

## DTO

| DTO | Rola |
|---|---|
| `DashboardStatsDto` | Agregat danych statystycznych. |
| `MonthlyTotalDto` | Agregat miesięczny. |

---

## Źródła danych

| Wartość | Źródło |
|---|---|
| `TotalDocuments` | `Documents.Query().CountAsync(...)` |
| `TotalClients` | `FirmRepository.GetTotalClientsAsync(userId)` |
| `TotalProducts` | `ProductRepository.GetTotalProductsAsync(userFirmId)` |
| `TotalBankAccounts` | `BankAccountRepository.GetTotalBankAccountsAsync(userFirmId)` |
| `MonthlyTotals` | Grupowanie dokumentów w `GetMonthlyTotalsAsync` |
