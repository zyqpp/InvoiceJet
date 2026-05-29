# Rejestracja użytkownika — Błędy i bezpieczeństwo

## Błędy procesu

| Warunek | Wyjątek | Status HTTP | Źródło mapowania |
|---|---|---|---|
| Użytkownik z adresem e-mail już istnieje | `UserAlreadyExistsException` | `400 Bad Request` | `ExceptionMiddleware` |
| Hasła nie są zgodne | `PasswordMismatchException` | `400 Bad Request` | `ExceptionMiddleware` |
| Hasło nie spełnia regex | `InvalidPasswordException` | `500 Internal Server Error` | Brak dedykowanego `catch` w `ExceptionMiddleware` |
| Inny błąd | `Exception` | `500 Internal Server Error` | `ExceptionMiddleware` |

---

## Uwagi bezpieczeństwa

- Hasło nie jest zapisywane w postaci jawnej. W bazie trafia wyłącznie `PasswordHash`.
- Token JWT zawiera dane identyfikujące użytkownika i rolę.
- Czas życia tokenu jest ustawiony na 10 minut.
- Endpoint rejestracji jest publiczny i nie wymaga autoryzacji.
- `UserRegisterDto` nie zawiera atrybutów walidacji `DataAnnotations`. [UWAGA: walidacja opiera się na logice serwisu i nie jest wspierana atrybutami modelu — WYMAGA WERYFIKACJI Z ZESPOŁEM]
