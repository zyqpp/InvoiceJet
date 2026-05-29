# Wystawienie nowej faktury — Błędy i bezpieczeństwo

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut kontrolera | `[Authorize(Roles = "User")]` |
| Schemat uwierzytelniania | `JwtBearerDefaults.AuthenticationScheme` |
| Źródło identyfikatora użytkownika | `IUserService.GetCurrentUserId()` |
| Wymagany token | Token JWT w nagłówku `Authorization` |

---

## Źródło kontekstu użytkownika

Proces nie przyjmuje `userId` ani `userFirmId` z body. Identyfikator użytkownika pochodzi z kontekstu HTTP przez `IUserService`.

Aktywna firma jest pobierana z repozytorium użytkowników:

```csharp
Users.GetUserFirmIdAsync(_userService.GetCurrentUserId())
```

---

## Błędy mapowane przez `ExceptionMiddleware`

| Warunek | Wyjątek | Status HTTP | Odpowiedź |
|---|---|---|---|
| Brak aktywnej firmy użytkownika | `UserHasNoAssociatedFirmException` | `400 Bad Request` | `{ "message": exception.Message }` |
| Brak aktywnego konta bankowego | `NoBankAccountAddedException` | `400 Bad Request` | `{ "message": exception.Message }` |
| Istniejący produkt nie został znaleziony | `Exception("Product not found.")` | `500 Internal Server Error` | `{ "message": "Product not found." }` |
| Inny nieobsłużony błąd | `Exception` | `500 Internal Server Error` | `{ "message": exception.Message }` |

---

## Błędy autoryzacji

| Warunek | Status HTTP | Źródło |
|---|---|---|
| Brak tokenu JWT | `401 Unauthorized` | ASP.NET Core Authentication |
| Token bez roli `User` | `403 Forbidden` | ASP.NET Core Authorization |

---

## Uwagi bezpieczeństwa

- Proces ustala `UserFirmId` po stronie API. Body żądania nie decyduje o aktywnej firmie użytkownika.
- Proces pobiera konto bankowe po `userFirmId` i `IsActive`.
- Proces przyjmuje `Client.Id` z body i przypisuje go do dokumentu bez widocznej weryfikacji relacji klienta z użytkownikiem. [UWAGA: weryfikacja własności klienta nie jest widoczna w `AddDocument` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- DTO nie zawiera atrybutów walidacyjnych dla pól wymaganych przez serwis. [UWAGA: brak widocznej walidacji DTO może skutkować błędami wykonania — WYMAGA WERYFIKACJI Z ZESPOŁEM]
