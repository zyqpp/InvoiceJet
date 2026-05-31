# Scenariusze testowe manualne: Autentykacja

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-MAN-AUTENTYKACJA |
| Typ dokumentu | scenariusze testowe manualne |
| Wersja | 0.1 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Scenariusze testowe obejmują rejestrację nowego konta, logowanie, walidację siły hasła oraz zachowanie systemu po wygaśnięciu tokenu JWT. Powiązane z UC-Globalny-Autentykacja i endpointami API-01, API-02.

---

## TC-100: Rejestracja z poprawnymi danymi (happy path)

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** UC-Globalny-Autentykacja, API-01

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Otwórz stronę `/register` | — | Formularz rejestracji widoczny z polami: imię, nazwisko, e-mail, hasło, powtórz hasło |
| 2 | Wypełnij formularz poprawnymi danymi | Imię: `Jan`, Nazwisko: `Kowalski`, e-mail: `test@example.com`, hasło: `Test@123`, powtórz: `Test@123` | Wszystkie pola wypełnione, przycisk „Zarejestruj się" aktywny |
| 3 | Kliknij „Zarejestruj się" | — | Wywołanie `POST /api/Auth/register` — status 200 OK |
| 4 | Sprawdź odpowiedź API | — | Response zawiera token JWT; token zapisany w `localStorage` pod kluczem `authToken` |
| 5 | Sprawdź przekierowanie | — | Użytkownik zostaje przekierowany na `/dashboard` |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-101: Rejestracja — hasło za krótkie (< 8 znaków)

**Typ:** Negatywny
**Priorytet:** Wysoki
**Powiązane:** UC-Globalny-Autentykacja (scenariusz A2), API-01

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Otwórz stronę `/register` | — | Formularz rejestracji widoczny |
| 2 | Wypełnij formularz z hasłem 7-znakowym | e-mail: `test@example.com`, hasło: `Te@1234` (7 znaków) | Pole hasła wypełnione |
| 3 | Kliknij „Zarejestruj się" | — | Wywołanie `POST /api/Auth/register` — status 400 Bad Request |
| 4 | Sprawdź komunikat błędu | — | Frontend wyświetla komunikat o wymaganiach hasła (min. 8 znaków) |
| 5 | Sprawdź stan formularza | — | Formularz pozostaje aktywny, dane użytkownika zachowane |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-102: Rejestracja — brak wymaganych znaków specjalnych

**Typ:** Negatywny
**Priorytet:** Wysoki
**Powiązane:** UC-Globalny-Autentykacja (scenariusz A2), API-01

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Otwórz stronę `/register` | — | Formularz rejestracji widoczny |
| 2 | Wypełnij hasło bez znaku specjalnego | hasło: `TestAbc1` (brak `@$!%*?&`) | Pole hasła wypełnione |
| 3 | Kliknij „Zarejestruj się" | — | Wywołanie `POST /api/Auth/register` — status 400 Bad Request |
| 4 | Sprawdź komunikat | — | Komunikat informuje o wymaganiu znaku specjalnego z zestawu `@$!%*?&` |
| 5 | Powtórz test z hasłem `TestAbc1!` | hasło: `TestAbc1!` | Status 200 OK — znak `!` jest w dozwolonym zestawie |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-103: Rejestracja — email już zajęty

**Typ:** Negatywny
**Priorytet:** Wysoki
**Powiązane:** UC-Globalny-Autentykacja (scenariusz A1), API-01

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Upewnij się, że konto `test@example.com` już istnieje w systemie | e-mail: `test@example.com` | Konto istnieje (po TC-100) |
| 2 | Otwórz `/register` i wypełnij formularz ponownie tym samym e-mailem | e-mail: `test@example.com`, hasło: `Test@123` | Formularz wypełniony |
| 3 | Kliknij „Zarejestruj się" | — | Wywołanie `POST /api/Auth/register` |
| 4 | Sprawdź odpowiedź API | — | Status błędu (np. 400 lub 409); odpowiedź wskazuje na zajęty adres e-mail |
| 5 | Sprawdź komunikat na UI | — | Frontend wyświetla komunikat „Adres e-mail jest już zarejestrowany" lub równoważny |
| 6 | Sprawdź stan formularza | — | Formularz pozostaje aktywny |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-104: Logowanie z poprawnymi danymi (happy path)

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** UC-Globalny-Autentykacja, API-02

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Otwórz stronę `/login` | — | Formularz logowania widoczny z polami: e-mail, hasło |
| 2 | Wypełnij formularz | e-mail: `test@example.com`, hasło: `Test@123` | Pola wypełnione |
| 3 | Kliknij „Zaloguj się" | — | Wywołanie `POST /api/Auth/login` — status 200 OK |
| 4 | Sprawdź odpowiedź | — | Response zawiera token JWT z claimami: `userId`, `firstName`, `email` |
| 5 | Sprawdź localStorage | — | Klucz `authToken` zawiera token JWT |
| 6 | Sprawdź przekierowanie | — | Użytkownik przekierowany na `/dashboard` |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-105: Logowanie — błędne hasło

**Typ:** Negatywny
**Priorytet:** Wysoki
**Powiązane:** UC-Globalny-Autentykacja (scenariusz A3), API-02

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Otwórz stronę `/login` | — | Formularz logowania widoczny |
| 2 | Wypełnij e-mail poprawnymi danymi, hasło błędne | e-mail: `test@example.com`, hasło: `BledneHaslo1!` | Pola wypełnione |
| 3 | Kliknij „Zaloguj się" | — | Wywołanie `POST /api/Auth/login` — status 401 Unauthorized |
| 4 | Sprawdź komunikat na UI | — | Frontend wyświetla komunikat „Nieprawidłowy login lub hasło" lub równoważny |
| 5 | Sprawdź localStorage | — | Klucz `authToken` nie istnieje lub nie został zaktualizowany |
| 6 | Sprawdź stan formularza | — | Formularz pozostaje aktywny |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-106: Wygaśnięcie tokenu JWT (po 10 minutach)

**Typ:** Negatywny / Anomalia
**Priorytet:** Wysoki
**Powiązane:** UC-Globalny-Autentykacja (scenariusz A4), API-02

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Zaloguj się na konto testowe | e-mail: `test@example.com`, hasło: `Test@123` | Zalogowano, token w localStorage |
| 2 | Odczekaj ponad 10 minut bez wykonywania żadnych żądań API | Czas: > 10 minut | Token JWT wygasł (exp claim przekroczony) |
| 3 | Wykonaj dowolną akcję wymagającą autoryzacji (np. przejdź do listy faktur) | — | Żądanie do API wraca z 401 Unauthorized |
| 4 | Sprawdź zachowanie frontendu | — | `JwtInterceptor` przechwytuje 401 i otwiera `TokenExpiredDialogComponent` |
| 5 | Sprawdź dialog | — | Widoczny dialog informujący o wygaśnięciu sesji |
| 6 | Potwierdź lub zamknij dialog | — | Token usunięty z localStorage; użytkownik przekierowany na `/login` |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
