# PUT /api/Document/DeleteDocuments — Usunięcie dokumentów

| Atrybut | Wartość |
|---|---|
| ID | API-26 |
| Metoda | PUT |
| URL | `/api/Document/DeleteDocuments` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentController.DeleteDocuments` |
| Serwis | `IDocumentService.DeleteDocuments` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Body (JSON) — `[FromBody] int[]`

```json
[1, 2, 3]
```

## Response

### 200 OK

```json
{ "message": "Documents deleted successfully." }
```

## Algorytm

1. Pobierz dokumenty z `DocumentProducts` (Include eager loading)
2. `RemoveRangeAsync(DocumentProducts)` — fizyczne usunięcie pozycji
3. `RemoveRangeAsync(Documents)` — fizyczne usunięcie dokumentów
4. `CompleteAsync()`

**Brak soft-delete — dane trwale usunięte.**

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
