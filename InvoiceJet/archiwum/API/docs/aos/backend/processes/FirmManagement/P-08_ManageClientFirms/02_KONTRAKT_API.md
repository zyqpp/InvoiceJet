# ManageClientFirms — Kontrakt API

---

## `API-08` — GET /api/Firm/GetUserClientFirms

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Firm/GetUserClientFirms` |
| Kontroler | `FirmController.cs › FirmController.GetUserClientFirms` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

### Parametry trasy / zapytania

Brak parametrów.

### Ciało żądania

Brak (endpoint GET bez body).

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `FirmDto[]` | Powodzenie — zwrot listy firm-klientów (może być pusta) |
| `401 Unauthorized` | — | Brak / niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

Przykład odpowiedzi (200 OK):
```json
[
  {
    "id": 2,
    "name": "Acme Corporation",
    "cui": "12345678",
    "regCom": "J40/2020/123",
    "address": "STR. Marticel Ion Dragomir, nr. 10",
    "county": "Bihor",
    "city": "Oradea"
  },
  {
    "id": 5,
    "name": "Tech Innovations Ltd",
    "cui": "87654321",
    "regCom": "J40/2021/456",
    "address": "BLD. Gheorghe Doja, nr. 5",
    "county": "Cluj",
    "city": "Cluj-Napoca"
  }
]
```

Jeśli użytkownik nie ma firm-klientów (IsClient=true):
```json
[]
```

---

## `API-09` — PUT /api/Firm/DeleteFirms

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/Firm/DeleteFirms` |
| Kontroler | `FirmController.cs › FirmController.DeleteFirms` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

### Parametry trasy / zapytania

| Parametr | Typ | Źródło | Opis |
|---|---|---|---|
| `firmIds` | `int[]` | query string (binding domyślne) | Tablica ID firm do usunięcia, np. `?firmIds=2&firmIds=5` |

### Ciało żądania

Brak (parametr bindowany z query string).

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | — | Powodzenie — wszystkie firmy usunięte |
| `400 Bad Request` | `{ "message": "..." }` | Brak firmy (WAL-01) lub firma powiązana z dokumentem (WAL-02) |
| `401 Unauthorized` | — | Brak / niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |
| `500 Internal Server Error` | `{ "message": "..." }` | Błąd serwera (np. generyczny `Exception`) |

Przykład żądania:
```
PUT /api/Firm/DeleteFirms?firmIds=2&firmIds=5
```

Przykład odpowiedzi (200 OK):
```
(Brak ciała odpowiedzi — status 200 wystarczający)
```

Przykład odpowiedzi (400 Bad Request) — firma nie znaleziona:
```json
{
  "message": "Product not found."
}
```

Przykład odpowiedzi (400 Bad Request) — firma powiązana z dokumentem:
```json
{
  "message": "Can't delete. Firm Acme Corporation is associated with a document."
}
```
