# Lista i szczegóły dokumentów — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Lista i szczegóły dokumentów |
| Numer procesu | `P-14` |
| Kontroler | `DocumentController` |
| Endpointy | `GET /api/Document/GetDocumentTableRecords/{documentTypeId}`, `GET /api/Document/GetDocumentById/{documentId}` |
| Serwis aplikacyjny | `DocumentService` |
| Metody serwisu | `GetDocumentTableRecords(int documentTypeId)`, `GetDocumentById(int documentId)` |
| DTO | `List<DocumentTableRecordDto>`, `DocumentRequestDto` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
