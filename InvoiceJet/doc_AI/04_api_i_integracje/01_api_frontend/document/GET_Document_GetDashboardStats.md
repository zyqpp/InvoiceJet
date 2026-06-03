# GET /api/Document/GetDashboardStats/{year}/{documentType} — Statystyki dashboardu

| Atrybut | Wartość |
|---|---|
| ID | API-30 |
| Metoda | GET |
| URL | `/api/Document/GetDashboardStats/{year}/{documentType}` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentController.GetDashboardStats` |
| Serwis | `IDocumentService.GetDashboardStats` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Path Parameters

| Parametr | Typ | Opis |
|---|---|---|
| `year` | `int` | Rok (np. `2026`) |
| `documentType` | `int` | `1=Faktura`, `2=Proforma`, `3=Storno` |

**Przykład:** `GET /api/Document/GetDashboardStats/2026/1`

## Response

### 200 OK — `DashboardStatsDto`

```json
{
  "totalDocuments": 15,
  "totalClients": 8,
  "totalProducts": 12,
  "totalBankAccounts": 2,
  "monthlyTotals": [
    { "month": 1, "invoiceAmount": 5000.00, "incomeAmount": 3000.00 },
    { "month": 3, "invoiceAmount": 8000.00, "incomeAmount": 8000.00 }
  ]
}
```

**Uwagi:**
- `monthlyTotals` zawiera tylko miesiące z dokumentami (brak wypełnienia zerami dla pustych miesięcy)
- `invoiceAmount` = suma `TotalPrice` wszystkich faktur danego miesiąca
- `incomeAmount` = suma `TotalPrice` tylko **opłaconych** faktur (`DocumentStatusId == 2`)

### 200 OK — brak aktywnej firmy

```json
{ "totalDocuments": 0, "totalClients": 0, "totalProducts": 0, "totalBankAccounts": 0, "monthlyTotals": [] }
```

## Zachowanie po stronie frontendu

`DashboardComponent` wywoływany przy `onSelectionChange()` (zmiana roku lub typu dokumentu). Dane zasilają wykres liniowy Chart.js (ng2-charts). Zawiera `console.log(invoiceAmounts)` i `console.log(incomeAmounts)`.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
