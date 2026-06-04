# GetDashboardStats — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Pobranie statystyk dashboardu` |
| Numer procesu | `P-18` |
| Kontroler(y) | `DocumentController` |
| Serwis(y) aplikacyjny | `DocumentService` |
| Metoda(y) serwisu | `DocumentService.GetDashboardStats`, `DocumentService.GetTotalDocumentsAsync` (prywatna), `DocumentService.GetMonthlyTotalsAsync` (prywatna) |
| DTO żądania | N/D (parametry trasy) |
| DTO odpowiedzi | `DashboardStatsDto` (z zagnieżdżonym `List<MonthlyTotalDto>`) |
| Encje | `Document`, `DocumentType`, `DocumentStatus`, `Firm`, `Product`, `BankAccount`, `UserFirm` |
| Repozytoria | `IUserRepository`, `IDocumentRepository`, `IFirmRepository`, `IProductRepository`, `IBankAccountRepository` |
| Wyjątki | brak wyjątków domenowych (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | brak |
| Autoryzacja | `[Authorize(Roles = "User")]` na klasie `DocumentController` |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `POZA ZAKRESEM — ETAP FULLSTACK` |

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-30` | `GET /api/Document/GetDashboardStats/{year}/{documentType}` | `DocumentController.GetDashboardStats` | Statystyki dla dashboardu (liczniki + zestawienie miesięczne) |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler | `DocumentController.cs › DocumentController.GetDashboardStats` |
| Serwis główna | `DocumentService.cs › DocumentService.GetDashboardStats` |
| Serwis pomocnicza (dokumenty) | `DocumentService.cs › DocumentService.GetTotalDocumentsAsync` |
| Serwis pomocnicza (miesięcznie) | `DocumentService.cs › DocumentService.GetMonthlyTotalsAsync` |
| Repozytorium użytkowników | `UserRepository.cs › UserRepository.GetUserFirmAsync` |
| Repozytorium dokumentów | `DocumentRepository.cs › DocumentRepository.Query` |
| Repozytorium firm | `FirmRepository.cs › FirmRepository.GetTotalClientsAsync` |
| Repozytorium produktów | `ProductRepository.cs › ProductRepository.GetTotalProductsAsync` |
| Repozytorium kont bankowych | `BankAccountRepository.cs › BankAccountRepository.GetTotalBankAccountsAsync` |
| Middleware błędów | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` |
