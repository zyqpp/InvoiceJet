# DTO: ProductRequestDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-05 |
| Plik | `InvoiceJet.Application/DTOs/ProductRequestDto.cs` |
| Kierunek | Request + Response (dwukierunkowy) |
| Endpointy | [GET /api/Product/GetAll](../../04_api_i_integracje/01_api_frontend/product/GET_Product_GetAll.md), [POST /api/Product/Add](../../04_api_i_integracje/01_api_frontend/product/POST_Product_Add.md), [PUT /api/Product/Edit](../../04_api_i_integracje/01_api_frontend/product/PUT_Product_Edit.md) |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `Id` | `int` | NIE | ID produktu (0 przy dodawaniu) |
| `Name` | `string` | NIE | Nazwa produktu/usługi (UNIQUE w DB!) |
| `MeasureUnit` | `string` | NIE | Jednostka miary (np. buc, kg, ore, luni) |
| `Price` | `decimal` | NIE | Cena jednostkowa netto |
| `VatRate` | `decimal` | NIE | Stawka VAT w % (np. 19.00) |

## Mapowanie AutoMapper

| Kierunek | Profile |
|---|---|
| `ProductRequestDto` → `Product` | `ProductProfile` |
| `Product` → `ProductRequestDto` | `ProductProfile` |

## Ograniczenie UNIQUE

`Product.Name` ma globalny UNIQUE INDEX w bazie — dwóch użytkowników nie może mieć produktu o tej samej nazwie.

## Przykład JSON

```json
{
  "id": 7,
  "name": "Programare web",
  "measureUnit": "ore",
  "price": 150.00,
  "vatRate": 19.00
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
