# GetDocumentAutofillInfo — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Pobranie danych do autouzupełnienia formularza dokumentu` |
| Numer procesu | `P-16` |
| Kontroler(y) | `DocumentController` |
| Serwis(y) aplikacyjny | `DocumentService` |
| Metoda(y) serwisu | `DocumentService.GetDocumentAutofillInfo` |
| DTO żądania | N/D (parametr trasy `documentTypeId`) |
| DTO odpowiedzi | `DocumentAutofillDto` |
| Encje | `Firm`, `DocumentSeries`, `DocumentType`, `DocumentStatus`, `Product`, `UserFirm` |
| Repozytoria | `IFirmRepository`, `IDocumentSeriesRepository`, `IDocumentStatusRepository`, `IProductRepository`, `IUserRepository` |
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
| `API-27` | `GET /api/Document/GetDocumentAutofillInfo/{documentTypeId}` | `DocumentController.GetDocumentAutofillInfo` | Dane do formularza: klienci, serie, statusy, produkty |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler | `DocumentController.cs › DocumentController.GetDocumentAutofillInfo` |
| Serwis | `DocumentService.cs › DocumentService.GetDocumentAutofillInfo` |
| Repozytorium użytkowników | `UserRepository.cs › UserRepository.GetUserFirmIdAsync` |
| Repozytorium firm | `FirmRepository.cs › FirmRepository.Query` |
| Repozytorium serii | `DocumentSeriesRepository.cs › DocumentSeriesRepository.Query` |
| Repozytorium statusów | `DocumentStatusRepository.cs › DocumentStatusRepository.Query` |
| Repozytorium produktów | `ProductRepository.cs › ProductRepository.Query` |
| Middleware błędów | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` |
