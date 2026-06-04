# AddFirm — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Dodanie firmy` |
| Numer procesu | `P-03` |
| Kontroler(y) | `FirmController` |
| Serwis(y) aplikacyjny | `FirmService`, `DocumentSeriesService` (efekt uboczny), `UserService` (tożsamość) |
| Metoda(y) serwisu | `FirmService.AddFirm`, `FirmService.ManageUserFirmRelation` (prywatna), `DocumentSeriesService.AddInitialDocumentSeries` (warunkowo) |
| DTO żądania | `FirmDto` |
| DTO odpowiedzi | `FirmDto` (z uzupełnionym `Id`) |
| Encje | `Firm` (zapis), `UserFirm` (zapis), `User` (aktualizacja `ActiveUserFirmId` — warunkowo), `DocumentSeries` (zapis × 3 — warunkowo), `DocumentType` (odczyt lookup) |
| Repozytoria | `IFirmRepository` (`_unitOfWork.Firms`), `IUserFirmRepository` (`_unitOfWork.UserFirms`), `IUserRepository` (`_unitOfWork.Users`), `IDocumentSeriesRepository` (`_unitOfWork.DocumentSeries`), `IDocumentTypeRepository` (`_unitOfWork.DocumentTypes`) |
| Wyjątki | brak wyjątków domenowych — błędy jako `DbUpdateException`, `NullReferenceException` → `500` (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | brak (ANAF: tylko `GetFirmDataFromAnaf` — inny proces) |
| Autoryzacja | `[Authorize(Roles = "User")]` dziedziczone z klasy `FirmController` |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `[POZA ZAKRESEM — ETAP FULLSTACK]` |

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-03` | `POST /api/Firm/AddFirm/{isClient}` | `FirmController.AddFirm` | Dodanie nowej firmy (własnej lub klienta) z automatycznym powiązaniem z użytkownikiem |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler | `FirmController.cs › FirmController.AddFirm` |
| Serwis — główna logika | `FirmService.cs › FirmService.AddFirm` |
| Serwis — relacja UserFirm | `FirmService.cs › FirmService.ManageUserFirmRelation` (prywatna) |
| Serwis — serie inicjalne | `DocumentSeriesService.cs › DocumentSeriesService.AddInitialDocumentSeries` |
| Serwis — tożsamość | `UserService.cs › UserService.GetCurrentUserId` |
| AutoMapper | `FirmProfile.cs › FirmProfile` — `CreateMap<Firm, FirmDto>().ReverseMap()` |
| Repozytorium — firma | `FirmRepository.cs` (dziedziczy `GenericRepository<Firm>`) |
| Repozytorium — relacja | `UserFirmRepository.cs › UserFirmRepository.GetUserFirmById` |
| Repozytorium — użytkownik | `UserRepository.cs › UserRepository.GetUserByIdAsync` |
| Jednostka pracy | `UnitOfWork.cs › UnitOfWork.CompleteAsync` (3 wywołania) |
