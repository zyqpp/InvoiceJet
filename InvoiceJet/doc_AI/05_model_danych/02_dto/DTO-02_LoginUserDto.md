# DTO: LoginUserDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-02 |
| Plik | `InvoiceJet.Application/DTOs/LoginUserDto.cs` |
| Kierunek | Request (Frontend → Backend) |
| Endpoint | [POST /api/Auth/login](../../04_api_i_integracje/01_api_frontend/auth/POST_Auth_login.md) |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `Email` | `string` | NIE | Adres email (identyfikator konta) |
| `Password` | `string` | NIE | Hasło w postaci jawnej (weryfikowane przez BCrypt) |

## Użycie

Przekazywany do `AuthService.LoginUser(loginUserDto)`. Hasło weryfikowane przez `BCrypt.Verify()` z `User.PasswordHash`.

## Przykład JSON

```json
{
  "email": "jan@example.com",
  "password": "Haslo123!"
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
