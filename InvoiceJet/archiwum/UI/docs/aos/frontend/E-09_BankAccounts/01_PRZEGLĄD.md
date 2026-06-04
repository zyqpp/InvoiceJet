# Bank Accounts — Przegląd

---

## 1. Układ ekranu

### 1.1 Diagram struktury

```
┌──────────────────────────────────────────────────────────────────────────┐
│ [Pasek nawigacyjny — NavbarComponent]                                    │
├──────────────────┬───────────────────────────────────────────────────────┤
│ [Menu boczne]    │ Bank Accounts                    [ + New Account ][⋮] │
│ Settings         ├───────────────────────────────────────────────────────┤
│  - Firm Details  │ [Pole Search                                   x]     │
│  - Bank Accounts←├───────────────────────────────────────────────────────┤
│  - Doc. Series   │ Grid Bank Accounts                                    │
│                  │ ┌────┬───────────┬────────────┬──────────┬──────────┐ │
│                  │ │ ☑  │ Bank Name │ IBAN       │ Currency │ Active   │ │
│                  │ ├────┼───────────┼────────────┼──────────┼──────────┤ │
│                  │ │ ☐  │ ...       │ ...        │ RON/EUR  │   ☑      │ │
│                  │ └────┴───────────┴────────────┴──────────┴──────────┘ │
│                  │ [MatPaginator: 10 / 20 / 30, first/last]              │
└──────────────────┴───────────────────────────────────────────────────────┘
```

### 1.2 Opis układu

Ekran składa się z paska tytułu, pola Search, gridu kont bankowych i paginacji. Pasek tytułu zawiera nazwę `Bank Accounts`, przycisk `New Account` i menu kontekstowe z operacją `Delete selected`.

Grid wykorzystuje `MatTableDataSource<IBankAccount>`. Wiersz gridu jest klikalny i otwiera dialog Edycja konta bankowego. Pierwsza kolumna zawiera pola wyboru do zaznaczania pojedynczych wierszy lub wszystkich wierszy.

---

## 2. Komponenty główne

| Sekcja | Typ | Opis |
|---|---|---|
| Pasek tytułu | `div.app-header` | Wyświetla tytuł `Bank Accounts`, przycisk `New Account` i menu kontekstowe. |
| Sekcja filtrów | `mat-form-field` | Pole `Search` filtruje dane przez `MatTableDataSource.filter`. |
| Grid kont bankowych | `table mat-table` | Wyświetla konta w kolumnach `select`, `bankName`, `iban`, `currency`, `isActive`. |
| Paginacja | `mat-paginator` | Udostępnia rozmiary strony wyników `10`, `20`, `30`. |
| Dialog Dodawanie/Edycja konta | `MatDialog` | Otwiera formularz konta bankowego. |

---

## 3. Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Przycisk New Account | `mat-raised-button` | Otwiera dialog Dodawanie konta bankowego. |
| Menu kontekstowe | `mat-menu` | Zawiera operację `Delete selected`. |
| Przycisk Delete selected | `mat-menu-item` | Usuwa zaznaczone konta, jeżeli istnieje co najmniej jedno zaznaczenie. |
| Pole Search | `input matInput` | Filtruje dane gridu po każdej zmianie wartości. |
| Przycisk Clear | `mat-icon-button` | Czyści pole Search i resetuje filtr gridu. |
| Checkbox nagłówka | `mat-checkbox` | Zaznacza lub odznacza wszystkie wiersze. |
| Checkbox wiersza | `mat-checkbox` | Zaznacza lub odznacza pojedynczy wiersz. |
| Wiersz gridu | `tr mat-row` | Otwiera dialog Edycja konta bankowego po kliknięciu. |

---

## 4. Scenariusz główny

1. Użytkownik przechodzi do ekranu `/dashboard/bank-accounts`.
2. `AuthGuard` dopuszcza dostęp, jeżeli `AuthService.isLoggedIn()` zwraca `true`.
3. `BankAccountsComponent.ngOnInit()` wywołuje `getUserBankAccounts()`.
4. `getUserBankAccounts()` wywołuje `BankAccountService.getUserFirmBankAccounts()`.
5. Odpowiedź typu `IBankAccount[]` jest mapowana przez `mapCurrencyNames(accounts)`.
6. Wynik jest przypisywany do `bankAccounts` i `dataSource.data`.
7. Ekran umożliwia filtrowanie, sortowanie, paginację, zaznaczanie, dodanie, edycję i usuwanie kont.

---

## 5. Stany ekranu

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Stan ładowania | Widoczny jest `mat-progress-bar`, gdy `!bankAccounts`. | Wejście na ekran przed odpowiedzią API. |
| Dane załadowane | `dataSource.data` zawiera tablicę kont bankowych. | Sukces `BankAccountService.getUserFirmBankAccounts()`. |
| Brak danych | `dataSource.data` jest pustą tablicą. | Sukces wywołania HTTP z pustą odpowiedzią. |
| Filtrowanie | `dataSource.filter` zawiera tekst wpisany w pole Search. | Zdarzenie `(keyup)` w polu Search. |
| Zaznaczanie | `SelectionModel<IBankAccount>` zawiera wybrane wiersze. | Kliknięcie checkboxa nagłówka lub checkboxa wiersza. |
| Dialog dodawania | `AddOrEditBankAccountDialogComponent` otwarty bez danych wejściowych. | Kliknięcie `New Account`. |
| Dialog edycji | `AddOrEditBankAccountDialogComponent` otwarty z obiektem `IBankAccount`. | Kliknięcie wiersza gridu. |

---

## 6. Dostępność i uprawnienia

| Warunek | Efekt |
|---|---|
| `AuthService.isLoggedIn()` zwraca `true` | Dostęp do ekranu jest dozwolony. |
| `AuthService.isLoggedIn()` zwraca `false` | `AuthGuard` wywołuje `AuthService.logout()` i przekierowuje do `/login`. |
| Token JWT istnieje w `localStorage` pod kluczem `authToken` | `AuthInterceptor` dodaje nagłówek `Authorization: Bearer {token}` do żądań HTTP. |

---

## 7. Notatki techniczne

- Komponent ekranu: `BankAccountsComponent`.
- Komponent dialogu: `AddOrEditBankAccountDialogComponent`.
- Model danych: `IBankAccount`.
- Serwis HTTP: `BankAccountService`.
- Źródło danych gridu: `MatTableDataSource<IBankAccount>`.
- Zaznaczanie wierszy: `SelectionModel<IBankAccount>(true, [])`.
- Dostępne waluty w UI: `RON` i `EUR`.

---

## Następne sekcje

- Szczegółowe dane o polach, kolumnach i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika frontendowa i przepływy UI: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
