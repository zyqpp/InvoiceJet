# Products — Przegląd

---

## 1. Układ ekranu

### 1.1 Diagram struktury

```
┌──────────────────────────────────────────────────────────────────────────┐
│ [Pasek nawigacyjny — NavbarComponent]                                    │
├──────────────────┬───────────────────────────────────────────────────────┤
│ [Menu boczne]    │ Products                         [ + New Product ][⋮] │
│                  ├───────────────────────────────────────────────────────┤
│ Dashboard        │ [Pole Search                                   x]     │
│ Documents        ├───────────────────────────────────────────────────────┤
│ Inventory        │ Grid Products                                         │
│  - Clients       │ ┌────┬──────┬───────┬──────────────────┬─────┬──────┐ │
│  - Products ←    │ │ ☑  │ Name │ Price │ Unit of Measure. │ TVA │ TVA? │ │
│ Settings         │ ├────┼──────┼───────┼──────────────────┼─────┼──────┤ │
│                  │ │ ☐  │ ...  │ ...   │ ...              │ ... │  ☑   │ │
│                  │ └────┴──────┴───────┴──────────────────┴─────┴──────┘ │
│                  │ [MatPaginator: 10 / 20 / 30, first/last]              │
└──────────────────┴───────────────────────────────────────────────────────┘
```

### 1.2 Opis układu

Ekran składa się z paska tytułu, pola Search, gridu produktów i paginacji. Pasek tytułu zawiera nazwę `Products`, przycisk `New Product` i menu kontekstowe z operacją `Delete selected`.

Grid wykorzystuje `MatTableDataSource<IProduct>`. Wiersz gridu jest klikalny i otwiera dialog Edycja produktu. Pierwsza kolumna zawiera pola wyboru do zaznaczania pojedynczych wierszy lub wszystkich wierszy.

---

## 2. Komponenty główne

### 2.1 Sekcje UI

| Sekcja | Typ | Opis |
|---|---|---|
| Pasek tytułu | `div.app-header` | Wyświetla tytuł `Products`, przycisk `New Product` i menu kontekstowe. |
| Sekcja filtrów | `mat-form-field` | Pole `Search` filtruje dane przez `MatTableDataSource.filter`. |
| Grid produktów | `table mat-table` | Wyświetla produkty w kolumnach `select`, `name`, `price`, `unitOfMeasurement`, `tvaValue`, `containsTva`. |
| Paginacja | `mat-paginator` | Udostępnia rozmiary strony wyników `10`, `20`, `30`. |
| Dialog Dodawanie/Edycja produktu | `MatDialog` | Otwiera formularz produktu jako dialog Angular Material. |

### 2.2 Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Przycisk New Product | `mat-raised-button` | Otwiera dialog Dodawanie produktu. |
| Menu kontekstowe | `mat-menu` | Zawiera operację `Delete selected`. |
| Przycisk Delete selected | `mat-menu-item` | Wysyła identyfikatory zaznaczonych produktów do usunięcia. |
| Pole Search | `input matInput` | Filtruje dane gridu po każdej zmianie wartości. |
| Przycisk Clear | `mat-icon-button` | Czyści pole Search i resetuje filtr gridu. |
| Checkbox nagłówka | `mat-checkbox` | Zaznacza lub odznacza wszystkie wiersze z bieżącego źródła danych. |
| Checkbox wiersza | `mat-checkbox` | Zaznacza lub odznacza pojedynczy wiersz. |
| Wiersz gridu | `tr mat-row` | Otwiera dialog Edycja produktu po kliknięciu. |

---

## 3. Scenariusz główny

1. Użytkownik przechodzi do ekranu `/dashboard/products`.
2. `AuthGuard` dopuszcza dostęp, jeżeli `AuthService.isLoggedIn()` zwraca `true`.
3. `ProductsComponent.ngOnInit()` wywołuje `getProducts()`.
4. `getProducts()` wywołuje `ProductService.getProductsForUserId()`.
5. Odpowiedź typu `IProduct[]` jest przypisywana do `products` i `dataSource.data`.
6. Grid wyświetla rekordy produktów.
7. Ekran umożliwia filtrowanie, sortowanie, paginację, zaznaczanie, dodanie, edycję i usuwanie produktów.

---

## 4. Stany ekranu

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Stan początkowy | Komponent jest inicjalizowany i wywołuje `getProducts()`. | Wejście na `/dashboard/products`. |
| Dane załadowane | `dataSource.data` zawiera tablicę produktów. | Sukces `ProductService.getProductsForUserId()`. |
| Brak danych | `dataSource.data` jest pustą tablicą. | Sukces wywołania HTTP z pustą odpowiedzią. |
| Filtrowanie | `dataSource.filter` zawiera tekst wpisany w pole Search. | Zdarzenie `(keyup)` w polu Search. |
| Wyczyść filtr | `dataSource.filter` jest pustym tekstem. | Kliknięcie przycisku Clear. |
| Zaznaczanie | `SelectionModel<IProduct>` zawiera wybrane wiersze. | Kliknięcie checkboxa nagłówka lub checkboxa wiersza. |
| Dialog dodawania | `AddOrEditProductDialogComponent` otwarty bez danych wejściowych. | Kliknięcie `New Product`. |
| Dialog edycji | `AddOrEditProductDialogComponent` otwarty z obiektem `IProduct`. | Kliknięcie wiersza gridu. |
| Błąd HTTP | Błąd przechodzi przez interceptory HTTP. | Odpowiedź HTTP 4xx lub 5xx. |

---

## 5. Dostępność i uprawnienia

| Warunek | Efekt |
|---|---|
| `AuthService.isLoggedIn()` zwraca `true` | Dostęp do ekranu jest dozwolony. |
| `AuthService.isLoggedIn()` zwraca `false` | `AuthGuard` wywołuje `AuthService.logout()` i przekierowuje do `/login`. |
| Token JWT istnieje w `localStorage` pod kluczem `authToken` | `AuthInterceptor` dodaje nagłówek `Authorization: Bearer {token}` do żądań HTTP. |
| Odpowiedź HTTP ma status `401` | `AuthInterceptor` przekierowuje do `/login` i wywołuje `AuthService.logout()`. |

---

## 6. Integracje widoczne z frontendu

| Integracja | Miejsce w UI | Wywołanie frontendowe |
|---|---|---|
| API aplikacji InvoiceJet | Lista produktów, dodanie, edycja, usuwanie | Metody `ProductService` używające `HttpClient`. |

> Dokument opisuje wyłącznie wywołania wykonywane przez frontend. Implementacja API nie jest częścią tego dokumentu.

---

## 7. Notatki techniczne

- Komponent ekranu: `ProductsComponent`.
- Komponent dialogu: `AddOrEditProductDialogComponent`.
- Model danych: `IProduct`.
- Serwis HTTP: `ProductService`.
- Źródło danych gridu: `MatTableDataSource<IProduct>`.
- Zaznaczanie wierszy: `SelectionModel<IProduct>(true, [])`.
- Sortowanie: `MatSort`.
- Paginacja: `MatPaginator`.
- Komunikaty sukcesu: `ToastrService`.

---

## Następne sekcje

- Szczegółowe dane o polach, kolumnach i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika frontendowa i przepływy UI: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
