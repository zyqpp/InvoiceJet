# POST /api/DocumentSeries/AddDocumentSeries — Dodanie serii dokumentów

| Atrybut | Wartość |
|---|---|
| ID | API-19 |
| Metoda | POST |
| URL | `/api/DocumentSeries/AddDocumentSeries` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentSeriesController.AddDocumentSeries` |
| Serwis | `IDocumentSeriesService.AddDocumentSeries` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

> **Anomalia A-05:** Kontroler ma własny `try/catch` — omija `ExceptionMiddleware`. Błąd zwracany jako `BadRequest(ex.Message)` — plain string, nie JSON.

## Request

### Body (JSON) — `[FromBody] DocumentSeriesDto`

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `id` | `int` | TAK (0 dla nowej) | — |
| `seriesName` | `string` | TAK | Prefiks (np. "FV", "PRO") |
| `firstNumber` | `int` | TAK | Pierwsza wartość numeracji |
| `currentNumber` | `int` | TAK | Bieżący numer (zazwyczaj = firstNumber) |
| `isDefault` | `bool` | TAK | Czy domyślna seria |
| `documentTypeId` | `int?` | NIE | Id typu dokumentu (1=Faktura, 2=Proforma, 3=Storno) |
| `documentType` | `object?` | NIE | Obiekt `{id, name}` — używany do mapowania `documentTypeId` |

**Przykład:**
```json
{
  "id": 0,
  "seriesName": "FV",
  "firstNumber": 1,
  "currentNumber": 1,
  "isDefault": true,
  "documentTypeId": 1,
  "documentType": { "id": 1, "name": "Factura" }
}
```

## Response

### 200 OK — pusta odpowiedź

### Błędy

| Status HTTP | Warunek |
|---|---|
| 400 Bad Request | Dowolny wyjątek — `BadRequest(ex.Message)` (plain string, nie JSON) |
| 401 Unauthorized | Brak/wygaśnięty token |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny z anomalią A-05. |
