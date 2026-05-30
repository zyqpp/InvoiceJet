# EditFirm — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Edycja danych firmy` |
| Numer procesu | `P-05` |
| Kontroler(y) | `FirmController` |
| Serwis(y) aplikacyjny | `FirmService`, `DocumentSeriesService` (efekt uboczny — scenariusz niestandardowy), `UserService` (tożsamość) |
| Metoda(y) serwisu | `FirmService.EditFirm`, `FirmService.ManageUserFirmRelation` (prywatna, współdzielona z P-03) |
| DTO żądania | `FirmDto` |
| DTO odpowiedzi | `FirmDto` (echo żądania — bez ponownego odczytu z DB) |
| Encje | `Firm` (aktualizacja), `UserFirm` (aktualizacja `IsClient` — normalny scenariusz), `UserFirm` (insert — scenariusz niestandardowy), `User` (aktualizacja `ActiveUserFirmId` — scenariusz niestandardowy), `DocumentSeries` (insert × 3 — scenariusz niestandardowy) |
| Repozytoria | `IFirmRepository` (`_unitOfWork.Firms`) — `GetByIdAsync`, `IUserFirmRepository` (`_unitOfWork.UserFirms`) — `GetUserFirmById`, `IUserRepository` (`_unitOfWork.Users`) — `GetUserByIdAsync` (scenariusz niestandardowy) |
| Wyjątki | `Exception("Firm not found.")` → catch-all → `500` (brak dedykowanego wyjątku domenowego — link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | brak |
| Autoryzacja | `[Authorize(Roles = "User")]` dziedziczone z klasy `FirmController` |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `[POZA ZAKRESEM — ETAP FULLSTACK]` |

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-05` | `PUT /api/Firm/EditFirm/{isClient}` | `FirmController.EditFirm` | Edycja pełnego zestawu danych istniejącej firmy oraz jej roli (klient / własna) |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler | `FirmController.cs › FirmController.EditFirm` |
| Serwis — główna logika | `FirmService.cs › FirmService.EditFirm` |
| Serwis — relacja UserFirm | `FirmService.cs › FirmService.ManageUserFirmRelation` (prywatna, współdzielona z P-03) |
| Serwis — serie inicjalne | `DocumentSeriesService.cs › DocumentSeriesService.AddInitialDocumentSeries` (warunkowo, scenariusz niestandardowy) |
| Serwis — tożsamość | `UserService.cs › UserService.GetCurrentUserId` |
| AutoMapper | `FirmProfile.cs › FirmProfile` — `CreateMap<Firm, FirmDto>().ReverseMap()` |
| Repozytorium — firma | `FirmRepository.cs` (dziedziczy `GenericRepository<Firm>`) — `GetByIdAsync` |
| Repozytorium — relacja | `UserFirmRepository.cs › UserFirmRepository.GetUserFirmById` |
| Repozytorium — użytkownik | `UserRepository.cs › UserRepository.GetUserByIdAsync` (scenariusz niestandardowy) |
| Jednostka pracy | `UnitOfWork.cs › UnitOfWork.CompleteAsync` (2 wywołania) |
