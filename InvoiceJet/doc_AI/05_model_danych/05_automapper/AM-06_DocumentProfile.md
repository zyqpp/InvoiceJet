# AutoMapper Profile: DocumentProfile

| Atrybut | Wartość |
|---|---|
| ID | AM-06 |
| Plik | `InvoiceJet.Application/MappingProfiles/DocumentProfile.cs` |
| Dotyczy | Dokumenty (faktury, proformy, storna) |
| Złożoność | WYSOKA — niestandardowe mapowania z LINQ projekcją inline |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Mapowania

### Document → DocumentRequestDto (Response — ładowanie do edycji)

```csharp
CreateMap<Document, DocumentRequestDto>()
    .ForMember(dest => dest.Seller,
        opt => opt.MapFrom(src => src.UserFirm))
    .ForMember(dest => dest.Products,
        opt => opt.MapFrom(src =>
            src.DocumentProducts!.Select(dp => new DocumentProductRequestDto {
                ProductId = dp.ProductId,
                Quantity = dp.Quantity,
                Price = dp.Price,
                VatRate = dp.VatRate,
                Name = dp.Product!.Name,
                MeasureUnit = dp.Product!.MeasureUnit
            }).ToList()));
```

#### Mapowania niestandardowe:

| Pole DTO | Źródło | Uwaga |
|---|---|---|
| `Seller` | `Document.UserFirm` | UserFirm → FirmRequestDto przez FirmProfile |
| `Products` | `Document.DocumentProducts` | Inline LINQ projekcja (nie osobny profil!) |
| `Client` | `Document.Client` | AutoMapper przez FirmProfile |
| `DocumentSeries` | `Document.DocumentSeries` | AutoMapper przez DocumentSeriesProfile |
| `BankAccount` | `Document.BankAccount` | AutoMapper przez BankAccountProfile |

### Document → DocumentTableRecordDto (Lista dokumentów)

```csharp
CreateMap<Document, DocumentTableRecordDto>()
    .ForMember(dest => dest.ClientName,
        opt => opt.MapFrom(src => src.Client!.Name))
    .ForMember(dest => dest.TotalValue,
        opt => opt.MapFrom(src => src.TotalPrice));
```

| Pole DTO | Źródło | Uwaga |
|---|---|---|
| `ClientName` | `Document.Client.Name` | JOIN wymagany (include Client) |
| `TotalValue` | `Document.TotalPrice` | Alias — zmiana nazwy |
| Pozostałe pola | Auto | Konwencja nazw |

### DocumentRequestDto → Document (Request — zapis nowego dokumentu)

```csharp
CreateMap<DocumentRequestDto, Document>()
    .ForMember(dest => dest.DocumentProducts, opt => opt.Ignore())
    .ForMember(dest => dest.UserFirmId, opt => opt.Ignore());
    // DocumentProducts i UserFirmId ustawiane ręcznie przez serwis
```

## Krytyczna anomalia — LINQ inline

Projekcja `DocumentProducts` jest wykonywana **inline w profilu** zamiast przez osobny `CreateMap<DocumentProduct, DocumentProductRequestDto>()`. Skutkuje to:
- Brakiem możliwości reużycia mapowania
- Koniecznością manualen aktualizacji dwóch miejsc przy zmianie DTO
- Ukrytą zależnością: `dp.Product!.Name` wymaga Include(`Product`) przy zapytaniu DB

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
