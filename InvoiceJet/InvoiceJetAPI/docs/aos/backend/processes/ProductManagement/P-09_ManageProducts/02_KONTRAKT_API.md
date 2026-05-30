# ManageProducts — Kontrakt API

---

## `API-10` — GET /api/Product/GetAllProductsForUserId

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Product/GetAllProductsForUserId` |
| Kontroler | `ProductController.cs › ProductController.GetAllProductsForUserId` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `ProductController`) |

### Parametry trasy / zapytania

Brak parametrów wejściowych. Tożsamość użytkownika pochodzi z JWT claim `userId`.

### Ciało żądania

Brak.

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `ICollection<ProductDto>` | Powodzenie; może być pusta kolekcja `[]` |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

Przykład odpowiedzi (`200 OK` — lista produktów):
```json
[
  {
    "id": 3,
    "name": "Usługa konsultingowa",
    "price": 500.00,
    "containsTva": false,
    "unitOfMeasurement": "ora",
    "tvaValue": 19
  },
  {
    "id": 7,
    "name": "Laptop Dell XPS 15",
    "price": 1200.00,
    "containsTva": true,
    "unitOfMeasurement": "buc",
    "tvaValue": 19
  }
]
```

Przykład odpowiedzi (`200 OK` — brak produktów):
```json
[]
```

---

## `API-11` — POST /api/Product/AddProduct

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/Product/AddProduct` |
| Kontroler | `ProductController.cs › ProductController.AddProduct` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `ProductController`) |

### Parametry trasy / zapytania

Brak.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `ProductDto` | `[FromBody]` (niejawny, wymuszony przez `[ApiController]`) |

Pole `id` przy tworzeniu powinno być `0` (lub pominięte) — DB nadaje wartość.

Przykład żądania:
```json
{
  "id": 0,
  "name": "Usługa konsultingowa",
  "price": 500.00,
  "containsTva": false,
  "unitOfMeasurement": "ora",
  "tvaValue": 19
}
```

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `ProductDto` | Produkt dodany; DTO zawiera `Id` nadany przez DB |
| `400 Bad Request` | `{ "message": "User has no associated firm." }` | Brak aktywnej firmy (WAL-01) |
| `500 Internal Server Error` | `{ "message": "Product with name ... already exists." }` | Duplikat nazwy w firmie (WAL-02) [UWAGA: powinno 400] |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

Przykład odpowiedzi (`200 OK`):
```json
{
  "id": 12,
  "name": "Usługa konsultingowa",
  "price": 500.00,
  "containsTva": false,
  "unitOfMeasurement": "ora",
  "tvaValue": 19
}
```

---

## `API-12` — PUT /api/Product/EditProduct

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/Product/EditProduct` |
| Kontroler | `ProductController.cs › ProductController.EditProduct` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `ProductController`) |

### Parametry trasy / zapytania

Brak. `Id` produktu do edycji przekazywane w body w polu `id`.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `ProductDto` | `[FromBody]` (niejawny) |

Pole `id` musi odpowiadać istniejącemu produktowi.

Przykład żądania:
```json
{
  "id": 12,
  "name": "Usługa konsultingowa (premium)",
  "price": 750.00,
  "containsTva": false,
  "unitOfMeasurement": "ora",
  "tvaValue": 19
}
```

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `ProductDto` | Produkt zaktualizowany |
| `500 Internal Server Error` | `{ "message": "Product not found." }` | Produkt o danym `id` nie istnieje (WAL-03) [UWAGA: powinno 400] |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

Przykład odpowiedzi (`200 OK`):
```json
{
  "id": 12,
  "name": "Usługa konsultingowa (premium)",
  "price": 750.00,
  "containsTva": false,
  "unitOfMeasurement": "ora",
  "tvaValue": 19
}
```

---

## `API-13` — PUT /api/Product/DeleteProducts

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/Product/DeleteProducts` |
| Kontroler | `ProductController.cs › ProductController.DeleteProducts` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `ProductController`) |

> [UWAGA: Endpoint używa metody `PUT` do usuwania zasobów, co jest niezgodne z konwencją REST (`DELETE`). Odzwierciedlono stan z kodu bez zmiany metody — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Parametry trasy / zapytania

| Parametr | Typ | Źródło | Opis |
|---|---|---|---|
| `productIds` | `int[]` | query string | Tablica ID produktów do usunięcia, np. `?productIds=3&productIds=7` |

### Ciało żądania

Brak.

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | — | Wszystkie produkty usunięte pomyślnie |
| `400 Bad Request` | `{ "message": "Can't delete. Product ... is associated with an invoice." }` | Produkt powiązany z fakturą (WAL-05) |
| `500 Internal Server Error` | `{ "message": "Product not found." }` | Produkt o danym ID nie istnieje (WAL-04) [UWAGA: powinno 400] |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

Przykład żądania:
```
PUT /api/Product/DeleteProducts?productIds=3&productIds=7
Authorization: Bearer <jwt>
```

Przykład odpowiedzi (`200 OK`): puste ciało.

Przykład odpowiedzi (`400 Bad Request`):
```json
{
  "message": "Can't delete. Product Usługa konsultingowa is associated with an invoice."
}
```
