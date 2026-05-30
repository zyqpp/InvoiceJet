# Dane autouzupełniania dokumentu — Błędy i bezpieczeństwo

## Błędy procesu

Proces nie rzuca dedykowanych wyjątków biznesowych w metodzie `GetDocumentAutofillInfo`.

| Warunek | Status HTTP |
|---|---|
| Brak tokenu | `401 Unauthorized` |
| Brak roli `User` | `403 Forbidden` |
| Nieobsłużony wyjątek infrastruktury | `500 Internal Server Error` |

---

## Uwagi bezpieczeństwa

- Proces pobiera dane wyłącznie dla kontekstu zalogowanego użytkownika.
- Dla braku aktywnej firmy proces zwraca pusty obiekt zamiast wyjątku.
