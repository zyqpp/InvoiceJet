# ManageClientFirms — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Zarządzanie firmami-klientami` |
| Numer procesu | `P-08` |
| Kontroler(y) | `FirmController` |
| Serwis(y) aplikacyjny | `FirmService` |
| Metoda(y) serwisu | `FirmService.GetUserClientFirms`, `FirmService.DeleteFirms` |
| DTO żądania | N/D (GET brak body, DELETE parametr) |
| DTO odpowiedzi | `FirmDto[]` (GET), N/D (DELETE zwraca pusty OK) |
| Encje | `Firm`, `UserFirm`, `Document` (tylko do walidacji) |
| Repozytoria | `IFirmRepository`, `IUserFirmRepository`, `IDocumentRepository` |
| Wyjątki | `Exception` (generyczny, WAL-01 [UWAGA]), `FirmAssociatedWithDocumentException` (WAL-02) — link: `../../KATALOG_WYJATKOW.md` |
| Integracje | brak |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `FirmController`) |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `[POZA ZAKRESEM — ETAP FULLSTACK]` |

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-08` | `GET /api/Firm/GetUserClientFirms` | `FirmController.GetUserClientFirms` | Pobranie listy firm-klientów użytkownika |
| `API-09` | `PUT /api/Firm/DeleteFirms` | `FirmController.DeleteFirms` | Usunięcie wybranych firm-klientów |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler — GET | `FirmController.cs › FirmController.GetUserClientFirms` |
| Kontroler — DELETE | `FirmController.cs › FirmController.DeleteFirms` |
| Serwis — GET | `FirmService.cs › FirmService.GetUserClientFirms` |
| Serwis — DELETE | `FirmService.cs › FirmService.DeleteFirms` |
| Repozytorium — UserFirm | `UserFirmRepository.cs › UserFirmRepository.GetUserFirmClients` |
| Repozytorium — Firm | `FirmRepository.cs › (GenericRepository methods)` |
| Repozytorium — Document | `DocumentRepository.cs › DocumentRepository.Query` |
| AutoMapper | `FirmProfile.cs › FirmProfile.CreateMap<Firm, FirmDto>()` |
| Serwis użytkownika | `UserService.cs › UserService.GetCurrentUserId` |
