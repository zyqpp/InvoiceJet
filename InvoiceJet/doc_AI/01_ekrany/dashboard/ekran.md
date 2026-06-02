# DashboardComponent — Ekran startowy

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-Dashboard |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Główny ekran aplikacji po zalogowaniu. Wyświetla statystyki firmy (liczniki dokumentów, klientów, produktów, kont bankowych) oraz interaktywny wykres liniowy miesięcznych przychodów dla wybranego roku i typu dokumentu. Chroniony przez `AuthGuard` — dostępny wyłącznie dla zalogowanych użytkowników.

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────┐
│ Rok: [2026 ▼]   Typ dokumentu: [Factura ▼]           │
├───────────┬───────────┬───────────┬──────────────────┤
│ Dokumenty │ Klienci   │ Produkty  │ Konta bankowe    │
│   [N]     │   [N]     │   [N]     │   [N]            │
├───────────┴───────────┴───────────┴──────────────────┤
│                                                      │
│   Wykres liniowy — miesięczne przychody (12 mies.)   │
│   Seria 1: invoiceAmount | Seria 2: incomeAmount     │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard` |
| Wymagana rola/uprawnienie | User (AuthGuard) |
| Punkty wejścia | Bezpośredni URL; przekierowanie po logowaniu (`/login`); przekierowanie po rejestracji (`/register`); klik „Dashboard" w sidebar |
| Powiązany kod komponentu | `src/app/components/dashboard/dashboard.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| `/dashboard/firm-details` | Klik „Dane firmy" w Sidebar | Zawsze | User |
| `/dashboard/clients` | Klik „Klienci" w Sidebar | Zawsze | User |
| `/dashboard/bank-accounts` | Klik „Konta bankowe" w Sidebar | Zawsze | User |
| `/dashboard/products` | Klik „Produkty" w Sidebar | Zawsze | User |
| `/dashboard/document-series` | Klik „Serie dokumentów" w Sidebar | Zawsze | User |
| `/dashboard/invoices` | Klik „Faktury" w Sidebar | Zawsze | User |
| `/dashboard/invoice-proformas` | Klik „Proformy" w Sidebar | Zawsze | User |
| `/dashboard/invoice-stornos` | Klik „Storna" w Sidebar | Zawsze | User |
| `/login` | Klik „Wyloguj" w Navbar | Zawsze | Brak |

## Sekcje ekranu

### Filtry

| ID filtru | Nazwa w UI | Typ | Link do dokumentu |
|---|---|---|---|
| FILTR-Dashboard-Rok | Rok | mat-select (liczba) | — |
| FILTR-Dashboard-TypDokumentu | Typ dokumentu | mat-select (enum) | — |

### Tabele i listy

Brak (dashboard zawiera liczniki i wykres, nie tabelę).

### Pola

Brak (ekran tylko do odczytu — selektory jako filtry).

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-Dashboard-ZmianaRoku | Zmiana roku (mat-select) | — |
| OP-Dashboard-ZmianaTypu | Zmiana typu dokumentu (mat-select) | [ALG-IZO Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) |

### Modale

Brak.

### Powiadomienia

Brak.

## Elementy UI — szczegóły

| Element | Opis |
|---|---|
| Selektor roku | `mat-select` — ostatnie 10 lat; domyślnie bieżący rok |
| Selektor typu dokumentu | `mat-select` — `Factura` (1), `Factura Proforma` (2), `Factura Storno` (3); domyślnie `1` |
| Licznik dokumentów | `TotalDocuments` z API |
| Licznik klientów | `TotalClients` z API |
| Licznik produktów | `TotalProducts` z API |
| Licznik kont bankowych | `TotalBankAccounts` z API |
| Wykres liniowy | ng2-charts `line` — 12 miesięcy, 2 serie: `invoiceAmount` + `incomeAmount` |

## Stan komponentu

| Pole | Typ | Wartość domyślna | Opis |
|---|---|---|---|
| `documentTypes` | `{id, name}[]` | hardcoded 3 typy | Opcje selektora typu dokumentu |
| `years` | `number[]` | ostatnie 10 lat | Opcje selektora roku |
| `selectedYear` | `number` | `new Date().getFullYear()` | Wybrany rok |
| `selectedDocumentType` | `number` | `1` | Wybrany typ dokumentu |
| `dashboardStats` | `IDashboardStats` | — | Dane statystyczne z API |
| `lineChartData` | `any[]` | — | Dane wykresu (ng2-charts) |
| `lineChartLabels` | `string[]` | 12 miesięcy ang. | Etykiety osi X wykresu |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie danych (ngOnInit + zmiany filtrów) | `GET /api/Document/GetDashboardStats/{year}/{documentType}` |

## Metody

| Metoda | Opis |
|---|---|
| `getDashboardData()` | Wywołuje API, aktualizuje `dashboardStats`, wywołuje `updateChartData()` |
| `onSelectionChange()` | Wywoływana przy zmianie selektora roku lub typu dokumentu |
| `updateChartData(monthlyTotals)` | Mapuje `monthlyTotals` na dane wykresu Chart.js |

## Powiązania

- Powiązane procesy: `../../02_procesy/dokumenty/dashboard_statystyki/proces.md`
- Powiązane API: `../../04_api_i_integracje/01_api_frontend/document/`
- Powiązane UC: Brak

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| Liczniki (TotalDocuments, TotalClients, TotalProducts, TotalBankAccounts) | [ALG-IZO Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Statystyki zwracane przez API (GET /api/Document/GetDashboardStats) dotyczą wyłącznie danych przypisanych do UserFirm aktualnie zalogowanego użytkownika |
| Wykres liniowy (invoiceAmount, incomeAmount) | [ALG-IZO Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Miesięczne przychody obliczane po stronie API wyłącznie dla dokumentów UserFirm zalogowanego użytkownika |
| OP-Dashboard-ZmianaTypu | [ALG-IZO Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Filtrowanie po typie dokumentu nadal zwraca dane izolowane do UserFirm — zmiana parametru nie przełamuje izolacji |

## Powiązania z kodem

- Komponent: `src/app/components/dashboard/dashboard.component.ts`
- Szablon HTML: `src/app/components/dashboard/dashboard.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

- DA-01: `console.log(invoiceAmounts)` i `console.log(incomeAmounts)` aktywne w `updateChartData()` w kodzie produkcyjnym.
- DA-02: `monthlyTotals` zwracany przez API tylko dla miesięcy z dokumentami — wykres pokazuje dane jedynie dla niepustych miesięcy, co może powodować nieciągłości na wykresie.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `dashboard/dashboard.md`. |
