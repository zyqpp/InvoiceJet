# ManageDocumentSeries — Kontrakt API

---

## `API-18` — GET /api/DocumentSeries/GetAllDocumentSeriesForUserId

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/DocumentSeries/GetAllDocumentSeriesForUserId` |
| Kontroler | `DocumentSeriesController.cs › DocumentSeriesController.GetAllDocumentSeriesForUserId` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `DocumentSeriesController`) |

### Parametry trasy / zapytania

Brak parametrów wejściowych. Tożsamość użytkownika pochodzi z JWT claim `userId`.

### Ciało żądania

Brak.

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `List<DocumentSeriesDto>` | Powodzenie; może być `[]` gdy brak firmy lub brak serii |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

Przykład odpowiedzi (`200 OK`):
```json
[
  {
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
  {
    "id": 2,
    "seriesName": "2026",
    "firstNumber": 1,
    "currentNumber": 1,
    "isDefault": true,
    "documentTypeId": 2,
    "documentType": {
      "id": 2,
      "name": "Factura Proforma"
    }
  },
  {
    "id": 3,
    "seriesName": "2026",
    "firstNumber": 1,
    "currentNumber": 1,
    "isDefault": true,
    "documentTypeId": 3,
    "documentType": {
      "id": 3,
      "name": "Factura Storno"
    }
  }
]
```

---

## `API-19` — POST /api/DocumentSeries/AddDocumentSeries

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/DocumentSeries/AddDocumentSeries` |
| Kontroler | `DocumentSeriesController.cs › DocumentSeriesController.AddDocumentSeries` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `DocumentSeriesController`) |

> **Uwaga o obsłudze błędów:** Kontroler ma własny `try/catch (Exception ex)` → zwraca `BadRequest(ex.Message)` dla KAŻDEGO wyjątku z serwisu. Wyjątki z `AddDocumentSeries` **nie trafiają do `ExceptionMiddleware`**.

### Parametry trasy / zapytania

Brak.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `DocumentSeriesDto` | `[FromBody]` |

Pole `id` przy tworzeniu powinno być `0`. Pole `documentType` musi zawierać obiekt z poprawnym `id` (1=Factura, 2=Factura Proforma, 3=Factura Storno).

Przykład żądania:
```json
{
  "id": 0,
  "seriesName": "2026-A",
  "firstNumber": 1,
  "currentNumber": 1,
  "isDefault": false,
  "documentTypeId": 1,
  "documentType": {
    "id": 1,
    "name": "Factura"
  }
}
```

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | — (puste ciało) | Seria dodana |
| `400 Bad Request` | `"User has no associated firm."` (plain text z `ex.Message`) | Brak aktywnej firmy — wyjątek przechwycony przez try/catch kontrolera |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

> [UWAGA: Odpowiedź `400` z kontrolera jest `BadRequest(ex.Message)` — ciało to plain string, **nie** obiekt JSON `{ "message": "..." }`. Różnica względem innych endpointów gdzie `ExceptionMiddleware` serialyzuje `{ "message": "..." }`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

Przykład odpowiedzi sukcesu (`200 OK`): puste ciało. Nowe `Id` serii **nie jest** zwracane.

---

## `API-20` — PUT /api/DocumentSeries/UpdateDocumentSeries

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/DocumentSeries/UpdateDocumentSeries` |
| Kontroler | `DocumentSeriesController.cs › DocumentSeriesController.UpdateDocumentSeries` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `DocumentSeriesController`) |

### Parametry trasy / zapytania

Brak. `Id` serii przekazywany w body.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `DocumentSeriesDto` | `[FromBody]` |

Przykład żądania:
```json
{
  "id": 1,
  "seriesName": "2026-B",
  "firstNumber": 1,
  "currentNumber": 3,
  "isDefault": true,
  "documentTypeId": 1,
  "documentType": {
    "id": 1,
    "name": "Factura"
  }
}
```

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | — (puste ciało) | Seria zaktualizowana |
| `500 Internal Server Error` | `{ "message": "Document Series not found" }` | Seria o danym `id` nie istnieje (WAL-02) [UWAGA: powinno być `400`] |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

---

## `API-21` — PUT /api/DocumentSeries/DeleteDocumentSeries

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/DocumentSeries/DeleteDocumentSeries` |
| Kontroler | `DocumentSeriesController.cs › DocumentSeriesController.DeleteDocumentSeries` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `DocumentSeriesController`) |

> [UWAGA: Endpoint używa metody HTTP `PUT` do usuwania zasobów — niezgodność z konwencją REST (`DELETE`). — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Parametry trasy / zapytania

| Parametr | Typ | Źródło | Opis |
|---|---|---|---|
| `documentSeriesIds` | `int[]` | query string (brak `[FromBody]`) | Tablica ID serii do usunięcia, np. `?documentSeriesIds=1&documentSeriesIds=2` |

> Brak atrybutu `[FromBody]` — bindowanie z **query string**. Różni się od `BankAccountController.DeleteUserFirmBankAccounts` (body) i podobne do `ProductController.DeleteProducts` (query string).

### Ciało żądania

Brak.

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | — | Serie usunięte; nieistniejące IDs ignorowane po cichu |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

Przykład żądania:
```
PUT /api/DocumentSeries/DeleteDocumentSeries?documentSeriesIds=4&documentSeriesIds=5
Authorization: Bearer <jwt>
```

Przykład odpowiedzi (`200 OK`): puste ciało.
