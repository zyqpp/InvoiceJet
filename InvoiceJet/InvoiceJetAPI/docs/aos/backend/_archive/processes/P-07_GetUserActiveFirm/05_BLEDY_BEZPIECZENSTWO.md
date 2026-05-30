# Pobranie aktywnej firmy użytkownika — Błędy i bezpieczeństwo

## Błędy procesu

Proces nie rzuca dedykowanych wyjątków biznesowych w `GetUserActiveFirm()`.

| Warunek | Status HTTP |
|---|---|
| Brak tokenu | `401 Unauthorized` |
| Brak roli `User` | `403 Forbidden` |
| Nieobsłużony błąd infrastruktury | `500 Internal Server Error` |

---

## Uwagi bezpieczeństwa

- Identyfikator użytkownika pochodzi z kontekstu tokenu.
- Endpoint nie przyjmuje parametrów wejściowych, które wskazują innego użytkownika.
