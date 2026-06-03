# POST /api/Auth/login — Logowanie użytkownika

| Atrybut | Wartość |
|---|---|
| ID | API-02 |
| Metoda | POST |
| URL | `/api/Auth/login` |
| Autoryzacja | Publiczny |
| Kontroler | `AuthController.Login` |
| Serwis | `IAuthService.LoginUser` |
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
| `email` | `string` | TAK | Adres email użytkownika |
| `password` | `string` | TAK | Hasło (plaintext) |

**Przykład:**
```json
{
  "email": "jan.kowalski@example.com",
  "password": "Password123!"
}
```

## Response

### 200 OK — sukces

Zwraca JWT Bearer Token jako plain string (nie JSON):
```
eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI...
```

**Payload zdekodowanego tokenu:**
| Claim | Wartość |
|---|---|
| `userId` | GUID użytkownika |
| `firstName` | Imię |
| `lastName` | Nazwisko |
| `email` | Email |
| `role` | `"User"` |

**Token wygasa po 10 minutach.**

### Błędy

| Status HTTP | Wyjątek | Warunek |
|---|---|---|
| 404 Not Found | `UserNotFoundException` | Email nie znaleziony w bazie |
| 400 Bad Request | `IncorrectPasswordException` | BCrypt.Verify() zwróciło false |
| 500 Internal Server Error | — | Niespodziewany błąd |

## Szczegóły algorytmu

1. Szukanie usera po `email` w tabeli `User` (`FirstOrDefaultAsync`)
2. Dodatkowy check: `user == null || user.Email != userDto.Email` (redundantny — jeśli null, rzuca wyjątek)
3. `BC.Verify(plainPassword, user.PasswordHash)` — weryfikacja BCrypt
4. `CreateToken(user)` — budowanie JWT (HmacSha512, 10 min)

## Zachowanie po stronie frontendu

1. `AuthService.login(user: ILoginUser)` → `POST /Auth/login`
2. Przy sukcesie: `localStorage.setItem("authToken", response.token)` + nawigacja do `/dashboard`
3. Przy błędzie: `errorMessage` wyświetlony w formularzu

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
