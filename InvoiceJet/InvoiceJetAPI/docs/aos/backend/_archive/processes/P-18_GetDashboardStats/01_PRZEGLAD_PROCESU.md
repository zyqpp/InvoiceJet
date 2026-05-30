# Statystyki dashboardu — Przegląd procesu

## Cel

Proces zwraca agregaty statystyczne dashboardu dla podanego roku i typu dokumentu: liczbę dokumentów, klientów, produktów, kont bankowych oraz miesięczne sumy.

---

## Diagram

```mermaid
flowchart TD
  A["GET /api/Document/GetDashboardStats/{year}/{documentType}"] --> B["DocumentService.GetDashboardStats()"]
  B --> C["Users.GetUserFirmAsync(currentUserId)"]
  C --> D{"Aktywna firma istnieje"}
  D -->|nie| E["Zwróć nowy DashboardStatsDto()"]
  D -->|tak| F["GetTotalDocumentsAsync(...)"]
  D --> G["_unitOfWork.Firms.GetTotalClientsAsync(...)"]
  D --> H["_unitOfWork.Products.GetTotalProductsAsync(...)"]
  D --> I["_unitOfWork.BankAccounts.GetTotalBankAccountsAsync(...)"]
  D --> J["GetMonthlyTotalsAsync(...)"]
  F --> K["Złożenie DashboardStatsDto"]
  G --> K
  H --> K
  I --> K
  J --> K
  K --> L["HTTP 200 OK"]
```
