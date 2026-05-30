# Edycja firmy — Błędy i bezpieczeństwo

## Błędy procesu

| Warunek | Wyjątek | Status HTTP |
|---|---|---|
| Firma nie istnieje | `Exception("Firm not found.")` | `500 Internal Server Error` |
| Inny błąd serwisu lub bazy | `Exception` | `500 Internal Server Error` |

---

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut | `[Authorize(Roles = "User")]` |
| Brak tokenu | `401 Unauthorized` |
| Brak roli | `403 Forbidden` |
