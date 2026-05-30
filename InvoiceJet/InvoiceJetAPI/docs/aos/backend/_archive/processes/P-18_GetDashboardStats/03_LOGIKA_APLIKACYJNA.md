# Statystyki dashboardu — Logika aplikacyjna

## Przepływ wykonania

1. Serwis pobiera aktywną firmę użytkownika.
2. Gdy aktywna firma nie istnieje, zwraca pusty `DashboardStatsDto`.
3. Serwis oblicza:
   - `TotalDocuments` przez `GetTotalDocumentsAsync(userFirmId, year, documentType)`,
   - `TotalClients` przez `Firms.GetTotalClientsAsync(userId)`,
   - `TotalProducts` przez `Products.GetTotalProductsAsync(userFirmId)`,
   - `TotalBankAccounts` przez `BankAccounts.GetTotalBankAccountsAsync(userFirmId)`,
   - `MonthlyTotals` przez `GetMonthlyTotalsAsync(userFirmId, year, documentType)`.
4. Serwis zwraca złożony obiekt `DashboardStatsDto`.

---

## Wyliczenia miesięczne

`GetMonthlyTotalsAsync`:

- filtruje dokumenty po `UserFirmId`, roku i typie dokumentu,
- grupuje po miesiącu daty wystawienia,
- wylicza:
  - `InvoiceAmount = sum(TotalPrice)`,
  - `IncomeAmount = sum(TotalPrice)` tylko dla statusu `Paid`.
