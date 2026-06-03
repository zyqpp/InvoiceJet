# LoginUser — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Użytkownik `tester+01@invoicejet.test` istnieje w tabeli `User` | rejestracja przez `POST /api/Auth/register` lub seed DB | `DT-02` (zarejestrowany użytkownik) |

Seed `DocumentType` / `DocumentStatus` nie jest wymagany dla logowania.

---

## 2. Dane poprawne (happy path)

### `TC-01` — Logowanie z poprawnymi danymi

Warunki wstępne: `DT-02` — użytkownik `tester+01@invoicejet.test` istnieje w bazie z hasłem `Strong@123`.

Żądanie (`POST /api/Auth/login`):
```json
{
  "email": "tester+01@invoicejet.test",
  "password": "Strong@123"
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `{ "token": "<jwt string>" }` — niepusty string JWT
- Skutek w bazie: brak (żaden rekord nie jest tworzony ani modyfikowany)
- Weryfikacja tokenu: zdekodowany JWT zawiera claimy `userId`, `firstName` (`"Anna"`), `lastName` (`"Testowa"`), `email` (`"tester+01@invoicejet.test"`), `ClaimTypes.Role` (`"User"`); token wygasa po 10 minutach

---

## 3. Dane niepoprawne (po jednej na regułę walidacji)

### `TC-N01` — łamie `WAL-01`: e-mail nie istnieje w bazie

Warunki wstępne: brak użytkownika `nonexistent@invoicejet.test` w bazie.

Żądanie:
```json
{
  "email": "nonexistent@invoicejet.test",
  "password": "Strong@123"
}
```
Oczekiwany rezultat:
- Status: `400 Bad Request`
- Odpowiedź: `{ "message": "User with email nonexistent@invoicejet.test not found." }`
- Skutek w bazie: brak zmian

---

### `TC-N02` — łamie `WAL-02`: błędne hasło

Warunki wstępne: `DT-02` — użytkownik `tester+01@invoicejet.test` istnieje z hasłem `Strong@123`.

Żądanie:
```json
{
  "email": "tester+01@invoicejet.test",
  "password": "WrongPassword@999"
}
```
Oczekiwany rezultat:
- Status: `400 Bad Request`
- Odpowiedź: `{ "message": "Password is incorrect." }`
- Skutek w bazie: brak zmian

---

## 4. Wartości brzegowe

| ID | Pole | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|
| `TC-B01` | `email` | `""` (pusty string) | `400` — `UserNotFoundException` (jeżeli user z `Email=""` nie istnieje) |
| `TC-B02` | `email` | `null` | `500` — `NullReferenceException` (brak `[Required]`) |
| `TC-B03` | `password` | `null` | `500` — `ArgumentNullException` lub `NullReferenceException` w `BC.Verify(null, hash)` |
| `TC-B04` | `password` | `""` (pusty string) | `400` — `IncorrectPasswordException` (`BC.Verify("", hash)` zwróci `false`) |
| `TC-B05` | `email` | adres e-mail z wielkich liter (`"TESTER+01@INVOICEJET.TEST"`) | zależy od collation SQL Server — domyślnie case-insensitive (`400` lub `200` w zależności od środowiska) [WYMAGA WERYFIKACJI] |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-02` | Zarejestrowany użytkownik `tester+01@invoicejet.test` z hasłem `Strong@123` | `TC-01`, `TC-N02` |
