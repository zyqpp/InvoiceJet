# DTO: DocumentProductRequestDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-08 |
| Plik | `InvoiceJet.Application/DTOs/DocumentProductRequestDto.cs` |
| Kierunek | Request + Response (zagnieżdżony w DocumentRequestDto) |
| Kontekst | Element listy `DocumentRequestDto.Products` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `ProductId` | `int` | NIE | ID produktu z katalogu |
| `Name` | `string` | TAK | Nazwa produktu (zduplikowana z katalogu — snapshot) |
| `MeasureUnit` | `string` | TAK | Jednostka miary (snapshot) |
| `Quantity` | `decimal` | NIE | Ilość |
| `Price` | `decimal` | NIE | Cena jednostkowa netto (snapshot) |
| `VatRate` | `decimal` | NIE | Stawka VAT % (snapshot) |

## Pattern "snapshot"

Pola `Name`, `MeasureUnit`, `Price`, `VatRate` są kopiowane do pozycji dokumentu w momencie wystawienia — stanowią historyczny zapis wartości nawet jeśli produkt zostanie zmieniony lub usunięty.

## Mapowanie AutoMapper (LINQ inline w profilu)

```csharp
// DocumentProfile — inline LINQ projection
src.DocumentProducts!.Select(dp => new DocumentProductRequestDto {
    ProductId = dp.ProductId,
    Quantity = dp.Quantity,
    Price = dp.Price,
    VatRate = dp.VatRate,
    Name = dp.Product!.Name,
    MeasureUnit = dp.Product!.MeasureUnit
}).ToList()
```

## Wartość pozycji (obliczana na frontendzie)

```
LineGross = Price × Quantity × (1 + VatRate/100)
```

## Przykład JSON

```json
{
  "productId": 7,
  "name": "Programare web",
  "measureUnit": "ore",
  "quantity": 10,
  "price": 150.00,
  "vatRate": 19.00
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
