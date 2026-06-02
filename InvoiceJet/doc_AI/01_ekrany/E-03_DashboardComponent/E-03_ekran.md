# E-03 DashboardComponent — Ekran startowy

| Pole | Wartość |
|---|---|
| ID dokumentu | E-03 |
| Typ dokumentu | ekran |
| Wersja | 1.0 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 |
| Data ostatniej modyfikacji | 2026-06-02 |

## Streszczenie

Główny ekran aplikacji po zalogowaniu. Wyświetla statystyki firmy (liczniki dokumentów, klientów, produktów, kont bankowych) oraz interaktywny wykres liniowy miesięcznych przychodów dla wybranego roku i typu dokumentu. Wszystkie dane izolowane per UserFirm — użytkownik widzi wyłącznie dane swojej firmy. Chroniony przez `AuthGuard` — dostępny wyłącznie dla zalogowanych użytkowników.

---

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

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard` |
| Wymagana rola | User (AuthGuard JWT) |
| Punkty wejścia | Bezpośredni URL; przekierowanie po logowaniu z [E-01](../E-01_LoginComponent/E-01_ekran.md); przekierowanie po rejestracji z [E-02](../E-02_RegisterComponent/E-02_ekran.md); klik „Dashboard" w Sidebar |
| Komponent Angular | [`DashboardComponent`](../../../../InvoiceJetUI/src/app/components/dashboard/dashboard.component.ts) |
| Szablon HTML | [`dashboard.component.html`](../../../../InvoiceJetUI/src/app/components/dashboard/dashboard.component.html) |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek | Uprawnienie |
|---|---|---|---|
| [E-04 Dane firmy](../E-04_FirmDetailsComponent/E-04_ekran.md) | Klik „Dane firmy" w Sidebar | zawsze | User |
| [E-05 Klienci](../E-05_ClientsComponent/E-05_ekran.md) | Klik „Klienci" w Sidebar | zawsze | User |
| [E-06 Konta bankowe](../E-06_BankAccountsComponent/E-06_ekran.md) | Klik „Konta bankowe" w Sidebar | zawsze | User |
| [E-07 Produkty](../E-07_ProductsComponent/E-07_ekran.md) | Klik „Produkty" w Sidebar | zawsze | User |
| [E-08 Serie dokumentów](../E-08_DocumentSeriesComponent/E-08_ekran.md) | Klik „Serie dokumentów" w Sidebar | zawsze | User |
| [E-09 Faktury](../E-09_InvoicesComponent/E-09_ekran.md) | Klik „Faktury" w Sidebar | zawsze | User |
| [E-01 Login](../E-01_LoginComponent/E-01_ekran.md) | Klik „Wyloguj" w Navbar | zawsze | Brak |

---

## Filtry

| ID | Nazwa w UI | Typ | Dokument |
|---|---|---|---|
| FILTR-E03-01 | Rok | mat-select (liczba, ostatnie 10 lat) | [E-03_FILTR-01.md](E-03_FILTR-01.md) |
| FILTR-E03-02 | Typ dokumentu | mat-select (Factura/Proforma/Storno) | [E-03_FILTR-02.md](E-03_FILTR-02.md) |

## Tabele i listy

Brak (dashboard zawiera liczniki i wykres, nie tabelę).

## Operacje

| ID | Etykieta UI | Dokument |
|---|---|---|
| OP-E03-01 | Zmiana roku (mat-select) | [E-03_OP-01.md](E-03_OP-01.md) |
| OP-E03-02 | Zmiana typu dokumentu (mat-select) | [E-03_OP-02.md](E-03_OP-02.md) |

## Modale

Brak.

## Scenariusze testowe

→ [E-03_TC.md](E-03_TC.md) — prereq JWT, prereq DB, selektory CSS, 3 scenariusze e2e

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint |
|---|---|---|
| Załadowanie danych (ngOnInit + zmiany filtrów) | GET | `/api/Document/GetDashboardStats/{year}/{documentType}` |

---

## Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| Liczniki (TotalDocuments, TotalClients, TotalProducts, TotalBankAccounts) | [ALG-10 Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Statystyki dotyczą wyłącznie danych przypisanych do UserFirm aktualnie zalogowanego użytkownika |
| Wykres liniowy (invoiceAmount, incomeAmount) | [ALG-10 Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Miesięczne przychody obliczane wyłącznie dla dokumentów UserFirm zalogowanego użytkownika |
| OP-E03-02 | [ALG-10 Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Filtrowanie po typie dokumentu nadal zwraca dane izolowane do UserFirm |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`dashboard.component.ts`](../../../../InvoiceJetUI/src/app/components/dashboard/dashboard.component.ts) |
| Szablon HTML | [`dashboard.component.html`](../../../../InvoiceJetUI/src/app/components/dashboard/dashboard.component.html) |

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

## Elementy UI

| Element | Opis |
|---|---|
| Selektor roku | `mat-select` — ostatnie 10 lat; domyślnie bieżący rok |
| Selektor typu dokumentu | `mat-select` — `Factura` (1), `Factura Proforma` (2), `Factura Storno` (3) |
| Licznik dokumentów | `TotalDocuments` z API |
| Licznik klientów | `TotalClients` z API |
| Licznik produktów | `TotalProducts` z API |
| Licznik kont bankowych | `TotalBankAccounts` z API |
| Wykres liniowy | ng2-charts `line` — 12 miesięcy, 2 serie: `invoiceAmount` + `incomeAmount` |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| DA-01 | `console.log(invoiceAmounts)` i `console.log(incomeAmounts)` aktywne w `updateChartData()` w kodzie produkcyjnym |
| DA-02 | `monthlyTotals` zwracany przez API tylko dla miesięcy z dokumentami — wykres może mieć nieciągłości |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
