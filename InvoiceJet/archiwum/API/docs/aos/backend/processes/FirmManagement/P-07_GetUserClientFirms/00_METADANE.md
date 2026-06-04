# GetUserClientFirms — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Pobranie firm-klientów użytkownika` |
| Numer procesu | `P-07` |
| Kontroler(y) | `FirmController` |
| Serwis(y) aplikacyjny | `FirmService`, `UserService` (tożsamość) |
| Metoda(y) serwisu | `FirmService.GetUserClientFirms` |
| DTO żądania | brak (endpoint bezparametrowy) |
| DTO odpowiedzi | `List<FirmDto>` (pusta lista gdy brak klientów) |
| Encje | `UserFirm` (odczyt — filtr `IsClient`), `Firm` (odczyt — mapowana do DTO) |
| Repozytoria | `IUserFirmRepository` (`_unitOfWork.UserFirms`) — `GetUserFirmClients` |
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
| `API-07` | `GET /api/Firm/GetUserClientFirms` | `FirmController.GetUserClientFirms` | Pobranie listy firm-klientów (`IsClient=true`) zalogowanego użytkownika |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler | `FirmController.cs › FirmController.GetUserClientFirms` |
| Serwis — główna logika | `FirmService.cs › FirmService.GetUserClientFirms` |
| Serwis — tożsamość | `UserService.cs › UserService.GetCurrentUserId` |
| Repozytorium — zapytanie | `UserFirmRepository.cs › UserFirmRepository.GetUserFirmClients` |
| AutoMapper | `FirmProfile.cs › FirmProfile` — `CreateMap<Firm, FirmDto>().ReverseMap()` |
| Encja wejściowa (filtr) | `UserFirm.cs › UserFirm.IsClient` |
| Encja wyjściowa | `Firm.cs › Firm` (mapowana do `FirmDto`) |
