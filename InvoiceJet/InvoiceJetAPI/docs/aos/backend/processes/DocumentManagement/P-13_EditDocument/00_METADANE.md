# EditDocument — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Edycja istniejącego dokumentu` |
| Numer procesu | `P-13` |
| Kontroler(y) | `DocumentController` |
| Serwis(y) aplikacyjny | `DocumentService` |
| Metoda(y) serwisu | `DocumentService.EditDocument`, `DocumentService.UpdateDocumentProducts` (prywatna) |
| DTO żądania | `DocumentRequestDto` |
| DTO odpowiedzi | `DocumentRequestDto` (oryginalny obiekt żądania) |
| Encje | `Document`, `DocumentProduct`, `Product` (opcjonalnie nowe) |
| Repozytoria | `IDocumentRepository`, `IDocumentProductRepository`, `IProductRepository`, `IUserRepository` |
| Wyjątki | `UserHasNoAssociatedFirmException` (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | brak |
| Autoryzacja | `[Authorize(Roles = "User")]` na klasie `DocumentController` |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `POZA ZAKRESEM — ETAP FULLSTACK` |

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-23` | `PUT /api/Document/EditDocument` | `DocumentController.EditDocument` | Edycja istniejącego dokumentu (pola + pozycje) |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler | `DocumentController.cs › DocumentController.EditDocument` |
| Serwis główna | `DocumentService.cs › DocumentService.EditDocument` |
| Serwis pozycje | `DocumentService.cs › DocumentService.UpdateDocumentProducts` |
| Middleware błędów | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` |
| Snapshot DB | `InvoiceJetDbContextModelSnapshot.cs` — encje `Document`, `DocumentProduct` |
