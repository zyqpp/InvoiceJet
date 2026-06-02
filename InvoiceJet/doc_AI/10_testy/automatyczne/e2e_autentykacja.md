# Scenariusze testów automatycznych E2E: Autentykacja

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-AUTO-E2E-AUTH |
| Typ dokumentu | scenariusze testów automatycznych E2E |
| Wersja | 1.0 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-06-02 |
| Narzędzie | Playwright (TypeScript) |

## Streszczenie

Scenariusze pokrywają pełny cykl autentykacji: rejestrację nowego użytkownika, logowanie, obsługę wygasłego tokenu JWT oraz walidację hasła po stronie frontendu. Wszystkie selektory są zweryfikowane w kodzie Angular Material (komponenty: `register.component.html`, `login.component.html`).

---

## TC-AUTO-001: Rejestracja nowego użytkownika (happy path)

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane algorytmy:**
- [ALG-04 JWT Token Creation](../../03_algorytmy/ALG-04_JwtTokenCreation.md)
- [ALG-03 Password Hashing](../../03_algorytmy/ALG-03_PasswordHashingVerification.md)

**Powiązane API:**
- `POST /api/Auth/register`

**Prereq w DB:**
- Brak konta z adresem `auto_register_001@invoicejet.test` w tabeli `User`

### Kroki

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | navigate | URL bar | `/register` | Strona załadowana; widoczny `mat-card-title` z tekstem "Register"; formularz `[formGroup="registerForm"]` aktywny |
| 2 | fill | `mat-form-field input[formControlName="firstName"]` | `Jan` | Pole wypełnione wartością "Jan" |
| 3 | fill | `mat-form-field input[formControlName="lastName"]` | `Kowalski` | Pole wypełnione wartością "Kowalski" |
| 4 | fill | `mat-form-field input[formControlName="email"]` | `auto_register_001@invoicejet.test` | Pole wypełnione; brak czerwonego `mat-error` |
| 5 | fill | `mat-form-field input[formControlName="password"]` | `Register1!` | Pole wypełnione; typ pola = `password` (wartość zamaskowana) |
| 6 | fill | `mat-form-field input[formControlName="passwordConfirmation"]` | `Register1!` | Pole wypełnione; wartość identyczna z polem password |
| 7 | click | `button[mat-raised-button][type="submit"]` | — | Żądanie `POST /api/Auth/register` wysłane (monitoruj Network tab); status odpowiedzi 200 OK |
| 8 | expect redirect | URL bar | `/dashboard` | Przeglądarka jest na `/dashboard`; widoczny komponent dashboard |
| 9 | evaluate localStorage | `window.localStorage.getItem('authToken')` | — | Wartość nie jest `null`; string zaczyna się od `eyJ` (base64 JWT header) |

### Walidacja algorytmu

| Weryfikacja | Oczekiwana wartość | Jak sprawdzić |
|---|---|---|
| [ALG-04] Token JWT zapisany w localStorage | `localStorage.authToken` nie jest null; zaczyna się od `eyJ` | `page.evaluate(() => localStorage.getItem('authToken'))` w Playwright |
| [ALG-04] Payload JWT zawiera userId i email | Po Base64-decode środkowej części tokenu: pola `userId` (int) i `email` ("auto_register_001@invoicejet.test") obecne | Dekoduj JWT payload w teście: `JSON.parse(atob(token.split('.')[1]))` |
| [ALG-03] Hasło nie jest przechowywane plain-text | Kolumna `PasswordHash` w tabeli `User` zaczyna się od `$2a$` (BCrypt) | Zapytanie DB: `SELECT PasswordHash FROM Users WHERE Email = 'auto_register_001@invoicejet.test'` |

### Cleanup

- Usuń rekord z `Users` gdzie `Email = 'auto_register_001@invoicejet.test'`
- Usuń powiązany rekord `UserFirm` (kaskadowo lub ręcznie)

---

