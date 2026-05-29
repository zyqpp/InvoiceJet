# Wystawienie nowej faktury — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Wystawienie nowej faktury |
| Numer procesu | `P-01` |
| Projekt | `InvoiceJetAPI` |
| Kontroler | `DocumentController` |
| Endpoint główny | `POST /api/Document/AddDocument` |
| Metoda kontrolera | `AddDocument(DocumentRequestDto documentRequestDto)` |
| Serwis aplikacyjny | `DocumentService` |
| Metoda serwisu | `AddDocument(DocumentRequestDto documentRequestDto)` |
| DTO żądania | `DocumentRequestDto` |
| DTO odpowiedzi | `DocumentRequestDto` |
| Encje | `Document`, `DocumentProduct`, `Product`, `BankAccount`, `DocumentSeries`, `UserFirm` |
| Repozytoria | `Users`, `BankAccounts`, `Documents`, `DocumentProducts`, `Products`, `DocumentSeries` |
| Autoryzacja | `[Authorize(Roles = "User")]` na `DocumentController` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |

---

## Pliki źródłowe

| Obszar | Plik |
|---|---|
| Kontroler | `InvoiceJet.Presentation/Controllers/DocumentController.cs` |
| Serwis | `InvoiceJet.Application/Services/Impl/DocumentService.cs` |
| Interfejs serwisu | `InvoiceJet.Application/Services/IDocumentService.cs` |
| DTO dokumentu | `InvoiceJet.Application/DTOs/DocumentRequestDto.cs` |
| DTO pozycji dokumentu | `InvoiceJet.Application/DTOs/DocumentProductRequestDto.cs` |
| DTO serii dokumentu | `InvoiceJet.Application/DTOs/DocumentSeriesDto.cs` |
| Encja dokumentu | `InvoiceJet.Domain/Models/Document.cs` |
| Encja pozycji dokumentu | `InvoiceJet.Domain/Models/DocumentProduct.cs` |
| Repozytorium dokumentów | `InvoiceJet.Infrastructure/Persistence/Repositories/DocumentRepository.cs` |
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
