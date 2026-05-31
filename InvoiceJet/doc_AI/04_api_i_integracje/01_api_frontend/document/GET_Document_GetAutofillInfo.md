# GET /api/Document/GetDocumentAutofillInfo/{documentTypeId} — Dane autouzupełniania

| Atrybut | Wartość |
|---|---|
| ID | API-27 |
| Metoda | GET |
| URL | `/api/Document/GetDocumentAutofillInfo/{documentTypeId}` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentController.GetDocumentAutofillInfo` |
| Serwis | `IDocumentService.GetDocumentAutofillInfo` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Path Parameters

| Parametr | Typ | Wartości | Opis |
|---|---|---|---|
| `documentTypeId` | `int` | `1`, `2`, `3` | Typ dokumentu — filtruje serie dokumentów |

## Response

### 200 OK — `DocumentAutofillDto`

```json
{
  "clients": [
    { "id": 10, "name": "Client SRL", "cui": "87654321", ... }
  ],
  "documentSeries": [
    {
      "id": 1,
      "seriesName": "FV",
      "firstNumber": 1,
      "currentNumber": 5,
      "isDefault": true,
      "documentTypeId": 1,
      "documentType": { "id": 1, "name": "Factura" }
    }
  ],
  "documentStatuses": [
    { "id": 1, "status": "Unpaid" },
    { "id": 2, "status": "Paid" }
  ],
  "products": [
    { "id": 1, "name": "Consulting Services", "price": 100.00, ... }
  ]
}
```

### 200 OK — brak aktywnej firmy

```json
{}
```

## Cel

Jednym żądaniem pobiera wszystkie dane potrzebne do formularza tworzenia/edycji faktury. Wywoływany przez `BaseInvoiceComponent.loadAutofillData()` w `ngOnInit`.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
