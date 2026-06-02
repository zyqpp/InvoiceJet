# TC-E06 — Scenariusze testowe (BankAccountsComponent)

| Pole | Wartość |
|---|---|
| ID dokumentu | TC-E06 |
| Typ dokumentu | scenariusze testowe |
| Ekran | [E-06 BankAccountsComponent](E-06_ekran.md) |
| Wersja | 1.0 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 |
| Data | 2026-06-02 |

## Prereq — autoryzacja (wymagane dla każdego testu)

| Wymaganie | Szczegół |
|---|---|
| Typ | JWT Bearer token |
| Rola | `"User"` w claims |
| Nagłówek HTTP | `Authorization: Bearer <token>` |
| Uzyskanie tokenu | POST `/api/Auth/login` |

## Prereq — dane w DB

| Encja | Minimum |
|---|---|
| `User` | ≥1 zalogowany użytkownik |
| `UserFirm` | Aktywny związek użytkownik–firma |
| `BankAccount` | ≥1 konto dla TC-E06-01, TC-E06-03, TC-E06-04 |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Przycisk Dodaj konto bankowe | `button[mat-raised-button]` z tekstem „Dodaj konto bankowe" |
| Wiersze tabeli | `tr[mat-row]` |
| Checkbox wiersza | `mat-checkbox` w `td` |
| Przycisk Edytuj przy wierszu | `button[mat-icon-button]` z `mat-icon` `edit` |
| Przycisk Usuń zaznaczone | `button` z tekstem „Usuń zaznaczone" |
| Paginator | `mat-paginator` |
| Pole IBAN w dialogu | `input[formControlName="iban"]` |

> Brak `data-cy` — do uzupełnienia.

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E06-01 | Lista kont bankowych | ≥1 konto BankAccount dla UserFirm | 1. Login 2. GET `/dashboard/bank-accounts` | [TAB-E06-01](E-06_TAB-01.md) z kontami; izolacja UserFirm ([ALG-10](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md)) |
| TC-E06-02 | Dodaj konto (walidacja IBAN) | — | 1. Login 2. GET `/dashboard/bank-accounts` 3. Klik [OP-E06-01] 4. Wpisz IBAN `RO49AAAA1B31007593840000`, wybierz walutę RON 5. Klik Save | HTTP POST; nowe konto pojawia się w [TAB-E06-01](E-06_TAB-01.md) |
| TC-E06-03 | Edytuj konto | ≥1 konto id=10 | 1. Login 2. GET `/dashboard/bank-accounts` 3. Klik [OP-E06-02] Edytuj przy koncie id=10 | Dialog z danymi konta; po zmianie nazwy banku i Save HTTP PUT; dane zaktualizowane |
| TC-E06-04 | Usuń zaznaczone | ≥1 konto id=10 | 1. Login 2. GET `/dashboard/bank-accounts` 3. Zaznacz konto id=10 4. Klik [OP-E06-03] Usuń zaznaczone | HTTP PUT `/api/BankAccount/Delete` z `[10]`; wiersz id=10 znika z tabeli |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
