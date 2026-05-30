# Rejestracja użytkownika — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/Auth/register` |
| Kontroler | `AuthController` |
| Metoda kontrolera | `Register([FromBody] UserRegisterDto userDto)` |
| Autoryzacja | Brak |
| Content-Type | `application/json` |

---

## Żądanie

Body żądania ma typ `UserRegisterDto`.

| Pole | Typ | Wykorzystanie |
|---|---|---|
| `id` | `Guid?` | Nie jest używane w logice rejestracji. |
| `firstName` | `string` | Mapowane do `User.FirstName`. |
| `lastName` | `string` | Mapowane do `User.LastName`. |
| `email` | `string` | Służy do wyszukania istniejącego użytkownika i mapowania do `User.Email`. |
| `password` | `string` | Walidowane regexem i hashowane. |
| `passwordConfirmation` | `string` | Porównywane z `password`. |

---

## Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `{ token: string }` | Rejestracja zakończona sukcesem. |
| `400 Bad Request` | `{ "message": string }` | `UserAlreadyExistsException` lub `PasswordMismatchException`. |
| `500 Internal Server Error` | `{ "message": string }` | `InvalidPasswordException` lub inny nieobsłużony wyjątek. |

---

## Reguła hasła

Regex używany w kodzie:

```regex
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$
```

Wymagania wynikające z regex:

- minimum 8 znaków,
- co najmniej jedna mała litera,
- co najmniej jedna wielka litera,
- co najmniej jedna cyfra,
- co najmniej jeden znak specjalny z zestawu `@$!%*?&`.
