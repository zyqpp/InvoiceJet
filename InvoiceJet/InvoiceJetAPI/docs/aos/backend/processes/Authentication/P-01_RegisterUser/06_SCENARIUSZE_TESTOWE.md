# RegisterUser — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Brak użytkownika z e-mailem `tester+01@invoicejet.test` w tabeli `User` | czysty stan bazy / sprzątanie po poprzednim teście | `DT-01` (precondition negatywna) |

Nie są wymagane żadne dodatkowe rekordy słownikowe. Seed `DocumentType` / `DocumentStatus` nie jest używany w tym procesie.

---

## 2. Dane poprawne (happy path)

### `TC-01` — Rejestracja nowego użytkownika z poprawnymi danymi

Warunki wstępne: brak użytkownika `tester+01@invoicejet.test` w bazie (`DT-01`).

Żądanie (`POST /api/Auth/register`):
```json
{
  "firstName": "Anna",
  "lastName": "Testowa",
  "email": "tester+01@invoicejet.test",
  "password": "Strong@123",
  "passwordConfirmation": "Strong@123"
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `{ "token": "<jwt string>" }` — niepusty string JWT
- Skutek w bazie: nowy rekord w tabeli `User`:
  - `Email = "tester+01@invoicejet.test"`
  - `FirstName = "Anna"`, `LastName = "Testowa"`
  - `PasswordHash` — hash BCrypt (zaczyna się od `$2a$` lub `$2b$`)
  - `Role = "User"`
  - `ActiveUserFirmId = NULL`

---

## 3. Dane niepoprawne (po jednej na regułę walidacji)

### `TC-N01` — łamie `WAL-01`: e-mail już zarejestrowany

Warunki wstępne: użytkownik `tester+01@invoicejet.test` **istnieje** w bazie (np. po `TC-01`).

Żądanie:
```json
{
  "firstName": "Drugi",
  "lastName": "Uzytkownik",
  "email": "tester+01@invoicejet.test",
  "password": "Strong@123",
  "passwordConfirmation": "Strong@123"
}
```
Oczekiwany rezultat:
- Status: `400 Bad Request`
- Odpowiedź: `{ "message": "User with email tester+01@invoicejet.test already exists." }`
- Skutek w bazie: brak zmian

---

### `TC-N02` — łamie `WAL-02`: hasło nie spełnia wymagań złożoności

Warunki wstępne: brak użytkownika `tester+02@invoicejet.test`.

Żądanie — brak znaku specjalnego:
```json
{
  "firstName": "Anna",
  "lastName": "Testowa",
  "email": "tester+02@invoicejet.test",
  "password": "Weakpassword1",
  "passwordConfirmation": "Weakpassword1"
}
```
Oczekiwany rezultat:
- Status: **`500 Internal Server Error`** ⚠ (błąd mapowania — powinno być 400)
- Odpowiedź: `{ "message": "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character." }`
- Skutek w bazie: brak zmian

---

### `TC-N03` — łamie `WAL-03`: hasła nie są identyczne

Warunki wstępne: brak użytkownika `tester+03@invoicejet.test`.

Żądanie:
```json
{
  "firstName": "Anna",
  "lastName": "Testowa",
  "email": "tester+03@invoicejet.test",
  "password": "Strong@123",
  "passwordConfirmation": "Different@456"
}
```
Oczekiwany rezultat:
- Status: `400 Bad Request`
- Odpowiedź: `{ "message": "Password confirmation doesn't match." }`
- Skutek w bazie: brak zmian

---

## 4. Wartości brzegowe

| ID | Pole | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|
| `TC-B01` | `email` | `""` (pusty string) | `400` — `UserAlreadyExistsException` jeżeli user z `Email=""` istnieje; w przeciwnym razie próba inserta z pustym email → wynik zależy od DB |
| `TC-B02` | `email` | `null` | `500` — `NullReferenceException` lub błąd EF Core (brak `[Required]` w DTO) |
| `TC-B03` | `password` | `null` | `500` — `NullReferenceException` przy `passwordRules.IsMatch(null)` lub `BC.HashPassword(null)` |
| `TC-B04` | `password` | `"1234567"` (7 znaków) | `500` — `InvalidPasswordException` (regex nie spełniony, ale status 500 przez błąd mapowania) |
| `TC-B05` | `password` | `"Short1@"` (8 znaków — min) | `200 OK` — spełnia regex (≥8, wielka, mała, cyfra, specjalny) |
| `TC-B06` | `password` | `"Strong#123"` (znak `#` spoza zestawu `@$!%*?&`) | `500` — `InvalidPasswordException` — znak `#` nie jest zaakceptowany przez regex |
| `TC-B07` | `email` | duplikat (drugi request z tym samym mailem bez usunięcia) | `400` — `UserAlreadyExistsException` |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-01` | Dane rejestracji nowego użytkownika (precondition: brak w bazie) | `TC-01`, `TC-N01` (jako precondition negatywna — user MUSI istnieć) |
