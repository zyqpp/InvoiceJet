# Zarządzanie kontami bankowymi — Błędy i bezpieczeństwo

## Błędy

| Warunek | Wyjątek | Status HTTP |
|---|---|---|
| Brak aktywnej firmy użytkownika | `UserHasNoAssociatedFirmException` | `400 Bad Request` |
| Konto powiązane z dokumentem | `BankAccountAssociatedWithDocumentsException` | `400 Bad Request` |
| Konto nie istnieje | `Exception("Bank account not found.")` | `500 Internal Server Error` |
| Inny błąd | `Exception` | `500 Internal Server Error` |

---

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut | `[Authorize(Roles = "User")]` |
| Brak tokenu | `401 Unauthorized` |
| Brak roli | `403 Forbidden` |
