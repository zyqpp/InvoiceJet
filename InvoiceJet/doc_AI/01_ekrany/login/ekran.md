# LoginComponent — Ekran logowania

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-Login |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran logowania do aplikacji InvoiceJet. Dostępny publicznie — bez wymogu autoryzacji (`AuthGuard` nie aktywny). Zawiera reaktywny formularz Angular z polami email i hasło. Po poprawnym zalogowaniu token JWT zapisywany jest w `localStorage` i użytkownik przekierowywany jest do dashboardu.

## Wizualizacja układu

```
┌─────────────────────────────────┐
│        InvoiceJet Login         │
├─────────────────────────────────┤
│  Email:    [________________]   │
│  Hasło:    [________________]👁 │
├─────────────────────────────────┤
│  [Komunikat błędu (opcjonalny)] │
├─────────────────────────────────┤
│         [  Zaloguj się  ]       │
│  Nie masz konta? Zarejestruj się│
└─────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/login` |
| Wymagana rola/uprawnienie | Brak (ekran publiczny) |
| Punkty wejścia | Bezpośredni URL; przekierowanie po wylogowaniu; przekierowanie po wygaśnięciu tokenu (TokenExpiredDialog) |
| Powiązany kod komponentu | `src/app/components/login/login.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| `/dashboard` | Submit formularza | `loginForm.valid` + sukces API | Brak (token zapisany) |
| `/register` | Klik „Zarejestruj się" | Zawsze | Brak |

## Sekcje ekranu

### Filtry

Brak.

### Tabele i listy

Brak.

### Pola

| ID pola | Nazwa w UI | Wymagalność | Link do dokumentu |
|---|---|---|---|
| POLE-Login-email | Email | wymagane | — |
| POLE-Login-password | Hasło | wymagane | — |

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-Login-Submit | Zaloguj się | — |
| OP-Login-TogglePassword | Pokaż/ukryj hasło (ikona 👁) | — |

### Modale

Brak.

### Powiadomienia

| ID powiadomienia | Typ | Treść / opis | Link do dokumentu |
|---|---|---|---|
| POW-Login-Blad | inline | `errorMessage` — komunikat błędu z API (np. „Nieprawidłowy email lub hasło") | — |

## Pola formularza — szczegóły

| Pole | Kontrolka | Walidacja | Opis |
|---|---|---|---|
| `email` | `mat-form-field` + `input[type=email]` | required | Adres email użytkownika |
| `password` | `mat-form-field` + `input[type=password]` | required | Hasło; toggle widoczności przez zmienną `hide` |

## Stan komponentu

| Pole | Typ | Opis |
|---|---|---|
| `errorMessage` | `string \| null` | Komunikat błędu z API — wyświetlany pod formularzem |
| `hide` | `boolean` | Ukrycie/pokazanie hasła (domyślnie `true`) |
| `loginForm` | `FormGroup` | Reaktywny formularz (email, password) |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Submit formularza | `POST /api/Auth/login` przez `AuthService.login()` |

## Przepływ po submit

1. `loginForm.valid` → wywołanie `authService.login({email, password})`
2. Sukces → `localStorage.setItem("authToken", response.token)` → `router.navigate(["/dashboard"])`
3. Błąd (401, 400) → `errorMessage = error.error` (wyświetlony inline na ekranie)

## Powiązania

- Powiązane procesy: `../../02_procesy/autentykacja/logowanie/proces.md`
- Powiązane API: `../../04_api_i_integracje/01_api_frontend/auth/`
- Powiązane UC: Brak

## Powiązania z kodem

- Komponent: `src/app/components/login/login.component.ts`
- Szablon HTML: `src/app/components/login/login.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `login/login.md`. |
