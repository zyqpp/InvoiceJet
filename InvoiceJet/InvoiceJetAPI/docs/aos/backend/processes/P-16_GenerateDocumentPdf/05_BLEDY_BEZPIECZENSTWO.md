# Generowanie dokumentu PDF — Błędy i bezpieczeństwo

## Błędy

| Warunek | Status HTTP | Źródło |
|---|---|---|
| Brak aktywnej firmy | `400 Bad Request` | `catch` w `DocumentController.GenerateDocument()` |
| Błąd podczas generowania PDF rzucający wyjątek | `400 Bad Request` | `catch` w kontrolerze |
| Błąd generowania PDF bez wyjątku (zwrócone `null`) | `200 OK` | `PdfGenerationService` łapie wyjątek i zwraca `null` |

---

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut | `[Authorize(Roles = "User")]` |
| Brak tokenu | `401 Unauthorized` |
| Brak roli | `403 Forbidden` |
