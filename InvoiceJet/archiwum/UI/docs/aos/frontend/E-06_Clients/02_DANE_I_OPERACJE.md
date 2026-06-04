# Clients — Dane i Operacje

---

## Zrzut ekranu

![Ekran Clients](screenshot.png)

---

## 1. Zakres danych widocznych na ekranie

Ekran prezentuje listę klientów w gridzie Angular Material. Dane gridu pochodzą ze zmiennej `dataSource`, której typ to `MatTableDataSource<IFirm>`.

Dialog Dodawanie/Edycja klienta prezentuje formularz reaktywny `firmDetailsForm`. Formularz obsługuje dane klienta w modelu `IFirm`.

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
| **Walidatory** | Brak |
| **Wartość domyślna** | Pusty tekst |

### 2.2 Przycisk Clear

| Atrybut | Wartość |
|---|---|
| **Nazwa elementu** | Przycisk Clear |
| **Typ elementu** | `button mat-icon-button` |
| **Widoczność** | Przycisk jest widoczny wyłącznie gdy `searchInput.value` nie jest puste. |
| **Ikona** | `clear` |
| **Event** | `(click)="clearSearch(searchInput)"` |
| **Handler** | `clearSearch(input: HTMLInputElement)` |
| **Skutek** | Czyści wartość pola Search, ustawia `dataSource.filter` na pusty tekst i resetuje paginator do pierwszej strony. |

---

## 3. Grid klientów

### 3.1 Opis gridu

| Atrybut | Wartość |
|---|---|
| **Komponent Angular** | `table mat-table` |
| **Źródło danych** | `dataSource` |
| **Typ źródła danych** | `MatTableDataSource<IFirm>` |
| **Zmienna pomocnicza** | `firms: IFirm[]` |
| **Kolumny** | `displayedColumns` |
| **Sortowanie** | Tak, przez `matSort` i `MatSort`. |
| **Paginacja** | Tak, przez `mat-paginator` i `MatPaginator`. |
| **Zaznaczanie wierszy** | Tak, przez `SelectionModel<IFirm>(true, [])`. |
| **Kliknięcie wiersza** | Otwiera dialog Edycja klienta przez `openEditClientDialog(row)`. |
| **Klasa CSS** | `mat-elevation-z2` |

### 3.2 Definicja kolumn

| # | `matColumnDef` | Nagłówek | Zawartość komórki | Typ | Sortowalna | Uwagi |
|---|---|---|---|---|---|---|
| 1 | `select` | Checkbox | `mat-checkbox` dla zaznaczenia wiersza | pole wyboru | Nie | Checkbox nagłówka obsługuje zaznaczanie wszystkich wierszy. |
| 2 | `name` | `Name` | `{{ element.name }}` | tekst | Tak | Kolumna sortowana przez `mat-sort-header`. |
| 3 | `cui` | `CUI` | `{{ element.cui }}` | tekst | Tak | Kolumna sortowana przez `mat-sort-header`. |
| 4 | `regCom` | `RegCom` | `{{ element.regCom }}` | tekst | Tak | Pole `regCom` jest opcjonalne w modelu `IFirm`. |
| 5 | `address` | `Address` | `{{ element.address }}` | tekst | Tak | Kolumna sortowana przez `mat-sort-header`. |
| 6 | `county` | `County` | `{{ element.county }}` | tekst | Tak | Kolumna sortowana przez `mat-sort-header`. |
| 7 | `city` | `City` | `{{ element.city }}` | tekst | Tak | Kolumna sortowana przez `mat-sort-header`. |

### 3.3 Paginacja

| Atrybut | Wartość |
|---|---|
| **Komponent** | `mat-paginator` |
| **Opcje rozmiaru strony** | `[10, 20, 30]` |
| **Przyciski pierwszej i ostatniej strony** | Tak, `showFirstLastButtons`. |
| **Powiązanie z gridem** | `this.dataSource.paginator = this.paginator` w `ngAfterViewInit()`. |
| **Typ paginacji** | Frontendowa paginacja danych znajdujących się w `MatTableDataSource`. |

### 3.4 Sortowanie

| Atrybut | Wartość |
|---|---|
| **Komponent** | `matSort` |
| **Powiązanie z gridem** | `this.dataSource.sort = this.sort` w `ngAfterViewInit()`. |
| **Handler zmiany sortowania** | `announceSortChange(sortState: any)` |
| **Komunikat dostępności** | `LiveAnnouncer.announce(...)` |
| **Opis sortowania** | Każda kolumna tekstowa posiada `mat-sort-header` i `sortActionDescription`. |

### 3.5 Zaznaczanie wierszy

| Atrybut | Wartość |
|---|---|
| **Model zaznaczenia** | `selection = new SelectionModel<IFirm>(true, [])` |
| **Zaznaczanie wielu wierszy** | Tak |
| **Checkbox nagłówka** | Wywołuje `masterToggle()`. |
| **Checkbox wiersza** | Wywołuje `selection.toggle(row)`. |
| **Zatrzymanie propagacji** | Checkbox wiersza używa `(click)="$event.stopPropagation()"`, aby kliknięcie checkboxa nie otwierało dialogu edycji. |
| **Sprawdzenie pełnego zaznaczenia** | `isAllSelected()` porównuje liczbę zaznaczonych wierszy z liczbą wierszy w `dataSource.data`. |

