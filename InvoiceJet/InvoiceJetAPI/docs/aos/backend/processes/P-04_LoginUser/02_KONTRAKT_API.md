# Logowanie użytkownika — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/Auth/login` |
| Kontroler | `AuthController` |
| Metoda kontrolera | `Login([FromBody] UserLoginDto userDto)` |
| Autoryzacja | Brak |
| Content-Type | `application/json` |

---

## Żądanie

Body żądania ma typ `UserLoginDto`.

| Pole | Typ | Wykorzystanie |
|---|---|---|
| `email` | `string` | Wyszukanie użytkownika. |
| `password` | `string` | Weryfikacja z `PasswordHash` przez `BC.Verify(...)`. |

---

## Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `{ token: string }` | Poprawne dane logowania. |
| `400 Bad Request` | `{ "message": string }` | `UserNotFoundException` lub `IncorrectPasswordException`. |
| `500 Internal Server Error` | `{ "message": string }` | Inny nieobsłużony wyjątek. |
