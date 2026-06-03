# E-06 BankAccountsComponent — Lista kont bankowych

| Pole | Wartość |
|---|---|
| ID dokumentu | E-06 |
| Typ dokumentu | ekran |
| Wersja | 1.0 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 |
| Data ostatniej modyfikacji | 2026-06-02 |

## Streszczenie

Ekran zarządzania kontami bankowymi własnej firmy użytkownika. Prezentuje tabelę kont z kolumnami: nazwa banku, IBAN, waluta, status aktywności. Operacje dodawania i edycji realizowane przez dialog Angular Material (`AddOrEditBankAccountDialogComponent`). Usunięcie zaznaczonych kont wywołuje API batch. Wszystkie dane izolowane per UserFirm. Chroniony przez `AuthGuard` (rola: User).

---

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────────┐
│ Konta bankowe                     [+ Dodaj konto bankowe]│
├──┬─────────────────┬──────────────────────┬────────┬─────┤
│☐ │ Nazwa banku     │ IBAN                 │ Waluta │ Akt.│
├──┼─────────────────┼──────────────────────┼────────┼─────┤
│☐ │ ...             │ RO49AAAA1B31007593840│ RON    │ Tak │
├──┴─────────────────┴──────────────────────┴────────┴─────┤
│ [Usuń zaznaczone]                          [Paginacja]    │
└──────────────────────────────────────────────────────────┘
```

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/bank-accounts` |
| Wymagana rola | User (AuthGuard JWT) |
| Punkty wejścia | Klik „Konta bankowe" w Sidebar |
| Komponent Angular | [`BankAccountsComponent`](../../../../InvoiceJetUI/src/app/components/firm/bank-accounts/bank-accounts.component.ts) |
| Szablon HTML | [`bank-accounts.component.html`](../../../../InvoiceJetUI/src/app/components/firm/bank-accounts/bank-accounts.component.html) |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek | Uprawnienie |
|---|---|---|---|
| Modal AddOrEditBankAccountDialog (dodaj) | [OP-E06-01](E-06_OP-01.md) | zawsze | User |
| Modal AddOrEditBankAccountDialog (edytuj) | [OP-E06-02](E-06_OP-02.md) | zawsze | User |

---

## Filtry

Brak.

## Tabele i listy

| ID | Nazwa | Dokument |
|---|---|---|
| TAB-E06-01 | Lista kont bankowych | [E-06_TAB-01.md](E-06_TAB-01.md) |

### Kolumny tabeli

| Kolumna | Źródło danych | Opis |
|---|---|---|
| Checkbox | `selection` | Zaznaczanie do operacji batch |
| `bankName` | `IBankAccount.bankName` | Nazwa banku |
| `iban` | `IBankAccount.iban` | Numer IBAN |
| `currency` | `IBankAccount.currency` | Waluta — mapowana: 0=Ron, 1=Eur |
| `isActive` | `IBankAccount.isActive` | Czy konto aktywne |

## Operacje

| ID | Etykieta UI | Dokument |
|---|---|---|
| OP-E06-01 | Dodaj konto bankowe | [E-06_OP-01.md](E-06_OP-01.md) |
| OP-E06-02 | Edytuj (przy wierszu) | [E-06_OP-02.md](E-06_OP-02.md) |
| OP-E06-03 | Usuń zaznaczone | [E-06_OP-03.md](E-06_OP-03.md) |

## Modale

| ID | Nazwa | Wywołane przez |
|---|---|---|
| MODAL-E06-01 | AddOrEditBankAccountDialog (dodaj) | OP-E06-01 |
| MODAL-E06-02 | AddOrEditBankAccountDialog (edytuj) | OP-E06-02 |

## Scenariusze testowe

→ [E-06_TC.md](E-06_TC.md) — prereq JWT, prereq DB, selektory CSS, 4 scenariusze e2e

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint |
|---|---|---|
| Załadowanie listy (ngOnInit) | GET | `/api/BankAccount/GetAll` |
| Usunięcie zaznaczonych | PUT | `/api/BankAccount/Delete` (`[FromBody] int[]`) |

---

## Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| OP-E06-01 | [ALG-10 Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Konto tworzone w kontekście UserFirm zalogowanego użytkownika |
| OP-E06-02 | [ALG-10 Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Edycja możliwa wyłącznie dla kont należących do UserFirm aktualnie zalogowanego użytkownika |
| OP-E06-03 | [ALG-10 Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Usunięcie batch działa tylko na kontach należących do UserFirm aktualnie zalogowanego użytkownika |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`bank-accounts.component.ts`](../../../../InvoiceJetUI/src/app/components/firm/bank-accounts/bank-accounts.component.ts) |
| Szablon HTML | [`bank-accounts.component.html`](../../../../InvoiceJetUI/src/app/components/firm/bank-accounts/bank-accounts.component.html) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| BA-01 | Brak filtru wyszukiwania na liście kont (w odróżnieniu od klientów i produktów) |
| BA-02 | Brak komunikatów sukcesu/błędu po operacjach CRUD |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
