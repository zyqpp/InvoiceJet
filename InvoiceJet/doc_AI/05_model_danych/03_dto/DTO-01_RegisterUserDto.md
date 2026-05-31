# DTO: RegisterUserDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-01 |
| Plik | `InvoiceJet.Application/DTOs/RegisterUserDto.cs` |
| Kierunek | Request (Frontend → Backend) |
| Endpoint | `POST /api/Auth/register` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `FirstName` | `string` | NIE | Imię użytkownika |
| `LastName` | `string` | NIE | Nazwisko użytkownika |
| `Email` | `string` | NIE | Adres email (login) |
| `Password` | `string` | NIE | Hasło (walidowane regex po stronie serwisu) |
| `PasswordConfirmation` | `string` | NIE | Potwierdzenie hasła |

## Walidacje

| Pole | Walidacja | Gdzie |
|---|---|---|
| `Password` | Regex: min 8 znaków, wielka/mała litera, cyfra, `[@$!%*?&]` | `AuthService.RegisterUser()` |
| `PasswordConfirmation` | Zgodność z `Password` | Frontend tylko |

## Mapowanie AutoMapper

`RegisterUserDto` → `User`:
- `FirstName` → `User.FirstName`
- `LastName` → `User.LastName`
- `Email` → `User.Email`
- `Password` → ignorowane (haszowane osobno)
- `PasswordHash` → ustawiane ręcznie przez `BCrypt.HashPassword`

## Przykład JSON

```json
{
  "firstName": "Jan",
  "lastName": "Kowalski",
  "email": "jan@example.com",
  "password": "Haslo123!",
  "passwordConfirmation": "Haslo123!"
}
```

## Anomalie

| # | Anomalia |
|---|---|
| DTO01-01 | Walidacja zgodności `Password` z `PasswordConfirmation` brak po stronie backendu — tylko frontend |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
