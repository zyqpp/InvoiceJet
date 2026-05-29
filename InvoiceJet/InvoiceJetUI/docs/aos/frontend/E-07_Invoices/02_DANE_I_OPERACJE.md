# Invoices — Dane i Operacje

---

## Zrzut ekranu

![Ekran Invoices](screenshot.png)

---

## 1. Zakres danych widocznych na ekranie

Ekran prezentuje listę faktur w gridzie Angular Material. Dane gridu pochodzą ze zmiennej `dataSource`, której typ to `MatTableDataSource<IDocumentTableRecord>`.

Ekran nie zawiera formularza edycji. Dodawanie i edycja faktury są realizowane przez nawigację do ekranów powiązanych z komponentem `AddOrEditInvoiceComponent`.

---

## 2. Sekcja filtrów

### 2.1 Pole Search

| Atrybut | Wartość |
|---|---|
| **Nazwa elementu** | Pole Search |
| **Typ elementu** | `input matInput` w `mat-form-field` |
| **Etykieta** | `Search` |
| **Tekst podpowiedzi** | `Search` |
| **Binding** | Brak `formControlName`; wartość odczytywana ze zdarzenia DOM. |
| **Event** | `(keyup)="applyFilter($event)"` |
| **Handler** | `applyFilter(event: Event)` |
| **Mechanizm filtrowania** | `this.dataSource.filter = filterValue.trim().toLowerCase()` |
| **Skutek dodatkowy** | Jeżeli istnieje paginator, wykonywane jest `this.dataSource.paginator.firstPage()`. |

### 2.2 Przycisk Clear

| Atrybut | Wartość |
|---|---|
| **Typ elementu** | `button mat-icon-button` |
| **Widoczność** | Przycisk jest widoczny wyłącznie gdy `searchInput.value` nie jest puste. |
| **Ikona** | `clear` |
| **Event** | `(click)="clearSearch(searchInput)"` |
| **Skutek** | Czyści wartość pola Search, ustawia `dataSource.filter` na pusty tekst i resetuje paginator do pierwszej strony wyników. |

---

## 3. Grid faktur

### 3.1 Opis gridu

| Atrybut | Wartość |
|---|---|
| **Komponent Angular** | `table mat-table` |
| **Źródło danych** | `dataSource` |
| **Typ źródła danych** | `MatTableDataSource<IDocumentTableRecord>` |
| **Zmienna pomocnicza** | `invoices: IDocumentTableRecord[]` |
| **Kolumny** | `displayedColumns` |
| **Sortowanie** | Tak, przez `matSort` i `MatSort`. |
| **Paginacja** | Tak, przez `mat-paginator` i `MatPaginator`. |
| **Zaznaczanie wierszy** | Tak, przez `SelectionModel<IDocumentTableRecord>(true, [])`. |
| **Kliknięcie wiersza** | Nawiguje do edycji przez `openEditInvoiceDialog(row)`. |

### 3.2 Definicja kolumn

| # | `matColumnDef` | Nagłówek | Zawartość komórki | Typ | Sortowalna | Uwagi |
|---|---|---|---|---|---|---|
| 1 | `select` | Checkbox | `mat-checkbox` dla zaznaczenia wiersza | pole wyboru | Nie | Checkbox nagłówka obsługuje zaznaczanie wszystkich wierszy. |
| 2 | `documentNumber` | `Document Number` | `{{ record.documentNumber }}` | tekst | Tak | Numer dokumentu. |
| 3 | `clientName` | `Client Name` | `{{ record.clientName }}` | tekst | Tak | Nazwa klienta. |
| 4 | `issueDate` | `Issue Date` | `{{ record.issueDate | date : "mediumDate" }}` | data | Tak | Data wystawienia. |
| 5 | `dueDate` | `Due Date` | `{{ record.dueDate | date : "mediumDate" }}` | data | Tak | Termin płatności. |
| 6 | `totalValue` | `Total Value` | `{{ record.totalValue }} RON` | liczba | Tak | Wartość dokumentu z sufiksem `RON`. |
| 7 | `documentStatus` | `Status` | `mat-chip` z `record.documentStatus?.status` | status | Tak | Status renderowany jako chip. |

---

## 4. Operacje ekranu

### 4.1 Tabela operacji

