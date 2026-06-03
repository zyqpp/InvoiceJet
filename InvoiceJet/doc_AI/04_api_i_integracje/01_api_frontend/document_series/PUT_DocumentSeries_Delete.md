# PUT /api/DocumentSeries/DeleteDocumentSeries — Usunięcie serii dokumentów

| Atrybut | Wartość |
|---|---|
| ID | API-21 |
| Metoda | PUT |
| URL | `/api/DocumentSeries/DeleteDocumentSeries` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentSeriesController.DeleteDocumentSeries` |
| Serwis | `IDocumentSeriesService.DeleteDocumentSeries` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

> **Anomalia A-03:** `PUT` zamiast `DELETE` do usuwania.  
> **Anomalia A-07:** `int[] documentSeriesIds` bez `[FromBody]` → binding z query string.

## Request

### Parametr (query string — nie body!)

**Przykład URL:**
```
PUT /api/DocumentSeries/DeleteDocumentSeries?documentSeriesIds=1&documentSeriesIds=2
```

## Response

### 200 OK — pusta odpowiedź

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny z anomaliami. |
