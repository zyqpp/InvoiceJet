# ManageDocumentPdf — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Generowanie i pobieranie PDF dokumentu` |
| Numer procesu | `P-17` |
| Kontroler(y) | `DocumentController` |
| Serwis(y) aplikacyjny | `DocumentService`, `IPdfGenerationService` |
| Metoda(y) serwisu | `DocumentService.GeneratePdfDocument`, `DocumentService.GetInvoicePdfStream` |
| DTO żądania | `DocumentRequestDto` |
| DTO odpowiedzi | puste body (API-28); `application/pdf` via `DocumentStreamDto` (API-29) |
| Encje | `UserFirm`, `Firm`, `Document`, `BankAccount` |
| Repozytoria | `IUserRepository`, `IDocumentRepository` |
| Wyjątki | `UserHasNoAssociatedFirmException` (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | `QuestPDF` (generowanie PDF via `PdfGenerationService`), zapis na dysk |
| Autoryzacja | `[Authorize(Roles = "User")]` na klasie `DocumentController` |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `POZA ZAKRESEM — ETAP FULLSTACK` |

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-28` | `POST /api/Document/GenerateDocumentPdf` | `DocumentController.GenerateDocument` | Zapis PDF na dysk serwera |
| `API-29` | `POST /api/Document/GetInvoicePdfStream` | `DocumentController.GetInvoicePdfStream` | Zwrócenie PDF jako strumień do pobrania |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler A | `DocumentController.cs › DocumentController.GenerateDocument` |
| Kontroler B | `DocumentController.cs › DocumentController.GetInvoicePdfStream` |
| Serwis A | `DocumentService.cs › DocumentService.GeneratePdfDocument` |
| Serwis B | `DocumentService.cs › DocumentService.GetInvoicePdfStream` |
| Serwis PDF (zapis) | `PdfGenerationService.cs › PdfGenerationService.GenerateInvoicePdf` |
| Serwis PDF (stream) | `PdfGenerationService.cs › PdfGenerationService.GetInvoicePdfStream` |
| Repozytorium użytkowników | `UserRepository.cs › UserRepository.GetUserFirmAsync` |
| Repozytorium dokumentów | `DocumentRepository.cs › DocumentRepository.Query` |
| Middleware błędów | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` |
