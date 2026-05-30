# RegisterUser — Logika aplikacyjna

## 0. Algorytm w skrócie

1. Kontroler odbiera `UserRegisterDto` z body i wywołuje `AuthService.RegisterUser(userDto)`.
2. Serwis sprawdza, czy e-mail już istnieje w bazie (`Users.Query().FirstOrDefaultAsync`).
3. Jeżeli istnieje — rzuca `UserAlreadyExistsException` → 400.
4. Sprawdza siłę hasła przez regex — jeżeli nie pasuje — rzuca `InvalidPasswordException` → **500** (błąd mapowania middleware).
5. Sprawdza zgodność `Password` i `PasswordConfirmation` — jeżeli różne — rzuca `PasswordMismatchException` → 400.
6. Tworzy encję `User` ręcznie (bez AutoMapper): email, BCrypt hash hasła, imię, nazwisko, rola = `"User"`.
7. Dodaje encję do kontekstu EF Core (`Users.AddAsync`).
8. Zatwierdza zapis (`CompleteAsync()` = `SaveChangesAsync`).
9. Wywołuje `CreateToken(user)` — buduje i podpisuje JWT.
10. Kontroler zwraca `200 OK` z `{ "token": "<jwt>" }`.

---

## 1. Wejście do procesu

Kotwica: `AuthController.cs › AuthController.Register`

```csharp
// AuthController.cs › AuthController.Register
[HttpPost("register")]
public async Task<ActionResult<User>> Register([FromBody] UserRegisterDto userDto)
{
    var token = await _authService.RegisterUser(userDto);
    return Ok(new { token });
}
```

Kontroler przekazuje DTO bezpośrednio do serwisu i wraca z `Ok(new { token })`. Nie wykonuje żadnej logiki walidacyjnej. Zwracany typ `ActionResult<User>` jest myląco oznaczony jako `User`, ale faktyczna odpowiedź to anonimowy obiekt `{ token }`.

> [UWAGA: Deklarowany typ zwracany `ActionResult<User>` w sygnaturze metody nie odpowiada faktycznie zwracanemu obiektowi `{ token }` — WYMAGA WERYFIKACJI Z ZESPOŁEM czy sygnatura jest celowa]

---

## 2. Walidacje (faza wejściowa)

Walidacje wykonywane są w `AuthService.RegisterUser` w podanej kolejności:

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | E-mail nie istnieje w `User` | `AuthService.cs › AuthService.RegisterUser` | `UserAlreadyExistsException` (szczegóły: plik 05, `WAL-01`) |
| 2 | Hasło spełnia regex złożoności | `AuthService.cs › AuthService.RegisterUser` | `InvalidPasswordException` (szczegóły: plik 05, `WAL-02`) |
| 3 | `Password == PasswordConfirmation` | `AuthService.cs › AuthService.RegisterUser` | `PasswordMismatchException` (szczegóły: plik 05, `WAL-03`) |

**WAL-01 — Unikalność e-mail:**
```csharp
// AuthService.cs › AuthService.RegisterUser
var existingUser = await _unitOfWork.Users.Query()
    .FirstOrDefaultAsync(u => u.Email == userDto.Email);
if (existingUser != null)
{
    throw new UserAlreadyExistsException(userDto.Email);
}
```

**WAL-02 — Siła hasła:**
```csharp
// AuthService.cs › AuthService.RegisterUser
var passwordRules = new Regex(@"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$");
if (!passwordRules.IsMatch(userDto.Password))
{
    throw new InvalidPasswordException();
}
```

**WAL-03 — Zgodność haseł:**
```csharp
// AuthService.cs › AuthService.RegisterUser
if (userDto.Password != userDto.PasswordConfirmation)
{
    throw new PasswordMismatchException();
}
```

---

## 3. Logika biznesowa

### Tworzenie encji `User`

Po przejściu walidacji serwis tworzy encję `User` ręcznie (bez AutoMapper):

