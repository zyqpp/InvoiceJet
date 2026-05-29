# Logowanie użytkownika — Błędy i bezpieczeństwo

## Błędy procesu

| Warunek | Wyjątek | Status HTTP | Źródło mapowania |
|---|---|---|---|
| Użytkownik nie istnieje | `UserNotFoundException` | `400 Bad Request` | `ExceptionMiddleware` |
| Niepoprawne hasło | `IncorrectPasswordException` | `400 Bad Request` | `ExceptionMiddleware` |
| Inny błąd | `Exception` | `500 Internal Server Error` | `ExceptionMiddleware` |

---

## Uwagi bezpieczeństwa

- Hasło wejściowe jest porównywane z hashem przez `BC.Verify`.
- Endpoint logowania jest publiczny i nie wymaga tokenu.
- Odpowiedź sukcesu zawiera wyłącznie token JWT.
- `UserLoginDto` nie zawiera atrybutów `DataAnnotations`. [WYMAGA WERYFIKACJI]
