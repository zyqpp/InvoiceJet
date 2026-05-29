# Dodanie firmy — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Dodanie firmy |
| Numer procesu | `P-02` |
| Projekt | `InvoiceJetAPI` |
| Kontroler | `FirmController` |
| Endpoint główny | `POST /api/Firm/AddFirm/{isClient}` |
| Metoda kontrolera | `AddFirm(FirmDto firmDto, bool isClient)` |
| Serwis aplikacyjny | `FirmService` |
| Metoda serwisu | `AddFirm(FirmDto firmDto, bool isClient)` |
| DTO żądania | `FirmDto` |
| DTO odpowiedzi | `FirmDto` |
| Encje | `Firm`, `UserFirm`, `User`, `DocumentSeries` |
| Repozytoria | `Firms`, `UserFirms`, `Users`, `DocumentSeries`, `DocumentTypes` |
| Autoryzacja | `[Authorize(Roles = "User")]` na `FirmController` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |

---

## Pliki źródłowe

| Obszar | Plik |
|---|---|
| Kontroler | `InvoiceJet.Presentation/Controllers/FirmController.cs` |
| Serwis | `InvoiceJet.Application/Services/Impl/FirmService.cs` |
| Interfejs serwisu | `InvoiceJet.Application/Services/IFirmService.cs` |
| DTO firmy | `InvoiceJet.Application/DTOs/FirmDto.cs` |
| Encja firmy | `InvoiceJet.Domain/Models/Firm.cs` |
| Encja relacji użytkownik-firma | `InvoiceJet.Domain/Models/UserFirm.cs` |
| Serwis serii dokumentów | `InvoiceJet.Application/Services/Impl/DocumentSeriesService.cs` |
| Repozytorium relacji | `InvoiceJet.Infrastructure/Persistence/Repositories/UserFirmRepository.cs` |
| Middleware błędów | `InvoiceJet.Presentation/Middleware/ExceptionMiddleware.cs` |

---

## Dokumenty procesu

- [01_PRZEGLAD_PROCESU.md](01_PRZEGLAD_PROCESU.md)
- [02_KONTRAKT_API.md](02_KONTRAKT_API.md)
- [03_LOGIKA_APLIKACYJNA.md](03_LOGIKA_APLIKACYJNA.md)
- [04_DANE_MODELE_MAPOWANIA.md](04_DANE_MODELE_MAPOWANIA.md)
- [05_BLEDY_BEZPIECZENSTWO.md](05_BLEDY_BEZPIECZENSTWO.md)
- [06_SCENARIUSZE_TESTOWE.md](06_SCENARIUSZE_TESTOWE.md)
- [HISTORIA_ZMIAN.md](HISTORIA_ZMIAN.md)
