# Ekran: Konta bankowe (Bank Accounts)

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-06 |
| Trasa | `/dashboard/bank-accounts` |
| Komponent | `BankAccountsComponent` |
| Plik | `src/app/components/firm/bank-accounts/bank-accounts.component.ts` |
| AuthGuard | TAK |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Lista kont bankowych firmy użytkownika z CRUD przez dialogi.

## Kolumny tabeli

`select`, `bankName`, `iban`, `currency`, `isActive`

**Uwaga:** `currency` wyświetlany jako nazwa (`mapCurrencyNames()`) — `0=Ron`, `1=Eur`.

## Dialogi

| Dialog | Wywołanie | Cel |
|---|---|---|
| `AddOrEditBankAccountDialogComponent` | `openNewBankAccountDialog()` | Dodanie konta |
| `AddOrEditBankAccountDialogComponent` | `openEditBankAccountDialog(account)` | Edycja konta |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie (ngOnInit) | `GET /api/BankAccount/GetUserFirmBankAccounts` |
| Usunięcie zaznaczonych | `PUT /api/BankAccount/DeleteUserFirmBankAccounts` `[FromBody] int[]` |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
