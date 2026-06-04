# Invoice Stornos — Przegląd

---

## 1. Układ ekranu

### 1.1 Diagram struktury

```text
+--------------------------------------------------------------------+
| [Pasek nawigacyjny - NavbarComponent]                              |
+------------------+-------------------------------------------------+
| [Menu boczne]    | Invoice Stornos                            [⋮]  |
| Documents        +-------------------------------------------------+
|  - Invoices      | [Pole Search                               x]   |
|  - Proformas     +-------------------------------------------------+
|  - Stornos <-    | Grid Invoice Stornos                            |
|                  | Document Number | Client | Issue | Due | Total  |
|                  | [MatPaginator: 10 / 20 / 30, first/last]        |
+------------------+-------------------------------------------------+
```

### 1.2 Opis układu

Ekran składa się z paska tytułu, pola Search, gridu dokumentów storno i paginacji. Pasek tytułu zawiera nazwę `Invoice Stornos` i menu kontekstowe z operacją `Delete selected`.

Kliknięcie wiersza gridu nawiguje do ekranu edycji storna.

---

## 2. Komponenty główne

| Sekcja | Typ | Opis |
|---|---|---|
| Pasek tytułu | `div.app-header` | Wyświetla tytuł i menu kontekstowe. |
| Sekcja filtrów | `mat-form-field` | Pole `Search` filtruje dane przez `MatTableDataSource.filter`. |
| Grid dokumentów storno | `table mat-table` | Wyświetla dokumenty w kolumnach `select`, `documentNumber`, `clientName`, `issueDate`, `dueDate`, `totalValue`, `documentStatus`. |
| Paginacja | `mat-paginator` | Udostępnia rozmiary strony wyników `10`, `20`, `30`. |
| Status dokumentu | `mat-chip` | Pokazuje `record.documentStatus?.status`. |

---

## 3. Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Menu kontekstowe | `mat-menu` | Zawiera operację `Delete selected`. |
| Delete selected | `mat-menu-item` | Usuwa zaznaczone dokumenty. |
| Pole Search | `input matInput` | Filtruje dane gridu po każdej zmianie wartości. |
| Przycisk Clear | `mat-icon-button` | Czyści pole Search i resetuje filtr gridu. |
| Checkbox nagłówka | `mat-checkbox` | Zaznacza lub odznacza wszystkie wiersze. |
| Checkbox wiersza | `mat-checkbox` | Zaznacza lub odznacza pojedynczy wiersz. |
| Wiersz gridu | `tr mat-row` | Nawiguje do `/dashboard/edit-invoice-storno/:id`. |

---

## 4. Scenariusz główny

1. Użytkownik przechodzi do ekranu `/dashboard/invoice-stornos`.
2. `AuthGuard` dopuszcza dostęp, jeżeli `AuthService.isLoggedIn()` zwraca `true`.
3. `InvoiceStornosComponent.ngOnInit()` wywołuje `loadInvoices()`.
4. `loadInvoices()` wywołuje `DocumentService.getDocuments(3)`.
5. Odpowiedź typu `IDocumentTableRecord[]` jest przypisywana do `dataSource.data` i `invoices`.
6. Grid wyświetla rekordy dokumentów storno.
7. Ekran umożliwia filtrowanie, sortowanie, paginację, zaznaczanie, przejście do edycji i usuwanie zaznaczonych dokumentów.

---

## 5. Stany ekranu

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Stan początkowy | `dataSource` i `invoices` zawierają puste tablice. | Konstrukcja komponentu. |
| Dane załadowane | `dataSource.data` zawiera tablicę dokumentów storno. | Sukces `DocumentService.getDocuments(3)`. |
| Brak danych | `dataSource.data` jest pustą tablicą. | Sukces wywołania HTTP z pustą odpowiedzią. |
| Filtrowanie | `dataSource.filter` zawiera tekst z pola Search. | Zdarzenie `(keyup)` w polu Search. |
| Zaznaczanie | `SelectionModel<IDocumentTableRecord>` zawiera wybrane wiersze. | Kliknięcie checkboxa nagłówka lub checkboxa wiersza. |
| Nawigacja edycji | Router przechodzi do `/dashboard/edit-invoice-storno/{id}`. | Kliknięcie wiersza gridu. |

---

## 6. Dostępność i uprawnienia

| Warunek | Efekt |
|---|---|
| `AuthService.isLoggedIn()` zwraca `true` | Dostęp do ekranu jest dozwolony. |
| `AuthService.isLoggedIn()` zwraca `false` | `AuthGuard` wywołuje `AuthService.logout()` i przekierowuje do `/login`. |
| Token JWT istnieje w `localStorage` pod kluczem `authToken` | `AuthInterceptor` dodaje nagłówek `Authorization: Bearer {token}` do żądań HTTP. |

---

## 7. Notatki techniczne

- Komponent ekranu: `InvoiceStornosComponent`.
- Model wiersza: `IDocumentTableRecord`.
- Serwis HTTP: `DocumentService`.
- Źródło danych gridu: `MatTableDataSource<IDocumentTableRecord>`.
- Typ dokumentu pobierany przez listę: `3`.

---

## Następne sekcje

- Szczegółowe dane o polach, kolumnach i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika frontendowa i przepływy UI: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
