# TransformToStorno — Kontrakt API

---

## `API-31` — PUT /api/Document/TransformToStorno

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/Document/TransformToStorno` |
| Kontroler | `DocumentController.cs › DocumentController.TransformToStorno` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

### Parametry trasy

Brak.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `int[]` | `[FromBody]` |

Przykład żądania (przekształcenie dwóch dokumentów):
```json
[3, 4]
```

Przykład żądania (pusta tablica — brak efektu):
```json
[]
```

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | puste body | Wszystkie dokumenty przekształcone pomyślnie |
| `401 Unauthorized` | — | Brak tokenu |
| `403 Forbidden` | — | Brak roli `User` |
| `500 Internal Server Error` | `{ "message": "User firm not found." }` | Użytkownik bez firmy (WAL-01) ⚠️ |
| `500 Internal Server Error` | `{ "message": "Document not found." }` | Dokument nieznaleziony lub nie należy do firmy (WAL-02) ⚠️ |

> ⚠️ Wyjątki WAL-01 i WAL-02 generują **500** zamiast odpowiednio **400** i **404** — użyto `new Exception(...)` zamiast domenowych wyjątków mapowanych w ExceptionMiddleware.

> ⚠️ Pusta tablica `[]` → `200 OK` bez zmian w bazie.

> ⚠️ Przy błędzie w połowie listy (WAL-02), dokumenty przetworzone przed błędem **są już zapisane** (brak transakcji obejmującej całość).

Przykład odpowiedzi sukcesu (`200 OK`): puste body.

Przykład odpowiedzi błędu (`500 Internal Server Error`):
```json
{ "message": "Document not found." }
```
