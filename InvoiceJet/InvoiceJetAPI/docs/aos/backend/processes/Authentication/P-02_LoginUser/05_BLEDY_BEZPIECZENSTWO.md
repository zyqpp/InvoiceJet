# LoginUser — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

Walidacje sprawdzane w `AuthService.cs › AuthService.LoginUser` w podanej kolejności:

| ID | Reguła | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | Użytkownik z podanym e-mailem istnieje w `User` | `AuthService.cs › AuthService.LoginUser` — `_unitOfWork.Users.Query().FirstOrDefaultAsync(u => u.Email == userDto.Email)` | `user == null` (lub teoretycznie `user.Email != userDto.Email` — zawsze fałsz) | `UserNotFoundException` | `400` | `"User with email {email} not found."` |
| `WAL-02` | Hasło pasuje do BCrypt hash w `User.PasswordHash` | `AuthService.cs › AuthService.LoginUser` — `BC.Verify(userDto.Password, user.PasswordHash)` | `BC.Verify` zwraca `false` | `IncorrectPasswordException` | `400` | `"Password is incorrect."` |

> Brak atrybutów `[Required]` w `UserLoginDto`. Pola `null` nie są walidowane na poziomie DTO.

---

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie w middleware? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| `UserNotFoundException` | tak | `400 Bad Request` | `ExceptionMiddleware.cs` |
| `IncorrectPasswordException` | tak | `400 Bad Request` | `ExceptionMiddleware.cs` |

Oba wyjątki są poprawnie zmapowane w `ExceptionMiddleware`. Pełen rejestr: `../../KATALOG_WYJATKOW.md`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze/akcji | N/D — brak `[Authorize]` na `AuthController` i metodzie `Login` |
| Wymagana rola | brak — endpoint publiczny |
| Źródło tożsamości | N/D — proces uwierzytelnia przez e-mail + hasło, nie przez token |
| Token | N/D jako wejście; generowany i zwracany jako wyjście |

---

## 4. Uwagi bezpieczeństwa

- Komunikaty błędów rozróżniają „nie znaleziono użytkownika" (`WAL-01`) od „złe hasło" (`WAL-02`). Atakujący może enumerować istniejące adresy e-mail na podstawie odpowiedzi API — `400 "not found"` vs `400 "incorrect"`. [UWAGA: możliwy email enumeration attack — WYMAGA WERYFIKACJI Z ZESPOŁEM czy jest to akceptowalne ryzyko]
- Brak ograniczenia liczby prób logowania (rate limiting / lockout) — endpoint publiczny bez throttlingu.
- Weryfikacja hasła jest bezpieczna: `BC.Verify` porównuje hash z plaintext — hasło jawne nigdzie nie jest zapisywane.
- [UWAGA: redundantny warunek `user.Email != userDto.Email` w `WAL-01` jest martwym kodem — nie wpływa na bezpieczeństwo, ale sygnalizuje potencjalny błąd logiczny — WYMAGA WERYFIKACJI Z ZESPOŁEM]
