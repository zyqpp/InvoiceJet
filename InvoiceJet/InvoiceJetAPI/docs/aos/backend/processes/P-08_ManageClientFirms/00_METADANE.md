# Zarządzanie firmami-klientami — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Zarządzanie firmami-klientami |
| Numer procesu | `P-08` |
| Kontroler | `FirmController` |
| Endpointy | `GET /api/Firm/GetUserClientFirms`, `PUT /api/Firm/DeleteFirms` |
| Serwis aplikacyjny | `FirmService` |
| Metody serwisu | `GetUserClientFirms()`, `DeleteFirms(int[] firmIds)` |
| DTO odpowiedzi | `List<FirmDto>` dla `GET` |
| Encje | `Firm`, `UserFirm`, `Document` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
