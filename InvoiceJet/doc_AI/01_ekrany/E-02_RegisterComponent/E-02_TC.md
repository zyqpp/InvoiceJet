# TC-E02 — Scenariusze testowe (RegisterComponent)

| Pole | Wartość |
|---|---|
| ID dokumentu | TC-E02 |
| Typ dokumentu | scenariusze testowe |
| Ekran | [E-02 RegisterComponent](E-02_ekran.md) |
| Wersja | 1.0 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 |
| Data | 2026-06-02 |

## Prereq — autoryzacja

Ekran publiczny — brak wymogu JWT dla dostępu do `/register`.

## Prereq — dane w DB

| Encja | Minimum |
|---|---|
| `User` | Brak (rejestrujemy nowego użytkownika) |
| Dla TC-E02-02 | User z emailem `exists@example.com` już istnieje |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Pole firstName | `input[formControlName="firstName"]` |
| Pole lastName | `input[formControlName="lastName"]` |
| Pole email | `input[formControlName="email"]` |
| Pole hasło | `input[formControlName="password"]` |
| Pole potwierdzenie hasła | `input[formControlName="passwordConfirmation"]` |
| Przycisk submit | `button[type="submit"]` |
| Komunikat błędu | `.error-message` lub `mat-error` |

> Brak `data-cy` — anomalia IA-03.

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E02-01 | Rejestracja happy path | Brak użytkownika z tym emailem | 1. GET `/register` 2. Wypełnij wszystkie pola poprawnymi danymi (hasło `Test1234!`) 3. Klik [OP-E02-01] | Redirect do `/dashboard`; token JWT w `localStorage["authToken"]`; serie FV/PRF/STN stworzone ([ALG-08](../../../03_algorytmy/dedykowane/inicjalizacja_serii_dokumentow.md)) |
| TC-E02-02 | Email już istnieje | User `exists@example.com` w DB | 1. GET `/register` 2. Wpisz email `exists@example.com` 3. Klik [OP-E02-01] | HTTP 400/409; `errorMessage` widoczny; brak redirect |
| TC-E02-03 | Hasło za słabe | — | 1. GET `/register` 2. Wpisz hasło `abc` (brak wielkiej, cyfry, <8 znaków) 3. Klik [OP-E02-01] | HTTP 400; błąd walidacji [ALG-03](../../../03_algorytmy/walidacji/walidacja_hasla.md) wyświetlony inline |
| TC-E02-04 | Hasła nie pasują | — | 1. GET `/register` 2. Wpisz `password = Test1234!`, `passwordConfirmation = Inne999!` 3. Klik [OP-E02-01] | HTTP 400; błąd niezgodności haseł wyświetlony; brak redirect |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