## TC-AUTO-002: Logowanie istniejącego użytkownika (happy path)

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane algorytmy:**
- [ALG-01 JWT Authentication Pipeline](../../03_algorytmy/ALG-01_JwtAuthentication.md)
- [ALG-03 Password Hashing](../../03_algorytmy/ALG-03_PasswordHashingVerification.md)

**Powiązane API:**
- `POST /api/Auth/login`

**Prereq w DB:**
- Konto `auto_login_002@invoicejet.test` z hasłem `Login002!` istnieje w tabeli `User` (wstawione przez fixture lub po TC-AUTO-001)
- Rekord `UserFirm` powiązany z tym kontem istnieje

### Kroki

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | navigate | URL bar | `/login` | Strona załadowana; `mat-card-title` z tekstem "Login"; formularz `[formGroup="loginForm"]` aktywny |
| 2 | verify element | `mat-form-field input[formControlName="email"]` | — | Element widoczny i interaktywny |
| 3 | verify element | `mat-form-field input[formControlName="password"]` | — | Element widoczny i interaktywny |
| 4 | fill | `mat-form-field input[formControlName="email"]` | `auto_login_002@invoicejet.test` | Pole wypełnione; placeholder "pat@example.com" zastąpiony wartością |
| 5 | fill | `mat-form-field input[formControlName="password"]` | `Login002!` | Pole wypełnione; typ = `password` (zamaskowane) |
| 6 | click | `button[mat-raised-button][color="primary"][type="submit"]` | — | Żądanie `POST /api/Auth/login` wysłane; status 200 OK |
| 7 | expect redirect | URL bar | `/dashboard` | URL zmieniony na `/dashboard`; widoczny dashboard |
| 8 | evaluate localStorage | `window.localStorage.getItem('authToken')` | — | Token JWT obecny; nie jest null |
| 9 | verify absence | `div.p-error` | — | Komunikat błędu `errorMessage` NIE jest widoczny |

### Walidacja algorytmu

| Weryfikacja | Oczekiwana wartość | Jak sprawdzić |
|---|---|---|
| [ALG-01] Token JWT w localStorage | `localStorage.authToken` string z 3 segmentami oddzielonymi `.` | `token.split('.').length === 3` |
| [ALG-01] Claim `userId` w payload | Wartość liczbowa (int > 0) | Dekoduj payload JWT: `JSON.parse(atob(token.split('.')[1])).userId` |
| [ALG-01] Claim `firstName` w payload | `"Jan"` (lub imię zarejestrowane) | `JSON.parse(atob(token.split('.')[1])).firstName` |
| [ALG-01] Claim `email` w payload | `"auto_login_002@invoicejet.test"` | `JSON.parse(atob(token.split('.')[1])).email` |

### Cleanup

- Wyczyść `localStorage` po teście: `page.evaluate(() => localStorage.clear())`
- Nie usuwaj konta (może być reużyte przez TC-AUTO-003)

---

## TC-AUTO-003: Wygaśnięcie tokenu JWT — pojawienie się TokenExpiredDialog

**Typ:** Anomalia / Edge case
**Priorytet:** Wysoki
**Powiązane algorytmy:**
- [ALG-01 JWT Authentication Pipeline](../../03_algorytmy/ALG-01_JwtAuthentication.md)

**Powiązane API:**
- `GET /api/Document/GetTableRecords` (dowolny chroniony endpoint)

**Prereq w DB:**
- Konto `auto_login_002@invoicejet.test` istnieje (prereq z TC-AUTO-002)

