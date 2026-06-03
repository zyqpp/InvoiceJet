# DTO: DashboardStatsDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-12 |
| Plik | `InvoiceJet.Application/DTOs/DashboardStatsDto.cs` |
| Kierunek | Response (Backend → Frontend) |
| Endpoint | `GET /api/Document/GetDashboardStats/{year}/{documentType}` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `TotalDocuments` | `int` | NIE | Łączna liczba dokumentów użytkownika |
| `TotalClients` | `int` | NIE | Łączna liczba klientów |
| `TotalProducts` | `int` | NIE | Łączna liczba produktów |
| `TotalBankAccounts` | `int` | NIE | Łączna liczba kont bankowych |
| `MonthlyTotals` | `List<MonthlyTotalDto>` | TAK | Miesięczne sumy dla wybranego roku i typu |

## MonthlyTotalDto (zagnieżdżony)

| Pole | Typ C# | Opis |
|---|---|---|
| `Month` | `int` | Numer miesiąca (1-12) |
| `InvoiceAmount` | `decimal` | Suma wartości faktur w miesiącu |
| `IncomeAmount` | `decimal` | Suma przychodów (zapłacone faktury) w miesiącu |

## Anomalia — niepełna lista miesięcy

`MonthlyTotals` zawiera **tylko miesiące z dokumentami** — puste miesiące są pomijane. Frontend musi uzupełnić brakujące miesiące (0 wartością) aby wykres liniowy był poprawny.

## Przykład JSON

```json
{
  "totalDocuments": 42,
  "totalClients": 8,
  "totalProducts": 15,
  "totalBankAccounts": 2,
  "monthlyTotals": [
    { "month": 1, "invoiceAmount": 5000.00, "incomeAmount": 4200.00 },
    { "month": 3, "invoiceAmount": 8500.00, "incomeAmount": 8500.00 },
    { "month": 5, "invoiceAmount": 12000.00, "incomeAmount": 9000.00 }
  ]
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
