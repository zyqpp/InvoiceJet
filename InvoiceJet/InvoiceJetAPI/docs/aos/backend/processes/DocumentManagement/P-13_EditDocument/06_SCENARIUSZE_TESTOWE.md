# EditDocument — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zarejestrowany użytkownik + JWT | rejestracja / logowanie | `DT-01`, `DT-02` |
| Aktywna firma + 3 serie + aktywne konto bankowe | firma + konto | `DT-03`, `DT-05` |
| Firma klienta (IsClient=true) | `POST /api/Firm/AddFirm/true` | `DT-07` |
| Istniejący dokument w DB | `POST /api/Document/AddDocument` (TC-01 z P-12) | `DT-08` (nowy) |

---

## 2. Dane poprawne (happy path)

### `TC-01` — Zmiana statusu dokumentu na Paid

Warunki wstępne: `DT-01`, `DT-02`, `DT-03`, `DT-05`, `DT-07`, `DT-08`.

Żądanie:
```
PUT /api/Document/EditDocument
Authorization: Bearer <jwt_DT-02>
Content-Type: application/json
```
```json
{
  "id": <Id_DT-08>,
  "documentNumber": "20260001",
  "seller": null,
  "client": { "id": <clientId_DT-07>, "name": "Firma Klient SRL", "cui": "87654321", "regCom": "J40/5678/2021", "address": "STR. CLIENTULUI NR. 2", "county": "ILFOV", "city": "VOLUNTARI" },
  "issueDate": "2026-05-30T00:00:00",
  "dueDate": "2026-06-30T00:00:00",
  "bankAccount": null,
  "documentSeries": null,
  "documentType": { "id": 1, "name": "Factura" },
  "documentStatus": { "id": 2, "status": "Paid" },
  "products": [
    { "id": 0, "name": "Consultanță IT", "unitPrice": 500.00, "totalPrice": 595.00, "containsTva": false, "unitOfMeasurement": "ora", "tvaValue": 19, "quantity": 1 }
  ]
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Skutek w bazie: `Document.DocumentStatusId = 2` (Paid); stary `DocumentProduct` usunięty; nowy `DocumentProduct` + nowy `Product` ("Consultanță IT") utworzone; `UnitPrice=500`, `TotalPrice=595`

---

## 3. Dane niepoprawne

### `TC-N01` — łamie `WAL-01`: brak firmy

Warunki wstępne: `DT-01`, `DT-02` (bez `DT-03`).
Żądanie: jak TC-01 (dowolny `id` dokumentu).
Oczekiwany rezultat: `400`, `{ "message": "User has no associated firm." }`

### `TC-N02` — łamie `WAL-02`: nieistniejący dokument

Warunki wstępne: `DT-01`, `DT-02`, `DT-03`.
Żądanie: jak TC-01 ale `"id": 99999`.
Oczekiwany rezultat: `500`, `{ "message": "Document not found." }`

### `TC-N03` — łamie `WAL-03`: produkt Id>0 z błędną nazwą

Warunki wstępne: `DT-01`, `DT-02`, `DT-03`, `DT-05`, `DT-07`, `DT-08`.
Żądanie: jak TC-01 ale w products `"id": <Id_DT-04>, "name": "ZŁA NAZWA"`.
Oczekiwany rezultat: `500`, `{ "message": "Product not found." }`

---

## 4. Wartości brzegowe

| ID | Pole | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|
| `TC-B01` | `documentStatus` | `null` | `200 OK`; `Document.DocumentStatusId = null` (nullable FK) |
| `TC-B02` | `products` | `[]` | `200 OK`; stare `DocumentProduct` usunięte; `UnitPrice=0`, `TotalPrice=0` |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-01`–`DT-03` | Użytkownik + JWT + firma | Wszystkie TC |
| `DT-05` | Aktywne konto bankowe | TC-01, TC-N03 |
| `DT-07` | Firma klienta | TC-01, TC-N03 |
| `DT-08` | Istniejący dokument do edycji | TC-01, TC-N02, TC-N03 |

---

## Definicja fixture'u `DT-08`

**Cel:** Dokument (faktura) gotowy do edycji.

**Precondition:** `DT-03`, `DT-05`, `DT-07`.

**Sposób przygotowania:** `POST /api/Document/AddDocument` jak w `P-12 TC-01`.

**Oczekiwany stan bazy:**
```
Document: Id=<generowany>, DocumentNumber="2026000N", DocumentStatusId=1 (Unpaid)
DocumentProduct: N rekordów powiązanych
DocumentSeries.CurrentNumber: +1
```

**Sprzątanie:** `PUT /api/Document/DeleteDocuments` z body `[<Id>]`.

**Zależności:** `DT-01`, `DT-02`, `DT-03`, `DT-05`, `DT-07`.
