# GET /api/DocumentSeries/GetAllDocumentSeriesForUserId — Lista serii dokumentów

| Atrybut | Wartość |
|---|---|
| ID | API-18 |
| Metoda | GET |
| URL | `/api/DocumentSeries/GetAllDocumentSeriesForUserId` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentSeriesController.GetAllDocumentSeriesForUserId` |
| Serwis | `IDocumentSeriesService.GetAllDocumentSeriesForUserId` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

Brak parametrów. userFirmId pobierany z JWT tokenu.

## Response

### 200 OK

```json
[
  {
    "id": 1,
    "seriesName": "FV",
    "firstNumber": 1,
    "currentNumber": 5,
    "isDefault": true,
    "documentTypeId": 1,
    "documentType": {
      "id": 1,
      "name": "Factura"
    }
  }
]
```

**Uwaga:** `documentType` to zagnieżdżona encja domenowa (nie DTO) — anomalia DTO-06-A.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
