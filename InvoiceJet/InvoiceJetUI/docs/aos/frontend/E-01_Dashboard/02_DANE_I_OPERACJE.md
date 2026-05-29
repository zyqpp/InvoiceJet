# Dashboard — Dane i Operacje

---

## Zrzut ekranu

![Ekran Dashboard](screenshot.png)

---

## 1. Zakres danych widocznych na ekranie

Ekran prezentuje dane zbiorcze z obiektu `dashboardStats`. Dane wykresu powstają z tablicy `monthlyTotals` zwracanej przez `DocumentService.getDashboardData(...)`.

---

## 2. Karty statystyk

| # | Karta | Ikona | Pole modelu | Typ wartości | Opis |
|---|---|---|---|---|---|
| 1 | `Clients` | `person` | `dashboardStats.totalClients` | liczba | Liczba klientów. |
| 2 | `Bank Accounts` | `account_balance` | `dashboardStats.totalBankAccounts` | liczba | Liczba kont bankowych. |
| 3 | `Documents` | `description` | `dashboardStats.totalDocuments` | liczba | Liczba dokumentów. |
| 4 | `Products` | `inventory` | `dashboardStats.totalProducts` | liczba | Liczba produktów. |

---

## 3. Kontrolki Overview

### 3.1 Pole Year

| Atrybut | Wartość |
|---|---|
| **Nazwa elementu** | Pole Year |
| **Typ elementu** | `mat-select` |
| **Binding** | `[(value)]="selectedYear"` |
| **Event** | `(selectionChange)="onSelectionChange()"` |
| **Wartość domyślna** | `new Date().getFullYear()` |
| **Dozwolone wartości** | Tablica `years` z 10 lat: rok bieżący i 9 poprzednich. |

### 3.2 Pole Document Type

| Atrybut | Wartość |
|---|---|
| **Nazwa elementu** | Pole Document Type |
| **Typ elementu** | `mat-select` |
| **Binding** | `[(value)]="selectedDocumentType"` |
| **Event** | `(selectionChange)="onSelectionChange()"` |
| **Wartość domyślna** | `1` |
| **Dozwolone wartości** | `1` — `Factura`; `2` — `Factura Proforma`; `3` — `Factura Storno`. |

---

## 4. Wykres

### 4.1 Konfiguracja wykresu

| Atrybut | Wartość |
|---|---|
| **Komponent** | `canvas baseChart` |
| **Typ wykresu** | `line` |
| **Dane** | `lineChartData` |
| **Etykiety osi X** | `lineChartLabels` |
| **Opcje** | `lineChartOptions` |
| **Legenda** | `lineChartLegend = true` |
| **Responsywność** | `responsive: true` |
| **Zachowanie proporcji** | `maintainAspectRatio: false` |
| **Osie Y** | `y` po lewej stronie i `y1` po prawej stronie. |

### 4.2 Serie danych

| # | Seria | Źródło | Oś Y | Opis |
|---|---|---|---|---|
| 1 | `Invoice Amount` | `monthlyTotals[n].invoiceAmount` | `y` | Kwota faktur dla miesiąca. |
| 2 | `Income Amount` | `monthlyTotals[n].incomeAmount` | `y1` | Kwota przychodu dla miesiąca. |

### 4.3 Mapowanie miesięcy

`updateChartData(monthlyTotals)` tworzy dwie tablice o długości `12`. Każda pozycja początkowo ma wartość `0`.

| Pole `IMonthlyTotal` | Transformacja | Wynik |
|---|---|---|
| `month` | `const index = total.month - 1` | Indeks tablicy od `0` do `11`. |
| `invoiceAmount` | `invoiceAmounts[index] = total.invoiceAmount` | Seria `Invoice Amount`. |
| `incomeAmount` | `incomeAmounts[index] = total.incomeAmount` | Seria `Income Amount`. |

---

## 5. Operacje ekranu

### 5.1 Tabela operacji

