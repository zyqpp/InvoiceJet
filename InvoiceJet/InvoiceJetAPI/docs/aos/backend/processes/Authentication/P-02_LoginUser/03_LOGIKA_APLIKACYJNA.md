# LoginUser — Logika aplikacyjna

## 0. Algorytm w skrócie

1. Kontroler odbiera `UserLoginDto` z body i wywołuje `AuthService.LoginUser(userDto)`.
2. Serwis wyszukuje użytkownika po e-mailu w bazie (`Users.Query().FirstOrDefaultAsync`).
3. Jeżeli użytkownik nie istnieje (lub sprawdzenie `user.Email != userDto.Email` — redundantne) → `UserNotFoundException` → 400.
4. Weryfikuje hasło przez BCrypt: `BC.Verify(userDto.Password, user.PasswordHash)`.
5. Jeżeli hasło niepoprawne → `IncorrectPasswordException` → 400.
6. Wywołuje `CreateToken(user)` — buduje i podpisuje JWT (identyczny mechanizm jak w P-01).
7. Kontroler zwraca `200 OK` z `{ "token": "<jwt>" }`.

---

## 1. Wejście do procesu

Kotwica: `AuthController.cs › AuthController.Login`

```csharp
// AuthController.cs › AuthController.Login
[HttpPost("login")]
public async Task<ActionResult<User>> Login([FromBody] UserLoginDto userDto)
{
    string token = await _authService.LoginUser(userDto);
    return Ok(new { token });
}
```

Kontroler przekazuje DTO bezpośrednio do serwisu i wraca z `Ok(new { token })`. Zwracany typ `ActionResult<User>` jest myląco oznaczony — faktyczna odpowiedź to `{ token }`.

---

## 2. Walidacje (faza wejściowa)

Walidacje wykonywane w `AuthService.LoginUser` w podanej kolejności:

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Użytkownik z podanym e-mailem istnieje w `User` | `AuthService.cs › AuthService.LoginUser` | `UserNotFoundException` (szczegóły: plik 05, `WAL-01`) |
| 2 | Hasło zgadza się z BCrypt hash | `AuthService.cs › AuthService.LoginUser` | `IncorrectPasswordException` (szczegóły: plik 05, `WAL-02`) |

**WAL-01 — Istnienie użytkownika:**
```csharp
// AuthService.cs › AuthService.LoginUser
var user = await _unitOfWork.Users.Query()
    .FirstOrDefaultAsync(u => u.Email == userDto.Email);
if (user == null || user.Email != userDto.Email)
{
    throw new UserNotFoundException(userDto.Email);
}
```

> [UWAGA: Warunek `user.Email != userDto.Email` jest redundantny — jeżeli `user != null`, to LINQ już zapewnił zgodność email. Ta gałąź warunki nigdy nie jest `true` samodzielnie — WYMAGA WERYFIKACJI Z ZESPOŁEM]

**WAL-02 — Weryfikacja hasła BCrypt:**
```csharp
// AuthService.cs › AuthService.LoginUser
if (!BC.Verify(userDto.Password, user.PasswordHash))
{
    throw new IncorrectPasswordException();
}
```

---

## 3. Logika biznesowa

### Generowanie tokenu JWT

Po pomyślnych walidacjach serwis wywołuje `CreateToken(user)` (metoda prywatna współdzielona z `RegisterUser`):

```csharp
// AuthService.cs › AuthService.LoginUser
string token = CreateToken(user);
return token;
```

`CreateToken` buduje listę claims z encji `User` i podpisuje JWT kluczem z `AppSettings:Token`. Szczegóły metody `CreateToken`: `P-01_RegisterUser/03_LOGIKA_APLIKACYJNA.md § 3` oraz `ZAGADNIENIA_PRZEKROJOWE.md § 1`.

### Tabela: pole encji → źródło (odczyt, nie zapis)

Proces odczytuje istniejący rekord `User`. Nie tworzy ani nie modyfikuje żadnych encji.

| Pole encji `User` | Użycie w procesie |
|---|---|
| `Id` | wsad do `CreateToken` — claim `userId` |
| `Email` | wsad do `CreateToken` — claim `email`; używany w `UserNotFoundException` |
| `FirstName` | wsad do `CreateToken` — claim `firstName` |
| `LastName` | wsad do `CreateToken` — claim `lastName` |
| `PasswordHash` | weryfikacja BCrypt |
| `Role` | nie jest odczytywany — claim `ClaimTypes.Role` jest hardcoded `"User"` w `CreateToken` |

---

## 4. Zapisy do bazy i transakcje

> Sekcja nie dotyczy tego procesu. Logowanie nie wykonuje żadnych operacji zapisu ani modyfikacji w bazie danych. `CompleteAsync()` nie jest wywoływane.

Jedyna operacja bazodanowa to odczyt:
```csharp
// AuthService.cs › AuthService.LoginUser (via GenericRepository.Query)
var user = await _unitOfWork.Users.Query()
    .FirstOrDefaultAsync(u => u.Email == userDto.Email);
```

---

## 5. Odpowiedź

```csharp
// AuthController.cs › AuthController.Login
return Ok(new { token });
```

Odpowiedź: `200 OK`, `Content-Type: application/json`, body: `{ "token": "<jwt string>" }`.

Odpowiedź nie zawiera danych użytkownika (Id, Email, imię, nazwisko) — tylko token.

---

## 6. Uwagi techniczne

- [UWAGA: `user.Email != userDto.Email` w warunku `WAL-01` jest martwym kodem — zapytanie LINQ filtruje po `u.Email == userDto.Email`, więc jeżeli obiekt `user` nie jest `null`, email musi się zgadzać — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Metoda `AuthService.CreateToken` jest prywatna i wspólna dla `RegisterUser` i `LoginUser` — zmiana w `CreateToken` wpływa na oba procesy.
- Weryfikacja BCrypt jest po stronie aplikacji — hash z DB jest pobierany i porównywany lokalnie. Nie istnieje metoda na bazie.
