# Zarządzanie produktami — Błędy i bezpieczeństwo

## Błędy

| Warunek | Wyjątek | Status HTTP |
|---|---|---|
| Brak aktywnej firmy użytkownika | `UserHasNoAssociatedFirmException` | `400 Bad Request` |
| Produkt powiązany z fakturą | `ProductAssociatedWithInvoiceException` | `400 Bad Request` |
| Produkt o tej samej nazwie już istnieje | `ProductWithSameNameExistsException` | `500 Internal Server Error` |
| Produkt nie istnieje | `Exception("Product not found.")` | `500 Internal Server Error` |

`ProductWithSameNameExistsException` nie ma dedykowanego `catch` w `ExceptionMiddleware`.

---

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut | `[Authorize(Roles = "User")]` |
| Brak tokenu | `401 Unauthorized` |
| Brak roli | `403 Forbidden` |