---

## 4. Dialog Dodawanie/Edycja klienta

### 4.1 Metadane dialogu

| Atrybut | Wartość |
|---|---|
| **Komponent** | `AddEditClientDialogComponent` |
| **Plik komponentu** | `src/app/components/firm/add-edit-client-dialog/add-edit-client-dialog.component.ts` |
| **Plik szablonu** | `src/app/components/firm/add-edit-client-dialog/add-edit-client-dialog.component.html` |
| **Formularz** | `firmDetailsForm: FormGroup` |
| **Tryb dodawania** | Dialog otwierany przez `openNewClientDialog()` bez danych wejściowych. |
| **Tryb edycji** | Dialog otwierany przez `openEditClientDialog(firm)` z obiektem `IFirm`. |
| **Blokada zamknięcia poza dialogiem** | Tylko tryb edycji: `disableClose: true`. |
| **Szerokość wizualna** | `550px` w `.dialog-container`. |
| **Pozycja wizualna** | Panel stały po prawej stronie ekranu. |

### 4.2 Pola formularza dialogu

| # | Nazwa pola | Etykieta UI | Typ elementu | `formControlName` | Wymagane | Walidatory | Komunikat błędu |
|---|---|---|---|---|---|---|---|
| 1 | Pole Nazwa firmy | `Firm Name` | `input matInput` | `firmName` | Tak | `Validators.required` | `Firm Name is required` |
| 2 | Pole CUI | `CUI Value` | `input matInput` z przyciskiem `cloud_download` | `cuiValue` | Tak | `Validators.required` | `CUI Value is required` |
| 3 | Pole RegCom | `Registration Number (RegCom)` | `input matInput` | `regCom` | Tak | `Validators.required` | `Registration Number is required` |
| 4 | Pole Adres | `Address` | `input matInput` | `address` | Tak | `Validators.required` | `Address is required` |
| 5 | Pole County | `County` | `input matInput` | `county` | Tak | `Validators.required` | `County is required` |
| 6 | Pole City | `City` | `input matInput` | `city` | Tak | `Validators.required` | `City is required` |

### 4.3 Wartości początkowe formularza

| Tryb | Wartości początkowe |
|---|---|
| Dodawanie klienta | Każde pole inicjalizowane jest pustym tekstem `""`. |
| Edycja klienta | `ngOnInit()` ustawia wartości formularza na podstawie `data: IFirm`. Brakujące wartości są zastępowane pustym tekstem. |

### 4.4 Mapowanie formularza do modelu `IFirm`

| Pole formularza | Pole w modelu `IFirm` | Uwagi |
|---|---|---|
| `firmName` | `name` | Wartość pola Nazwa firmy. |
| `cuiValue` | `cui` | Wartość pola CUI. |
| `regCom` | `regCom` | Wartość pola RegCom. |
| `address` | `address` | Wartość pola Adres. |
| `county` | `county` | Wartość pola County. |
| `city` | `city` | Wartość pola City. |
| `data?.id ?? 0` | `id` | W trybie edycji używany jest identyfikator przekazany do dialogu. W trybie dodawania używane jest `0`. |

---

## 5. Operacje ekranu

### 5.1 Tabela operacji

| # | Nazwa operacji | Typ elementu | Lokalizacja | Event | Handler | Warunek aktywności |
|---|---|---|---|---|---|---|
| 1 | Dodawanie klienta | `button mat-raised-button` | Pasek tytułu | `(click)` | `openNewClientDialog()` | Zawsze aktywna. |
| 2 | Edycja klienta | `tr mat-row` | Wiersz gridu | `(click)` | `openEditClientDialog(row)` | Aktywna dla każdego wiersza. |
| 3 | Filtrowanie klientów | `input matInput` | Sekcja Search | `(keyup)` | `applyFilter($event)` | Aktywna gdy ekran jest załadowany. |
| 4 | Czyszczenie filtra | `button mat-icon-button` | Pole Search | `(click)` | `clearSearch(searchInput)` | Widoczna gdy pole Search ma wartość. |
| 5 | Zaznaczanie wszystkich wierszy | `mat-checkbox` | Nagłówek gridu | `(change)` | `masterToggle()` | Aktywna gdy grid jest wyrenderowany. |
| 6 | Zaznaczanie wiersza | `mat-checkbox` | Wiersz gridu | `(change)` | `selection.toggle(row)` | Aktywna dla każdego wiersza. |
| 7 | Usuwanie zaznaczonych | `button mat-menu-item` | Menu kontekstowe | `(click)` | `deleteSelected()` | Operacja wykonuje żądanie tylko gdy `selection.selected.length > 0`. |
| 8 | Pobieranie danych z ANAF | `button mat-icon-button` | Dialog, pole CUI | `(click)` | `onCloudIconClick()` | Aktywna niezależnie od walidacji pola CUI. |
| 9 | Zapis formularza klienta | `button mat-raised-button` | Dialog | `(ngSubmit)` | `onSubmit()` | Wykonuje zapis tylko gdy `firmDetailsForm.valid`. |
| 10 | Anulowanie edycji | `button mat-stroked-button` | Dialog | `(click)` | `closeDialog()` | Widoczne tylko w trybie edycji. |

