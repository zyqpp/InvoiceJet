# Zarządzanie seriami dokumentów — Błędy i bezpieczeństwo

## Błędy

| Operacja | Warunek | Status HTTP |
|---|---|---|
| Dodanie | Brak aktywnej firmy (`UserHasNoAssociatedFirmException`) | `400 Bad Request` |
| Dodanie | Dowolny wyjątek w serwisie | `400 Bad Request` (lokalny `catch` w kontrolerze) |
| Aktualizacja | Seria nie istnieje (`Exception("Document Series not found")`) | `500 Internal Server Error` |
| Usuwanie | Nieobsłużony błąd | `500 Internal Server Error` |

---

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut | `[Authorize(Roles = "User")]` |
| Brak tokenu | `401 Unauthorized` |
| Brak roli | `403 Forbidden` |