```csharp
// AuthService.cs › AuthService.RegisterUser
var user = new User
{
    Email = userDto.Email,
    PasswordHash = BC.HashPassword(userDto.Password),
    FirstName = userDto.FirstName,
    LastName = userDto.LastName,
    Role = "User"
};
```

### Tabela: pole encji `User` → źródło

| Pole encji `User` | Źródło |
|---|---|
| `Id` | generowany przez SQL Server (NEWID / sequence — typ `uniqueidentifier`) |
| `Email` | `userDto.Email` |
| `FirstName` | `userDto.FirstName` |
| `LastName` | `userDto.LastName` |
| `PasswordHash` | `BC.HashPassword(userDto.Password)` — BCrypt hash |
| `Role` | stała `"User"` (hardcoded) |
| `ActiveUserFirmId` | `NULL` — nie ustawiane przy rejestracji |

### Generowanie tokenu JWT

Po zapisie encji serwis wywołuje `CreateToken(user)`:

```csharp
// AuthService.cs › AuthService.CreateToken
private string CreateToken(User user)
{
    var claims = new List<Claim>
    {
        new("userId", user.Id.ToString()),
        new("firstName", user.FirstName),
        new("lastName", user.LastName),
        new("email", user.Email),
        new(ClaimTypes.Role, "User")
    };
    var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(
        _configuration.GetSection("AppSettings:Token").Value!));
    var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha512Signature);
    var token = new JwtSecurityToken(
        claims: claims,
        expires: DateTime.UtcNow.AddMinutes(10),
        signingCredentials: credentials
    );
    return new JwtSecurityTokenHandler().WriteToken(token);
}
```

Konfiguracja JWT pochodzi z `AppSettings:Token` (`appsettings.json`). Szczegóły JWT w `ZAGADNIENIA_PRZEKROJOWE.md § 1`.

---

## 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | `CompleteAsync()` |
|---|---|---|---|
| 1 | `AddAsync(user)` — dodanie User do śledzenia EF Core | `GenericRepository.cs › GenericRepository.AddAsync` | nie (tylko staging) |
| 2 | `CompleteAsync()` | `UnitOfWork.cs › UnitOfWork.CompleteAsync` | tak — `SaveChangesAsync` → zapis do DB |

```csharp
// AuthService.cs › AuthService.RegisterUser
await _unitOfWork.Users.AddAsync(user);
await _unitOfWork.CompleteAsync();
```

> Transakcyjność: Proces wykonuje jedno `CompleteAsync()`. Nie używa jawnej transakcji (`BeginTransactionAsync`). Zapis jest atomowy na poziomie jednego `SaveChangesAsync`.

---

## 5. Odpowiedź

Kontroler zwraca `Ok(new { token })` po pomyślnym wykonaniu serwisu:

```csharp
// AuthController.cs › AuthController.Register
return Ok(new { token });
```

Odpowiedź: `200 OK`, `Content-Type: application/json`, body: `{ "token": "<jwt string>" }`.

Odpowiedź **nie zawiera** danych nowo utworzonego użytkownika (np. `Id`, `Email`) — zwracany jest wyłącznie token.

---

## 6. Uwagi techniczne

- [UWAGA: `InvalidPasswordException` nie jest rejestrowany w `ExceptionMiddleware`. Jego message trafia do catch-all `Exception` → `500 Internal Server Error`. Klient dostaje `500` zamiast oczekiwanego `400` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `User.Email` nie ma unikalnego indeksu w bazie. Przy równoległych żądaniach rejestracji z tym samym e-mailem oba mogą przejść sprawdzenie `existingUser != null` przed zapisem. Pierwsze `CompleteAsync()` zapisze — drugie wyrzuci wyjątek DB (nieokreślony, nie domenowy) → `500` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `UserRegisterDto.Id` (typ `Guid?`) jest obecny w DTO, ale `AuthService.RegisterUser` go nie odczytuje i nie używa. Id encji `User` jest generowane przez bazę — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Hasło jest haszowane algorytmem BCrypt: `BC.HashPassword(userDto.Password)` (alias BCrypt.Net.BCrypt). Sól jest generowana wewnętrznie przez BCrypt.