### Kroki

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | navigate | URL bar | `/login` | Strona logowania załadowana |
| 2 | fill | `mat-form-field input[formControlName="email"]` | `auto_login_002@invoicejet.test` | Pole wypełnione |
| 3 | fill | `mat-form-field input[formControlName="password"]` | `Login002!` | Pole wypełnione |
| 4 | click | `button[mat-raised-button][type="submit"]` | — | Login udany; redirect do `/dashboard`; `localStorage.authToken` ustawiony |
| 5 | evaluate | `window.localStorage.setItem('authToken', EXPIRED_TOKEN)` | Wygasły token JWT: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIxIiwiZW1haWwiOiJhdXRvX2xvZ2luXzAwMkBpbnZvaWNlamV0LnRlc3QiLCJleHAiOjE2MDAwMDAwMDB9.INVALID_SIG` | Token w localStorage zastąpiony wygasłym tokenem |
| 6 | navigate | URL bar | `/dashboard/invoices` | Przeglądarka wysyła `GET /api/Document/GetTableRecords` z nagłówkiem `Authorization: Bearer <expired_token>`; serwer odpowiada 401 Unauthorized |
| 7 | expect element visible | `mat-dialog-container` | — | Dialog `TokenExpiredDialogComponent` pojawia się w ciągu 3 sekund |
| 8 | verify text in dialog | `mat-dialog-container` | Dowolny tekst informujący o wygaśnięciu sesji | `mat-dialog-container` zawiera tekst informacyjny (np. "Session expired" lub "Token expired") |
| 9 | click | `mat-dialog-container button[mat-raised-button]` | — | Dialog zamknięty; `localStorage.authToken` usunięty lub null |
| 10 | expect redirect | URL bar | `/login` | Użytkownik na stronie `/login` |

### Walidacja algorytmu

| Weryfikacja | Oczekiwana wartość | Jak sprawdzić |
|---|---|---|
| [ALG-01] HTTP Interceptor przechwytuje 401 | `TokenExpiredDialogComponent` zostaje otwarty | `mat-dialog-container` widoczny w DOM |
| [ALG-01] Token usunięty po zamknięciu dialogu | `localStorage.authToken` = null | `page.evaluate(() => localStorage.getItem('authToken'))` === null |
| [ALG-01] Redirect na `/login` po dialogu | URL = `/login` | `page.url()` ends with `/login` |

### Cleanup

- Wyczyść localStorage
- Użytkownik wraca do strony `/login` automatycznie

---

## TC-AUTO-004: Walidacja hasła — przypadki negatywne (frontend)

**Typ:** Negatywny
**Priorytet:** Wysoki
**Powiązane algorytmy:**
- [ALG-03 Password Hashing](../../03_algorytmy/ALG-03_PasswordHashingVerification.md)

**Powiązane API:**
- `POST /api/Auth/register` (oczekiwany status 400 lub brak wywołania dla walidacji frontendowej)

**Prereq w DB:**
- Brak (test walidacji frontendowej, nie wymaga DB)

### Kroki — podscenariusz A: Hasło za krótkie (< 8 znaków)

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | navigate | URL bar | `/register` | Strona rejestracji załadowana |
| 2 | fill | `mat-form-field input[formControlName="firstName"]` | `Test` | Pole wypełnione |
| 3 | fill | `mat-form-field input[formControlName="lastName"]` | `Walidacja` | Pole wypełnione |
| 4 | fill | `mat-form-field input[formControlName="email"]` | `walidacja_a@invoicejet.test` | Pole wypełnione |
| 5 | fill | `mat-form-field input[formControlName="password"]` | `Kr0t!` | Pole wypełnione (5 znaków — poniżej limitu 8) |
| 6 | fill | `mat-form-field input[formControlName="passwordConfirmation"]` | `Kr0t!` | Pole wypełnione |
| 7 | click | `button[mat-raised-button][type="submit"]` | — | Formularz NIE jest wysłany do API LUB API zwraca 400; brak redirect na `/dashboard` |
| 8 | expect error visible | `mat-form-field:has(input[formControlName="password"]) mat-error` | — | Komunikat błędu widoczny pod polem hasła |

### Kroki — podscenariusz B: Brak wielkiej litery

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | navigate | URL bar | `/register` | Strona rejestracji załadowana |
| 2 | fill | `mat-form-field input[formControlName="firstName"]` | `Test` | Pole wypełnione |
| 3 | fill | `mat-form-field input[formControlName="lastName"]` | `Walidacja` | Pole wypełnione |
| 4 | fill | `mat-form-field input[formControlName="email"]` | `walidacja_b@invoicejet.test` | Pole wypełnione |
| 5 | fill | `mat-form-field input[formControlName="password"]` | `malelitry1!` | Pole wypełnione (8 znaków, brak wielkiej litery, ma cyfrę i znak specjalny) |
| 6 | fill | `mat-form-field input[formControlName="passwordConfirmation"]` | `malelitry1!` | Pole wypełnione |
| 7 | click | `button[mat-raised-button][type="submit"]` | — | Formularz NIE jest wysłany do API LUB API zwraca 400 |
| 8 | verify no redirect | URL bar | — | URL pozostaje `/register`; brak `localStorage.authToken` |

### Kroki — podscenariusz C: Brak cyfry

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | navigate | URL bar | `/register` | Strona rejestracji załadowana |
| 2 | fill | `mat-form-field input[formControlName="firstName"]` | `Test` | Pole wypełnione |
| 3 | fill | `mat-form-field input[formControlName="lastName"]` | `Walidacja` | Pole wypełnione |
| 4 | fill | `mat-form-field input[formControlName="email"]` | `walidacja_c@invoicejet.test` | Pole wypełnione |
| 5 | fill | `mat-form-field input[formControlName="password"]` | `BezCyfry!` | Pole wypełnione (9 znaków, wielka litera, znak specjalny, brak cyfry) |
| 6 | fill | `mat-form-field input[formControlName="passwordConfirmation"]` | `BezCyfry!` | Pole wypełnione |
| 7 | click | `button[mat-raised-button][type="submit"]` | — | Formularz NIE jest wysłany do API LUB API zwraca 400 |
| 8 | verify no redirect | URL bar | — | URL pozostaje `/register`; brak `localStorage.authToken` |

### Kroki — podscenariusz D: Poprawne hasło (weryfikacja pozytywna, kontrolna)

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | navigate | URL bar | `/register` | Strona rejestracji załadowana |
| 2 | fill | `mat-form-field input[formControlName="firstName"]` | `Test` | Pole wypełnione |
| 3 | fill | `mat-form-field input[formControlName="lastName"]` | `Poprawny` | Pole wypełnione |
| 4 | fill | `mat-form-field input[formControlName="email"]` | `walidacja_d@invoicejet.test` | Pole wypełnione |
| 5 | fill | `mat-form-field input[formControlName="password"]` | `Poprawne1!` | Pole wypełnione (wielka litera + cyfra + znak specjalny `!` + 9 znaków) |
| 6 | fill | `mat-form-field input[formControlName="passwordConfirmation"]` | `Poprawne1!` | Pole wypełnione |
| 7 | click | `button[mat-raised-button][type="submit"]` | — | `POST /api/Auth/register` wywołany; status 200 OK |
| 8 | expect redirect | URL bar | `/dashboard` | Redirect na `/dashboard`; token w localStorage |

### Walidacja algorytmu

| Weryfikacja | Oczekiwana wartość | Jak sprawdzić |
|---|---|---|
| [ALG-03] Regex hasła — min 8 znaków | Hasło `Kr0t!` (5 znaków) odrzucone | URL pozostaje `/register` po submit; brak authToken w localStorage |
| [ALG-03] Regex hasła — wymagana wielka litera | Hasło `malelitry1!` odrzucone | URL pozostaje `/register` po submit |
| [ALG-03] Regex hasła — wymagana cyfra | Hasło `BezCyfry!` odrzucone | URL pozostaje `/register` po submit |
| [ALG-03] Dozwolone znaki specjalne: `@$!%*?&` | Hasło `Poprawne1!` przyjęte | Redirect na `/dashboard` |

### Cleanup

- Usuń konto `walidacja_d@invoicejet.test` jeśli zostało utworzone (podscenariusz D)
- Wyczyść localStorage

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. Selektory zweryfikowane w `register.component.html` i `login.component.html`. |
