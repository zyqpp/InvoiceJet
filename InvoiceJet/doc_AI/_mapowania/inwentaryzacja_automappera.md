# Inwentaryzacja AutoMapper — profile mapowań

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Źródło | `InvoiceJetAPI/InvoiceJet.Application/MappingProfiles/` |

## Lista profili (7)

| ID | Profil | Plik | Mapowania | Dokument | Status |
|---|---|---|---|---|---|
| AM-01 | `BankAccountProfile` | `BankAccountProfile.cs` | `BankAccount ↔ BankAccountDto` (ReverseMap) | [link](../05_model_danych/04_automapper/AM-01_BankAccountProfile.md) | szkic |
| AM-02 | `FirmProfile` | `FirmProfile.cs` | `Firm ↔ FirmDto` (ReverseMap) | [link](../05_model_danych/04_automapper/AM-02_FirmProfile.md) | szkic |
| AM-03 | `ProductProfile` | `ProductProfile.cs` | `Product ↔ ProductDto` (ReverseMap) | [link](../05_model_danych/04_automapper/AM-03_ProductProfile.md) | szkic |
| AM-04 | `DocumentStatusProfile` | `DocumentStatusProfile.cs` | `DocumentStatus ↔ DocumentStatusDto` (ReverseMap) | [link](../05_model_danych/04_automapper/AM-04_DocumentStatusProfile.md) | szkic |
| AM-05 | `DocumentSeriesProfile` | `DocumentSeriesProfile.cs` | `DocumentSeries → DocumentSeriesDto`, `DocumentSeriesDto → DocumentSeries` (custom) | [link](../05_model_danych/04_automapper/AM-05_DocumentSeriesProfile.md) | szkic |
| AM-06 | `DocumentProductProfile` | `DocumentProductProfile.cs` | `DocumentProductRequestDto → Product` (custom, jednostronny) | [link](../05_model_danych/04_automapper/AM-06_DocumentProductProfile.md) | szkic |
| AM-07 | `DocumentProfile` | `DocumentProfile.cs` | `Document → DocumentRequestDto`, `Document → DocumentTableRecordDto` (custom) | [link](../05_model_danych/04_automapper/AM-07_DocumentProfile.md) | szkic |

## Szczegóły mapowań

### AM-01 `BankAccountProfile`

```csharp
CreateMap<BankAccount, BankAccountDto>().ReverseMap();
```

- Mapowanie symetryczne — wszystkie pola tej samej nazwy mapowane automatycznie.
- `ReverseMap()` tworzy odwrotne mapowanie `BankAccountDto → BankAccount`.

---

### AM-02 `FirmProfile`

```csharp
CreateMap<Firm, FirmDto>().ReverseMap();
```

- Mapowanie symetryczne.
- `ReverseMap()` tworzy `FirmDto → Firm`.

---

### AM-03 `ProductProfile`

```csharp
CreateMap<Product, ProductDto>().ReverseMap();
```

- Mapowanie symetryczne.
- `ReverseMap()` tworzy `ProductDto → Product`.

---

### AM-04 `DocumentStatusProfile`

```csharp
CreateMap<DocumentStatus, DocumentStatusDto>().ReverseMap();
```

- Mapowanie symetryczne.
- `ReverseMap()` tworzy `DocumentStatusDto → DocumentStatus`.

---

### AM-05 `DocumentSeriesProfile`

```csharp
// DocumentSeries → DocumentSeriesDto (automatyczne — te same nazwy pól)
CreateMap<DocumentSeries, DocumentSeriesDto>();

// DocumentSeriesDto → DocumentSeries (z konfiguracją)
CreateMap<DocumentSeriesDto, DocumentSeries>()
    .ForMember(dest => dest.DocumentTypeId,
               opt => opt.MapFrom(src => src.DocumentType!.Id))
    .ForMember(dest => dest.DocumentType, opt => opt.Ignore());
```

