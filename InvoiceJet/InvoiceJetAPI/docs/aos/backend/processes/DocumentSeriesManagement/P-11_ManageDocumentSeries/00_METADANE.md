# ManageDocumentSeries — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Zarządzanie seriami dokumentów` |
| Numer procesu | `P-11` |
| Kontroler(y) | `DocumentSeriesController` |
| Serwis(y) aplikacyjny | `DocumentSeriesService` |
| Metoda(y) serwisu | `DocumentSeriesService.GetAllDocumentSeriesForUserId`, `DocumentSeriesService.AddDocumentSeries`, `DocumentSeriesService.UpdateDocumentSeries`, `DocumentSeriesService.DeleteDocumentSeries` |
| DTO żądania | `DocumentSeriesDto` (Add, Update) |
| DTO odpowiedzi | `DocumentSeriesDto` (Get) |
| Encje | `DocumentSeries`, `DocumentType` |
| Repozytoria | `IDocumentSeriesRepository` (`DocumentSeriesRepository`), `IUserRepository` (`GetUserFirmIdAsync`) |
| Wyjątki | `UserHasNoAssociatedFirmException` (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | brak |
| Autoryzacja | `[Authorize(Roles = "User")]` na klasie `DocumentSeriesController` |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `POZA ZAKRESEM — ETAP FULLSTACK` |

---

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-18` | `GET /api/DocumentSeries/GetAllDocumentSeriesForUserId` | `DocumentSeriesController.GetAllDocumentSeriesForUserId` | Pobranie listy serii dokumentów aktywnej firmy użytkownika |
| `API-19` | `POST /api/DocumentSeries/AddDocumentSeries` | `DocumentSeriesController.AddDocumentSeries` | Dodanie nowej serii dokumentów |
| `API-20` | `PUT /api/DocumentSeries/UpdateDocumentSeries` | `DocumentSeriesController.UpdateDocumentSeries` | Aktualizacja istniejącej serii dokumentów |
| `API-21` | `PUT /api/DocumentSeries/DeleteDocumentSeries` | `DocumentSeriesController.DeleteDocumentSeries` | Usunięcie serii dokumentów (batch) |

> [UWAGA: `API-21` używa metody HTTP `PUT` zamiast `DELETE`. Kotwica: `DocumentSeriesController.cs` — `[HttpPut("DeleteDocumentSeries")]`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler — GET | `DocumentSeriesController.cs › DocumentSeriesController.GetAllDocumentSeriesForUserId` |
| Kontroler — ADD | `DocumentSeriesController.cs › DocumentSeriesController.AddDocumentSeries` |
| Kontroler — UPDATE | `DocumentSeriesController.cs › DocumentSeriesController.UpdateDocumentSeries` |
| Kontroler — DELETE | `DocumentSeriesController.cs › DocumentSeriesController.DeleteDocumentSeries` |
| Serwis — GET | `DocumentSeriesService.cs › DocumentSeriesService.GetAllDocumentSeriesForUserId` |
| Serwis — ADD | `DocumentSeriesService.cs › DocumentSeriesService.AddDocumentSeries` |
| Serwis — UPDATE | `DocumentSeriesService.cs › DocumentSeriesService.UpdateDocumentSeries` |
| Serwis — DELETE | `DocumentSeriesService.cs › DocumentSeriesService.DeleteDocumentSeries` |
| Repozytorium — GET | `DocumentSeriesRepository.cs › DocumentSeriesRepository.GetAllDocumentSeriesForActiveUserFirm` |
| Repozytorium — ADD/UPDATE/DELETE | `GenericRepository.cs › GenericRepository.AddAsync` / `UpdateAsync` / `RemoveRangeAsync` |
| DTO | `DocumentSeriesDto.cs › DocumentSeriesDto` |
| Profil AutoMapper | `DocumentSeriesProfile.cs › DocumentSeriesProfile` |
| Wyjątek WAL-01 | `UserHasNoAssociatedFirmException.cs › UserHasNoAssociatedFirmException` |
| Middleware błędów | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` |
| Snapshot DB | `InvoiceJetDbContextModelSnapshot.cs` — encje `DocumentSeries`, `DocumentType` |
