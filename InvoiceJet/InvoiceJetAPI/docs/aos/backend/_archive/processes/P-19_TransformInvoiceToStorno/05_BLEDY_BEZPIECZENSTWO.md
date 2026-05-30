# Transformacja faktury do storna — Błędy i bezpieczeństwo

## Błędy

| Warunek | Wyjątek | Status HTTP |
|---|---|---|
| Brak aktywnej firmy | `Exception("User firm not found.")` | `500 Internal Server Error` |
| Dokument spoza firmy lub brak dokumentu | `Exception("Document not found.")` | `500 Internal Server Error` |
| Inny błąd | `Exception` | `500 Internal Server Error` |

---

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut | `[Authorize(Roles = "User")]` |
| Brak tokenu | `401 Unauthorized` |
| Brak roli | `403 Forbidden` |
