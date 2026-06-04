# Invoice Stornos — Logika frontendowa

---

## 1. Zakres dokumentu

Dokument opisuje logikę wykonywaną przez frontend ekranu Invoice Stornos. Dokument nie opisuje implementacji backendu, reguł bazy danych ani wewnętrznego przetwarzania po stronie API.

---

## 2. Inicjalizacja ekranu

```mermaid
flowchart TD
  A["Wejście na /dashboard/invoice-stornos"] --> B["AuthGuard.canActivate()"]
  B --> C{"AuthService.isLoggedIn()"}
  C -->|true| D["InvoiceStornosComponent.ngOnInit()"]
  C -->|false| E["AuthService.logout() i router.navigate('/login')"]
  D --> F["loadInvoices()"]
  F --> G["DocumentService.getDocuments(3)"]
  G --> H["dataSource.data = invoices"]
  H --> I["invoices = response"]
```

`loadInvoices()` pobiera dokumenty przez `DocumentService.getDocuments(3)`. Parametr `3` oznacza typ dokumentu używany przez listę Invoice Stornos.

---

## 3. Przepływ filtrowania, sortowania i paginacji

Filtrowanie działa przez `MatTableDataSource.filter`. Wartość z pola Search jest przycinana, zamieniana na małe litery i przypisywana do `dataSource.filter`.

Sortowanie działa przez `MatSort`. Po inicjalizacji widoku `ngAfterViewInit()` przypisuje `this.sort` do `dataSource.sort`.

Paginacja działa przez `MatPaginator`. Po inicjalizacji widoku `ngAfterViewInit()` przypisuje `this.paginator` do `dataSource.paginator`.

---

## 4. Przepływ zaznaczania wierszy

Checkbox wiersza wywołuje `selection.toggle(row)`. Kliknięcie checkboxa zatrzymuje propagację zdarzenia, dlatego nie uruchamia nawigacji do edycji.

Checkbox nagłówka wywołuje `masterToggle()`. Jeżeli wszystkie wiersze są zaznaczone, `selection.clear()` usuwa zaznaczenie. Jeżeli nie wszystkie wiersze są zaznaczone, każdy wiersz z `dataSource.data` jest dodawany do `selection`.

---

## 5. Przepływ edycji storna

```mermaid
flowchart TD
  A["Kliknięcie wiersza gridu"] --> B["openEditInvoiceStornoDialog(row)"]
  B --> C["router.navigate(['/dashboard/edit-invoice-storno', row.id])"]
  C --> D["Render AddOrEditInvoiceStornoComponent w trybie edycji"]
```

`openEditInvoiceStornoDialog(row)` przekazuje identyfikator storna jako parametr trasy.

---

## 6. Przepływ usuwania zaznaczonych dokumentów

```mermaid
flowchart TD
  A["Kliknięcie Delete selected"] --> B["deleteSelected()"]
  B --> C["console.log(selection.selected)"]
  C --> D["documentIds = selection.selected.map(doc => doc.id)"]
  D --> E["DocumentService.deleteDocuments(documentIds)"]
  E --> F["loadInvoices() po sukcesie"]
  E --> G["console.error(...) przy błędzie"]
```

Metoda nie wykonuje lokalnej walidacji liczby zaznaczonych dokumentów. Po sukcesie lista jest pobierana ponownie przez `loadInvoices()`.

---

## 7. Obsługa sukcesu i błędów

Sukces pobrania danych jest obsługiwany przez przypisanie odpowiedzi do `dataSource.data` i `invoices`.

Sukces usunięcia powoduje ponowne wywołanie `loadInvoices()`. Komponent nie pokazuje lokalnego komunikatu sukcesu.

Błędy HTTP są obsługiwane przez interceptory:

- `AuthInterceptor` obsługuje status `401` przekierowaniem do `/login`.
- `ErrorInterceptor` wyświetla komunikaty błędów przez `ToastrService.error(...)`.

---

## 8. Ograniczenia opisu

- Dokument nie opisuje formularza edycji storna.
- Dokument nie opisuje sposobu usuwania dokumentów po stronie API.
- Dokument nie opisuje sposobu tworzenia storna z faktury po stronie API.
- Dokument nie traktuje zakomentowanego przycisku `New Storno` jako aktywnej operacji UI.
