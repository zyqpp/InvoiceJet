# GetDashboardStats — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zalogowany użytkownik z rolą `User` + JWT | seed / rejestracja | `DT-01` |
| Aktywna firma użytkownika (`UserFirm`) | `POST /api/Firm/AddFirm/false` | `DT-03` |
| Firma klienta | `POST /api/Firm/AddFirm/true` | `DT-07` |
| Dokument (faktura) z 2026 roku | `POST /api/Document/AddDocument` | `DT-08` |

---

## 2. Dane poprawne (happy path)

### `TC-01` — Statystyki dla Faktury w 2026

Warunki wstępne: `DT-01`, `DT-03`, `DT-07`, `DT-08`.

Żądanie:
```http
GET /api/Document/GetDashboardStats/2026/1
Authorization: Bearer <token>
```

Oczekiwany rezultat:
- Status: `200 OK`
- `totalDocuments`: liczba faktur z 2026 roku (min. 1 z DT-08)
- `totalClients`: 1 (Firma Klient SRL z DT-07)
- `monthlyTotals`: min. 1 element dla maja 2026

```json
{
  "totalDocuments": 1,
  "totalClients": 1,
  "totalProducts": 0,
  "totalBankAccounts": 1,
  "monthlyTotals": [
    { "month": 5, "invoiceAmount": 595.00, "incomeAmount": 0.00 }
  ]
}
```

---

### `TC-02` — Statystyki dla Proformy (brak dokumentów)

Warunki wstępne: `DT-01`, `DT-03`.

Żądanie:
```http
GET /api/Document/GetDashboardStats/2026/2
Authorization: Bearer <token>
```

Oczekiwany rezultat:
- Status: `200 OK`
- `totalDocuments`: `0`
- `monthlyTotals`: `[]`

---

### `TC-03` — Statystyki dla roku bez dokumentów

Warunki wstępne: `DT-01`, `DT-03`.

Żądanie:
```http
GET /api/Document/GetDashboardStats/2025/1
Authorization: Bearer <token>
```

Oczekiwany rezultat:
- Status: `200 OK`
- `totalDocuments`: `0`
- `monthlyTotals`: `[]`

---

## 3. Dane niepoprawne

### `TC-N01` — Użytkownik bez firmy

Warunki wstępne: `DT-01` (user bez `UserFirm`).

Żądanie:
```http
GET /api/Document/GetDashboardStats/2026/1
Authorization: Bearer <token>
```

Oczekiwany rezultat (faktyczne — zerowy DTO):
```json
{
  "totalDocuments": 0,
  "totalClients": 0,
  "totalProducts": 0,
  "totalBankAccounts": 0,
  "monthlyTotals": null
}
```

---

### `TC-N02` — Brak JWT

Żądanie:
```http
GET /api/Document/GetDashboardStats/2026/1
```

Oczekiwany rezultat:
- Status: `401 Unauthorized`

---

## 4. Wartości brzegowe

| ID | Pole | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|
| `TC-B01` | `year` | `0` | `200 OK`; `totalDocuments=0`, `monthlyTotals=[]` |
| `TC-B02` | `year` | `9999` | `200 OK`; `totalDocuments=0`, `monthlyTotals=[]` |
| `TC-B03` | `documentType` | `0` (nieistniejący typ) | `200 OK`; `totalDocuments=0`, `monthlyTotals=[]` |
| `TC-B04` | `documentType` | `999` | `200 OK`; `totalDocuments=0`, `monthlyTotals=[]` |
| `TC-B05` | Dokument z `DocumentStatusId=2` (Paid) | DT-08 zmieniony na Paid | `incomeAmount` = wartość dokumentu |
| `TC-B06` | `monthlyTotals` | dokumenty w różnych miesiącach | tylko miesiące z dokumentami (nie 12) |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-01` | Zalogowany użytkownik + JWT | wszystkie TC |
| `DT-03` | Aktywna firma użytkownika | `TC-01`–`TC-03`, `TC-B01`–`TC-B06` |
| `DT-07` | Firma klienta | `TC-01` |
| `DT-08` | Istniejący dokument faktury (rok 2026) | `TC-01`, `TC-B05`, `TC-B06` |
