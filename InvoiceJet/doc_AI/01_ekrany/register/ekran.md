# RegisterComponent — Ekran rejestracji

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-Register |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran rejestracji nowego konta użytkownika w aplikacji InvoiceJet. Dostępny publicznie — bez wymogu autoryzacji. Formularz reaktywny Angular z polami: imię, nazwisko, email, hasło, potwierdzenie hasła. Po pomyślnej rejestracji token JWT zapisywany jest w `localStorage` i użytkownik automatycznie przekierowywany jest do dashboardu (bez konieczności ponownego logowania).

## Wizualizacja układu

```
┌─────────────────────────────────┐
│      InvoiceJet — Rejestracja   │
├─────────────────────────────────┤
│  Imię:          [_____________] │
│  Nazwisko:      [_____________] │
│  Email:         [_____________] │
│  Hasło:         [_____________] │
│  Potw. hasła:   [_____________] │
├─────────────────────────────────┤
│  [Komunikat błędu (opcjonalny)] │
├─────────────────────────────────┤
│        [  Zarejestruj się  ]    │
│  Masz konto? Zaloguj się        │
└─────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/register` |
| Wymagana rola/uprawnienie | Brak (ekran publiczny) |
| Punkty wejścia | Bezpośredni URL; klik „Zarejestruj się" z ekranu Login |
| Powiązany kod komponentu | `src/app/components/register/register.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| `/dashboard` | Submit formularza | Sukces API (201) | Brak (token zapisany) |
| `/login` | Klik „Zaloguj się" | Zawsze | Brak |

## Sekcje ekranu

### Filtry

Brak.

### Tabele i listy

Brak.

### Pola

| ID pola | Nazwa w UI | Wymagalność | Link do dokumentu |
|---|---|---|---|
| POLE-Register-firstName | Imię | wymagane | — |
| POLE-Register-lastName | Nazwisko | wymagane | — |
| POLE-Register-email | Email | wymagane | — |
| POLE-Register-password | Hasło | wymagane | — |
| POLE-Register-passwordConfirmation | Potwierdzenie hasła | wymagane | — |

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-Register-Submit | Zarejestruj się | — |

### Modale

Brak.

### Powiadomienia

| ID powiadomienia | Typ | Treść / opis | Link do dokumentu |
|---|---|---|---|
| POW-Register-Blad | inline | `errorMessage` — komunikat błędu z API (np. email zajęty, słabe hasło) | — |

## Pola formularza — szczegóły

| Pole | Walidacja | Opis |
|---|---|---|
| `firstName` | required | Imię użytkownika |
| `lastName` | required | Nazwisko użytkownika |
| `email` | required | Adres email (unikalny w systemie) |
| `password` | required | Hasło — min 8 znaków, walidacja regex po stronie API |
| `passwordConfirmation` | required | Potwierdzenie hasła |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Submit formularza | `POST /api/Auth/register` przez `AuthService.register()` |

## Przepływ po submit

1. Wywołanie `authService.register({firstName, lastName, email, password, passwordConfirmation})`
2. Sukces → `localStorage.setItem("authToken", response.token)` → `router.navigate(["/dashboard"])`
3. Błąd (400 — walidacja hasła, 409 — email zajęty) → `errorMessage` wyświetlony inline na ekranie

## Powiązania

- Powiązane procesy: `../../02_procesy/autentykacja/rejestracja/proces.md`
- Powiązane API: `../../04_api_i_integracje/01_api_frontend/auth/`
- Powiązane UC: Brak

## Powiązania z kodem

- Komponent: `src/app/components/register/register.component.ts`
- Szablon HTML: `src/app/components/register/register.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

- Brak walidacji frontendu dla siły hasła (tylko backend waliduje przez regex).
- Brak walidacji frontendu zgodności `password` z `passwordConfirmation` (tylko backend).

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `register/register.md`. |
