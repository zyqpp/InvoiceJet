# AutoMapper Profile: AuthProfile

| Atrybut | Wartość |
|---|---|
| ID | AM-01 |
| Plik | `InvoiceJet.Application/MappingProfiles/AuthProfile.cs` |
| Dotyczy | Rejestracja i logowanie użytkowników |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Mapowania

### RegisterUserDto → User

```csharp
CreateMap<RegisterUserDto, User>()
    .ForMember(dest => dest.PasswordHash, opt => opt.Ignore());
    // Pozostałe pola: FirstName, LastName, Email — nazwy zgodne, mapowanie automatyczne
```

| Pole źródłowe (DTO) | Pole docelowe (Encja) | Uwaga |
|---|---|---|
| `FirstName` | `User.FirstName` | Auto |
| `LastName` | `User.LastName` | Auto |
| `Email` | `User.Email` | Auto |
| `Password` | — | Ignorowane |
| `PasswordConfirmation` | — | Ignorowane |
| — | `User.PasswordHash` | `Ignore()` — ustawiane przez `BCrypt` |

## Pola ignorowane

- `PasswordHash` — ustawiane ręcznie po mapowaniu przez `BCrypt.Net.BCrypt.HashPassword()`
- `Password`, `PasswordConfirmation` — nie są mapowane na encję

## Użycie

```csharp
// AuthService.RegisterUser
var user = _mapper.Map<User>(registerUserDto);
user.PasswordHash = BCrypt.Net.BCrypt.HashPassword(registerUserDto.Password);
await _unitOfWork.Users.AddAsync(user);
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
