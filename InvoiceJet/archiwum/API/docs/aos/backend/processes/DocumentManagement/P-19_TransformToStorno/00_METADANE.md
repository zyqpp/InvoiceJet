# TransformToStorno — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Przekształcenie dokumentów w faktury storno` |
| Numer procesu | `P-19` |
| Kontroler(y) | `DocumentController` |
| Serwis(y) aplikacyjny | `DocumentService` |
| Metoda(y) serwisu | `DocumentService.TransformToStorno` |
| DTO żądania | `int[]` (`[FromBody]`) |
| DTO odpowiedzi | puste body (`200 OK`) |
| Encje | `Document` |
| Repozytoria | `IUserRepository`, `IDocumentRepository` |
| Wyjątki | `Exception("User firm not found.")`, `Exception("Document not found.")` — niemapowane → **500** (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | brak |
| Autoryzacja | `[Authorize(Roles = "User")]` na klasie `DocumentController` |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `POZA ZAKRESEM — ETAP FULLSTACK` |

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-31` | `PUT /api/Document/TransformToStorno` | `DocumentController.TransformToStorno` | Zmiana typu dokumentów na Storno (DocumentTypeId=3) |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler | `DocumentController.cs › DocumentController.TransformToStorno` |
| Serwis | `DocumentService.cs › DocumentService.TransformToStorno` |
| Repozytorium użytkowników | `UserRepository.cs › UserRepository.GetUserFirmIdAsync` |
| Repozytorium dokumentów | `DocumentRepository.cs › DocumentRepository.Query` |
| Middleware błędów | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` |
| Snapshot DB | `InvoiceJetDbContextModelSnapshot.cs` — encja `Document` |