| # | Nazwa operacji | Typ elementu | Lokalizacja | Event | Handler | Warunek aktywności |
|---|---|---|---|---|---|---|
| 1 | Pobranie faktur | N/D | Inicjalizacja komponentu | `ngOnInit()` | `loadInvoices()` | Wejście na ekran. |
| 2 | Nowa faktura | `button mat-raised-button` | Pasek tytułu | `(click)` | `openNewInvoiceDialog()` | Zawsze aktywna. |
| 3 | Edycja faktury | `tr mat-row` | Wiersz gridu | `(click)` | `openEditInvoiceDialog(row)` | Aktywna dla każdego wiersza. |
| 4 | Filtrowanie faktur | `input matInput` | Sekcja Search | `(keyup)` | `applyFilter($event)` | Aktywna gdy ekran jest załadowany. |
| 5 | Czyszczenie filtra | `button mat-icon-button` | Pole Search | `(click)` | `clearSearch(searchInput)` | Widoczna gdy pole Search ma wartość. |
| 6 | Zaznaczanie wszystkich wierszy | `mat-checkbox` | Nagłówek gridu | `(change)` | `masterToggle()` | Aktywna gdy grid jest wyrenderowany. |
| 7 | Zaznaczanie wiersza | `mat-checkbox` | Wiersz gridu | `(change)` | `selection.toggle(row)` | Aktywna dla każdego wiersza. |
| 8 | Transformacja do storna | `button mat-menu-item` | Menu kontekstowe | `(click)` | `transformToStorno()` | Kod wykonuje żądanie także dla pustej tablicy identyfikatorów. |
| 9 | Usuwanie zaznaczonych | `button mat-menu-item` | Menu kontekstowe | `(click)` | `deleteSelected()` | Kod wykonuje żądanie także dla pustej tablicy identyfikatorów. |

### 4.2 Nawigacje

| Operacja | Handler | Trasa docelowa | Dane przekazywane |
|---|---|---|---|
| Nowa faktura | `openNewInvoiceDialog()` | `dashboard/add-invoice` | Brak |
| Edycja faktury | `openEditInvoiceDialog(row)` | `/dashboard/edit-invoice/{row.id}` | `row.id` |

### 4.3 Szczegóły operacji HTTP wywoływanych z frontendu

| Operacja | Metoda serwisu | Wywołanie HTTP z `DocumentService` | Typ danych |
|---|---|---|---|
| Pobranie faktur | `getDocuments(1)` | `GET {apiUrl}/Document/GetDocumentTableRecords/1` | `IDocumentTableRecord[]` |
| Usunięcie zaznaczonych | `deleteDocuments(documentIds)` | `PUT {apiUrl}/Document/DeleteDocuments` | `number[]` |
| Transformacja do storna | `transformToStorno(documentIds)` | `PUT {apiUrl}/Document/TransformToStorno` | `number[]` |

---

## 5. Komunikaty i obsługa błędów

### 5.1 Komunikaty sukcesu

Ekran Invoices nie wyświetla lokalnych komunikatów sukcesu po usunięciu ani transformacji do storna.

### 5.2 Obsługa błędów lokalnych

| Źródło | Zachowanie frontendowe |
|---|---|
| `deleteSelected()` | Błąd trafia do `console.error("Error deleting documents", err)`. |
| `transformToStorno()` | Błąd trafia do `console.error("Error transforming to storno", err)`. |

### 5.3 Obsługa błędów HTTP

| Źródło | Zachowanie frontendowe |
|---|---|
| `AuthInterceptor` dla statusu `401` | Przekierowuje do `/login` i wywołuje `AuthService.logout()`. |
| `ErrorInterceptor` dla statusu `400` | Wyświetla `ToastrService.error(message, "Error")`. |
| `ErrorInterceptor` dla statusu `401` | Wyświetla `ToastrService.error("Session has expired", "Unauthorized")`. |
| `ErrorInterceptor` dla statusu `404` | Wyświetla `ToastrService.error(message, "Not Found")`. |
| `ErrorInterceptor` dla statusu `500` | Wyświetla `ToastrService.error(message, "Error")`. |

---

## 6. Zależności techniczne ekranu

| Typ | Nazwa | Plik |
|---|---|---|
| Komponent | `InvoicesComponent` | `src/app/components/invoices/invoices.component.ts` |
| Serwis | `DocumentService` | `src/app/services/document.service.ts` |
| Model danych | `IDocumentTableRecord` | `src/app/models/IDocumentTableRecord.ts` |
| Model danych | `IDocumentStatus` | `src/app/models/IDocumentStatus.ts` |
| Routing | `Router` | Angular Router |
| Guard | `AuthGuard` | `src/app/guards/auth.guard.ts` |
| Interceptor | `AuthInterceptor` | `src/app/services/interceptor/auth.interceptor.ts` |
| Interceptor | `ErrorInterceptor` | `src/app/services/interceptor/error.interceptor.ts` |

---

## 7. Znane uwagi wynikające z kodu

- `deleteSelected()` nie sprawdza liczby zaznaczonych dokumentów przed wywołaniem serwisu.
- `transformToStorno()` nie sprawdza liczby zaznaczonych dokumentów przed wywołaniem serwisu.
- `deleteSelected()` i `transformToStorno()` nie czyszczą `selection` po sukcesie.
- `loadInvoices()`, `deleteSelected()` i `transformToStorno()` wykonują `console.log(...)`.
- Ekran nie pokazuje lokalnego stanu ładowania danych.
- Ekran nie wyświetla lokalnego komunikatu sukcesu po usunięciu ani transformacji.
