# POST /api/Document/GenerateDocumentPdf — Generowanie PDF (zapis na dysk)

| Atrybut | Wartość |
|---|---|
| ID | API-28 |
| Metoda | POST |
| URL | `/api/Document/GenerateDocumentPdf` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentController.GenerateDocument` |
| Serwis | `IDocumentService.GeneratePdfDocument` → `IPdfGenerationService.GenerateInvoicePdf` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

> **Anomalia A-04:** Kontroler ma własny `try/catch` — omija `ExceptionMiddleware`.  
> **Anomalia A-06:** `PdfGenerationService.GenerateInvoicePdf` hardcodes `new InvoiceDocument()` — zawsze faktura zwykła, ignoruje `DocumentType`.

## Request

### Body (JSON) — `DocumentRequestDto`

Takie same pola jak w `POST_Document_Add.md`.

## Response

### 200 OK — pusta odpowiedź

PDF jest generowany i zapisywany na dysku serwera. Klient **nie** otrzymuje pliku.

### Błędy

| Status HTTP | Warunek |
|---|---|
| 400 Bad Request | Dowolny wyjątek (własny try/catch: `return BadRequest(ex.Message)`) |
| 400 Bad Request | `UserHasNoAssociatedFirmException` |

## Zachowanie po stronie frontendu

`BaseInvoiceComponent.generateInvoicePdf()` — wywołuje ten endpoint, ale **ignoruje odpowiedź** (tylko `console.log`). Nie wyświetla użytkownikowi żadnego feedbacku poza logiem w konsoli.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny z anomaliami. |
