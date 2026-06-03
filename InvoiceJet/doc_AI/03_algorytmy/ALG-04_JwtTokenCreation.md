# Algorytm: Tworzenie tokenu JWT (CreateToken)

| Atrybut | Wartość |
|---|---|
| ID | ALG-04 |
| Nazwa | JWT Token Creation |
| Kategoria | Bezpieczeństwo |
| Pliki | `AuthService.cs › CreateToken()` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Budowanie podpisanego tokenu JWT zawierającego claims użytkownika, używanego zarówno po rejestracji jak i po zalogowaniu.

## Kod źródłowy

```csharp
private string CreateToken(User user)
{
    var claims = new List<Claim>
    {
        new Claim("userId", user.Id.ToString()),
        new Claim("firstName", user.FirstName),
        new Claim("lastName", user.LastName),
        new Claim("email", user.Email),
        new Claim(ClaimTypes.Role, "User")
    };

    var key = new SymmetricSecurityKey(
        Encoding.UTF8.GetBytes(_configuration["AppSettings:Token"]!)
    );

    var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha512Signature);

    var token = new JwtSecurityToken(
        claims: claims,
        expires: DateTime.UtcNow.AddMinutes(10),
        signingCredentials: creds
    );

    return new JwtSecurityTokenHandler().WriteToken(token);
}
```

## Claims tokenu

| Claim | Typ | Wartość |
|---|---|---|
| `userId` | Custom | `user.Id.ToString()` |
| `firstName` | Custom | `user.FirstName` |
| `lastName` | Custom | `user.LastName` |
| `email` | Custom | `user.Email` |
| `role` | `ClaimTypes.Role` | `"User"` (stała wartość) |
| `exp` | Standard | `DateTime.UtcNow + 10 minut` |

## Parametry podpisywania

| Parametr | Wartość |
|---|---|
| Klucz | `AppSettings:Token` (z appsettings.json / środowiskowych) |
| Algorytm | `HmacSha512Signature` |
| Encoding | `UTF8` |

## Dostęp do claims na backendzie

```csharp
// W kontrolerze:
var userId = int.Parse(User.FindFirst("userId")!.Value);
var email = User.FindFirst("email")!.Value;
var role = User.FindFirst(ClaimTypes.Role)!.Value; // "User"
```

## Walidacja tokenu na backendzie (Program.cs)

```csharp
options.TokenValidationParameters = new TokenValidationParameters {
    ValidateIssuerSigningKey = true,
    IssuerSigningKey = new SymmetricSecurityKey(
        Encoding.UTF8.GetBytes(config["AppSettings:Token"]!)
    ),
    ValidateIssuer = false,
    ValidateAudience = false,
    ClockSkew = TimeSpan.Zero  // dokładne wygaśnięcie bez marginesu
};
```

## Anomalie

| # | Anomalia |
|---|---|
| JWT-01 | `!` (null-forgiving) przy odczycie klucza — jeśli `AppSettings:Token` nie istnieje, wyjątek runtime zamiast błędu konfiguracji |
| JWT-02 | `ValidateIssuer=false` + `ValidateAudience=false` — słabsze bezpieczeństwo |
| JWT-03 | 10 minut to bardzo krótki czas sesji |
| JWT-04 | Rola zawsze `"User"` (hardkodowana) — brak systemu ról |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
