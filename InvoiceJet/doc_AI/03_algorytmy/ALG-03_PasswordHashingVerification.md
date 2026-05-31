# Algorytm: Haszowanie i weryfikacja hasła (BCrypt)

| Atrybut | Wartość |
|---|---|
| ID | ALG-03 |
| Nazwa | Password Hashing & Verification (BCrypt) |
| Kategoria | Bezpieczeństwo |
| Pliki | `AuthService.cs › RegisterUser()`, `AuthService.cs › LoginUser()` |
| Biblioteka | `BCrypt.Net-Next 4.0.3` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Bezpieczne przechowywanie haseł użytkowników przy użyciu adaptacyjnej funkcji haszowania BCrypt.

## Walidacja siły hasła

Przed haszowaniem sprawdzane jest spełnienie reguł:

```csharp
// Regex: min 8 znaków, duża litera, mała litera, cyfra, znak specjalny
Regex regex = new Regex(@"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$");
if (!regex.IsMatch(registerUserDto.Password)) {
    throw new InvalidPasswordException();
}
```

### Reguły hasła

| Reguła | Pattern |
|---|---|
| Min. 8 znaków | `.{8,}` |
| Co najmniej 1 mała litera | `(?=.*[a-z])` |
| Co najmniej 1 duża litera | `(?=.*[A-Z])` |
| Co najmniej 1 cyfra | `(?=.*\d)` |
| Co najmniej 1 znak specjalny | `(?=.*[@$!%*?&])` |

Dozwolone znaki specjalne: `@`, `$`, `!`, `%`, `*`, `?`, `&` (tylko te 7!)

## Haszowanie (rejestracja)

```csharp
string passwordHash = BCrypt.Net.BCrypt.HashPassword(registerUserDto.Password);
var user = _mapper.Map<User>(registerUserDto);
user.PasswordHash = passwordHash;
```

BCrypt automatycznie generuje salt i wbudowuje go w hash. Wynikowy hash ma format:
```
$2a$11$<22-znakowy-salt><31-znakowy-hash>
```

Domyślny work factor BCrypt.Net-Next: `11` (2^11 = 2048 iteracji).

## Weryfikacja (logowanie)

```csharp
bool isPasswordValid = BCrypt.Net.BCrypt.Verify(loginUserDto.Password, user.PasswordHash);
if (!isPasswordValid) {
    throw new InvalidCredentialsException();
}
```

`BCrypt.Verify()` wyciąga salt z przechowywanego hasha i porównuje — bezpieczne przed timing attacks.

## Model danych

| Tabela | Kolumna | Typ |
|---|---|---|
| `User` | `PasswordHash` | `nvarchar(max)` |

Czyste hasło **nigdy** nie jest przechowywane.

## Anomalie

| # | Anomalia |
|---|---|
| BCR-01 | Znaki specjalne ograniczone do `[@$!%*?&]` — użytkownicy nie mogą używać innych znaków specjalnych (np. `#`, `^`, `(`, `)`) |
| BCR-02 | Walidacja hasła tylko po stronie backend (regex) — frontend może nie ostrzegać o wymaganiach |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
