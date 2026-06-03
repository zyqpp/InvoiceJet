# AutoMapper Profile: UserFirmProfile

| Atrybut | Wartość |
|---|---|
| ID | AM-07 |
| Plik | `InvoiceJet.Application/MappingProfiles/UserFirmProfile.cs` |
| Dotyczy | Powiązanie użytkownika z firmą (UserFirm) |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Mapowania

### UserFirm → FirmRequestDto (Seller w dokumencie)

```csharp
CreateMap<UserFirm, FirmRequestDto>()
    .ForMember(dest => dest.Id, opt => opt.MapFrom(src => src.Firm!.Id))
    .ForMember(dest => dest.FirmName, opt => opt.MapFrom(src => src.Firm!.FirmName))
    .ForMember(dest => dest.CuiValue, opt => opt.MapFrom(src => src.Firm!.CuiValue))
    .ForMember(dest => dest.RegCom, opt => opt.MapFrom(src => src.Firm!.RegCom))
    .ForMember(dest => dest.Address, opt => opt.MapFrom(src => src.Firm!.Address))
    .ForMember(dest => dest.County, opt => opt.MapFrom(src => src.Firm!.County))
    .ForMember(dest => dest.City, opt => opt.MapFrom(src => src.Firm!.City));
```

Mapuje `UserFirm.Firm` (nawigacja) → `FirmRequestDto`. Używane gdy dokument ma zwrócić dane sprzedawcy (Seller) w `DocumentRequestDto`.

## Zależność od Include

Mapowanie wymaga załadowania nawigacji `UserFirm.Firm` przez EF Core Include:

```csharp
// DocumentRepository — wymagane Include:
.Include(d => d.UserFirm).ThenInclude(uf => uf.Firm)
```

Jeśli Include jest pominięty → `NullReferenceException` z operatora `!` (`src.Firm!.Id`).

## Anomalie

| # | Anomalia |
|---|---|
| AM07-01 | Operator `!` (null-forgiving) — jeśli `UserFirm.Firm` nie załadowane, rzuca `NullReferenceException` zamiast czytelnego błędu |
| AM07-02 | `UserFirm.FirmId` jest nullable — możliwy scenariusz gdy użytkownik nie ma firmy (FirmId=null) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
