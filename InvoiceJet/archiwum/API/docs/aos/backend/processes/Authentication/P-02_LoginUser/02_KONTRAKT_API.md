# LoginUser — Kontrakt API

## `API-02` — POST /api/Auth/login

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/Auth/login` |
| Kontroler | `AuthController.cs › AuthController.Login` |
| Autoryzacja | N/D — endpoint publiczny (brak `[Authorize]`) |

### Parametry trasy / zapytania

> Sekcja nie dotyczy tego procesu. Endpoint nie przyjmuje parametrów trasy ani zapytania.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `UserLoginDto` | `[FromBody]` |

Pola `UserLoginDto` (`Application/DTOs/UserLoginDto.cs`):

| Pole | Typ C# | Wymagane | Opis |
|---|---|---|---|
| `Email` | `string` | tak* | Adres e-mail — wyszukiwany w tabeli `User` |
| `Password` | `string` | tak* | Hasło jawne — weryfikowane BCrypt względem `User.PasswordHash` |

> *Brak atrybutów `[Required]` w DTO — pola `null` nie są odrzucane przez model validation ASP.NET Core.

Przykład żądania:
```json
{
  "email": "tester+01@invoicejet.test",
  "password": "Strong@123"
}
```

### Odpowiedź

| Status | Typ / kształt | Warunek |
|---|---|---|
| `200 OK` | `{ "token": "<jwt string>" }` | Logowanie pomyślne; token JWT ważny 10 minut |
| `400 Bad Request` | `{ "message": "User with email <email> not found." }` | Brak użytkownika z podanym e-mailem — `UserNotFoundException` |
| `400 Bad Request` | `{ "message": "Password is incorrect." }` | Hasło niezgodne z hashem w bazie — `IncorrectPasswordException` |
| `500 Internal Server Error` | `{ "message": "<system error>" }` | Inny nieobsłużony wyjątek (np. `NullReferenceException` gdy pole DTO jest `null`) |

Przykład odpowiedzi sukcesu:
```json
{
  "token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI..."
}
```

Przykład odpowiedzi błędu (nieznany e-mail):
```json
{
  "message": "User with email tester+01@invoicejet.test not found."
}
```

Przykład odpowiedzi błędu (złe hasło):
```json
{
  "message": "Password is incorrect."
}
```
