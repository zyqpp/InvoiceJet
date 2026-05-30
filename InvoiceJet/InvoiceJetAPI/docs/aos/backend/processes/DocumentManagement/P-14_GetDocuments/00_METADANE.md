# GetDocuments — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Odczyt dokumentów (lista + szczegóły)` |
| Numer procesu | `P-14` |
| Kontroler(y) | `DocumentController` |
| Serwis(y) aplikacyjny | `DocumentService` |
| Metoda(y) serwisu | `DocumentService.GetDocumentTableRecords`, `DocumentService.GetDocumentById` |
| DTO żądania | N/D (parametry trasy) |
| DTO odpowiedzi | `List<DocumentTableRecordDto>` (API-24), `DocumentRequestDto` (API-25) |
| Encje | `Document`, `DocumentProduct`, `Product`, `DocumentStatus`, `Firm` (Client) |
| Repozytoria | `IDocumentRepository`, `IUserRepository` |
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
| `API-24` | `GET /api/Document/GetDocumentTableRecords/{documentTypeId}` | `DocumentController.GetDocumentTableRecords` | Lista dokumentów danego typu (skrócona tabela) |
| `API-25` | `GET /api/Document/GetDocumentById/{documentId}` | `DocumentController.GetDocumentById` | Pełny obiekt dokumentu po Id |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler A | `DocumentController.cs › DocumentController.GetDocumentTableRecords` |
| Kontroler B | `DocumentController.cs › DocumentController.GetDocumentById` |
| Serwis A | `DocumentService.cs › DocumentService.GetDocumentTableRecords` |
| Serwis B | `DocumentService.cs › DocumentService.GetDocumentById` |
| Repozytorium A | `DocumentRepository.cs › DocumentRepository.GetAllDocumentsByType` |
| Repozytorium B | `DocumentRepository.cs › DocumentRepository.GetDocumentWithAllInfo` |
| Profil AutoMapper | `DocumentProfile.cs › DocumentProfile` (ctor) |
| Middleware błędów | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` |
| Snapshot DB | `InvoiceJetDbContextModelSnapshot.cs` — encje `Document`, `DocumentProduct` |
