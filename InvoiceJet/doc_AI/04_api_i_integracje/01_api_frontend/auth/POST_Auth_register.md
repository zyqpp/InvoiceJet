# POST /api/Auth/register — Rejestracja użytkownika

| Atrybut | Wartość |
|---|---|
| ID | API-01 |
| Metoda | POST |
| URL | `/api/Auth/register` |
| Autoryzacja | Publiczny (brak `[Authorize]`) |
| Kontroler | `AuthController.Register` |
| Serwis | `IAuthService.RegisterUser` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Request

### Headers
| Nagłówek | Wartość |
|---|---|
| `Content-Type` | `application/json` |

### Body (JSON)

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `firstName` | `string` | TAK | Imię |
| `lastName` | `string` | TAK | Nazwisko |
| `email` | `string` | TAK | Adres email |
| `password` | `string` | TAK | Hasło (min 8 znaków, duże/małe litery, cyfra, znak specjalny) |
| `passwordConfirmation` | `string` | TAK | Potwierdzenie hasła (musi być identyczne z `password`) |

**Przykład:**
```json
{
  "firstName": "Jan",
  "lastName": "Kowalski",
  "email": "jan.kowalski@example.com",
  "password": "Password123!",
  "passwordConfirmation": "Password123!"
}
```

## Response

### 200 OK — sukces

Zwraca JWT Bearer Token jako plain string (nie JSON):
```
eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI...
```

**Ważne:** Token wygasa po **10 minutach**.

### Błędy

| Status HTTP | Wyjątek | Warunek |
|---|---|---|
| 409 Conflict | `UserAlreadyExistsException` | Email już istnieje w bazie |
| 400 Bad Request | `InvalidPasswordException` | Hasło nie spełnia wymagań regex |
| 400 Bad Request | `PasswordMismatchException` | `password ≠ passwordConfirmation` |
| 500 Internal Server Error | — | Niespodziewany błąd |

**Przykład odpowiedzi błędu (409):**
```json
{ "message": "User with email jan.kowalski@example.com already exists." }
```

## Walidacja hasła

Regex: `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$`

| Wymaganie | Opis |
|---|---|
| Minimum 8 znaków | — |
| Przynajmniej 1 mała litera | `[a-z]` |
| Przynajmniej 1 wielka litera | `[A-Z]` |
| Przynajmniej 1 cyfra | `\d` |
| Przynajmniej 1 znak specjalny | `[@$!%*?&]` |
| Tylko dozwolone znaki | `[A-Za-z\d@$!%*?&]` |

## Zachowanie po stronie frontendu

1. `AuthService.register(user: IRegisterUser)` → `POST /Auth/register`
2. Przy sukcesie: `localStorage.setItem("authToken", response.token)` + nawigacja do `/dashboard`
3. Przy błędzie: `errorMessage` wyświetlony w formularzu

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
