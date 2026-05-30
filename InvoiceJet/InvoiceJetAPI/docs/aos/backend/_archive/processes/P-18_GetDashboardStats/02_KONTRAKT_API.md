# Statystyki dashboardu — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Document/GetDashboardStats/{year}/{documentType}` |
| Parametry | `year: int`, `documentType: int` |
| Odpowiedź | `DashboardStatsDto` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

---

## Odpowiedź `DashboardStatsDto`

| Pole | Typ |
|---|---|
| `totalDocuments` | `int` |
| `totalClients` | `int` |
| `totalProducts` | `int` |
| `totalBankAccounts` | `int` |
| `monthlyTotals` | `List<MonthlyTotalDto>` |
