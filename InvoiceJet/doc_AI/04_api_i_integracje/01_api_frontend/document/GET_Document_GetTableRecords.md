# GET /api/Document/GetDocumentTableRecords/{documentTypeId} — Lista dokumentów

| Atrybut | Wartość |
|---|---|
| ID | API-24 |
| Metoda | GET |
| URL | `/api/Document/GetDocumentTableRecords/{documentTypeId}` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentController.GetDocumentTableRecords` |
| Serwis | `IDocumentService.GetDocumentTableRecords` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Path Parameters

| Parametr | Typ | Wartości | Opis |
|---|---|---|---|
| `documentTypeId` | `int` | `1=Faktura`, `2=Proforma`, `3=Storno` | Typ dokumentów do pobrania |

## Response

### 200 OK

```json
[
  {
    "id": 1,
    "documentNumber": "FV0001",
    "clientName": "Client SRL",
    "issueDate": "2026-05-31T00:00:00",
    "dueDate": "2026-06-14T00:00:00",
    "totalValue": 119.00,
    "documentStatus": {
      "id": 1,
      "status": "Unpaid"
    }
  }
]
```

**Uwaga:** `documentStatus` to zagnieżdżona encja domenowa, nie DTO.

### 200 OK — brak aktywnej firmy

```json
[]
```

## Mapowanie

`Document.Client.Name → clientName`, `Document.TotalPrice → totalValue` (AutoMapper DocumentProfile).

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
