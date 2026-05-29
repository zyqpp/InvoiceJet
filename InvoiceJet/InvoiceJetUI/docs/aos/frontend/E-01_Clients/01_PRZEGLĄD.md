# Clients — Przegląd

---

## 1. Layout ekranu

### 1.1 Diagram struktury

```
┌──────────────────────────────────────────────────────────────────┐
│ [NAGŁÓWEK APLIKACJI — NavbarComponent]                           │
├──────────────────┬───────────────────────────────────────────────┤
│                  │  Clients                 [ + New client ] [⋮] │
│  [SIDEBAR]       ├───────────────────────────────────────────────┤
│  Dashboard       │  [Pole Search                            x]   │
│  Documents       ├───────────────────────────────────────────────┤
│  Inventory       │  Grid Clients                                │
│   - Clients      │  ┌────┬──────┬─────┬────────┬─────────┬─────┐│
│   - Products     │  │ ☑  │ Name │ CUI │ RegCom │ Address │ ... ││
│  Settings        │  ├────┼──────┼─────┼────────┼─────────┼─────┤│
│   - Firm Details │  │ ☐  │ ...  │ ... │ ...    │ ...     │ ... ││
│   - Bank Accounts│  │ ☐  │ ...  │ ... │ ...    │ ...     │ ... ││
│   - Doc. Series  │  └────┴──────┴─────┴────────┴─────────┴─────┘│
│                  │  [MatPaginator: 10 / 20 / 30, first/last]    │
└──────────────────┴───────────────────────────────────────────────┘
```

### 1.2 Opis layoutu

Ekran składa się z obszaru roboczego zawierającego pasek tytułu, pole wyszukiwania, grid klientów oraz paginację. Pasek tytułu zawiera nazwę ekranu `Clients`, przycisk `New client` oraz menu kontekstowe z opcją `Delete selected`.

Grid wykorzystuje `MatTableDataSource<IFirm>`. Wiersz gridu jest klikalny i otwiera dialog Edycja klienta. Pierwsza kolumna zawiera pola wyboru do zaznaczania pojedynczych wierszy lub wszystkich wierszy.

---

## 2. Komponenty główne

### 2.1 Sekcje UI

| Sekcja | Typ | Opis |
|---|---|---|
| Pasek tytułu | `div.app-header` | Wyświetla tytuł `Clients`, przycisk `New client` i menu kontekstowe. |
| Sekcja filtrów | `mat-form-field` | Pole `Search` filtruje dane po tekście przez `MatTableDataSource.filter`. |
| Grid klientów | `table mat-table` | Wyświetla klientów w kolumnach `select`, `name`, `cui`, `regCom`, `address`, `county`, `city`. |
| Paginacja | `mat-paginator` | Udostępnia rozmiary strony `10`, `20`, `30` i przyciski pierwszej oraz ostatniej strony. |
| Dialog Dodawanie/Edycja klienta | `MatDialog` | Otwiera formularz klienta jako prawy panel o stałej szerokości `550px`. |

### 2.2 Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Przycisk New client | `mat-raised-button` | Otwiera dialog Dodawanie klienta. |
| Menu kontekstowe | `mat-menu` | Zawiera operację `Delete selected`. |
| Przycisk Delete selected | `mat-menu-item` | Usuwa zaznaczone wiersze, jeżeli istnieje co najmniej jeden zaznaczony klient. |
| Pole Search | `input matInput` | Filtruje dane gridu po każdej zmianie wartości. |
| Przycisk Clear | `mat-icon-button` | Czyści pole Search i resetuje filtr gridu. |
| Checkbox nagłówka | `mat-checkbox` | Zaznacza lub odznacza wszystkie wiersze z bieżącego źródła danych. |
| Checkbox wiersza | `mat-checkbox` | Zaznacza lub odznacza pojedynczy wiersz. |
| Wiersz gridu | `tr mat-row` | Otwiera dialog Edycja klienta po kliknięciu. |

---

## 3. Scenariusz główny

