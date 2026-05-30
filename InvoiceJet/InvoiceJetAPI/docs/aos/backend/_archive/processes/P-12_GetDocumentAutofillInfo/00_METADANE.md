# Dane autouzupełniania dokumentu — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Dane autouzupełniania dokumentu |
| Numer procesu | `P-12` |
| Kontroler | `DocumentController` |
| Endpoint główny | `GET /api/Document/GetDocumentAutofillInfo/{documentTypeId}` |
| Metoda kontrolera | `GetDocumentAutofillInfo(int documentTypeId)` |
| Serwis aplikacyjny | `DocumentService` |
| Metoda serwisu | `GetDocumentAutofillInfo(int documentTypeId)` |
| DTO odpowiedzi | `DocumentAutofillDto` |
| Encje | `Firm`, `DocumentSeries`, `DocumentStatus`, `Product`, `UserFirm` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
