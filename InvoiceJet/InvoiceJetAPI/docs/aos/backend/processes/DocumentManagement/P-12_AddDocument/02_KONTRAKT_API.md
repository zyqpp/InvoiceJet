# AddDocument — Kontrakt API

---

## `API-22` — POST /api/Document/AddDocument

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/Document/AddDocument` |
| Kontroler | `DocumentController.cs › DocumentController.AddDocument` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `DocumentController`) |

### Parametry trasy / zapytania

Brak parametrów trasy / zapytania. Tożsamość użytkownika pochodzi z JWT claim `userId`.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `DocumentRequestDto` | inferred from body (brak explicit `[FromBody]`) |

Pola wymagane w żądaniu:
- `client.id` — Id firmy klienta (musi istnieć w DB jako firma klienta użytkownika)
- `issueDate` — data wystawienia
- `documentSeries.id` — Id serii (musi istnieć; używany do inkrementacji)
- `documentSeries.seriesName` + `documentSeries.currentNumber` — składowe `DocumentNumber`
- `documentSeries.documentType.id` — typ dokumentu (1=Factura, 2=Factura Proforma, 3=Factura Storno)
- `products` — co najmniej jeden element z `name`, `unitPrice`, `totalPrice`, `quantity`

Przykład żądania — faktura z jednym nowym produktem (`id=0`) i jednym istniejącym (`id>0`):
```json
{
  "id": 0,
  "documentNumber": null,
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
  "documentSeries": {
    "id": 1,
    "seriesName": "2026",
    "firstNumber": 1,
    "currentNumber": 3,
    "isDefault": true,
    "documentTypeId": 1,
    "documentType": {
      "id": 1,
      "name": "Factura"
    }
  },
  "documentType": null,
  "documentStatus": null,
  "products": [
    {
      "id": 0,
      "name": "Consultanță IT",
      "unitPrice": 500.00,
      "totalPrice": 595.00,
      "containsTva": false,
      "unitOfMeasurement": "ora",
      "tvaValue": 19,
      "quantity": 1
    },
    {
      "id": 7,
      "name": "Usługa konsultingowa",
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

> **Uwaga:** Pole `seller` jest ignorowane przez serwis przy AddDocument. Pole `bankAccount` jest ignorowane — serwis automatycznie pobiera aktywne konto bankowe. Pole `documentNumber` jest ignorowane — wyliczany przez serwis.

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `DocumentRequestDto` | Dokument wystawiony |
| `400 Bad Request` | `{ "message": "User has no associated firm." }` | Brak aktywnej firmy (WAL-01) |
| `400 Bad Request` | `{ "message": "Please add a bank account, before generating a document." }` | Brak aktywnego konta bankowego (WAL-02) |
| `500 Internal Server Error` | `{ "message": "Product not found." }` | Produkt o `Id > 0` nie znaleziony po `Name+UserFirmId` (WAL-03) ⚠️ |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

Przykład odpowiedzi (`200 OK`) — **oryginalny DTO żądania bez modyfikacji**:
```json
{
  "id": 0,
  "documentNumber": null,
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
  "documentSeries": { "id": 1, "seriesName": "2026", "currentNumber": 3, "..." },
  "documentType": null,
  "documentStatus": null,
  "products": [ "..." ]
}
```

> [UWAGA: Odpowiedź `200 OK` zawiera **oryginalny obiekt żądania** (pole `id=0`), nie encję z DB. Klient nie zna `Id` nowo wystawionego dokumentu ani `DocumentNumber` obliczonego przez serwis. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

> [UWAGA: `500 Internal Server Error` dla WAL-03 (`"Product not found."`) zamiast `400`/`404`. Brak dedykowanego wyjątku. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
