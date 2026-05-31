# PUT /api/DocumentSeries/UpdateDocumentSeries — Edycja serii dokumentów

| Atrybut | Wartość |
|---|---|
| ID | API-20 |
| Metoda | PUT |
| URL | `/api/DocumentSeries/UpdateDocumentSeries` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentSeriesController.UpdateDocumentSeries` |
| Serwis | `IDocumentSeriesService.UpdateDocumentSeries` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Body (JSON) — `[FromBody] DocumentSeriesDto` z `id > 0`

```json
{
  "id": 1,
  "seriesName": "FV",
  "firstNumber": 1,
  "currentNumber": 5,
  "isDefault": true,
  "documentTypeId": 1,
  "documentType": { "id": 1, "name": "Factura" }
}
```

## Response

### 200 OK — pusta odpowiedź

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
