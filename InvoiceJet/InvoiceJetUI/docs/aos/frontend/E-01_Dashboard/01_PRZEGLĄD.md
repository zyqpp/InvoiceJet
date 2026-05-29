# Dashboard — Przegląd

---

## 1. Układ ekranu

### 1.1 Diagram struktury

```
┌──────────────────────────────────────────────────────────────────────────┐
│ [Pasek nawigacyjny — NavbarComponent]                                    │
├──────────────────┬───────────────────────────────────────────────────────┤
│ [Menu boczne]    │ Dashboard                                             │
│ Dashboard ←      ├───────────────────────────────────────────────────────┤
│ Documents        │ [Clients] [Bank Accounts] [Documents] [Products]      │
│ Inventory        ├───────────────────────────────────────────────────────┤
│ Settings         │ Overview                         [Year] [Doc. Type]   │
│                  │                                                       │
│                  │ [Wykres liniowy: Invoice Amount / Income Amount]      │
│                  │                                                       │
└──────────────────┴───────────────────────────────────────────────────────┘
```

### 1.2 Opis układu

Ekran składa się z nagłówka `Dashboard`, czterech kart statystyk i sekcji `Overview` z wykresem liniowym. Sekcja `Overview` zawiera listę rozwijaną `Year` i listę rozwijaną `Document Type`.

Karty statystyk pokazują wartości z `dashboardStats`: `totalClients`, `totalBankAccounts`, `totalDocuments` i `totalProducts`.

---

## 2. Komponenty główne

### 2.1 Sekcje UI

| Sekcja | Typ | Opis |
|---|---|---|
| Pasek tytułu | `div.app-header` | Wyświetla tytuł `Dashboard`. |
| Karty statystyk | `mat-card` | Pokazują liczby klientów, kont bankowych, dokumentów i produktów. |
| Sekcja Overview | `mat-card` | Zawiera kontrolki wyboru i wykres. |
| Kontrolka Year | `mat-select` | Wybiera rok statystyk. |
| Kontrolka Document Type | `mat-select` | Wybiera typ dokumentu dla statystyk. |
| Wykres | `canvas baseChart` | Renderuje dane `lineChartData` z etykietami miesięcy. |

### 2.2 Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Year | `mat-select` | Zmiana wartości wywołuje `onSelectionChange()`. |
| Document Type | `mat-select` | Zmiana wartości wywołuje `onSelectionChange()`. |

---

## 3. Scenariusz główny

1. Użytkownik przechodzi do ekranu `/dashboard`.
2. `AuthGuard` dopuszcza dostęp, jeżeli `AuthService.isLoggedIn()` zwraca `true`.
3. `DashboardComponent.ngOnInit()` wywołuje `getDashboardData()`.
4. `getDashboardData()` wywołuje `DocumentService.getDashboardData(selectedYear, selectedDocumentType)`.
5. Odpowiedź typu `IDashboardStats` jest przypisywana do `dashboardStats`.
6. `updateChartData(data.monthlyTotals)` przygotowuje serie wykresu.
7. Ekran renderuje karty statystyk i wykres.

---

## 4. Stany ekranu

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Stan początkowy | `dashboardStats` zawiera wartości `0` i pustą tablicę `monthlyTotals`. | Konstrukcja komponentu. |
| Dane załadowane | `dashboardStats` zawiera odpowiedź API. | Sukces `DocumentService.getDashboardData(...)`. |
| Zmiana roku | `selectedYear` zmienia wartość i wywołuje ponowne pobranie danych. | `selectionChange` w polu Year. |
| Zmiana typu dokumentu | `selectedDocumentType` zmienia wartość i wywołuje ponowne pobranie danych. | `selectionChange` w polu Document Type. |
| Wykres pusty | Serie wykresu zawierają wartości `0` dla miesięcy bez danych. | Brak pozycji dla danego miesiąca w `monthlyTotals`. |
| Błąd HTTP | Błąd przechodzi przez interceptory HTTP. | Odpowiedź HTTP 4xx lub 5xx. |

---

## 5. Dostępność i uprawnienia

| Warunek | Efekt |
|---|---|
| `AuthService.isLoggedIn()` zwraca `true` | Dostęp do ekranu jest dozwolony. |
| `AuthService.isLoggedIn()` zwraca `false` | `AuthGuard` wywołuje `AuthService.logout()` i przekierowuje do `/login`. |
| Token JWT istnieje w `localStorage` pod kluczem `authToken` | `AuthInterceptor` dodaje nagłówek `Authorization: Bearer {token}` do żądania statystyk. |

---

## 6. Notatki techniczne

- Komponent ekranu: `DashboardComponent`.
- Serwis HTTP: `DocumentService`.
- Model statystyk: `IDashboardStats`.
- Model wartości miesięcznej: `IMonthlyTotal`.
- Typ wykresu: `line`.
- Etykiety wykresu: miesiące od `January` do `December`.
- Serie wykresu: `Invoice Amount` i `Income Amount`.

---

## Następne sekcje

- Szczegółowe dane o polach, wykresie i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika frontendowa i przepływy UI: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
