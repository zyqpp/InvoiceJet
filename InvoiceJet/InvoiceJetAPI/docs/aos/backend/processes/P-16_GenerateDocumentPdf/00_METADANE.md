# Generowanie dokumentu PDF — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Generowanie dokumentu PDF |
| Numer procesu | `P-16` |
| Kontroler | `DocumentController` |
| Endpoint główny | `POST /api/Document/GenerateDocumentPdf` |
| Metoda kontrolera | `GenerateDocument(DocumentRequestDto documentRequestDTO)` |
| Serwis aplikacyjny | `DocumentService` |
| Metoda serwisu | `GeneratePdfDocument(DocumentRequestDto documentRequestDto)` |
| Serwis infrastrukturalny | `PdfGenerationService` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
