# GetFirmFromAnaf — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Pobranie danych firmy z ANAF` |
| Numer procesu | `P-04` |
| Kontroler(y) | `FirmController` |
| Serwis(y) aplikacyjny | `FirmService` |
| Metoda(y) serwisu | `FirmService.GetFirmDataFromAnaf` |
| DTO żądania | brak (parametr trasy `cui`) |
| DTO odpowiedzi | `FirmDto` (Id zawsze 0) |
| Encje | brak — proces nie dotyka bazy danych |
| Repozytoria | brak |
| Wyjątki | `AnafFirmNotFoundException` → `404` (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | **ANAF REST API** — `https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva` |
| Autoryzacja | `[Authorize(Roles = "User")]` dziedziczone z klasy `FirmController` |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `[POZA ZAKRESEM — ETAP FULLSTACK]` |

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-04` | `GET /api/Firm/fromAnaf/{cui}` | `FirmController.GetFirmDataFromAnaf` | Pobranie danych firmy z publicznego ANAF API na podstawie numeru CUI (autofill formularza) |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler | `FirmController.cs › FirmController.GetFirmDataFromAnaf` |
| Serwis — główna logika | `FirmService.cs › FirmService.GetFirmDataFromAnaf` |
| Konfiguracja URL ANAF | `appsettings.json › AppSettings:AnafApiUrl` |
| HttpClient | `FirmService.cs:24` — `new HttpClient()` (bez IHttpClientFactory) |
| Wyjątek domenowy | `AnafFirmNotFoundException.cs` |
