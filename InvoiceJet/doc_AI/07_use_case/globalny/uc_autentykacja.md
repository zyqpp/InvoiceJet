# Use Case: Autentykacja użytkownika

| Pole | Wartość |
|---|---|
| ID dokumentu | UC-Globalny-Autentykacja |
| Typ dokumentu | use case |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Przypadek użycia opisuje trzy powiązane procesy autentykacji: rejestrację nowego konta, logowanie do istniejącego konta oraz wylogowanie. Obejmuje również scenariusz automatycznego wygaśnięcia sesji JWT po 10 minutach. Wszystkie trzy operacje są dostępne bez uprzedniego zalogowania, z wyjątkiem wylogowania.

## Aktorzy

| Aktor | Rola |
|---|---|
| Użytkownik | Osoba rejestrująca konto lub logująca się do istniejącego konta w aplikacji InvoiceJet |

## Warunki wstępne

- Aplikacja dostępna pod adresem `/login` lub `/register`
- Backend InvoiceJet API dostępny i odpowiadający

## Scenariusz główny — Rejestracja

1. Użytkownik otwiera `/register`
2. Wypełnia formularz: imię, nazwisko, adres e-mail, hasło (x2)
3. Klika „Zarejestruj się" → system wywołuje `POST /api/Auth/register`
4. Backend waliduje unikalność adresu e-mail w bazie
5. Backend weryfikuje hasło przez wyrażenie regularne (min. 8 znaków, wielka litera, mała litera, cyfra, znak specjalny `@$!%*?&`)
6. Backend haszuje hasło algorytmem BCrypt
7. Backend tworzy rekordy `User` i `UserFirm` w bazie danych
8. Backend generuje i zwraca token JWT (ważny 10 minut)
9. Frontend zapisuje token w `localStorage` pod kluczem `authToken`
10. Użytkownik zostaje przekierowany na `/dashboard`

## Scenariusz główny — Logowanie

1. Użytkownik otwiera `/login`
2. Wypełnia adres e-mail i hasło
3. Klika „Zaloguj się" → system wywołuje `POST /api/Auth/login`
4. Backend weryfikuje istnienie adresu e-mail w bazie
5. Backend weryfikuje hasło przez `BCrypt.Verify`
6. Backend generuje i zwraca token JWT (ważny 10 minut)
7. Frontend zapisuje token w `localStorage` pod kluczem `authToken`
8. Użytkownik zostaje przekierowany na `/dashboard`

## Scenariusz główny — Wylogowanie

1. Użytkownik klika „Wyloguj" w nawigacji
2. Frontend usuwa token z `localStorage` (`localStorage.removeItem("authToken")`)
3. Użytkownik zostaje przekierowany na `/login`
4. Brak server-side invalidation tokenu — token wygasa naturalnie po upływie 10 minut

## Scenariusze alternatywne

### A1: Błąd rejestracji — e-mail już istnieje

1. Backend zwraca odpowiedź z kodem błędu (email zajęty)
2. Frontend wyświetla komunikat o zajętym adresie e-mail
3. Formularz pozostaje aktywny — użytkownik może poprawić dane

### A2: Błąd rejestracji — hasło nie spełnia wymagań

1. Backend zwraca błąd walidacji wyrażenia regularnego
2. Frontend wyświetla komunikat z wymaganiami dotyczącymi hasła
3. Formularz pozostaje aktywny

### A3: Błąd logowania — nieprawidłowe dane

1. Backend zwraca 401 Unauthorized
2. Frontend wyświetla komunikat o nieprawidłowym loginie lub haśle
3. Formularz pozostaje aktywny

### A4: Wygaśnięcie sesji JWT

1. Użytkownik pracuje w aplikacji przez ponad 10 minut
2. Token JWT wygasa
3. Kolejne żądanie do API zwraca 401 Unauthorized
4. `JwtInterceptor` przechwytuje odpowiedź i otwiera `TokenExpiredDialogComponent`
5. Token jest usuwany z `localStorage`
6. Użytkownik zostaje przekierowany na `/login`

## Diagram (Mermaid flowchart)

```mermaid
flowchart TD
    Start([Start]) --> Choice{Akcja}
    Choice -->|Rejestracja| Reg_Form[Otwórz /register]
    Choice -->|Logowanie| Log_Form[Otwórz /login]
    Choice -->|Wylogowanie| Logout[Klik Wyloguj]

    Reg_Form --> Reg_Fill[Wypełnij formularz\nimię, nazwisko, email, hasło x2]
    Reg_Fill --> Reg_Submit[POST /api/Auth/register]
    Reg_Submit --> Reg_Val{Walidacja\nbackend}
    Reg_Val -->|email zajęty| Reg_ErrEmail[Komunikat: e-mail zajęty]
    Reg_ErrEmail --> Reg_Fill
    Reg_Val -->|hasło za słabe| Reg_ErrPass[Komunikat: wymagania hasła]
    Reg_ErrPass --> Reg_Fill
    Reg_Val -->|OK| Reg_Hash[BCrypt haszowanie\nTworzenie User + UserFirm]
    Reg_Hash --> JWT_New[Generuj JWT 10 min]
    JWT_New --> Save[Zapisz w localStorage]
    Save --> Dashboard[/dashboard]

    Log_Form --> Log_Fill[Wypełnij email + hasło]
    Log_Fill --> Log_Submit[POST /api/Auth/login]
    Log_Submit --> Log_Val{Weryfikacja\nBCrypt}
    Log_Val -->|błąd| Log_Err[Komunikat: nieprawidłowe dane]
    Log_Err --> Log_Fill
    Log_Val -->|OK| JWT_Login[Generuj JWT 10 min]
    JWT_Login --> Save

    Logout --> Remove[localStorage.removeItem\nauthToken]
    Remove --> Login[/login]

    Dashboard --> Working[Praca w aplikacji]
    Working --> Expire{Token\nwygasł?}
    Expire -->|Nie| Working
    Expire -->|Tak 401| Dialog[TokenExpiredDialogComponent]
    Dialog --> Remove
```

## Powiązane ekrany

| Ekran | Link |
|---|---|
| Logowanie | `../../01_ekrany/login/ekran.md` |
| Rejestracja | `../../01_ekrany/register/ekran.md` |
| Dashboard (cel przekierowania) | `../../01_ekrany/dashboard/ekran.md` |

## Powiązane procesy

| Proces | Link |
|---|---|
| Rejestracja | `../../02_procesy/autentykacja/rejestracja/proces.md` |
| Logowanie | `../../02_procesy/autentykacja/logowanie/proces.md` |

## Wątpliwości i braki

- Brak server-side invalidation tokenu przy wylogowaniu — po stronie bezpieczeństwa token pozostaje ważny przez resztę 10 minut po wylogowaniu.
- Brak mechanizmu odświeżania tokenu (refresh token) — użytkownik musi logować się co 10 minut przy aktywnej pracy.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — rozszerzona na podstawie UC-01 z diagramem Mermaid. |
