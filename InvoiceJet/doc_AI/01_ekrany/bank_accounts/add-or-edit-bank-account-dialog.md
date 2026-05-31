# Dialog: Dodaj/Edytuj konto bankowe (Add/Edit Bank Account Dialog)

| Atrybut | Wartość |
|---|---|
| ID | DIALOG-02 |
| Komponent | `AddOrEditBankAccountDialogComponent` |
| Plik | `src/app/components/bank-accounts/add-or-edit-bank-account-dialog/add-or-edit-bank-account-dialog.component.ts` |
| Otwierany z | EKRAN-06 (lista kont bankowych) |
| Typ | `MatDialog` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Modal Angular Material do dodawania i edycji konta bankowego własnej firmy. Dane konta przekazywane przez `MAT_DIALOG_DATA`.

## Pola formularza

| Pole | Kontrolka | Walidacja | Opis |
|---|---|---|---|
| `bankName` | `mat-form-field` | required | Nazwa banku |
| `iban` | `mat-form-field` | required | Numer IBAN |
| `currency` | `mat-form-field` | required | Waluta (np. RON, EUR) |

## Dane wejściowe (MAT_DIALOG_DATA)

| Pole | Typ | Opis |
|---|---|---|
| `bankAccount` | `IBankAccount \| null` | `null` = tryb dodawania; obiekt = tryb edycji |

## Przepływ

### Tryb dodawania
1. Formularz pusty
2. Submit → `POST /api/BankAccount/Add`
3. Dialog zamknięty z wynikiem → lista odświeżona

### Tryb edycji
1. Formularz wypełniony danymi konta
2. Submit → `PUT /api/BankAccount/Edit`
3. Dialog zamknięty z wynikiem → lista odświeżona

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Dodanie konta | `POST /api/BankAccount/Add` |
| Edycja konta | `PUT /api/BankAccount/Edit` |

## Anomalie

| # | Anomalia |
|---|---|
| DA-01 | Usunięcie konta bankowego (`PUT /api/BankAccount/Delete`) jest dostępne z EKRAN-06, nie z dialogu — realizowane bezpośrednio z listy |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
