# GET /api/Document/GetDocumentById/{documentId} — Pobieranie dokumentu

| Atrybut | Wartość |
|---|---|
| ID | API-25 |
| Metoda | GET |
| URL | `/api/Document/GetDocumentById/{documentId}` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentController.GetDocumentById` |
| Serwis | `IDocumentService.GetDocumentById` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Path Parameters

| Parametr | Typ | Opis |
|---|---|---|
| `documentId` | `int` | ID dokumentu |

## Response

### 200 OK — pełny `DocumentRequestDto`

```json
{
  "id": 1,
  "documentNumber": "FV0001",
  "seller": {
    "id": 42,
    "name": "My Company SRL",
    "cui": "12345678",
    "regCom": "J12/345/2020",
    "address": "STR. EXAMPLE 1",
    "county": "BUCURESTI",
    "city": "SECTOR 1"
  },
  "client": { "id": 10, "name": "Client SRL", ... },
  "issueDate": "2026-05-31T00:00:00",
  "dueDate": "2026-06-14T00:00:00",
  "bankAccount": { "id": 1, "bankName": "BRD", "iban": "RO49...", "currency": 0, "isActive": true },
  "documentSeries": { "id": 1, "seriesName": "FV", ... },
  "documentType": { "id": 1, "name": "Factura" },
  "documentStatus": { "id": 1, "status": "Unpaid" },
  "products": [
    {
      "id": 5,
      "name": "Consulting Services",
      "unitPrice": 100.00,
      "totalPrice": 119.00,
      "containsTva": true,
      "unitOfMeasurement": "hr",
      "tvaValue": 19,
      "quantity": 1
    }
  ]
}
```

**Mapowanie:** `Document.UserFirm.Firm → Seller`, inline LINQ projection dla `products` (AutoMapper DocumentProfile).

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
