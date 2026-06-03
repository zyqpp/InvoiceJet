# GetDocuments — Kontrakt API

---

## `API-24` — GET /api/Document/GetDocumentTableRecords/{documentTypeId}

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Document/GetDocumentTableRecords/{documentTypeId}` |
| Kontroler | `DocumentController.cs › DocumentController.GetDocumentTableRecords` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

### Parametry trasy

| Parametr | Typ | Źródło | Opis |
|---|---|---|---|
| `documentTypeId` | `int` | `[FromRoute]` | Id typu dokumentu: 1=Factura, 2=Factura Proforma, 3=Factura Storno |

### Ciało żądania

Brak.

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `List<DocumentTableRecordDto>` | Powodzenie; `[]` gdy brak firmy lub brak dokumentów |
| `401 Unauthorized` | — | Brak tokenu |
| `403 Forbidden` | — | Brak roli `User` |

Przykład odpowiedzi (`200 OK`):
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

## `API-25` — GET /api/Document/GetDocumentById/{documentId}

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Document/GetDocumentById/{documentId}` |
| Kontroler | `DocumentController.cs › DocumentController.GetDocumentById` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

### Parametry trasy

| Parametr | Typ | Źródło | Opis |
|---|---|---|---|
| `documentId` | `int` | `[FromRoute]` | Id dokumentu |

### Ciało żądania

Brak.

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `DocumentRequestDto` | Powodzenie |
| `200 OK` | `null` | Dokument o danym Id nie istnieje (brak `404`) ⚠️ |
| `401 Unauthorized` | — | Brak tokenu |
| `403 Forbidden` | — | Brak roli `User` |

> [UWAGA: Nieistniejący `documentId` → `200 OK null` zamiast `404 Not Found`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

Przykład odpowiedzi (`200 OK`):
```json
{
  "id": 3,
  "documentNumber": "20260001",
  "seller": null,
  "client": { "id": 5, "name": "Firma Klient SRL", "cui": "87654321", "regCom": "J40/5678/2021", "address": "STR. CLIENTULUI NR. 2", "county": "ILFOV", "city": "VOLUNTARI" },
  "issueDate": "2026-05-30T00:00:00",
  "dueDate": "2026-06-30T00:00:00",
  "bankAccount": null,
  "documentSeries": null,
  "documentType": null,
  "documentStatus": { "id": 1, "status": "Unpaid" },
  "products": [
    { "id": 1, "name": "Consultanță IT", "unitPrice": 500.00, "totalPrice": 595.00, "containsTva": false, "unitOfMeasurement": "ora", "tvaValue": 19, "quantity": 1 }
  ]
}
```
