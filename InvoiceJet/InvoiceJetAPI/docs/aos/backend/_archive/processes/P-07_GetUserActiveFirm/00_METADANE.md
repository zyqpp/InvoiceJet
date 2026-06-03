# Pobranie aktywnej firmy użytkownika — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Pobranie aktywnej firmy użytkownika |
| Numer procesu | `P-07` |
| Kontroler | `FirmController` |
| Endpoint główny | `GET /api/Firm/GetUserActiveFirm` |
| Metoda kontrolera | `GetUserActiveFirm()` |
| Serwis aplikacyjny | `FirmService` |
| Metoda serwisu | `GetUserActiveFirm()` |
| DTO odpowiedzi | `FirmDto` |
| Encje | `User`, `UserFirm`, `Firm` |
| Repozytoria | `Users` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
