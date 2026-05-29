# Rejestracja użytkownika — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Rejestracja nowego użytkownika | Unikalny e-mail i hasło zgodne z regex. | `200 OK`, odpowiedź zawiera `token`, nowy rekord `User` istnieje w bazie. |
| TC-02 | Token po rejestracji zawiera rolę | Rejestracja zakończona sukcesem. | JWT zawiera claim roli `User`. |

---

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Próba rejestracji istniejącego e-maila | E-mail już istnieje w bazie. | `400 Bad Request`, komunikat z `UserAlreadyExistsException`. |
| TC-N02 | Hasło i potwierdzenie są różne | `password != passwordConfirmation`. | `400 Bad Request`, komunikat z `PasswordMismatchException`. |
| TC-N03 | Hasło nie spełnia regex | Hasło bez wymaganych znaków. | `500 Internal Server Error`, komunikat z `InvalidPasswordException`. |

---

## Dane testowe przykładowe

```json
{
  "firstName": "Jan",
  "lastName": "Kowalski",
  "email": "jan.kowalski@example.com",
  "password": "Strong!123",
  "passwordConfirmation": "Strong!123"
}
```
