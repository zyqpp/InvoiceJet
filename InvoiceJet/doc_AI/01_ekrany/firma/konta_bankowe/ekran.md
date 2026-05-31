# BankAccountsComponent — Lista kont bankowych

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-KontaBankowe |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran zarządzania kontami bankowymi własnej firmy użytkownika. Prezentuje tabelę kont z kolumnami: nazwa banku, IBAN, waluta, status aktywności. Operacje dodawania i edycji realizowane przez dialog Angular Material. Usunięcie zaznaczonych kont wywołuje API batch. Chroniony przez AuthGuard (rola: User).

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────────┐
│ Konta bankowe                     [+ Dodaj konto bankowe]│
├──┬─────────────────┬──────────────────────┬────────┬─────┤
│☐ │ Nazwa banku     │ IBAN                 │ Waluta │ Akt.│
├──┼─────────────────┼──────────────────────┼────────┼─────┤
│☐ │ ...             │ ...                  │ RON    │ Tak │
├──┴─────────────────┴──────────────────────┴────────┴─────┤
│ [Usuń zaznaczone]                          [Paginacja]    │
└──────────────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/bank-accounts` |
| Wymagana rola/uprawnienie | User (AuthGuard) |
| Punkty wejścia | Klik „Konta bankowe" w Sidebar |
| Powiązany kod komponentu | `src/app/components/firm/bank-accounts/bank-accounts.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| Modal AddOrEditBankAccountDialog | Klik „Dodaj konto bankowe" | Zawsze | User |
| Modal AddOrEditBankAccountDialog (edycja) | Klik „Edytuj" przy wierszu | Zawsze | User |

## Sekcje ekranu

### Filtry

Brak.

### Tabele i listy

| ID tabeli | Nazwa | Link do dokumentu |
|---|---|---|
| TAB-KontaBankowe-ListaKont | Lista kont bankowych | — |

### Kolumny tabeli

| Kolumna | Źródło danych | Opis |
|---|---|---|
| Checkbox (select) | `selection` | Zaznaczanie do operacji batch |
| `bankName` | `IBankAccount.bankName` | Nazwa banku |
| `iban` | `IBankAccount.iban` | Numer IBAN |
| `currency` | `IBankAccount.currency` | Waluta — mapowana przez `mapCurrencyNames()`: 0=Ron, 1=Eur |
| `isActive` | `IBankAccount.isActive` | Czy konto aktywne |

### Pola

Brak (ekran listowy — bez pól formularza bezpośrednio na ekranie).

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-KontaBankowe-DodajKonto | Dodaj konto bankowe | — |
| OP-KontaBankowe-EdytujKonto | Edytuj (przy wierszu) | — |
| OP-KontaBankowe-UsunZaznaczone | Usuń zaznaczone | — |

### Modale

| ID modalu | Nazwa | Wywołane przez | Link do dokumentu |
|---|---|---|---|
| MODAL-KontaBankowe-DodajKonto | AddOrEditBankAccountDialog (dodaj) | OP-KontaBankowe-DodajKonto | `dialog_dodaj_konto/modal.md` |
| MODAL-KontaBankowe-EdytujKonto | AddOrEditBankAccountDialog (edytuj) | OP-KontaBankowe-EdytujKonto | `dialog_dodaj_konto/modal.md` |

### Powiadomienia

Brak.

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie (ngOnInit) | [GET /api/BankAccount/GetAll](../../../04_api_i_integracje/01_api_frontend/bank_account/GET_BankAccount_GetAll.md) |
| Usunięcie zaznaczonych | [PUT /api/BankAccount/Delete](../../../04_api_i_integracje/01_api_frontend/bank_account/PUT_BankAccount_Delete.md) `[FromBody] int[]` |

## Powiązania

- Powiązane procesy: `../../../02_procesy/konta_bankowe/pobierz_konta/proces.md`, `../../../02_procesy/konta_bankowe/usun_konta/proces.md`
- Powiązane API: `../../../04_api_i_integracje/01_api_frontend/bank_account/`
- Powiązane UC: Brak

## Powiązania z kodem

- Komponent: `src/app/components/firm/bank-accounts/bank-accounts.component.ts`
- Szablon HTML: `src/app/components/firm/bank-accounts/bank-accounts.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `bank_accounts/bank-accounts.md`. |
