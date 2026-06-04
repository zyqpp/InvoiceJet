# Document Series — Przegląd

---

## 1. Układ ekranu

### 1.1 Diagram struktury

```
┌──────────────────────────────────────────────────────────────────────────┐
│ [Pasek nawigacyjny — NavbarComponent]                                    │
├──────────────────┬───────────────────────────────────────────────────────┤
│ [Menu boczne]    │ Document Series                  [ + New Series ][⋮]  │
│ Settings         ├───────────────────────────────────────────────────────┤
│  - Firm Details  │ [Pole Search                                   x]     │
│  - Bank Accounts ├───────────────────────────────────────────────────────┤
│  - Doc. Series ← │ Grid Document Series                                  │
│                  │ ┌────┬───────────────┬────────────┬───────┬────┬────┐ │
│                  │ │ ☑  │ Document Type │ Series Name│ First │Cur.│Def │ │
│                  │ ├────┼───────────────┼────────────┼───────┼────┼────┤ │
│                  │ │ ☐  │ Factura       │ ...        │ ...   │... │ ☑  │ │
│                  │ └────┴───────────────┴────────────┴───────┴────┴────┘ │
│                  │ [MatPaginator: 10 / 20 / 30, first/last]              │
└──────────────────┴───────────────────────────────────────────────────────┘
```

### 1.2 Opis układu

Ekran składa się z paska tytułu, pola Search, gridu serii dokumentów i paginacji. Pasek tytułu zawiera nazwę `Document Series`, przycisk `New Series` i menu kontekstowe z operacją `Delete selected`.

Grid wykorzystuje `MatTableDataSource<IDocumentSeries>`. Wiersz gridu jest klikalny i otwiera dialog Edycja serii dokumentów. Pierwsza kolumna zawiera pola wyboru do zaznaczania pojedynczych wierszy lub wszystkich wierszy.

---

## 2. Komponenty główne

| Sekcja | Typ | Opis |
|---|---|---|
| Pasek tytułu | `div.app-header` | Wyświetla tytuł `Document Series`, przycisk `New Series` i menu kontekstowe. |
| Sekcja filtrów | `mat-form-field` | Pole `Search` filtruje dane przez `MatTableDataSource.filter`. |
| Grid serii | `table mat-table` | Wyświetla serie w kolumnach `select`, `documentType`, `seriesName`, `firstNumber`, `currentNumber`, `isDefault`. |
| Paginacja | `mat-paginator` | Udostępnia rozmiary strony wyników `10`, `20`, `30`. |
| Dialog Dodawanie/Edycja serii | `MatDialog` | Otwiera formularz serii dokumentów. |

---

## 3. Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Przycisk New Series | `mat-raised-button` | Otwiera dialog Dodawanie serii dokumentów. |
| Menu kontekstowe | `mat-menu` | Zawiera operację `Delete selected`. |
| Przycisk Delete selected | `mat-menu-item` | Usuwa zaznaczone serie dokumentów. |
| Pole Search | `input matInput` | Filtruje dane gridu po każdej zmianie wartości. |
| Przycisk Clear | `mat-icon-button` | Czyści pole Search i resetuje filtr gridu. |
| Checkbox nagłówka | `mat-checkbox` | Zaznacza lub odznacza wszystkie wiersze. |
| Checkbox wiersza | `mat-checkbox` | Zaznacza lub odznacza pojedynczy wiersz. |
| Wiersz gridu | `tr mat-row` | Otwiera dialog Edycja serii po kliknięciu. |

---

## 4. Scenariusz główny

1. Użytkownik przechodzi do ekranu `/dashboard/document-series`.
2. `AuthGuard` dopuszcza dostęp, jeżeli `AuthService.isLoggedIn()` zwraca `true`.
3. `DocumentSeriesComponent.ngOnInit()` wywołuje `getDocumentSeries()`.
4. `getDocumentSeries()` wywołuje `DocumentSeriesService.getDocumentSeriesForUserId()`.
5. Odpowiedź typu `IDocumentSeries[]` jest przypisywana do `documentSeriesList` i `dataSource.data`.
6. Grid wyświetla rekordy serii dokumentów.
7. Ekran umożliwia filtrowanie, sortowanie, paginację, zaznaczanie, dodanie, edycję i usuwanie serii.

---

## 5. Stany ekranu

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Stan ładowania | Widoczny jest `mat-progress-bar`, gdy `!documentSeriesList`. | Wejście na ekran przed odpowiedzią API. |
| Dane załadowane | `dataSource.data` zawiera tablicę serii dokumentów. | Sukces `getDocumentSeriesForUserId()`. |
| Brak danych | `dataSource.data` jest pustą tablicą. | Sukces wywołania HTTP z pustą odpowiedzią. |
| Filtrowanie | `dataSource.filter` zawiera tekst wpisany w pole Search. | Zdarzenie `(keyup)` w polu Search. |
| Zaznaczanie | `SelectionModel<IDocumentSeries>` zawiera wybrane wiersze. | Kliknięcie checkboxa nagłówka lub checkboxa wiersza. |
| Dialog dodawania | `AddOrEditDocumentSeriesDialogComponent` otwarty z `data: null`. | Kliknięcie `New Series`. |
| Dialog edycji | `AddOrEditDocumentSeriesDialogComponent` otwarty z obiektem `IDocumentSeries`. | Kliknięcie wiersza gridu. |

---

## 6. Dostępność i uprawnienia

| Warunek | Efekt |
|---|---|
| `AuthService.isLoggedIn()` zwraca `true` | Dostęp do ekranu jest dozwolony. |
| `AuthService.isLoggedIn()` zwraca `false` | `AuthGuard` wywołuje `AuthService.logout()` i przekierowuje do `/login`. |
| Token JWT istnieje w `localStorage` pod kluczem `authToken` | `AuthInterceptor` dodaje nagłówek `Authorization: Bearer {token}` do żądań HTTP. |

---

## 7. Notatki techniczne

- Komponent ekranu: `DocumentSeriesComponent`.
- Komponent dialogu: `AddOrEditDocumentSeriesDialogComponent`.
- Model danych: `IDocumentSeries`.
- Model typu dokumentu: `IDocumentType`.
- Serwis HTTP: `DocumentSeriesService`.
- Źródło danych gridu: `MatTableDataSource<IDocumentSeries>`.
- Zaznaczanie wierszy: `SelectionModel<IDocumentSeries>(true, [])`.

---

## Następne sekcje

- Szczegółowe dane o polach, kolumnach i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika frontendowa i przepływy UI: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
