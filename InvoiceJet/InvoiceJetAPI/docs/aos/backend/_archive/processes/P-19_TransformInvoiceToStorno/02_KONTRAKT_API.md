# Transformacja faktury do storna — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/Document/TransformToStorno` |
| Wejście | `int[] documentIds` (`[FromBody]`) |
| Wyjście | `200 OK` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

---

## Kody odpowiedzi

| Status | Warunek |
|---|---|
| `200 OK` | Wszystkie dokumenty z listy zostały przetworzone. |
| `401 Unauthorized` | Brak tokenu. |
| `403 Forbidden` | Brak roli `User`. |
| `500 Internal Server Error` | `Exception("User firm not found.")`, `Exception("Document not found.")` lub inny wyjątek. |
