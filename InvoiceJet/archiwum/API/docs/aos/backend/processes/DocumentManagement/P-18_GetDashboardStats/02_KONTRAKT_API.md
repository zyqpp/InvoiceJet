# GetDashboardStats — Kontrakt API

---

## `API-30` — GET /api/Document/GetDashboardStats/{year}/{documentType}

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Document/GetDashboardStats/{year}/{documentType}` |
| Kontroler | `DocumentController.cs › DocumentController.GetDashboardStats` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

### Parametry trasy

| Parametr | Typ | Źródło | Opis |
|---|---|---|---|
| `year` | `int` | `[FromRoute]` | Rok wystawienia dokumentów (np. `2026`) |
| `documentType` | `int` | `[FromRoute]` | Id typu dokumentu: 1=Faktura, 2=Proforma, 3=Storno |

### Ciało żądania

Brak.

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `DashboardStatsDto` | Powodzenie; zera i `null` MonthlyTotals gdy brak firmy |
| `401 Unauthorized` | — | Brak tokenu |
| `403 Forbidden` | — | Brak roli `User` |

Przykład odpowiedzi (`200 OK` — firma z dokumentami):
```json
{
  "totalDocuments": 5,
  "totalClients": 3,
  "totalProducts": 8,
  "totalBankAccounts": 1,
  "monthlyTotals": [
    { "month": 1, "invoiceAmount": 1200.00, "incomeAmount": 595.00 },
    { "month": 5, "invoiceAmount": 595.00, "incomeAmount": 0.00 }
  ]
}
```

> `monthlyTotals` zawiera tylko miesiące z dokumentami (nie 12 wierszy). Brakujące miesiące = brak obrotów.

Przykład odpowiedzi (`200 OK` — brak firmy ⚠️):
```json
{
  "totalDocuments": 0,
  "totalClients": 0,
  "totalProducts": 0,
  "totalBankAccounts": 0,
  "monthlyTotals": null
}
```
