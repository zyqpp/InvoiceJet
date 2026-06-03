# TC-E01 — Scenariusze testowe (LoginComponent)

| Pole | Wartość |
|---|---|
| ID dokumentu | TC-E01 |
| Typ dokumentu | scenariusze testowe |
| Ekran | [E-01 LoginComponent](E-01_ekran.md) |
| Wersja | 1.0 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 |
| Data | 2026-06-02 |

## Prereq — autoryzacja

Ekran publiczny — brak wymogu JWT dla dostępu do `/login`.  
Token JWT jest **wynikiem** testu (TC-E01-01), nie wejściem.

## Prereq — dane w DB

| Encja | Minimum |
|---|---|
| `User` | ≥1 użytkownik z emailem `test@example.com` i hasłem `Test1234!` |
| `Firm` (UserFirm) | — (wymagane dopiero po logowaniu dla dashboardu) |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Pole email | `input[formControlName="email"]` |
| Pole hasło | `input[formControlName="password"]` |
| Przycisk submit | `button[type="submit"]` |
| Komunikat błędu | `.error-message` lub `mat-error` |
| Toggle widoczności hasła | `button[mat-icon-button]` z `mat-icon` `visibility` / `visibility_off` |

> Brak `data-cy` — anomalia IA-01.

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E01-01 | Login happy path | User `test@example.com` / `Test1234!` | 1. GET `/login` 2. Wpisz email 3. Wpisz hasło 4. Klik [OP-E01-01] | Redirect do `/dashboard`; token JWT w `localStorage["authToken"]` |
| TC-E01-02 | Błędne hasło | User istnieje | 1. GET `/login` 2. Wpisz email 3. Wpisz złe hasło 4. Klik [OP-E01-01] | HTTP 401; `errorMessage` widoczny na ekranie; brak redirect |
| TC-E01-03 | Puste pola — walidacja wymagalności | — | 1. GET `/login` 2. Klik [OP-E01-01] bez wypełniania | Formularz nie wysłany; pola z błędem `mat-error` (required) |
| TC-E01-04 | Brak autoryzacji — redirect | Brak tokenu w localStorage | 1. Usuń token z localStorage 2. GET `/dashboard` | Redirect do `/login`; AuthGuard aktywny |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
