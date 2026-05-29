# Bank Accounts — Logika frontendowa

---

## 1. Zakres dokumentu

Dokument opisuje logikę wykonywaną przez frontend ekranu Bank Accounts. Dokument nie opisuje implementacji backendu, reguł bazy danych ani wewnętrznego przetwarzania po stronie API.

---

## 2. Inicjalizacja ekranu

### 2.1 Przepływ inicjalizacji

```mermaid
flowchart TD
  A["Wejście na /dashboard/bank-accounts"] --> B["AuthGuard.canActivate()"]
  B --> C{"AuthService.isLoggedIn()"}
  C -->|true| D["BankAccountsComponent.ngOnInit()"]
  C -->|false| E["AuthService.logout() i router.navigate('/login')"]
  D --> F["getUserBankAccounts()"]
  F --> G["BankAccountService.getUserFirmBankAccounts()"]
  G --> H["mapCurrencyNames(accounts)"]
  H --> I["bankAccounts = mappedAccounts"]
  I --> J["dataSource.data = bankAccounts"]
```

### 2.2 Opis przepływu

`AuthGuard` kontroluje dostęp do trasy `/dashboard/bank-accounts`. Jeżeli użytkownik jest zalogowany, komponent wywołuje `getUserBankAccounts()` podczas `ngOnInit()`.

Po otrzymaniu odpowiedzi `IBankAccount[]` komponent mapuje wartości enum `Currency` na nazwy `RON` albo `EUR`. Wynik trafia do `bankAccounts` i `dataSource.data`.

---

## 3. Przepływ mapowania waluty

`mapCurrencyNames(accounts)` przechodzi po każdym koncie bankowym. Metoda szuka dopasowania w lokalnej tablicy `currencies`.

| Wartość `account.currency` | Wynik `currencyName` |
|---|---|
| `Currency.Ron` / `0` | `RON` |
| `Currency.Eur` / `1` | `EUR` |
| Brak dopasowania | `Unknown` |

---

## 4. Przepływ filtrowania, sortowania i paginacji

Filtrowanie działa przez `MatTableDataSource.filter`. Wartość z pola Search jest przycinana, zamieniana na małe litery i przypisywana do `dataSource.filter`.

Sortowanie działa przez `MatSort`. Po inicjalizacji widoku `ngAfterViewInit()` przypisuje `this.sort` do `dataSource.sort`.

Paginacja działa przez `MatPaginator`. Po inicjalizacji widoku `ngAfterViewInit()` przypisuje `this.paginator` do `dataSource.paginator`.

---

## 5. Przepływ zaznaczania wierszy

Checkbox wiersza wywołuje `selection.toggle(row)`. Kliknięcie checkboxa zatrzymuje propagację zdarzenia, dlatego nie otwiera dialogu Edycja konta.

Checkbox nagłówka wywołuje `masterToggle()`. Jeżeli wszystkie wiersze są zaznaczone, `selection.clear()` usuwa zaznaczenie. Jeżeli nie wszystkie wiersze są zaznaczone, każdy wiersz z `dataSource.data` jest dodawany do `selection`.

---

## 6. Przepływ dodawania konta bankowego

```mermaid
flowchart TD
  A["Kliknięcie New Account"] --> B["openNewBankAccountDialog()"]
  B --> C["MatDialog.open(AddOrEditBankAccountDialogComponent)"]
  C --> D["Dialog w trybie dodawania"]
  D --> E["onSubmit()"]
  E --> F{"bankAccountForm.invalid"}
  F -->|true| G["errorMessage = Please fill in all required fields."]
  F -->|false| H["BankAccountService.addBankAccount(bankAccountData)"]
  H --> I["Toastr: Bank account added"]
  I --> J["dialogRef.close(true)"]
  J --> K["afterClosed()"]
  K --> L["getUserBankAccounts()"]
```

Po zamknięciu dialogu z wartością prawdziwą ekran odświeża grid przez `getUserBankAccounts()` i czyści zaznaczenie.

---

## 7. Przepływ edycji konta bankowego

```mermaid
flowchart TD
  A["Kliknięcie wiersza gridu"] --> B["openEditBankAccountDialog(bankAccount)"]
  B --> C["selection.clear()"]
  C --> D["MatDialog.open(..., data: bankAccount, disableClose: true)"]
  D --> E["ngOnInit(): bankAccountForm.setValue(...)"]
  E --> F["onSubmit()"]
  F --> G{"bankAccountForm.invalid"}
  G -->|true| H["errorMessage = Please fill in all required fields."]
  G -->|false| I["BankAccountService.editBankAccount(bankAccountData)"]
  I --> J["Toastr: Bank account updated"]
  J --> K["dialogRef.close(true)"]
  K --> L["afterClosed()"]
  L --> M["getUserBankAccounts()"]
```

Dialog edycji otrzymuje obiekt `IBankAccount` przez `MAT_DIALOG_DATA`. `ngOnInit()` ustawia `isEditMode = true` i wypełnia formularz wartościami z `data`.

---

## 8. Przepływ usuwania zaznaczonych kont

`deleteSelected()` tworzy tablicę identyfikatorów przez `this.selection.selected.map((s) => s.id)`.

Jeżeli tablica zawiera co najmniej jeden identyfikator, metoda wywołuje `BankAccountService.deleteBankAccounts(selectedIds)`. Po sukcesie ekran odświeża grid, czyści zaznaczenie i wyświetla komunikat `Bank accounts deleted successfully.`.

---

## 9. Reguły walidacji frontendowej

Formularz dialogu kończy działanie i ustawia komunikat błędu, gdy `bankAccountForm.invalid` ma wartość `true`.

Walidatory `Validators.required` posiadają pola `bankName`, `iban` i `currency`. Pole `isActive` nie ma walidatora.

---

## 10. Obsługa sukcesu i błędów

Sukces operacji dodawania, edycji i usuwania jest obsługiwany lokalnie przez `ToastrService.success(...)`.

Błędy HTTP są obsługiwane przez interceptory:

- `AuthInterceptor` obsługuje status `401` przekierowaniem do `/login`.
- `ErrorInterceptor` wyświetla komunikaty błędów przez `ToastrService.error(...)`.

---

## 11. Ograniczenia opisu

- Dokument nie opisuje walidacji backendowej.
- Dokument nie opisuje sposobu weryfikacji formatu IBAN po stronie API.
- Dokument nie opisuje sposobu powiązania konta bankowego z firmą po stronie API.
