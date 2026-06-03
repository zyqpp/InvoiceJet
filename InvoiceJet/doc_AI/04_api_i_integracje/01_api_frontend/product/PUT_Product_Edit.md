# PUT /api/Product/EditProduct — Edycja produktu

| Atrybut | Wartość |
|---|---|
| ID | API-12 |
| Metoda | PUT |
| URL | `/api/Product/EditProduct` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `ProductController.EditProduct` |
| Serwis | `IProductService.EditProduct` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Body (JSON) — `ProductDto` z `id > 0`

```json
{
  "id": 1,
  "name": "Consulting Services Updated",
  "price": 120.00,
  "containsTva": true,
  "unitOfMeasurement": "hr",
  "tvaValue": 19
}
```

## Response

### 200 OK — zwraca zaktualizowany `ProductDto`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
