# Invoices — Logika frontendowa

---

## 1. Zakres dokumentu

Dokument opisuje logikę wykonywaną przez frontend ekranu Invoices. Dokument nie opisuje implementacji backendu, reguł bazy danych ani wewnętrznego przetwarzania po stronie API.

---

## 2. Inicjalizacja ekranu

### 2.1 Przepływ inicjalizacji

```mermaid
flowchart TD
  A["Wejście na /dashboard/invoices"] --> B["AuthGuard.canActivate()"]
  B --> C{"AuthService.isLoggedIn()"}
  C -->|true| D["InvoicesComponent.ngOnInit()"]
  C -->|false| E["AuthService.logout() i router.navigate('/login')"]
  D --> F["loadInvoices()"]
  F --> G["DocumentService.getDocuments(1)"]
  G --> H["dataSource.data = invoices"]
  H --> I["invoices = response"]
```

### 2.2 Opis przepływu

`AuthGuard` kontroluje dostęp do trasy `/dashboard/invoices`. Jeżeli użytkownik jest zalogowany, komponent wywołuje `loadInvoices()` podczas `ngOnInit()`.

`loadInvoices()` pobiera dokumenty przez `DocumentService.getDocuments(1)`. Parametr `1` oznacza typ dokumentu używany przez listę Invoices.

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

## 5. Przepływ dodawania faktury

```mermaid
flowchart TD
  A["Kliknięcie New Invoice"] --> B["openNewInvoiceDialog()"]
  B --> C["router.navigate(['dashboard/add-invoice'])"]
  C --> D["Render AddOrEditInvoiceComponent"]
```

Operacja nie otwiera dialogu. Nazwa metody zawiera słowo `Dialog`, ale implementacja wykonuje nawigację do trasy dodawania faktury.

---

## 6. Przepływ edycji faktury

```mermaid
flowchart TD
  A["Kliknięcie wiersza gridu"] --> B["openEditInvoiceDialog(row)"]
  B --> C["router.navigate(['/dashboard/edit-invoice', row.id])"]
  C --> D["Render AddOrEditInvoiceComponent w trybie edycji"]
```

`openEditInvoiceDialog(row)` przekazuje identyfikator faktury jako parametr trasy.

---

## 7. Przepływ usuwania zaznaczonych dokumentów

```mermaid
flowchart TD
  A["Kliknięcie Delete selected"] --> B["deleteSelected()"]
  B --> C["documentIds = selection.selected.map(doc => doc.id)"]
  C --> D["DocumentService.deleteDocuments(documentIds)"]
  D --> E["loadInvoices() po sukcesie"]
  D --> F["console.error(...) przy błędzie"]
```

Metoda nie wykonuje lokalnej walidacji liczby zaznaczonych dokumentów. Po sukcesie lista jest pobierana ponownie przez `loadInvoices()`.

---

## 8. Przepływ transformacji do storna

```mermaid
flowchart TD
  A["Kliknięcie Transform to storno"] --> B["transformToStorno()"]
  B --> C["documentIds = selection.selected.map(doc => doc.id)"]
  C --> D["DocumentService.transformToStorno(documentIds)"]
  D --> E["loadInvoices() po sukcesie"]
  D --> F["console.error(...) przy błędzie"]
```

Metoda nie wykonuje lokalnej walidacji liczby zaznaczonych dokumentów. Po sukcesie lista jest pobierana ponownie przez `loadInvoices()`.

---

## 9. Obsługa sukcesu i błędów

Sukces pobrania danych jest obsługiwany przez przypisanie odpowiedzi do `dataSource.data` i `invoices`.

Sukces usunięcia i transformacji powoduje ponowne wywołanie `loadInvoices()`. Komponent nie pokazuje lokalnego komunikatu sukcesu.

Błędy lokalne w `deleteSelected()` i `transformToStorno()` są zapisywane przez `console.error(...)`.

Błędy HTTP są obsługiwane przez interceptory:

- `AuthInterceptor` obsługuje status `401` przekierowaniem do `/login`.
- `ErrorInterceptor` wyświetla komunikaty błędów przez `ToastrService.error(...)`.

---

## 10. Ograniczenia opisu

- Dokument nie opisuje formularza dodawania ani edycji faktury. Ten zakres jest opisany w dokumentacji `E-02_InvoiceDetails`.
- Dokument nie opisuje sposobu transformacji do storna po stronie API.
- Dokument nie opisuje sposobu usuwania dokumentów po stronie API.
