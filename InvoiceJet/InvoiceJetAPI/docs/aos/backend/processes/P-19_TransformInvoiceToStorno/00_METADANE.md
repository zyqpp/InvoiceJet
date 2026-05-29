# Transformacja faktury do storna — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Transformacja faktury do storna |
| Numer procesu | `P-19` |
| Kontroler | `DocumentController` |
| Endpoint główny | `PUT /api/Document/TransformToStorno` |
| Metoda kontrolera | `TransformToStorno([FromBody] int[] documentIds)` |
| Serwis aplikacyjny | `DocumentService` |
| Metoda serwisu | `TransformToStorno(int[] documentIds)` |
| Encje | `Document`, `UserFirm` |
| Enum | `DocumentTypeEnum.StornoInvoice` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