| # | Nazwa operacji | Typ elementu | Lokalizacja | Event | Handler | Warunek aktywności |
|---|---|---|---|---|---|---|
| 1 | Pobranie statystyk | N/D | Inicjalizacja komponentu | `ngOnInit()` | `getDashboardData()` | Wejście na ekran. |
| 2 | Zmiana roku | `mat-select` | Sekcja Overview | `(selectionChange)` | `onSelectionChange()` | Lista Year jest aktywna. |
| 3 | Zmiana typu dokumentu | `mat-select` | Sekcja Overview | `(selectionChange)` | `onSelectionChange()` | Lista Document Type jest aktywna. |
| 4 | Aktualizacja wykresu | N/D | Komponent TS | Wywołanie po odpowiedzi API | `updateChartData(monthlyTotals)` | Odpowiedź API zawiera `monthlyTotals`. |

### 5.2 Szczegóły operacji HTTP wywoływanych z frontendu

| Operacja | Metoda serwisu | Wywołanie HTTP z `DocumentService` | Typ danych |
|---|---|---|---|
| Pobranie statystyk dashboardu | `getDashboardData(year, documentType)` | `GET {apiUrl}/Document/GetDashboardStats/{year}/{documentType}` | `IDashboardStats` |

> Tabela opisuje wyłącznie wywołania wykonywane z poziomu frontendu. Nie opisuje implementacji endpointu.

---

## 6. Komunikaty i obsługa błędów

### 6.1 Komunikaty sukcesu

Ekran Dashboard nie wyświetla lokalnego komunikatu sukcesu po pobraniu statystyk.

### 6.2 Walidacje

Ekran Dashboard nie zawiera formularza reaktywnego i nie posiada walidatorów pól.

### 6.3 Obsługa błędów HTTP

| Źródło | Zachowanie frontendowe |
|---|---|
| `AuthInterceptor` dla statusu `401` | Przekierowuje do `/login` i wywołuje `AuthService.logout()`. |
| `ErrorInterceptor` dla statusu `400` | Wyświetla `ToastrService.error(message, "Error")`. |
| `ErrorInterceptor` dla statusu `401` | Wyświetla `ToastrService.error("Session has expired", "Unauthorized")`. |
| `ErrorInterceptor` dla statusu `404` | Wyświetla `ToastrService.error(message, "Not Found")`. |
| `ErrorInterceptor` dla statusu `500` | Wyświetla `ToastrService.error(message, "Error")`. |

---

## 7. Zależności techniczne ekranu

| Typ | Nazwa | Plik |
|---|---|---|
| Komponent | `DashboardComponent` | `src/app/components/dashboard/dashboard.component.ts` |
| Serwis | `DocumentService` | `src/app/services/document.service.ts` |
| Model danych | `IDashboardStats` | `src/app/models/IDashboardStats.ts` |
| Model danych | `IMonthlyTotal` | `src/app/models/IMonthlyTotal.ts` |
| Biblioteka | `ng2-charts` | `package.json` |
| Biblioteka | `chart.js` | `package.json` |
| Guard | `AuthGuard` | `src/app/guards/auth.guard.ts` |
| Interceptor | `AuthInterceptor` | `src/app/services/interceptor/auth.interceptor.ts` |
| Interceptor | `ErrorInterceptor` | `src/app/services/interceptor/error.interceptor.ts` |

---

## 8. Znane uwagi wynikające z kodu

- `IDashboardStats.monthlyTotals` jest oznaczone jako opcjonalne, ale `getDashboardData()` przekazuje `data.monthlyTotals` bez sprawdzenia do `updateChartData(...)`.
- `updateChartData(monthlyTotals)` wywołuje `monthlyTotals.forEach(...)`. Brak tablicy `monthlyTotals` w odpowiedzi API zakończy działanie metody błędem.
- `updateChartData(...)` wykonuje `console.log(invoiceAmounts)` i `console.log(incomeAmounts)`.
- Ekran nie pokazuje lokalnego stanu ładowania danych.
