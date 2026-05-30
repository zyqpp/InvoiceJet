# Edycja dokumentu — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/Document/EditDocument` |
| Wejście | `DocumentRequestDto` |
| Wyjście | `DocumentRequestDto` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

---

## Kody odpowiedzi

| Status | Warunek |
|---|---|
| `200 OK` | Dokument i pozycje zaktualizowane. |
| `400 Bad Request` | `UserHasNoAssociatedFirmException`. |
| `401 Unauthorized` | Brak tokenu. |
| `403 Forbidden` | Brak roli `User`. |
| `500 Internal Server Error` | `Exception("Document not found.")` lub inne nieobsłużone wyjątki. |
