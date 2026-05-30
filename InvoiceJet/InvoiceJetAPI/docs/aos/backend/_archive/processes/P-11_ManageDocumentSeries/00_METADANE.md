# Zarządzanie seriami dokumentów — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Zarządzanie seriami dokumentów |
| Numer procesu | `P-11` |
| Kontroler | `DocumentSeriesController` |
| Endpointy | `GET /api/DocumentSeries/GetAllDocumentSeriesForUserId`, `POST /api/DocumentSeries/AddDocumentSeries`, `PUT /api/DocumentSeries/UpdateDocumentSeries`, `PUT /api/DocumentSeries/DeleteDocumentSeries` |
| Serwis aplikacyjny | `DocumentSeriesService` |
| Metody serwisu | `GetAllDocumentSeriesForUserId()`, `AddDocumentSeries()`, `UpdateDocumentSeries()`, `DeleteDocumentSeries()` |
| DTO | `DocumentSeriesDto` |
| Encje | `DocumentSeries`, `DocumentType`, `UserFirm` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
