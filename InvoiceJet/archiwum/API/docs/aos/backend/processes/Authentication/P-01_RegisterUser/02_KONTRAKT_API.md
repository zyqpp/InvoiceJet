# RegisterUser — Kontrakt API

## `API-01` — POST /api/Auth/register

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/Auth/register` |
| Kontroler | `AuthController.cs › AuthController.Register` |
| Autoryzacja | N/D — endpoint publiczny (brak `[Authorize]`) |

### Parametry trasy / zapytania

> Sekcja nie dotyczy tego procesu. Endpoint nie przyjmuje parametrów trasy ani zapytania.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `UserRegisterDto` | `[FromBody]` |

Pola `UserRegisterDto` (`Application/DTOs/UserRegisterDto.cs`):

| Pole | Typ C# | Wymagane | Opis |
|---|---|---|---|
| `Id` | `Guid?` | nie | Ignorowane przez serwis — id generuje baza |
| `FirstName` | `string` | tak* | Imię użytkownika |
| `LastName` | `string` | tak* | Nazwisko użytkownika |
| `Email` | `string` | tak* | Adres e-mail (musi być unikalny) |
| `Password` | `string` | tak* | Hasło (musi spełniać regex złożoności) |
| `PasswordConfirmation` | `string` | tak* | Powtórzenie hasła (musi być identyczne z `Password`) |

> *Brak atrybutów `[Required]` w DTO — "wymagane" oznacza tu wymaganie biznesowe egzekwowane w serwisie lub przez ORM, nie przez model validation ASP.NET.

Przykład żądania:
```json
{
  "firstName": "Anna",
  "lastName": "Testowa",
  "email": "anna.testowa@example.com",
  "password": "Strong@123",
  "passwordConfirmation": "Strong@123"
}
```

### Odpowiedź

| Status | Typ / kształt | Warunek |
|---|---|---|
| `200 OK` | `{ "token": "<jwt string>" }` | Rejestracja pomyślna; token JWT ważny 10 minut |
| `400 Bad Request` | `{ "message": "User with email <email> already exists." }` | E-mail już zarejestrowany — `UserAlreadyExistsException` |
| `400 Bad Request` | `{ "message": "Password confirmation doesn't match." }` | `Password != PasswordConfirmation` — `PasswordMismatchException` |
| `500 Internal Server Error` | `{ "message": "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character." }` | Hasło nie spełnia regex — `InvalidPasswordException` (niezmapowany w middleware → catch-all 500) |
| `500 Internal Server Error` | `{ "message": "<system error>" }` | Inny nieobsłużony wyjątek (np. NullReferenceException gdy pole DTO jest null) |

Przykład odpowiedzi sukcesu:
```json
{
  "token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI..."
}
```

Przykład odpowiedzi błędu (duplikat e-mail):
```json
{
  "message": "User with email anna.testowa@example.com already exists."
}
```

Przykład odpowiedzi błędu (słabe hasło — uwaga: status 500, nie 400):
```json
{
  "message": "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character."
}
```