### 5.2 Szczegóły operacji HTTP wywoływanych z frontendu

| Operacja | Metoda serwisu | Wywołanie HTTP z `FirmService` | Typ danych |
|---|---|---|---|
| Pobranie klientów | `getUserClientFirms()` | `GET {apiUrl}/Firm/GetUserClientFirms/` | `IFirm[]` |
| Dodanie klienta | `addFirm(firm, true)` | `POST {apiUrl}/Firm/AddFirm/true` | `IFirm` |
| Edycja klienta | `editFirm(firm, true)` | `PUT {apiUrl}/Firm/EditFirm/true` | `IFirm` |
| Usunięcie zaznaczonych | `deleteFirms(firmIds)` | `PUT {apiUrl}/Firm/DeleteFirms/` | `number[]` |
| Pobranie danych z ANAF | `getFirmFromAnaf(cuiValue)` | `GET {apiUrl}/Firm/fromAnaf/{cuiValue}` | `IFirm` |

> Tabela opisuje wyłącznie wywołania wykonywane z poziomu frontendu. Nie opisuje implementacji endpointów.

---

## 6. Komunikaty i obsługa błędów

### 6.1 Komunikaty sukcesu

| Operacja | Komunikat | Mechanizm |
|---|---|---|
| Dodanie klienta | `Firm added successfully` | `ToastrService.success(...)` |
| Edycja klienta | `Firm details updated successfully` | `ToastrService.success(...)` |
| Usunięcie zaznaczonych | `Firms deleted successfully` | `ToastrService.success(...)` |
| Pobranie danych z ANAF | `Firm details fetched from ANAF` | `ToastrService.success(...)` |

### 6.2 Komunikaty walidacyjne

| Pole | Warunek | Komunikat |
|---|---|---|
| `firmName` | `required` | `Firm Name is required` |
| `cuiValue` | `required` | `CUI Value is required` |
| `regCom` | `required` | `Registration Number is required` |
| `address` | `required` | `Address is required` |
| `county` | `required` | `County is required` |
| `city` | `required` | `City is required` |

### 6.3 Obsługa błędów HTTP

| Źródło | Zachowanie frontendowe |
|---|---|
| `AuthInterceptor` dla statusu `401` | Przekierowuje do `/login` i wywołuje `AuthService.logout()`. |
| `ErrorInterceptor` dla statusu `400` | Wyświetla `ToastrService.error(message, "Error")`. |
| `ErrorInterceptor` dla statusu `401` | Wyświetla `ToastrService.error("Session has expired", "Unauthorized")`. |
| `ErrorInterceptor` dla statusu `404` | Wyświetla `ToastrService.error(message, "Not Found")`. |
| `ErrorInterceptor` dla statusu `500` | Wyświetla `ToastrService.error(message, "Error")`. |
| `ErrorInterceptor` dla innych statusów | Wyświetla `ToastrService.error("An unexpected error has occurred.", "Unexpected Error")`. |

---

## 7. Zależności techniczne ekranu

| Typ | Nazwa | Plik |
|---|---|---|
| Komponent | `ClientsComponent` | `src/app/components/firm/clients/clients.component.ts` |
| Dialog | `AddEditClientDialogComponent` | `src/app/components/firm/add-edit-client-dialog/add-edit-client-dialog.component.ts` |
| Serwis | `FirmService` | `src/app/services/firm.service.ts` |
| Model danych | `IFirm` | `src/app/models/IFirm.ts` |
| Guard | `AuthGuard` | `src/app/guards/auth.guard.ts` |
| Interceptor | `AuthInterceptor` | `src/app/services/interceptor/auth.interceptor.ts` |
| Interceptor | `ErrorInterceptor` | `src/app/services/interceptor/error.interceptor.ts` |

---

## 8. Znane uwagi wynikające z kodu

- `mat-progress-bar` jest widoczny tylko gdy `!firms`. Zmienna `firms` jest inicjalizowana jako pusta tablica, dlatego warunek jest fałszywy od początku działania komponentu.
- `deleteSelected()` nie wyświetla komunikatu, gdy nie zaznaczono żadnego wiersza.
- `onCloudIconClick()` nie sprawdza, czy pole `cuiValue` zawiera wartość przed wywołaniem serwisu.
- `onSubmit()` posiada gałąź `else` ustawiającą `errorMessage`, ale wcześniejszy warunek `if (this.firmDetailsForm.invalid) { return; }` powoduje, że ta gałąź nie zostanie wykonana dla niepoprawnego formularza.
