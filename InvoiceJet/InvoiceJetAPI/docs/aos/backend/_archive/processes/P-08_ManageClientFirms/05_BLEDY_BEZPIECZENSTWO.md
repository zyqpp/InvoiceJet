# Zarządzanie firmami-klientami — Błędy i bezpieczeństwo

## Błędy

| Warunek | Wyjątek | Status HTTP |
|---|---|---|
| Firma nie istnieje | `Exception("Product not found.")` | `500 Internal Server Error` |
| Firma ma powiązanie z dokumentem | `FirmAssociatedWithDocumentException` | `500 Internal Server Error` |
| Inny błąd | `Exception` | `500 Internal Server Error` |

`FirmAssociatedWithDocumentException` nie ma dedykowanego `catch` w `ExceptionMiddleware`.

---

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut | `[Authorize(Roles = "User")]` |
| Brak tokenu | `401 Unauthorized` |
| Brak roli | `403 Forbidden` |
