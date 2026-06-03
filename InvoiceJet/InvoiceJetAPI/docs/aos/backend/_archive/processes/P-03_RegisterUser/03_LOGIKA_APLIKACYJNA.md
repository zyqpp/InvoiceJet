# Rejestracja użytkownika — Logika aplikacyjna

## Przepływ wykonania

1. `AuthController.Register()` przekazuje `UserRegisterDto` do `AuthService.RegisterUser()`.
2. Serwis sprawdza, czy istnieje użytkownik o tym samym `Email`.
3. Serwis waliduje `Password` przez regex.
4. Serwis porównuje `Password` i `PasswordConfirmation`.
5. Serwis tworzy encję `User`.
6. Serwis hashuje hasło przez `BCrypt.Net.BCrypt.HashPassword(...)`.
7. Serwis zapisuje encję przez `Users.AddAsync(user)` i `_unitOfWork.CompleteAsync()`.
8. Serwis generuje token przez `CreateToken(user)`.
9. Kontroler zwraca `Ok(new { token })`.

---

## Tworzenie encji użytkownika

| Pole `User` | Źródło |
|---|---|
| `Email` | `userDto.Email` |
| `PasswordHash` | `BC.HashPassword(userDto.Password)` |
| `FirstName` | `userDto.FirstName` |
| `LastName` | `userDto.LastName` |
| `Role` | Stała wartość `"User"` |

---

## Generowanie tokenu

`CreateToken(User user)` tworzy listę claimów:

- `userId`,
- `firstName`,
- `lastName`,
- `email`,
- `ClaimTypes.Role = "User"`.

Token jest podpisany kluczem `AppSettings:Token` i algorytmem `HmacSha512Signature`.
Token wygasa po `10` minutach (`DateTime.UtcNow.AddMinutes(10)`).
