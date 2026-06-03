# E-02 RegisterComponent — Ekran rejestracji

| Pole | Wartość |
|---|---|
| ID dokumentu | E-02 |
| Typ dokumentu | ekran |
| Wersja | 1.0 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 |
| Data ostatniej modyfikacji | 2026-06-02 |

## Streszczenie

Ekran rejestracji nowego konta użytkownika w aplikacji InvoiceJet. Dostępny publicznie — bez wymogu autoryzacji. Formularz reaktywny Angular z polami: imię, nazwisko, email, hasło, potwierdzenie hasła. Po pomyślnej rejestracji token JWT zapisywany jest w `localStorage` i użytkownik automatycznie przekierowywany jest do dashboardu (bez konieczności ponownego logowania). Przy rejestracji tworzone są automatycznie domyślne serie dokumentów (FV/PRF/STN).

---

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

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/register` |
| Wymagana rola | Brak (ekran publiczny) |
| Punkty wejścia | Bezpośredni URL; klik „Zarejestruj się" z [E-01 Login](../E-01_LoginComponent/E-01_ekran.md) |
| Komponent Angular | [`RegisterComponent`](../../../../InvoiceJetUI/src/app/components/register/register.component.ts) |
| Szablon HTML | [`register.component.html`](../../../../InvoiceJetUI/src/app/components/register/register.component.html) |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek | Uprawnienie |
|---|---|---|---|
| [E-03 Dashboard](../E-03_DashboardComponent/E-03_ekran.md) | [OP-E02-01](E-02_OP-01.md) sukces | sukces API (201) | Brak (token zapisany) |
| [E-01 Login](../E-01_LoginComponent/E-01_ekran.md) | Klik „Zaloguj się" | zawsze | Brak |

---

## Filtry

Brak.

## Tabele i listy

Brak.

## Pola

| ID | Nazwa w UI | Wymagalność | Algorytm |
|---|---|---|---|
| POLE-E02-firstName | Imię | wymagane | — |
| POLE-E02-lastName | Nazwisko | wymagane | — |
| POLE-E02-email | Email | wymagane | — |
| POLE-E02-password | Hasło | wymagane | [ALG-03 Walidacja hasła](../../../03_algorytmy/walidacji/walidacja_hasla.md) |
| POLE-E02-passwordConfirmation | Potwierdzenie hasła | wymagane | [ALG-03 Walidacja hasła](../../../03_algorytmy/walidacji/walidacja_hasla.md) |

## Operacje

| ID | Etykieta UI | Dokument |
|---|---|---|
| OP-E02-01 | Zarejestruj się | [E-02_OP-01.md](E-02_OP-01.md) |

## Modale

Brak.

## Scenariusze testowe

→ [E-02_TC.md](E-02_TC.md) — prereq DB, selektory CSS, 4 scenariusze e2e

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint |
|---|---|---|
| Submit formularza | POST | `/api/Auth/register` przez `AuthService.register()` |

---

## Przepływ po submit

1. Wywołanie `authService.register({firstName, lastName, email, password, passwordConfirmation})`
2. Sukces (201) → `localStorage.setItem("authToken", response.token)` → `router.navigate(["/dashboard"])`
3. Błąd (400 — walidacja hasła, 409 — email zajęty) → `errorMessage` wyświetlony inline

---

## Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| POLE-E02-password | [ALG-03 Walidacja hasła](../../../03_algorytmy/walidacji/walidacja_hasla.md) | Walidacja siły hasła (regex min 8 znaków, wielka litera, cyfra) + BCrypt hash przy zapisie |
| POLE-E02-passwordConfirmation | [ALG-03 Walidacja hasła](../../../03_algorytmy/walidacji/walidacja_hasla.md) | Walidacja zgodności `password` z `passwordConfirmation` |
| OP-E02-01 | [ALG-04 JWT Creation](../../../03_algorytmy/autoryzacyjne/tworzenie_tokenu_jwt.md) | Tworzenie tokenu JWT po pomyślnej rejestracji |
| OP-E02-01 | [ALG-07 UserFirm](../../../03_algorytmy/dedykowane/zarzadzanie_relacja_userfirm.md) | ManageUserFirmRelation — powiązanie nowego użytkownika z firmą |
| OP-E02-01 | [ALG-08 Serie dokumentów](../../../03_algorytmy/dedykowane/inicjalizacja_serii_dokumentow.md) | Automatyczne tworzenie domyślnych serii FV/PRF/STN po pierwszej firmie |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`register.component.ts`](../../../../InvoiceJetUI/src/app/components/register/register.component.ts) |
| Szablon HTML | [`register.component.html`](../../../../InvoiceJetUI/src/app/components/register/register.component.html) |

## Stan komponentu

| Pole | Typ | Opis |
|---|---|---|
| `errorMessage` | `string \| null` | Komunikat błędu z API — wyświetlany pod formularzem |
| `registerForm` | `FormGroup` | Reaktywny formularz (firstName, lastName, email, password, passwordConfirmation) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| IA-01 | Brak walidacji frontendu dla siły hasła — tylko backend waliduje przez regex |
| IA-02 | Brak walidacji frontendu zgodności `password` z `passwordConfirmation` — tylko backend |
| IA-03 | Brak `data-cy` / `data-testid` — selektory nieodporne na zmiany UI |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
