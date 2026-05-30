# Usuwanie dokumentów — Błędy i bezpieczeństwo

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut | `[Authorize(Roles = "User")]` |
| Brak tokenu | `401 Unauthorized` |
| Brak roli | `403 Forbidden` |

---

## Błędy

Dedykowane wyjątki biznesowe nie są rzucane w metodzie `DeleteDocuments`.

| Warunek | Status HTTP |
|---|---|
| Nieobsłużony wyjątek infrastruktury | `500 Internal Server Error` |
