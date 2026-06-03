# GetUserActiveFirm — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Pobranie aktywnej firmy użytkownika` |
| Numer procesu | `P-06` |
| Kontroler(y) | `FirmController` |
| Serwis(y) aplikacyjny | `FirmService`, `UserService` (tożsamość) |
| Metoda(y) serwisu | `FirmService.GetUserActiveFirm` |
| DTO żądania | brak (endpoint bezparametrowy) |
| DTO odpowiedzi | `FirmDto` (pusty gdy brak aktywnej firmy) |
| Encje | `User` (odczyt), `UserFirm` (odczyt — `ActiveUserFirm`), `Firm` (odczyt — mapowana do DTO) |
| Repozytoria | `IUserRepository` (`_unitOfWork.Users`) — `GetUserFirmAsync` |
| Wyjątki | brak wyjątków domenowych (proces read-only, defensywny) |
| Integracje | brak |
| Autoryzacja | `[Authorize(Roles = "User")]` dziedziczone z klasy `FirmController` |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `[POZA ZAKRESEM — ETAP FULLSTACK]` |

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-06` | `GET /api/Firm/GetUserActiveFirm` | `FirmController.GetUserActiveFirm` | Pobranie danych aktywnej firmy zalogowanego użytkownika |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler | `FirmController.cs › FirmController.GetUserActiveFirm` |
| Serwis — główna logika | `FirmService.cs › FirmService.GetUserActiveFirm` |
| Serwis — tożsamość | `UserService.cs › UserService.GetCurrentUserId` |
| Repozytorium — zapytanie | `UserRepository.cs › UserRepository.GetUserFirmAsync` |
| AutoMapper | `FirmProfile.cs › FirmProfile` — `CreateMap<Firm, FirmDto>().ReverseMap()` |
| Encja wejściowa | `User.cs › User.ActiveUserFirm` (FK `ActiveUserFirmId`, nullable) |
| Encja wyjściowa | `Firm.cs › Firm` (mapowana do `FirmDto`) |
