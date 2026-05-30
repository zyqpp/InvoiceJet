# RegisterUser — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

Walidacje sprawdzane w `AuthService.cs › AuthService.RegisterUser` w podanej kolejności:

| ID | Reguła | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | E-mail nie istnieje w tabeli `User` | `AuthService.cs › AuthService.RegisterUser` — `_unitOfWork.Users.Query().FirstOrDefaultAsync(u => u.Email == userDto.Email)` | `existingUser != null` | `UserAlreadyExistsException` | `400` | `"User with email {email} already exists."` |
| `WAL-02` | Hasło spełnia regex złożoności | `AuthService.cs › AuthService.RegisterUser` — `passwordRules.IsMatch(userDto.Password)` | regex nie pasuje | `InvalidPasswordException` | **`500`** ⚠ | `"Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character."` |
| `WAL-03` | `Password == PasswordConfirmation` | `AuthService.cs › AuthService.RegisterUser` — `userDto.Password != userDto.PasswordConfirmation` | hasła są różne | `PasswordMismatchException` | `400` | `"Password confirmation doesn't match."` |

> ⚠ `WAL-02`: `InvalidPasswordException` **nie jest jawnie mapowany** w `ExceptionMiddleware.cs`. Trafia do `catch (Exception ex)` → `500 Internal Server Error`. Oczekiwany byłby `400 Bad Request`. Szczegóły: `../../KATALOG_WYJATKOW.md`.

> Brak atrybutów walidacyjnych w `UserRegisterDto` — brak walidacji DTO (model validation). Pola `null` nie są odrzucane przez ASP.NET Core przed dotarciem do serwisu.

Regex dla `WAL-02` (dosłownie z kodu):
```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$
```
Wymagania: ≥8 znaków, przynajmniej jedna mała litera, jedna duża litera, jedna cyfra, jeden znak specjalny z zestawu `@$!%*?&`. Znaki spoza tego zestawu (np. `#`, `^`) nie są akceptowane nawet jeżeli hasło jest silne.

---

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie w middleware? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| `UserAlreadyExistsException` | tak | `400 Bad Request` | `ExceptionMiddleware.cs` |
| `InvalidPasswordException` | **nie** ⚠ | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all) |
| `PasswordMismatchException` | tak | `400 Bad Request` | `ExceptionMiddleware.cs` |

> ⚠ `InvalidPasswordException` brakuje w `ExceptionMiddleware`. Stan na kod źródłowy: `catch (AnafFirmNotFoundException ex)`, `catch (BankAccountAssociatedWithDocumentsException ex)`, ..., `catch (PasswordMismatchException ex)`, `catch (Exception ex)` — `InvalidPasswordException` nie pojawia się. Pełen rejestr: `../../KATALOG_WYJATKOW.md`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze/akcji | N/D — brak `[Authorize]` na `AuthController` i metodzie `Register` |
| Wymagana rola | brak — endpoint publiczny |
| Źródło tożsamości | N/D — proces nie odczytuje tożsamości wywołującego |
| Token | N/D jako wejście; generowany i zwracany jako wyjście |

---

## 4. Uwagi bezpieczeństwa

- [UWAGA: `InvalidPasswordException` zwraca `500` zamiast `400`. Klient otrzymuje szczegółowy komunikat o wymaganiach hasła przez 500 — jest to informacja wyciekająca przez błędny kod statusu — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: brak unikalnego indeksu DB na `User.Email` — możliwy wyścig dwóch równoległych rejestracji z tym samym e-mailem — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Hasło jest bezpiecznie haszowane BCrypt (`BC.HashPassword`) — hasło jawne nie jest nigdzie zapisywane ani logowane.
- Brak ograniczenia liczby prób rejestracji (rate limiting) — w kodzie nie widać throttlingu — endpoint publiczny.
