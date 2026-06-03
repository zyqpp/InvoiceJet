# GetDocumentAutofillInfo — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zalogowany użytkownik z rolą `User` + JWT | seed / rejestracja | `DT-01` |
| Aktywna firma użytkownika (`UserFirm`) | `POST /api/Firm/AddFirm/false` | `DT-03` |
| Firma klienta powiązana | `POST /api/Firm/AddFirm/true` | `DT-07` |
| Seria dokumentów dla firmy i typu | `POST /api/DocumentSeries/AddDocumentSeries` | `DT-05` |

---

## 2. Dane poprawne (happy path)

### `TC-01` — Autofill dla Faktury (documentTypeId=1)

Warunki wstępne: `DT-01`, `DT-03`, `DT-07`, `DT-05`.

Żądanie:
```http
GET /api/Document/GetDocumentAutofillInfo/1
Authorization: Bearer <token>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `DocumentAutofillDto` z:
  - `clients`: lista firm klienckich użytkownika (min. 1 z `DT-07`)
  - `documentSeries`: lista serii o `DocumentTypeId=1` dla firmy (min. 1 z `DT-05`)
  - `documentStatuses`: `[{ "id": 1, "status": "Unpaid" }, { "id": 2, "status": "Paid" }]` (zawsze 2)
  - `products`: lista produktów firmy

```json
{
  "clients": [
    { "id": 5, "name": "Firma Klient SRL", "cui": "87654321", "regCom": "J40/5678/2021", "address": "STR. CLIENTULUI NR. 2", "county": "ILFOV", "city": "VOLUNTARI" }
  ],
  "documentSeries": [
    { "id": 2, "name": "2026", "currentNumber": 1, "documentType": { "id": 1, "type": "Factura" } }
  ],
  "documentStatuses": [
    { "id": 1, "status": "Unpaid" },
    { "id": 2, "status": "Paid" }
  ],
  "products": []
}
```

---

### `TC-02` — Autofill dla Proformy (documentTypeId=2) — brak serii

Warunki wstępne: `DT-01`, `DT-03` (brak serii Proforma w bazie).

Żądanie:
```http
GET /api/Document/GetDocumentAutofillInfo/2
Authorization: Bearer <token>
```

Oczekiwany rezultat:
- Status: `200 OK`
- `documentSeries`: `[]`
- Pozostałe listy: zgodnie z danymi firmy

---

## 3. Dane niepoprawne (po jednej na regułę walidacji)

### `TC-N01` — Użytkownik bez firmy ⚠️

Warunki wstępne: `DT-01` (zalogowany user bez `UserFirm`).

Żądanie:
```http
GET /api/Document/GetDocumentAutofillInfo/1
Authorization: Bearer <token>
```

Oczekiwany rezultat (faktyczne — niestandardowe):
- Status: `200 OK`
- Odpowiedź:
```json
{
  "clients": null,
  "documentSeries": null,
  "documentStatuses": null,
  "products": null
}
```

> [UWAGA: `null` zamiast `[]` dla wszystkich list. Frontend może crashować. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

### `TC-N02` — Brak JWT

Żądanie:
```http
GET /api/Document/GetDocumentAutofillInfo/1
```

Oczekiwany rezultat:
- Status: `401 Unauthorized`

---

## 4. Wartości brzegowe

| ID | Pole | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|
| `TC-B01` | `documentTypeId` | `0` | `200 OK`; `documentSeries: []` (brak serii dla type=0) |
| `TC-B02` | `documentTypeId` | `999` | `200 OK`; `documentSeries: []` |
| `TC-B03` | `documentTypeId` | `-1` | `200 OK`; `documentSeries: []` |
| `TC-B04` | Brak klientów | firma bez IsClient=true | `200 OK`; `clients: []` |
| `TC-B05` | Brak produktów | firma bez produktów | `200 OK`; `products: []` |
| `TC-B06` | `documentStatuses` | seed zawsze 2 rekordy | zawsze `[Unpaid, Paid]` niezależnie od firmy |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-01` | Zalogowany użytkownik + JWT | wszystkie TC |
| `DT-03` | Aktywna firma użytkownika (UserFirm) | `TC-01`, `TC-02`, `TC-B01`–`TC-B06` |
| `DT-05` | Seria dokumentów Faktura (DocumentTypeId=1) | `TC-01` |
| `DT-07` | Firma klienta „Firma Klient SRL" | `TC-01` |
