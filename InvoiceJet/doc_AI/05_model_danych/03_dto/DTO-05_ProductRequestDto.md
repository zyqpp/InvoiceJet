# DTO: ProductRequestDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-05 |
| Plik | `InvoiceJet.Application/DTOs/ProductRequestDto.cs` |
| Kierunek | Request + Response (dwukierunkowy) |
| Endpointy | `GET /api/Product/GetAll`, `POST /api/Product/Add`, `PUT /api/Product/Edit` |
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
