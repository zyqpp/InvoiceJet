# AutoMapper Profile: BankAccountProfile

| Atrybut | Wartość |
|---|---|
| ID | AM-03 |
| Plik | `InvoiceJet.Application/MappingProfiles/BankAccountProfile.cs` |
| Dotyczy | Konta bankowe firmy |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Mapowania

### BankAccountRequestDto → BankAccount

```csharp
CreateMap<BankAccountRequestDto, BankAccount>();
// Wszystkie pola mapowane automatycznie
```

| Pole DTO | Pole Encji |
|---|---|
| `Id` | `BankAccount.Id` |
| `BankName` | `BankAccount.BankName` |
| `Iban` | `BankAccount.Iban` |
| `Currency` | `BankAccount.Currency` |

Pole `UserFirmId` nie jest w DTO — ustawiane ręcznie przez serwis po mapowaniu.

### BankAccount → BankAccountRequestDto

```csharp
CreateMap<BankAccount, BankAccountRequestDto>();
```

## Uwaga

`BankAccount.UserFirmId` (FK) nie jest mapowany przez AutoMapper — ustawiany przez serwis:

```csharp
var bankAccount = _mapper.Map<BankAccount>(bankAccountRequestDto);
bankAccount.UserFirmId = userFirmId; // ustawiane ręcznie
await _unitOfWork.BankAccounts.AddAsync(bankAccount);
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
