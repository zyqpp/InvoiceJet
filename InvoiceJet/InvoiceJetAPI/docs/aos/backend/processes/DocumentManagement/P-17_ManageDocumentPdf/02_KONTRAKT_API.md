# ManageDocumentPdf — Kontrakt API

---

## `API-28` — POST /api/Document/GenerateDocumentPdf

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/Document/GenerateDocumentPdf` |
| Kontroler | `DocumentController.cs › DocumentController.GenerateDocument` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

### Parametry trasy

Brak.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `DocumentRequestDto` | `[FromBody]` (implicit) |

Przykład żądania:
```json
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

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | puste body | PDF zapisany na dysku (lub błąd zapisu połknięty przez PdfGenerationService ⚠️) |
| `400 Bad Request` | `string` | Wyjątek złapany przez kontrolerowy try/catch (w tym `UserHasNoAssociatedFirmException`) |
| `401 Unauthorized` | — | Brak tokenu |
| `403 Forbidden` | — | Brak roli `User` |

Przykład odpowiedzi sukcesu (`200 OK`): puste body.

Przykład odpowiedzi błędu (`400 Bad Request`):
```
User has no associated firm.
```

> ⚠️ Kontroler ma własny `try/catch` — wyjątki są zwracane jako `BadRequest(ex.Message)` z pominięciem `ExceptionMiddleware`. PDF zapisywany pod ścieżką `<BaseDir>/Documents/Invoice_<CurrentNumber>.pdf`.

---

## `API-29` — POST /api/Document/GetInvoicePdfStream

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/Document/GetInvoicePdfStream` |
| Kontroler | `DocumentController.cs › DocumentController.GetInvoicePdfStream` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

### Parametry trasy

Brak.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `DocumentRequestDto` | `[FromBody]` (implicit) |

Przykład żądania: identyczny jak API-28.

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `application/pdf` (binary) | PDF wygenerowany pomyślnie |
| `400 Bad Request` | `string` | `PdfContent == null` (błąd generowania) lub `UserHasNoAssociatedFirmException` (przez middleware) |
| `401 Unauthorized` | — | Brak tokenu |
| `403 Forbidden` | — | Brak roli `User` |
| `500 Internal Server Error` | — | Niezmapowany wyjątek |

Przykład odpowiedzi sukcesu (`200 OK`):
- Content-Type: `application/pdf`
- Content-Disposition: `attachment; filename="Invoice_20260001.pdf"`
- Body: bajty pliku PDF

Przykład odpowiedzi błędu (`400 Bad Request`):
```
Failed to generate the PDF document.
```
