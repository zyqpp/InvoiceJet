# Logowanie użytkownika — Logika aplikacyjna

## Przepływ wykonania

1. `AuthController.Login()` przekazuje `UserLoginDto` do `AuthService.LoginUser()`.
2. Serwis wyszukuje użytkownika po `Email`.
3. Gdy użytkownik nie istnieje, serwis rzuca `UserNotFoundException`.
4. Serwis weryfikuje hasło przez `BC.Verify(...)`.
5. Gdy hasło jest niepoprawne, serwis rzuca `IncorrectPasswordException`.
6. Serwis generuje token przez `CreateToken(user)`.
7. Kontroler zwraca `Ok(new { token })`.

---

## Token JWT

Logowanie korzysta z tej samej metody `CreateToken(User user)` co rejestracja:

- claimy: `userId`, `firstName`, `lastName`, `email`, rola `User`,
- podpis: `HmacSha512Signature`,
- źródło klucza: `AppSettings:Token`,
- czas życia: `10` minut.
