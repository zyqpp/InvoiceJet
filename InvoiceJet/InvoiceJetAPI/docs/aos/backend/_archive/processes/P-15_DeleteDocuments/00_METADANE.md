# Usuwanie dokumentów — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Usuwanie dokumentów |
| Numer procesu | `P-15` |
| Kontroler | `DocumentController` |
| Endpoint główny | `PUT /api/Document/DeleteDocuments` |
| Metoda kontrolera | `DeleteDocuments([FromBody] int[] documentIds)` |
| Serwis aplikacyjny | `DocumentService` |
| Metoda serwisu | `DeleteDocuments(int[] documentIds)` |
| Encje | `Document`, `DocumentProduct` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
