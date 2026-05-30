# Statystyki dashboardu — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Statystyki dashboardu |
| Numer procesu | `P-18` |
| Kontroler | `DocumentController` |
| Endpoint główny | `GET /api/Document/GetDashboardStats/{year}/{documentType}` |
| Metoda kontrolera | `GetDashboardStats(int year, int documentType)` |
| Serwis aplikacyjny | `DocumentService` |
| Metoda serwisu | `GetDashboardStats(int year, int documentType)` |
| DTO odpowiedzi | `DashboardStatsDto` |
| Encje | `Document`, `Firm`, `Product`, `BankAccount`, `UserFirm` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
