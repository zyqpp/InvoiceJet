# POST /api/Product/AddProduct — Dodanie produktu

| Atrybut | Wartość |
|---|---|
| ID | API-11 |
| Metoda | POST |
| URL | `/api/Product/AddProduct` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `ProductController.AddProduct` |
| Serwis | `IProductService.AddProduct` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Body (JSON) — `ProductDto`

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `id` | `int` | TAK (0 dla nowego) | — |
| `name` | `string` | TAK | Unikalna nazwa produktu (UNIQUE INDEX w DB) |
| `price` | `decimal` | TAK | Cena bazowa |
| `containsTva` | `bool` | NIE | Domyślnie `false` |
| `unitOfMeasurement` | `string?` | NIE | Jednostka miary |
| `tvaValue` | `int` | NIE | Procent VAT, domyślnie `19` |

**Przykład:**
```json
{
  "id": 0,
  "name": "Consulting Services",
  "price": 100.00,
  "containsTva": false,
  "unitOfMeasurement": "hr",
  "tvaValue": 19
}
```

## Response

### 200 OK — zwraca `ProductDto` z nadanym `Id`

### Błędy

| Status HTTP | Warunek |
|---|---|
| 500 | Produkt o tej nazwie już istnieje (UNIQUE INDEX naruszenie) |
| 401 Unauthorized | Brak/wygaśnięty token |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
