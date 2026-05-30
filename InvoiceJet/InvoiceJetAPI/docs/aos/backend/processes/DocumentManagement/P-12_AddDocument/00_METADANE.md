# AddDocument — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Wystawienie nowego dokumentu (faktury)` |
| Numer procesu | `P-12` |
| Kontroler(y) | `DocumentController` |
| Serwis(y) aplikacyjny | `DocumentService` |
| Metoda(y) serwisu | `DocumentService.AddDocument`, `DocumentService.UpdateDocumentProducts` (prywatna), `DocumentService.IncreaseDocumentSeriesNumber` (prywatna) |
| DTO żądania | `DocumentRequestDto` (zawiera `List<DocumentProductRequestDto>`) |
| DTO odpowiedzi | `DocumentRequestDto` (oryginalny obiekt żądania — bez nadanego Id) |
| Encje | `Document`, `DocumentProduct`, `Product` (nowe), `DocumentSeries` (CurrentNumber++), `BankAccount` (odczyt) |
| Repozytoria | `IDocumentRepository`, `IDocumentProductRepository`, `IProductRepository`, `IDocumentSeriesRepository`, `IBankAccountRepository`, `IUserRepository` |
| Wyjątki | `UserHasNoAssociatedFirmException`, `NoBankAccountAddedException` (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | brak (PDF nie jest generowany w tym procesie — P-17) |
| Autoryzacja | `[Authorize(Roles = "User")]` na klasie `DocumentController` |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `POZA ZAKRESEM — ETAP FULLSTACK` |

---

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-22` | `POST /api/Document/AddDocument` | `DocumentController.AddDocument` | Wystawienie nowego dokumentu (faktury / proforma / storno) |

---

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler | `DocumentController.cs › DocumentController.AddDocument` |
| Serwis — główna | `DocumentService.cs › DocumentService.AddDocument` |
| Serwis — pozycje | `DocumentService.cs › DocumentService.UpdateDocumentProducts` |
| Serwis — seria | `DocumentService.cs › DocumentService.IncreaseDocumentSeriesNumber` |
| Repozytorium dokumentów | `DocumentRepository.cs › DocumentRepository` (GetByIdAsync z GenericRepository) |
| Repozytorium pozycji | `DocumentProductRepository.cs › DocumentProductRepository.GetAllDocumentProductsForDocument` |
| Repozytorium produktów | `GenericRepository.cs › GenericRepository.AddAsync` / `.Query()` |
| Repozytorium serii | `GenericRepository.cs › GenericRepository.GetByIdAsync` / `.UpdateAsync` |
| DTO główne | `DocumentRequestDto.cs › DocumentRequestDto` |
| DTO pozycji | `DocumentProductRequestDto.cs › DocumentProductRequestDto` |
| Profil AutoMapper (produkt) | `DocumentProductProfile.cs › DocumentProductProfile` |
| Wyjątek WAL-01 | `UserHasNoAssociatedFirmException.cs › UserHasNoAssociatedFirmException` |
| Wyjątek WAL-02 | `NoBankAccountAddedException.cs › NoBankAccountAddedException` |
| Middleware błędów | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` |
| Snapshot DB | `InvoiceJetDbContextModelSnapshot.cs` — encje `Document`, `DocumentProduct` |
