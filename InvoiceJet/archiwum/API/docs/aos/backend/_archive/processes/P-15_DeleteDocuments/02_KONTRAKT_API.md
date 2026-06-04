# Usuwanie dokumentów — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/Document/DeleteDocuments` |
| Wejście | `int[] documentIds` (`[FromBody]`) |
| Wyjście | `200 OK` i obiekt `{ Message = "Documents deleted successfully." }` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

---

## Kody odpowiedzi

| Status | Warunek |
|---|---|
| `200 OK` | Operacja zakończona sukcesem. |
| `401 Unauthorized` | Brak tokenu. |
| `403 Forbidden` | Brak roli `User`. |
| `500 Internal Server Error` | Nieobsłużony wyjątek infrastruktury. |
