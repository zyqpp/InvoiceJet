# Edycja firmy — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Edycja firmy |
| Numer procesu | `P-06` |
| Kontroler | `FirmController` |
| Endpoint główny | `PUT /api/Firm/EditFirm/{isClient}` |
| Metoda kontrolera | `EditFirm([FromBody] FirmDto firmDto, bool isClient)` |
| Serwis aplikacyjny | `FirmService` |
| Metoda serwisu | `EditFirm(FirmDto firmDto, bool isClient)` |
| DTO żądania | `FirmDto` |
| DTO odpowiedzi | `FirmDto` |
| Encje | `Firm`, `UserFirm` |
| Repozytoria | `Firms`, `UserFirms` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
