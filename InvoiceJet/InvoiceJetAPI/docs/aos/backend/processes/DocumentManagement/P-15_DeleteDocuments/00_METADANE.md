# DeleteDocuments — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Usunięcie dokumentów` |
| Numer procesu | `P-15` |
| Kontroler(y) | `DocumentController` |
| Serwis(y) aplikacyjny | `DocumentService` |
| Metoda(y) serwisu | `DocumentService.DeleteDocuments` |
| DTO żądania | `int[]` (`[FromBody]`) |
| DTO odpowiedzi | `{ message: string }` (obiekt anonimowy) |
| Encje | `Document`, `DocumentProduct` |
| Repozytoria | `IDocumentRepository`, `IDocumentProductRepository` |
| Wyjątki | brak wyjątków domenowych (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | brak |
| Autoryzacja | `[Authorize(Roles = "User")]` na klasie `DocumentController` |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `POZA ZAKRESEM — ETAP FULLSTACK` |

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-26` | `PUT /api/Document/DeleteDocuments` | `DocumentController.DeleteDocuments` | Usunięcie listy dokumentów wraz z pozycjami |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler | `DocumentController.cs › DocumentController.DeleteDocuments` |
| Serwis | `DocumentService.cs › DocumentService.DeleteDocuments` |
| Repozytorium dokumentów | `DocumentRepository.cs › DocumentRepository.Query` |
| Repozytorium pozycji | `DocumentProductRepository.cs › DocumentProductRepository.RemoveRangeAsync` |
| Middleware błędów | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` |
| Snapshot DB | `InvoiceJetDbContextModelSnapshot.cs` — encje `Document`, `DocumentProduct` |
