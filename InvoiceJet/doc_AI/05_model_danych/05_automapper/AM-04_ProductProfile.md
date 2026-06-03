# AutoMapper Profile: ProductProfile

| Atrybut | Wartość |
|---|---|
| ID | AM-04 |
| Plik | `InvoiceJet.Application/MappingProfiles/ProductProfile.cs` |
| Dotyczy | Produkty i usługi katalogu |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Mapowania

### ProductRequestDto → Product

```csharp
CreateMap<ProductRequestDto, Product>();
// Wszystkie pola mapowane automatycznie
```

| Pole DTO | Pole Encji |
|---|---|
| `Id` | `Product.Id` |
| `Name` | `Product.Name` |
| `MeasureUnit` | `Product.MeasureUnit` |
| `Price` | `Product.Price` |
| `VatRate` | `Product.VatRate` |

Pole `UserFirmId` nie jest w DTO — ustawiane ręcznie przez serwis.

### Product → ProductRequestDto

```csharp
CreateMap<Product, ProductRequestDto>();
```

## Uwaga

`Product.UserFirmId` ustawiane ręcznie przez serwis po mapowaniu:

```csharp
var product = _mapper.Map<Product>(productRequestDto);
product.UserFirmId = userFirmId;
await _unitOfWork.Products.AddAsync(product);
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
