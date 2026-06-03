# E-01 LoginComponent — Ekran logowania

| Pole | Wartość |
|---|---|
| ID dokumentu | E-01 |
| Typ dokumentu | ekran |
| Wersja | 1.0 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 |
| Data ostatniej modyfikacji | 2026-06-02 |

## Streszczenie

Ekran logowania do aplikacji InvoiceJet. Dostępny publicznie — bez wymogu autoryzacji (`AuthGuard` nie aktywny). Zawiera reaktywny formularz Angular z polami email i hasło. Po poprawnym zalogowaniu token JWT zapisywany jest w `localStorage` i użytkownik przekierowywany jest do dashboardu.

---

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

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/login` |
| Wymagana rola | Brak (ekran publiczny) |
| Punkty wejścia | Bezpośredni URL; przekierowanie po wylogowaniu; przekierowanie po wygaśnięciu tokenu (TokenExpiredDialog) |
| Komponent Angular | [`LoginComponent`](../../../../InvoiceJetUI/src/app/components/login/login.component.ts) |
| Szablon HTML | [`login.component.html`](../../../../InvoiceJetUI/src/app/components/login/login.component.html) |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek | Uprawnienie |
|---|---|---|---|
| [E-03 Dashboard](../E-03_DashboardComponent/E-03_ekran.md) | [OP-E01-01](E-01_OP-01.md) sukces | `loginForm.valid` + sukces API | Brak (token zapisany) |
| [E-02 Rejestracja](../E-02_RegisterComponent/E-02_ekran.md) | Klik „Zarejestruj się" | zawsze | Brak |

---

## Filtry

Brak.

## Tabele i listy

Brak.

## Pola

| ID | Nazwa w UI | Wymagalność | Algorytm |
|---|---|---|---|
| POLE-E01-email | Email | wymagane | — |
| POLE-E01-password | Hasło | wymagane | [ALG-03 Walidacja hasła](../../../03_algorytmy/walidacji/walidacja_hasla.md) |

## Operacje

| ID | Etykieta UI | Dokument |
|---|---|---|
| OP-E01-01 | Zaloguj się | [E-01_OP-01.md](E-01_OP-01.md) |
| OP-E01-02 | Pokaż/ukryj hasło (👁) | [E-01_OP-02.md](E-01_OP-02.md) |

## Modale

Brak.

## Scenariusze testowe

→ [E-01_TC.md](E-01_TC.md) — prereq JWT, prereq DB, selektory CSS, 4 scenariusze e2e

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint |
|---|---|---|
| Submit formularza | POST | `/api/Auth/login` przez `AuthService.login()` |

---

## Przepływ po submit

1. `loginForm.valid` → wywołanie `authService.login({email, password})`
2. Sukces → `localStorage.setItem("authToken", response.token)` → `router.navigate(["/dashboard"])`
3. Błąd (401, 400) → `errorMessage = error.error` (wyświetlony inline na ekranie)

---

## Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| POLE-E01-password | [ALG-03 Walidacja hasła](../../../03_algorytmy/walidacji/walidacja_hasla.md) | BCrypt verify na serwerze przy logowaniu |
| OP-E01-01 | [ALG-01 JWT Auth](../../../03_algorytmy/autoryzacyjne/weryfikacja_tokenu_jwt.md) | Pipeline JWT: backend + Angular interceptor |
| OP-E01-01 | [ALG-04 JWT Creation](../../../03_algorytmy/autoryzacyjne/tworzenie_tokenu_jwt.md) | Tworzenie tokenu JWT po poprawnym logowaniu |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`login.component.ts`](../../../../InvoiceJetUI/src/app/components/login/login.component.ts) |
| Szablon HTML | [`login.component.html`](../../../../InvoiceJetUI/src/app/components/login/login.component.html) |

## Stan komponentu

| Pole | Typ | Opis |
|---|---|---|
| `errorMessage` | `string \| null` | Komunikat błędu z API — wyświetlany pod formularzem |
| `hide` | `boolean` | Ukrycie/pokazanie hasła (domyślnie `true`) |
| `loginForm` | `FormGroup` | Reaktywny formularz (email, password) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| IA-01 | Brak `data-cy` / `data-testid` — selektory nieodporne na zmiany UI |
| IA-02 | Brak walidacji formatu email po stronie frontendu (tylko `required`) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
