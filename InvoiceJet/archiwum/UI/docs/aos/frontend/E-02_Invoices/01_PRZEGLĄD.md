# Invoices — Przegląd

---

## 1. Układ ekranu

### 1.1 Diagram struktury

```
┌──────────────────────────────────────────────────────────────────────────┐
│ [Pasek nawigacyjny — NavbarComponent]                                    │
├──────────────────┬───────────────────────────────────────────────────────┤
│ [Menu boczne]    │ Invoices                         [ + New Invoice ][⋮] │
│ Documents        ├───────────────────────────────────────────────────────┤
│  - Invoices ←    │ [Pole Search                                   x]     │
│  - Proformas     ├───────────────────────────────────────────────────────┤
│  - Stornos       │ Grid Invoices                                         │
│                  │ ┌────┬────────────┬────────┬───────┬─────┬────┬────┐ │
│                  │ │ ☑  │ Doc Number │ Client │ Issue │ Due │Sum │Stat│ │
│                  │ ├────┼────────────┼────────┼───────┼─────┼────┼────┤ │
│                  │ │ ☐  │ ...        │ ...    │ ...   │ ... │... │... │ │
│                  │ └────┴────────────┴────────┴───────┴─────┴────┴────┘ │
│                  │ [MatPaginator: 10 / 20 / 30, first/last]              │
└──────────────────┴───────────────────────────────────────────────────────┘
```

### 1.2 Opis układu

Ekran składa się z paska tytułu, pola Search, gridu faktur i paginacji. Pasek tytułu zawiera nazwę `Invoices`, przycisk `New Invoice` i menu kontekstowe.

Menu kontekstowe zawiera operacje `Transform to storno` i `Delete selected`. Kliknięcie wiersza gridu nawiguje do ekranu edycji faktury.

---

## 2. Komponenty główne

| Sekcja | Typ | Opis |
|---|---|---|
| Pasek tytułu | `div.app-header` | Wyświetla tytuł `Invoices`, przycisk `New Invoice` i menu kontekstowe. |
| Sekcja filtrów | `mat-form-field` | Pole `Search` filtruje dane przez `MatTableDataSource.filter`. |
| Grid faktur | `table mat-table` | Wyświetla faktury w kolumnach `select`, `documentNumber`, `clientName`, `issueDate`, `dueDate`, `totalValue`, `documentStatus`. |
| Paginacja | `mat-paginator` | Udostępnia rozmiary strony wyników `10`, `20`, `30`. |
| Status dokumentu | `mat-chip` | Pokazuje `record.documentStatus?.status`. |

---

## 3. Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Przycisk New Invoice | `mat-raised-button` | Nawiguje do `/dashboard/add-invoice`. |
| Menu kontekstowe | `mat-menu` | Zawiera operacje `Transform to storno` i `Delete selected`. |
| Transform to storno | `mat-menu-item` | Wywołuje transformację zaznaczonych faktur do storna. |
| Delete selected | `mat-menu-item` | Usuwa zaznaczone dokumenty. |
| Pole Search | `input matInput` | Filtruje dane gridu po każdej zmianie wartości. |
| Przycisk Clear | `mat-icon-button` | Czyści pole Search i resetuje filtr gridu. |
| Checkbox nagłówka | `mat-checkbox` | Zaznacza lub odznacza wszystkie wiersze. |
| Checkbox wiersza | `mat-checkbox` | Zaznacza lub odznacza pojedynczy wiersz. |
| Wiersz gridu | `tr mat-row` | Nawiguje do `/dashboard/edit-invoice/:id`. |

---

## 4. Scenariusz główny

1. Użytkownik przechodzi do ekranu `/dashboard/invoices`.
2. `AuthGuard` dopuszcza dostęp, jeżeli `AuthService.isLoggedIn()` zwraca `true`.
3. `InvoicesComponent.ngOnInit()` wywołuje `loadInvoices()`.
4. `loadInvoices()` wywołuje `DocumentService.getDocuments(1)`.
5. Odpowiedź typu `IDocumentTableRecord[]` jest przypisywana do `dataSource.data` i `invoices`.
6. Grid wyświetla rekordy faktur.
7. Ekran umożliwia filtrowanie, sortowanie, paginację, zaznaczanie, przejście do dodawania, przejście do edycji i operacje na zaznaczonych dokumentach.

---

## 5. Stany ekranu

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Stan początkowy | `dataSource` zawiera pustą tablicę, a `invoices` zawiera pustą tablicę. | Konstrukcja komponentu. |
| Dane załadowane | `dataSource.data` zawiera tablicę faktur. | Sukces `DocumentService.getDocuments(1)`. |
| Brak danych | `dataSource.data` jest pustą tablicą. | Sukces wywołania HTTP z pustą odpowiedzią. |
| Filtrowanie | `dataSource.filter` zawiera tekst wpisany w pole Search. | Zdarzenie `(keyup)` w polu Search. |
| Zaznaczanie | `SelectionModel<IDocumentTableRecord>` zawiera wybrane wiersze. | Kliknięcie checkboxa nagłówka lub checkboxa wiersza. |
| Nawigacja dodawania | Router przechodzi do `dashboard/add-invoice`. | Kliknięcie `New Invoice`. |
| Nawigacja edycji | Router przechodzi do `/dashboard/edit-invoice/{id}`. | Kliknięcie wiersza gridu. |

---

## 6. Dostępność i uprawnienia

| Warunek | Efekt |
|---|---|
| `AuthService.isLoggedIn()` zwraca `true` | Dostęp do ekranu jest dozwolony. |
| `AuthService.isLoggedIn()` zwraca `false` | `AuthGuard` wywołuje `AuthService.logout()` i przekierowuje do `/login`. |
| Token JWT istnieje w `localStorage` pod kluczem `authToken` | `AuthInterceptor` dodaje nagłówek `Authorization: Bearer {token}` do żądań HTTP. |

---

## 7. Notatki techniczne

- Komponent ekranu: `InvoicesComponent`.
- Model wiersza: `IDocumentTableRecord`.
- Serwis HTTP: `DocumentService`.
- Źródło danych gridu: `MatTableDataSource<IDocumentTableRecord>`.
- Zaznaczanie wierszy: `SelectionModel<IDocumentTableRecord>(true, [])`.
- Typ dokumentu pobierany przez listę: `1`.

---

## Następne sekcje

- Szczegółowe dane o polach, kolumnach i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika frontendowa i przepływy UI: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
