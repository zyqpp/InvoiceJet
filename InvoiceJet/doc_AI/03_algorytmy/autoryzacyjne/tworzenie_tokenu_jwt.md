# Tworzenie tokenu JWT (CreateToken) — algorytm

| Pole | Wartość |
|---|---|
| ID dokumentu | ALG-Autoryzacyjne-TworzenieTokenuJwt |
| Typ dokumentu | algorytm |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Algorytm buduje podpisany token JWT zawierający claims użytkownika (ID, imię, nazwisko, email, rola). Token jest wystawiany zarówno po pomyślnej rejestracji jak i po poprawnym zalogowaniu. Stanowi punkt wyjścia dla całego mechanizmu autoryzacji w InvoiceJet.

## Cel algorytmu

Wygenerowanie podpisanego tokenu JWT z claimami identyfikującymi użytkownika, ważnego przez 10 minut, który frontend przechowuje i dołącza do kolejnych żądań HTTP.

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| ID algorytmu | ALG-Autoryzacyjne-TworzenieTokenuJwt |
| Kategoria | autoryzacyjne |
| Wejście | `User user` — encja użytkownika z bazy danych |
| Wyjście | `string` — podpisany token JWT (Base64url) |
| Złożoność (orientacyjna) | O(1) |
| Gdzie wywoływany | `AuthService` — po rejestracji i po zalogowaniu |
| Powiązana metoda w kodzie | `AuthService.CreateToken(User user)` |

## Opis krok po kroku

1. Zbuduj listę claims z danych użytkownika:
   ```csharp
   var claims = new List<Claim>
   {
       new Claim("userId", user.Id.ToString()),
       new Claim("firstName", user.FirstName),
       new Claim("lastName", user.LastName),
       new Claim("email", user.Email),
       new Claim(ClaimTypes.Role, "User")
   };
   ```
2. Pobierz klucz symetryczny z konfiguracji (`AppSettings:Token`):
   ```csharp
   var key = new SymmetricSecurityKey(
       Encoding.UTF8.GetBytes(_configuration["AppSettings:Token"]!)
   );
   ```
3. Utwórz `SigningCredentials` z algorytmem `HmacSha512Signature`:
   ```csharp
   var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha512Signature);
   ```
4. Zbuduj `JwtSecurityToken` z claimami, datą wygaśnięcia i kredencjałami:
   ```csharp
   var token = new JwtSecurityToken(
       claims: claims,
       expires: DateTime.UtcNow.AddMinutes(10),
       signingCredentials: creds
   );
   ```
5. Serializuj token do stringa: `return new JwtSecurityTokenHandler().WriteToken(token);`
6. Zwróć token do wywołującego (`RegisterUser()` lub `LoginUser()`).

## Claims tokenu

| Claim | Typ | Wartość |
|---|---|---|
| `userId` | Custom | `user.Id.ToString()` |
| `firstName` | Custom | `user.FirstName` |
| `lastName` | Custom | `user.LastName` |
| `email` | Custom | `user.Email` |
| `role` | `ClaimTypes.Role` | `"User"` (hardkodowana stała wartość) |
| `exp` | Standard (JWT) | `DateTime.UtcNow + 10 minut` |

## Parametry podpisywania

| Parametr | Wartość |
|---|---|
| Klucz | `AppSettings:Token` (z `appsettings.json` lub zmiennych środowiskowych) |
| Algorytm | `SecurityAlgorithms.HmacSha512Signature` |
| Encoding klucza | `UTF8` |
| Czas ważności | 10 minut (`DateTime.UtcNow.AddMinutes(10)`) |

## Dostęp do claims na backendzie (kontrolery)

```csharp
var userId = int.Parse(User.FindFirst("userId")!.Value);
var email = User.FindFirst("email")!.Value;
var role = User.FindFirst(ClaimTypes.Role)!.Value; // zawsze "User"
```

## Przypadki brzegowe

| Przypadek | Dane wejściowe | Oczekiwane zachowanie |
|---|---|---|
| `AppSettings:Token` brak w konfiguracji | `null` z konfiguracji | Wyjątek NullReferenceException przy `Encoding.UTF8.GetBytes(null!)` — crash aplikacji |
| `user.Id` = 0 | Niezapisany użytkownik | Token z `userId=0`; konsekwencje przy izolacji danych |
| `user.FirstName` lub `user.LastName` puste | `""` | Token z pustym claimem — brak błędu technicznego |
| Klucz zbyt krótki dla HMAC-SHA512 | Klucz < 64 bajty | Wyjątek `ArgumentOutOfRangeException` z `SymmetricSecurityKey` |

## Powiązania

- Wywoływany z procesu: [`../../02_procesy/autentykacja/rejestracja/proces.md`](../../02_procesy/autentykacja/rejestracja/proces.md), [`../../02_procesy/autentykacja/logowanie/proces.md`](../../02_procesy/autentykacja/logowanie/proces.md)
- Wywoływany z endpointu: [`../../04_api_i_integracje/01_api_frontend/auth/`](../../04_api_i_integracje/01_api_frontend/auth/)
- Powiązane algorytmy: [`weryfikacja_tokenu_jwt.md`](weryfikacja_tokenu_jwt.md) — faza weryfikacji wystawionego tokenu

## Powiązania z kodem

- Klasa implementująca: `InvoiceJet.Application/Services/AuthService.cs`
- Metoda: `AuthService.CreateToken(User user)`

## Wątpliwości i braki

- **JWT-01:** Operator `!` (null-forgiving) przy odczycie klucza — jeśli `AppSettings:Token` nie istnieje w konfiguracji, wyjątek runtime zamiast czytelnego błędu konfiguracji. Zalecane: walidacja konfiguracji przy starcie.
- **JWT-02:** `ValidateIssuer=false` i `ValidateAudience=false` w konfiguracji walidacji — słabsze bezpieczeństwo (zob. `weryfikacja_tokenu_jwt.md`).
- **JWT-03:** 10 minut to bardzo krótki czas sesji dla aplikacji biznesowej.
- **JWT-04:** Rola zawsze hardkodowana jako `"User"` — brak możliwości rozróżnienia ról bez zmiany kodu.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — na podstawie ALG-04_JwtTokenCreation.md. |
