# Dashboard — Logika frontendowa

---

## 1. Zakres dokumentu

Dokument opisuje logikę wykonywaną przez frontend ekranu Dashboard. Dokument nie opisuje implementacji backendu, reguł bazy danych ani wewnętrznego przetwarzania po stronie API.

---

## 2. Inicjalizacja ekranu

### 2.1 Przepływ inicjalizacji

```mermaid
flowchart TD
  A["Wejście na /dashboard"] --> B["AuthGuard.canActivate()"]
  B --> C{"AuthService.isLoggedIn()"}
  C -->|true| D["DashboardComponent.ngOnInit()"]
  C -->|false| E["AuthService.logout() i router.navigate('/login')"]
  D --> F["getDashboardData()"]
  F --> G["DocumentService.getDashboardData(selectedYear, selectedDocumentType)"]
  G --> H["dashboardStats = data"]
  H --> I["updateChartData(data.monthlyTotals)"]
  I --> J["lineChartData = serie wykresu"]
```

### 2.2 Opis przepływu

`DashboardComponent` inicjalizuje `selectedYear` aktualnym rokiem, a `selectedDocumentType` wartością `1`. Metoda `ngOnInit()` wywołuje `getDashboardData()`.

Po otrzymaniu odpowiedzi `IDashboardStats` komponent przypisuje dane do `dashboardStats` i aktualizuje wykres przez `updateChartData(...)`.

---

## 3. Przepływ zmiany filtrów

### 3.1 Zmiana roku

Lista `Year` ma binding `[(value)]="selectedYear"`. Zmiana wyboru wywołuje `onSelectionChange()`, a ta metoda wywołuje `getDashboardData()`.

### 3.2 Zmiana typu dokumentu

Lista `Document Type` ma binding `[(value)]="selectedDocumentType"`. Zmiana wyboru wywołuje `onSelectionChange()`, a ta metoda wywołuje `getDashboardData()`.

### 3.3 Wywołanie API

`getDashboardData()` przekazuje aktualne wartości `selectedYear` i `selectedDocumentType` do `DocumentService.getDashboardData(year, documentType)`.

---

## 4. Przepływ przygotowania wykresu

```mermaid
flowchart TD
  A["monthlyTotals"] --> B["invoiceAmounts = Array(12).fill(0)"]
  A --> C["incomeAmounts = Array(12).fill(0)"]
  B --> D["Pętla po monthlyTotals"]
  C --> D
  D --> E["index = month - 1"]
  E --> F["invoiceAmounts[index] = invoiceAmount"]
  E --> G["incomeAmounts[index] = incomeAmount"]
  F --> H["lineChartData"]
  G --> H["lineChartData"]
```

`updateChartData(monthlyTotals)` przygotowuje dwie serie danych. Miesiące bez rekordu z API pozostają z wartością `0`.

---

## 5. Reguły wartości domyślnych

| Element | Wartość domyślna | Źródło |
|---|---|---|
| `selectedYear` | Aktualny rok | `new Date().getFullYear()` |
| `selectedDocumentType` | `1` | Inicjalizacja pola klasy |
| `dashboardStats.totalDocuments` | `0` | Inicjalizacja pola klasy |
| `dashboardStats.totalClients` | `0` | Inicjalizacja pola klasy |
| `dashboardStats.totalProducts` | `0` | Inicjalizacja pola klasy |
| `dashboardStats.totalBankAccounts` | `0` | Inicjalizacja pola klasy |
| `dashboardStats.monthlyTotals` | `[]` | Inicjalizacja pola klasy |

---

## 6. Reguły typów dokumentów

Lista typów dokumentów jest zdefiniowana lokalnie w komponencie:

| Id | Nazwa |
|---|---|
| `1` | `Factura` |
| `2` | `Factura Proforma` |
| `3` | `Factura Storno` |

Wybór wartości wpływa na parametr `documentType` w wywołaniu `DocumentService.getDashboardData(...)`.

---

## 7. Obsługa sukcesu i błędów

Sukces pobrania danych jest obsługiwany przez przypisanie odpowiedzi do `dashboardStats` i aktualizację `lineChartData`.

Błędy HTTP są obsługiwane przez interceptory:

- `AuthInterceptor` obsługuje status `401` przekierowaniem do `/login`.
- `ErrorInterceptor` wyświetla komunikaty błędów przez `ToastrService.error(...)`.

---

## 8. Ograniczenia opisu

- Dokument nie opisuje sposobu wyliczania statystyk po stronie API.
- Dokument nie opisuje definicji biznesowej kwot `invoiceAmount` i `incomeAmount`.
- Dokument nie opisuje implementacji biblioteki Chart.js poza konfiguracją widoczną w komponencie.
