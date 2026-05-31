# AddOrEditBankAccountDialogComponent — Dialog dodaj/edytuj konto bankowe

| Pole | Wartość |
|---|---|
| ID dokumentu | MODAL-KontaBankowe-DodajKonto |
| Typ dokumentu | modal |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Modal Angular Material do dodawania i edycji konta bankowego własnej firmy użytkownika. Otwierany z ekranu listy kont bankowych przez `MatDialog.open()`. Dane konta przekazywane przez `MAT_DIALOG_DATA`. Działa w trybie dodawania (pusty formularz) lub edycji (wypełniony formularz danymi konta).

## Charakterystyka modalu

| Atrybut | Wartość |
|---|---|
| ID modalu | MODAL-KontaBankowe-DodajKonto |
| Nazwa / tytuł w UI | Dodaj konto bankowe / Edytuj konto bankowe |
| Wywołany przez operację | OP-KontaBankowe-DodajKonto, OP-KontaBankowe-EdytujKonto |
| Ekran nadrzędny | `../ekran.md` (BankAccountsComponent) |
| Typ modalu | formularz |
| Zamknięcie przez Escape | tak |
| Zamknięcie przez klik tła | tak |

## Wizualizacja układu

```
┌─────────────────────────────────────────┐
│ Dodaj konto / Edytuj konto          [X] │
├─────────────────────────────────────────┤
│ Nazwa banku:  [_________________________]│
│ IBAN:         [_________________________]│
│ Waluta:       [RON / EUR ▼]             │
├─────────────────────────────────────────┤
│ [Anuluj]                    [Zapisz]    │
└─────────────────────────────────────────┘
```

## Pola modalu

| ID pola | Nazwa w UI | Typ | Wymagalność | Link do dokumentu |
|---|---|---|---|---|
| POLE-DodajKonto-bankName | Nazwa banku | mat-form-field (input) | wymagane | — |
| POLE-DodajKonto-iban | IBAN | mat-form-field (input) | wymagane | — |
| POLE-DodajKonto-currency | Waluta | mat-form-field / mat-select | wymagane | — |

## Dane wejściowe (MAT_DIALOG_DATA)

| Pole | Typ | Opis |
|---|---|---|
| `bankAccount` | `IBankAccount \| null` | `null` = tryb dodawania; obiekt = tryb edycji |

## Operacje modalu

| Przycisk | Akcja | Wywołuje operację | Zamyka modal |
|---|---|---|---|
| Zapisz (tryb dodaj) | Wywołuje `POST /api/BankAccount/Add` | Tak | tak (z wynikiem) |
| Zapisz (tryb edytuj) | Wywołuje `PUT /api/BankAccount/Edit` | Tak | tak (z wynikiem) |
| Anuluj | Zamknięcie bez zmian | Nie | tak |

## Przepływ

### Tryb dodawania
1. Formularz pusty
2. Submit → `POST /api/BankAccount/Add`
3. Dialog zamknięty z wynikiem → lista kont odświeżona

### Tryb edycji
1. Formularz wypełniony danymi konta
2. Submit → `PUT /api/BankAccount/Edit`
3. Dialog zamknięty z wynikiem → lista kont odświeżona

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Dodanie konta | `POST /api/BankAccount/Add` |
| Edycja konta | `PUT /api/BankAccount/Edit` |

## Możliwe wyniki

| Wynik | Warunki | Komunikat | Następna akcja |
|---|---|---|---|
| Sukces dodania | API zwróci 200/201 | Brak komunikatu | Modal zamknięty; lista kont odświeżona |
| Sukces edycji | API zwróci 200 | Brak komunikatu | Modal zamknięty; lista kont odświeżona |
| Błąd API | API zwróci 400/500 | Brak widocznego komunikatu (anomalia) | Modal pozostaje otwarty |
| Anulowanie | Użytkownik klika Anuluj lub Escape | Brak | Modal zamknięty, brak zmian |

## Powiązania z kodem

- Komponent modalu: `src/app/components/bank-accounts/add-or-edit-bank-account-dialog/add-or-edit-bank-account-dialog.component.ts`
- Szablon HTML: `src/app/components/bank-accounts/add-or-edit-bank-account-dialog/add-or-edit-bank-account-dialog.component.html`

## Wątpliwości i braki

- DA-01: Usunięcie konta bankowego (`PUT /api/BankAccount/DeleteUserFirmBankAccounts`) jest dostępne z ekranu listy kont, nie z tego dialogu — realizowane bezpośrednio z listy przez operację batch.
- Brak widocznego komunikatu błędu dla użytkownika w przypadku niepowodzenia API.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `bank_accounts/add-or-edit-bank-account-dialog.md`. |
