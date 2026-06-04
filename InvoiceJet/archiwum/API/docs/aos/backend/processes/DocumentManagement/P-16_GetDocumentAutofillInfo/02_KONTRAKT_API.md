# GetDocumentAutofillInfo — Kontrakt API

---

## `API-27` — GET /api/Document/GetDocumentAutofillInfo/{documentTypeId}

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Document/GetDocumentAutofillInfo/{documentTypeId}` |
| Kontroler | `DocumentController.cs › DocumentController.GetDocumentAutofillInfo` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

### Parametry trasy

| Parametr | Typ | Źródło | Opis |
|---|---|---|---|
| `documentTypeId` | `int` | `[FromRoute]` | Id typu dokumentu: 1=Faktura, 2=Proforma, 3=Storno. Używany do filtrowania serii dokumentów. |

### Ciało żądania

Brak.

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `DocumentAutofillDto` | Powodzenie; pola mogą być `null` gdy brak firmy ⚠️ |
| `401 Unauthorized` | — | Brak tokenu |
| `403 Forbidden` | — | Brak roli `User` |

Przykład odpowiedzi (`200 OK` — użytkownik z firmą):
```json
{
  "clients": [
    {
      "id": 5,
      "name": "Firma Klient SRL",
      "cui": "87654321",
      "regCom": "J40/5678/2021",
      "address": "STR. CLIENTULUI NR. 2",
      "county": "ILFOV",
      "city": "VOLUNTARI"
    }
  ],
  "documentSeries": [
    {
      "id": 2,
      "name": "2026",
      "currentNumber": 1,
      "documentType": { "id": 1, "type": "Factura" }
    }
  ],
  "documentStatuses": [
    { "id": 1, "status": "Unpaid" },
    { "id": 2, "status": "Paid" }
  ],
  "products": [
    { "id": 1, "name": "Consultanță IT", "price": 500.00, "tvaValue": 19 }
  ]
}
```

Przykład odpowiedzi (`200 OK` — użytkownik bez firmy ⚠️):
```json
{
  "clients": null,
  "documentSeries": null,
  "documentStatuses": null,
  "products": null
}
```

> ⚠️ Gdy użytkownik nie ma powiązanej firmy, serwis zwraca `new DocumentAutofillDto()` — wszystkie listy mają wartość `null`, nie `[]`. Może powodować błędy po stronie frontendu. Kotwica: `DocumentService.cs › DocumentService.GetDocumentAutofillInfo`.
