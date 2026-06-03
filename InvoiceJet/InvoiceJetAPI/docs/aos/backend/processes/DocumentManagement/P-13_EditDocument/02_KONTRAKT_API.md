# EditDocument — Kontrakt API

---

## `API-23` — PUT /api/Document/EditDocument

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/Document/EditDocument` |
| Kontroler | `DocumentController.cs › DocumentController.EditDocument` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `DocumentController`) |

### Parametry trasy / zapytania

Brak. `Id` dokumentu przekazywany w body.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `DocumentRequestDto` | inferred from body |

Przykład żądania — edycja istniejącego dokumentu (zmiana statusu na Paid, zmiana produktów):
```json
{
  "id": 3,
  "documentNumber": "20260003",
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
  "documentType": {
    "id": 1,
    "name": "Factura"
  },
  "documentStatus": {
    "id": 2,
    "status": "Paid"
  },
  "products": [
    {
      "id": 7,
      "name": "Usługa konsultingowa",
      "unitPrice": 500.00,
      "totalPrice": 595.00,
      "containsTva": false,
      "unitOfMeasurement": "ora",
      "tvaValue": 19,
      "quantity": 2
    }
  ]
}
```

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `DocumentRequestDto` | Dokument zaktualizowany |
| `400 Bad Request` | `{ "message": "User has no associated firm." }` | Brak aktywnej firmy (WAL-01) |
| `500 Internal Server Error` | `{ "message": "Document not found." }` | Dokument o danym `Id` nie istnieje (WAL-02) ⚠️ |
| `500 Internal Server Error` | `{ "message": "Product not found." }` | Produkt nie znaleziony po `Name+UserFirmId` (WAL-03) ⚠️ |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

Przykład odpowiedzi (`200 OK`): oryginalny DTO z żądania (bez remapowania z DB).

> [UWAGA: `500` dla WAL-02 i WAL-03 zamiast `404`/`400`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
