# Pobranie strumienia PDF faktury — Błędy i bezpieczeństwo

## Błędy

| Warunek | Status HTTP | Źródło |
|---|---|---|
| Brak aktywnej firmy | `400 Bad Request` | `ExceptionMiddleware` (`UserHasNoAssociatedFirmException`) |
| Generator zwróci `null` | `400 Bad Request` | Warunek w kontrolerze |
| Inny wyjątek | `500 Internal Server Error` | `ExceptionMiddleware` |

---

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut | `[Authorize(Roles = "User")]` |
| Brak tokenu | `401 Unauthorized` |
| Brak roli | `403 Forbidden` |