1. Użytkownik przechodzi do ekranu `/dashboard/clients`.
2. `AuthGuard` dopuszcza dostęp, jeżeli `AuthService.isLoggedIn()` zwraca `true`.
3. `ClientsComponent.ngOnInit()` wywołuje `getUserFirms()`.
4. `getUserFirms()` wywołuje `FirmService.getUserClientFirms()`.
5. Odpowiedź typu `IFirm[]` jest przypisywana do `firms` i `dataSource.data`.
6. Grid wyświetla rekordy klientów.
7. Użytkownik może filtrować, sortować, przełączać strony, zaznaczać wiersze, dodać klienta lub edytować klienta przez kliknięcie wiersza.

---

## 4. Stany ekranu

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Stan początkowy | Komponent jest inicjalizowany i wywołuje `getUserFirms()`. | Wejście na `/dashboard/clients`. |
| Dane załadowane | `dataSource.data` zawiera tablicę klientów. Grid renderuje wiersze. | Sukces `FirmService.getUserClientFirms()`. |
| Brak danych | `dataSource.data` jest pustą tablicą. Grid renderuje bez wierszy danych. | Sukces wywołania HTTP z pustą tablicą. |
| Filtrowanie | `dataSource.filter` zawiera tekst wpisany w pole Search. | Zdarzenie `(keyup)` w polu Search. |
| Wyczyść filtr | `dataSource.filter` jest pustym tekstem. Pole Search jest czyszczone. | Kliknięcie przycisku Clear. |
| Zaznaczanie | `SelectionModel<IFirm>` zawiera wybrane wiersze. | Kliknięcie checkboxa nagłówka lub checkboxa wiersza. |
| Dialog dodawania | `AddEditClientDialogComponent` otwarty bez danych wejściowych. | Kliknięcie przycisku `New client`. |
| Dialog edycji | `AddEditClientDialogComponent` otwarty z obiektem `IFirm`. | Kliknięcie wiersza gridu. |
| Błąd HTTP | Błąd obsługiwany przez interceptory HTTP. | Odpowiedź HTTP 4xx lub 5xx. |

---

## 5. Dostępność i uprawnienia

| Warunek | Efekt |
|---|---|
| `AuthService.isLoggedIn()` zwraca `true` | Dostęp do ekranu jest dozwolony. |
| `AuthService.isLoggedIn()` zwraca `false` | `AuthGuard` wywołuje `AuthService.logout()` i przekierowuje do `/login`. |
| Token JWT istnieje w `localStorage` pod kluczem `authToken` | `AuthInterceptor` dodaje nagłówek `Authorization: Bearer {token}` do żądań HTTP. |
| Odpowiedź HTTP ma status `401` | `AuthInterceptor` przekierowuje do `/login` i wywołuje `AuthService.logout()`. |

---

## 6. Integracje zewnętrzne widoczne z frontendu

| Integracja | Miejsce w UI | Wywołanie frontendowe |
|---|---|---|
| API aplikacji InvoiceJet | Lista klientów, dodanie, edycja, usuwanie | Metody `FirmService` używające `HttpClient`. |
| ANAF | Przycisk `cloud_download` przy polu CUI w dialogu | `FirmService.getFirmFromAnaf(cuiValue)`. |

> Dokument opisuje wyłącznie wywołania wykonywane przez frontend. Implementacja API i przetwarzanie po stronie backendu nie są częścią tego dokumentu.

---

## 7. Notatki techniczne

- Komponent ekranu: `ClientsComponent`.
- Komponent dialogu: `AddEditClientDialogComponent`.
- Model danych: `IFirm`.
- Serwis HTTP: `FirmService`.
- Źródło danych gridu: `MatTableDataSource<IFirm>`.
- Zaznaczanie wierszy: `SelectionModel<IFirm>(true, [])`.
- Sortowanie: `MatSort`.
- Paginacja: `MatPaginator`.
- Komunikaty sukcesu: `ToastrService`.
- Komunikaty błędu HTTP: `ErrorInterceptor`.

---

## Następne sekcje

- Szczegółowe dane o polach, kolumnach i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika frontendowa i przepływy UI: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