- Kierunek `DocumentSeriesDto → DocumentSeries`: `DocumentTypeId` pobierane z zagnieżdżonego `src.DocumentType.Id`.
- `DocumentType` na encji domenowej ignorowany (nie mapowany z DTO).
- **Uwaga:** `src.DocumentType!.Id` — użycie `!` (null-forgiving operator); jeśli `DocumentType` jest null, wyrzuci `NullReferenceException`.

---

### AM-06 `DocumentProductProfile`

```csharp
CreateMap<DocumentProductRequestDto, Product>()
    .ForMember(dest => dest.Price,
               opt => opt.MapFrom(src => src.UnitPrice))
    .ForMember(dest => dest.UserFirm,    opt => opt.Ignore())
    .ForMember(dest => dest.UserFirmId,  opt => opt.Ignore());
```

- Tylko kierunek `DocumentProductRequestDto → Product` (jednostronny — brak `ReverseMap`).
- `Price` ← `UnitPrice` (zmiana nazwy pola).
- `UserFirm` i `UserFirmId` ignorowane (uzupełniane przez serwis).
- **Uwaga:** Brak odwrotnego mapowania `Product → DocumentProductRequestDto` — realizowane ręcznie w `DocumentProfile` (inline projection LINQ).

---

### AM-07 `DocumentProfile`

```csharp
// Document → DocumentRequestDto (używane przy pobieraniu dokumentu)
CreateMap<Document, DocumentRequestDto>()
    .ForMember(dest => dest.Id,     opt => opt.MapFrom(src => src.Id))
    .ForMember(dest => dest.Seller, opt => opt.MapFrom(src => src.UserFirm))
    .ForMember(dest => dest.Products, opt => opt.MapFrom(src =>
        src.DocumentProducts!.Select(dp => new DocumentProductRequestDto
        {
            Id                 = dp.Id,
            Name               = dp.Product!.Name,
            UnitPrice          = dp.UnitPrice,
            TotalPrice         = dp.TotalPrice,
            ContainsTva        = dp.Product.ContainsTva,
            UnitOfMeasurement  = dp.Product.UnitOfMeasurement!,
            TvaValue           = dp.Product != null ? dp.Product.TvaValue : 0,
            Quantity           = (int)dp.Quantity
        }).ToList()));

// Document → DocumentTableRecordDto (używane przy listowaniu)
CreateMap<Document, DocumentTableRecordDto>()
    .ForMember(dest => dest.ClientName,
               opt => opt.MapFrom(src => src.Client!.Name))
    .ForMember(dest => dest.TotalValue,
               opt => opt.MapFrom(src => src.TotalPrice));
```

- `Document → DocumentRequestDto`:
  - `Seller` ← `UserFirm` (firma wystawiająca, zmiana nazwy)
  - `Products` — inline LINQ projection z `DocumentProduct` i zagnieżdżonego `Product`
  - **Uwaga AM-07-A:** `dp.Product != null ? dp.Product.TvaValue : 0` — warunkowe null-check na `dp.Product`, ale jednocześnie `dp.Product!.Name` bez null-check → niespójność w tym samym lambdzie
- `Document → DocumentTableRecordDto`:
  - `ClientName` ← `Client.Name` (relacja nawigacyjna)
  - `TotalValue` ← `TotalPrice` (zmiana nazwy)

## Anomalie AutoMapper

| # | Anomalia |
|---|---|
| AM-A01 | `DocumentProductProfile` jednostronny; odwrotne mapowanie Product→DTO realizowane inline w `DocumentProfile` — duplikacja logiki |
| AM-A02 | `DocumentSeriesProfile`: `src.DocumentType!.Id` — null-forgiving bez null-check; ryzyko NullReferenceException gdy `DocumentType` null |
| AM-A03 | `DocumentProfile`: niespójna obsługa null: `dp.Product!.Name` (bez sprawdzenia) vs `dp.Product != null ? dp.Product.TvaValue : 0` (ze sprawdzeniem) w tym samym lambdzie |
| AM-A04 | `BankAccountProfile` i `FirmProfile` — brak namespace (brak `namespace ...;` na górze pliku), co jest niespójnością stylową w projekcie |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Inwentaryzacja 7 profili AutoMapper z cytatami kodu. |
