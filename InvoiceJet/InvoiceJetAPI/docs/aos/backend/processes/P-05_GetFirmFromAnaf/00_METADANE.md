# Pobranie firmy z ANAF — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Pobranie firmy z ANAF |
| Numer procesu | `P-05` |
| Kontroler | `FirmController` |
| Endpoint główny | `GET /api/Firm/fromAnaf/{cui}` |
| Metoda kontrolera | `GetFirmDataFromAnaf(string cui)` |
| Serwis aplikacyjny | `FirmService` |
| Metoda serwisu | `GetFirmDataFromAnaf(string cui)` |
| DTO żądania | Parametr trasy `cui` |
| DTO odpowiedzi | `FirmDto` |
| Integracje | Zewnętrzne API ANAF (`AppSettings:AnafApiUrl`) |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
