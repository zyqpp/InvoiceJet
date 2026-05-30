# GetDocuments — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zalogowany użytkownik z rolą `User` + JWT | seed / rejestracja | `DT-01` |
| Aktywna firma użytkownika (`UserFirm`) | `POST /api/Firm/AddFirm/false` | `DT-03` |
| Firma klienta powiązana z UserFirm | `POST /api/Firm/AddFirm/true` | `DT-07` |
| Istniejący dokument (faktura) | `POST /api/Document/AddDocument` | `DT-08` |

---

## 2. Dane poprawne (happy path)

### `TC-01` — Lista dokumentów według typu (Faktura)

Warunki wstępne: `DT-01`, `DT-03`, `DT-07`, `DT-08`.

Żądanie:
```http
GET /api/Document/GetDocumentTableRecords/1
Authorization: Bearer <token>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: tablica `DocumentTableRecordDto` z przynajmniej jednym elementem
- Każdy element zawiera: `id`, `documentNumber`, `clientName`, `issueDate`, `dueDate`, `totalValue`, `documentStatus`
- Brak dokumentów innych użytkowników

```json
[
  {
    "id": 3,
    "documentNumber": "20260001",
    "clientName": "Firma Klient SRL",
    "issueDate": "2026-05-30T00:00:00",
    "dueDate": "2026-06-30T00:00:00",
    "totalValue": 595.00,
    "documentStatus": { "id": 1, "status": "Unpaid" }
  }
]
```

---

### `TC-02` — Lista dokumentów według typu Proforma (pusty wynik)

Warunki wstępne: `DT-01`, `DT-03` (brak dokumentów Proforma w bazie).

Żądanie:
```http
GET /api/Document/GetDocumentTableRecords/2
Authorization: Bearer <token>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `[]`

---

### `TC-03` — Pobranie dokumentu po Id

Warunki wstępne: `DT-01`, `DT-03`, `DT-07`, `DT-08` (dokument o `id=3`).

Żądanie:
```http
GET /api/Document/GetDocumentById/3
Authorization: Bearer <token>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: obiekt `DocumentRequestDto` z zagnieżdżonymi `products`, `documentStatus`, `client`
- Pole `seller` = `null` (brak Include `UserFirm` w `GetDocumentWithAllInfo`)

```json
{
  "id": 3,
  "documentNumber": "20260001",
  "seller": null,
  "client": {
    "id": 5,
    "name": "Firma Klient SRL",
    "cui": "87654321",
    "regCom": "J40/5678/2021",
    "address": "STR. CLIENTULUI NR. 2",
    "county": "ILFOV",
    "city": "VOLUNTARI"
  },
  "issueDate": "2026-05-30T00:00:00",
  "dueDate": "2026-06-30T00:00:00",
  "bankAccount": null,
  "documentSeries": null,
  "documentType": null,
  "documentStatus": { "id": 1, "status": "Unpaid" },
  "products": [
    {
      "id": 1,
      "name": "Consultanță IT",
      "unitPrice": 500.00,
      "totalPrice": 595.00,
      "containsTva": false,
      "unitOfMeasurement": "ora",
      "tvaValue": 19,
      "quantity": 1
    }
  ]
}
```

---

## 3. Dane niepoprawne (po jednej na regułę walidacji)

Brak reguł WAL w procesie P-14. Poniżej zachowania dla przypadków brzegowych bezpieczeństwa:

### `TC-N01` — Nieistniejące `documentId` ⚠️

Warunki wstępne: `DT-01`.

Żądanie:
```http
GET /api/Document/GetDocumentById/999999
Authorization: Bearer <token>
```

Oczekiwany rezultat (faktyczne, niestandardowe):
- Status: `200 OK`
- Odpowiedź: `null`

> [UWAGA: Zamiast `404 Not Found`, serwer zwraca `200 OK null`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

### `TC-N02` — Brak JWT (nieautoryzowany)

Żądanie:
```http
GET /api/Document/GetDocumentTableRecords/1
```

Oczekiwany rezultat:
- Status: `401 Unauthorized`

---

### `TC-N03` — Odczyt dokumentu cudzego użytkownika ⚠️

Warunki wstępne: `DT-01` (user A), `DT-01` (user B, osobna rejestracja), dokument należący do user B o `id=7`.

Żądanie (wysyłane przez user A z własnym JWT):
```http
GET /api/Document/GetDocumentById/7
Authorization: Bearer <token-user-A>
```

Oczekiwany rezultat (faktyczne, błąd bezpieczeństwa):
- Status: `200 OK`
- Odpowiedź: pełen obiekt dokumentu użytkownika B

> [UWAGA: Brak ownership check — `GetDocumentById` nie weryfikuje `UserFirmId`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 4. Wartości brzegowe

| ID | Pole | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|
| `TC-B01` | `documentTypeId` | `0` (nieistniejący typ) | `200 OK []` — filtrowanie po `DocumentTypeId=0` zwraca pustą listę |
| `TC-B02` | `documentTypeId` | `999` (nieistniejący typ) | `200 OK []` |
| `TC-B03` | `documentTypeId` | `-1` (ujemny) | `200 OK []` |
| `TC-B04` | `documentId` | `0` | `200 OK null` (no 404) |
| `TC-B05` | `documentId` | `-1` | `200 OK null` (no 404) |
| `TC-B06` | Użytkownik bez firmy | `GetUserFirmAsync` = null | `GET /GetDocumentTableRecords/1` → `200 OK []` |
| `TC-B07` | Konto z firmą, ale zero dokumentów | pusta tabela `Document` | `200 OK []` |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-01` | Zalogowany użytkownik + JWT | `TC-01`–`TC-03`, `TC-N01`–`TC-N03`, `TC-B01`–`TC-B07` |
| `DT-03` | Aktywna firma użytkownika (UserFirm) | `TC-01`–`TC-03`, `TC-B06`, `TC-B07` |
| `DT-07` | Firma klienta „Firma Klient SRL" | `TC-01`, `TC-03` |
| `DT-08` | Istniejący dokument faktury `id=3` | `TC-01`, `TC-03`, `TC-N03` |
