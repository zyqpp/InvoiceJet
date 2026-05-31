# GET /api/Product/GetAllProductsForUserId — Lista produktów

| Atrybut | Wartość |
|---|---|
| ID | API-10 |
| Metoda | GET |
| URL | `/api/Product/GetAllProductsForUserId` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `ProductController.GetAllProductsForUserId` |
| Serwis | `IProductService.GetUserFirmProducts` |
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
    "name": "Consulting Services",
    "price": 100.00,
    "containsTva": false,
    "unitOfMeasurement": "hr",
    "tvaValue": 19
  }
]
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
