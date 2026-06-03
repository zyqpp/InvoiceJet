# DeleteDocuments — Kontrakt API

---

## `API-26` — PUT /api/Document/DeleteDocuments

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` ⚠️ (semantycznie powinno być `DELETE`) |
| Ścieżka | `/api/Document/DeleteDocuments` |
| Kontroler | `DocumentController.cs › DocumentController.DeleteDocuments` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

### Parametry trasy

Brak.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `int[]` | `[FromBody]` |

Przykład żądania (usunięcie dwóch dokumentów):
```json
[3, 7]
```

Przykład żądania (pusta tablica — brak efektu):
```json
[]
```

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `{ "message": string }` | Powodzenie (również gdy tablica pusta lub ID nieistniejące) |
| `401 Unauthorized` | — | Brak tokenu |
| `403 Forbidden` | — | Brak roli `User` |
| `500 Internal Server Error` | `{ "message": "..." }` | Wyjątek DB lub `NullReferenceException` |

Przykład odpowiedzi (`200 OK`):
```json
{
  "message": "Documents deleted successfully."
}
```

> ⚠️ Odpowiedź `200 OK` jest zwracana nawet gdy:
> - żaden z podanych `documentIds` nie istnieje w bazie,
> - podana tablica jest pusta `[]`,
> - usunięto dokumenty innego użytkownika (brak ownership check).
