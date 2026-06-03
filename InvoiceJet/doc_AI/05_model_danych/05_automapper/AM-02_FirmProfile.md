# AutoMapper Profile: FirmProfile

| Atrybut | Wartość |
|---|---|
| ID | AM-02 |
| Plik | `InvoiceJet.Application/MappingProfiles/FirmProfile.cs` |
| Dotyczy | Firma własna i firmy klientów |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Mapowania

### FirmRequestDto → Firm

```csharp
CreateMap<FirmRequestDto, Firm>();
// Wszystkie pola mapowane automatycznie przez konwencję nazw
```

| Pole źródłowe (DTO) | Pole docelowe (Encja) |
|---|---|
| `Id` | `Firm.Id` |
| `FirmName` | `Firm.FirmName` |
| `CuiValue` | `Firm.CuiValue` |
| `RegCom` | `Firm.RegCom` |
| `Address` | `Firm.Address` |
| `County` | `Firm.County` |
| `City` | `Firm.City` |

### Firm → FirmRequestDto

```csharp
CreateMap<Firm, FirmRequestDto>();
// Odwrócenie — wszystkie pola mapowane automatycznie
```

## Użycie

```csharp
// FirmService.AddFirm
var firm = _mapper.Map<Firm>(firmRequestDto);
await _unitOfWork.Firms.AddAsync(firm);

// FirmService.GetUserActiveFirm (response)
return _mapper.Map<FirmRequestDto>(firm);

// FirmService.GetFirmDataFromAnaf (response)
return _mapper.Map<FirmRequestDto>(anafData);
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
