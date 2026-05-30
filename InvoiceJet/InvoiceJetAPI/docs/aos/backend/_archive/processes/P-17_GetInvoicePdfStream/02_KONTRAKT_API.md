# Pobranie strumienia PDF faktury — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/Document/GetInvoicePdfStream` |
| Wejście | `DocumentRequestDto` |
| Wyjście sukcesu | Plik `application/pdf` |
| Autoryzacja | `[Authorize(Roles = "User")]` |

---

## Kody odpowiedzi

| Status | Warunek |
|---|---|
| `200 OK` | `PdfContent` nie jest `null`. |
| `400 Bad Request` | `PdfContent == null` lub `UserHasNoAssociatedFirmException`. |
| `401 Unauthorized` | Brak tokenu. |
| `403 Forbidden` | Brak roli `User`. |
| `500 Internal Server Error` | Inny nieobsłużony wyjątek. |
