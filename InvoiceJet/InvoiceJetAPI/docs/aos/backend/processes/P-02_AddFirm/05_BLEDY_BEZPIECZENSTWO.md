# Dodanie firmy — Błędy i bezpieczeństwo

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut kontrolera | `[Authorize(Roles = "User")]` |
| Schemat uwierzytelniania | `JwtBearerDefaults.AuthenticationScheme` |
| Źródło identyfikatora użytkownika | `IUserService.GetCurrentUserId()` |
| Wymagany token | Token JWT w nagłówku `Authorization` |

---

## Źródło kontekstu użytkownika

Proces nie przyjmuje identyfikatora użytkownika z body ani z trasy. Identyfikator użytkownika pochodzi z kontekstu HTTP przez `IUserService`.

Relacja `UserFirm` jest tworzona dla użytkownika zwróconego przez:

```csharp
_userService.GetCurrentUserId()
```

---

## Błędy autoryzacji

| Warunek | Status HTTP | Źródło |
|---|---|---|
| Brak tokenu JWT | `401 Unauthorized` | ASP.NET Core Authentication |
| Token bez roli `User` | `403 Forbidden` | ASP.NET Core Authorization |

---

## Błędy procesu

| Warunek | Status HTTP | Źródło |
|---|---|---|
| Błąd EF Core przy zapisie firmy | `500 Internal Server Error` | `ExceptionMiddleware` dla `Exception` |
| Błąd EF Core przy zapisie relacji | `500 Internal Server Error` | `ExceptionMiddleware` dla `Exception` |
| Brak użytkownika przy `Users.GetUserByIdAsync(...)` | `500 Internal Server Error` | Użycie `user!` może spowodować błąd wykonania. |

---

## Uwagi bezpieczeństwa

- `UserId` nie pochodzi z żądania. API ustala użytkownika na podstawie tokenu.
- Parametr `isClient` pochodzi z trasy i bezpośrednio ustawia `UserFirm.IsClient`.
- Proces nie sprawdza unikalności `Cui`. [UWAGA: duplikaty firm według CUI nie są blokowane w `AddFirm` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Proces nie sprawdza, czy `FirmDto.Id` ma wartość `0` dla nowej firmy. [UWAGA: zachowanie dla niezerowego `FirmDto.Id` zależy od EF Core — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Proces może ustawić pierwszą dodaną firmę jako `ActiveUserFirm` niezależnie od wartości `isClient`. [UWAGA: brak warunku `isClient == false` przy ustawianiu aktywnej firmy — WYMAGA WERYFIKACJI Z ZESPOŁEM]
