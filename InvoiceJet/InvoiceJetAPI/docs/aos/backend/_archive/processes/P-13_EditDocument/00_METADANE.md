# Edycja dokumentu — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Edycja dokumentu |
| Numer procesu | `P-13` |
| Kontroler | `DocumentController` |
| Endpoint główny | `PUT /api/Document/EditDocument` |
| Metoda kontrolera | `EditDocument(DocumentRequestDto documentRequestDto)` |
| Serwis aplikacyjny | `DocumentService` |
| Metoda serwisu | `EditDocument(DocumentRequestDto documentRequestDto)` |
| DTO wejścia/wyjścia | `DocumentRequestDto` |
| Encje | `Document`, `DocumentProduct`, `Product` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
