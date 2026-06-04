# ManageDocumentPdf — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zalogowany użytkownik z rolą `User` + JWT | seed / rejestracja | `DT-01` |
| Aktywna firma użytkownika (`UserFirm`) | `POST /api/Firm/AddFirm/false` | `DT-03` |
| Firma klienta | `POST /api/Firm/AddFirm/true` | `DT-07` |
| Seria dokumentów (dla numeru PDF) | `POST /api/DocumentSeries/AddDocumentSeries` | `DT-05` |
| Dokument (dla API-29 — konto bankowe z dokumentu) | `POST /api/Document/AddDocument` | `DT-08` |

---

## 2. Dane poprawne (happy path)

### `TC-01` — Generowanie PDF na dysk (API-28)

Warunki wstępne: `DT-01`, `DT-03`, `DT-07`, `DT-05`.

Żądanie:
```http
POST /api/Document/GenerateDocumentPdf
Authorization: Bearer <token>
Content-Type: application/json

{
  "id": 3,
  "documentNumber": "20260001",
  "seller": null,
  "client": { "id": 5, "name": "Firma Klient SRL", "cui": "87654321", "regCom": "J40/5678/2021", "address": "STR. CLIENTULUI NR. 2", "county": "ILFOV", "city": "VOLUNTARI" },
  "issueDate": "2026-05-30T00:00:00",
  "dueDate": "2026-06-30T00:00:00",
  "bankAccount": null,
  "documentSeries": { "id": 2, "name": "2026", "currentNumber": 1, "documentType": null },
  "documentType": { "id": 1, "type": "Factura" },
  "documentStatus": { "id": 1, "status": "Unpaid" },
  "products": [
    { "id": 1, "name": "Consultanță IT", "unitPrice": 500.00, "totalPrice": 595.00, "containsTva": false, "unitOfMeasurement": "ora", "tvaValue": 19, "quantity": 1 }
  ]
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Body: puste
- Skutek na dysku: plik `Documents/Invoice_20260001.pdf` (lub `Invoice_1.pdf` gdy brak DocumentNumber) zapisany na serwerze

---

### `TC-02` — Pobranie PDF jako strumień (API-29)

Warunki wstępne: `DT-01`, `DT-03`, `DT-07`, `DT-05`, `DT-08`.

Żądanie:
```http
POST /api/Document/GetInvoicePdfStream
Authorization: Bearer <token>
Content-Type: application/json

(identyczny body jak TC-01)
```

Oczekiwany rezultat:
- Status: `200 OK`
- Content-Type: `application/pdf`
- Content-Disposition: `attachment; filename="Invoice_20260001.pdf"`
- Body: bajty PDF

---

## 3. Dane niepoprawne (po jednej na regułę walidacji)

### `TC-N01` — łamie WAL-01A/WAL-01B: użytkownik bez firmy

Warunki wstępne: `DT-01` (user bez `UserFirm`).

Żądanie (dla API-28):
```http
POST /api/Document/GenerateDocumentPdf
Authorization: Bearer <token>
Content-Type: application/json

{ ...DocumentRequestDto... }
```

Oczekiwany rezultat (API-28 — przez kontrolerowy catch):
- Status: `400 Bad Request`
- Body: `User has no associated firm.` (plain string)

Oczekiwany rezultat (API-29 — przez ExceptionMiddleware):
- Status: `400 Bad Request`
- Body: `{ "message": "User has no associated firm." }`

> ⚠️ Różna struktura odpowiedzi błędu w zależności od endpointu (API-28: string; API-29: JSON).

---

### `TC-N02` — łamie WAL-02B: błąd generowania PDF (API-29)

Warunki wstępne: `DT-01`, `DT-03` (PdfGenerationService zwraca null — np. błąd fabryki).

Oczekiwany rezultat:
- Status: `400 Bad Request`
- Body: `Failed to generate the PDF document.`

---

## 4. Wartości brzegowe

| ID | Pole | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|
| `TC-B01` | `documentNumber` | `null` + `documentSeries` z `currentNumber=1` | PDF nazwany `Invoice_1.pdf` |
| `TC-B02` | `documentNumber` | `null` + `documentSeries = null` | API-29: `NullReferenceException → 500` (`DocumentSeries!` null forgiving) |
| `TC-B03` | `documentType` | `null` | API-29: błąd w `DocumentFactoryProvider` → `PdfContent = null` → `400 Bad Request` |
| `TC-B04` | `products` | `[]` (pusta lista) | `200 OK`; PDF z pustą tabelą pozycji |
| `TC-B05` | Brak dokumentów w firmie (API-29) | `Documents.Query()` pusta | `documentBankAccount = null`; PDF bez konta bankowego |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-01` | Zalogowany użytkownik + JWT | wszystkie TC |
| `DT-03` | Aktywna firma użytkownika | `TC-01`, `TC-02`, `TC-B01`–`TC-B05` |
| `DT-05` | Seria dokumentów Faktura | `TC-01`, `TC-02`, `TC-B01` |
| `DT-07` | Firma klienta | `TC-01`, `TC-02` |
| `DT-08` | Istniejący dokument (konto bankowe dla API-29) | `TC-02` |
