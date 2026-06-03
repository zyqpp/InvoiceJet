# Pobranie strumienia PDF faktury — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Pobranie strumienia PDF faktury |
| Numer procesu | `P-17` |
| Kontroler | `DocumentController` |
| Endpoint główny | `POST /api/Document/GetInvoicePdfStream` |
| Metoda kontrolera | `GetInvoicePdfStream(DocumentRequestDto documentRequestDto)` |
| Serwis aplikacyjny | `DocumentService` |
| Metoda serwisu | `GetInvoicePdfStream(DocumentRequestDto documentRequestDto)` |
| DTO pośrednie | `DocumentStreamDto` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
