# Edycja dokumentu — Błędy i bezpieczeństwo

## Błędy

| Warunek | Wyjątek | Status HTTP |
|---|---|---|
| Brak aktywnej firmy użytkownika | `UserHasNoAssociatedFirmException` | `400 Bad Request` |
| Dokument nie istnieje | `Exception("Document not found.")` | `500 Internal Server Error` |
| Brak produktu przy pozycji `id > 0` | `Exception("Product not found.")` | `500 Internal Server Error` |

---

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut | `[Authorize(Roles = "User")]` |
| Brak tokenu | `401 Unauthorized` |
| Brak roli | `403 Forbidden` |

---

## Uwagi bezpieczeństwa

- Proces nie sprawdza jawnie, czy dokument należy do aktywnej firmy użytkownika przed aktualizacją po `Id`. [UWAGA: weryfikacja własności rekordu dokumentu nie jest widoczna w metodzie `EditDocument` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
