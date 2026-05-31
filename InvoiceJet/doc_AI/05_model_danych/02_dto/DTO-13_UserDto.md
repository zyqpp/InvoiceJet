# DTO: UserDto (TokenResponseDto)

| Atrybut | Wartość |
|---|---|
| ID | DTO-13 |
| Plik | `InvoiceJet.Application/DTOs/UserDto.cs` (lub `TokenResponseDto.cs`) |
| Kierunek | Response (Backend → Frontend) |
| Endpointy | [POST /api/Auth/register](../../04_api_i_integracje/01_api_frontend/auth/POST_Auth_register.md), [POST /api/Auth/login](../../04_api_i_integracje/01_api_frontend/auth/POST_Auth_login.md) |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `Token` | `string` | NIE | JWT token do uwierzytelnienia dalszych żądań |

## Cel

Najprostszy możliwy response — zawiera tylko token JWT. Frontend przechowuje go w `localStorage` pod kluczem `"authToken"`.

## Przykład JSON

```json
{
  "token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIxIiwiZmlyc3ROYW1lIjoiSmFuIiwibGFzdE5hbWUiOiJLb3dhbHNraSIsImVtYWlsIjoiamFuQGV4YW1wbGUuY29tIiwicm9sZSI6IlVzZXIiLCJleHAiOjE3NDg2OTM2MDB9.signature"
}
```

## JWT payload (po zdekodowaniu)

```json
{
  "userId": "1",
  "firstName": "Jan",
  "lastName": "Kowalski",
  "email": "jan@example.com",
  "role": "User",
  "exp": 1748693600
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
