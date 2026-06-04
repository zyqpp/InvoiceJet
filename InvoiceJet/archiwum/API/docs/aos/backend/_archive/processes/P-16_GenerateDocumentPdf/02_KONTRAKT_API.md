# Generowanie dokumentu PDF — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/Document/GenerateDocumentPdf` |
| Wejście | `DocumentRequestDto` |
| Wyjście | `200 OK` bez body |
| Autoryzacja | `[Authorize(Roles = "User")]` |

---

## Kody odpowiedzi

| Status | Warunek |
|---|---|
| `200 OK` | Kontroler nie przechwycił wyjątku serwisu. |
| `400 Bad Request` | Kontroler przechwycił wyjątek i zwrócił `BadRequest(ex.Message)`. |
| `401 Unauthorized` | Brak tokenu. |
| `403 Forbidden` | Brak roli `User`. |
