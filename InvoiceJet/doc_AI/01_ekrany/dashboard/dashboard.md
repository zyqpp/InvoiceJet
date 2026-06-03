# Ekran: Dashboard

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-03 |
| Trasa | `/dashboard` |
| Komponent | `DashboardComponent` |
| Plik | `src/app/components/dashboard/dashboard.component.ts` |
| AuthGuard | TAK |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Ekran startowy po zalogowaniu. Wyświetla statystyki (liczniki) i wykres liniowy miesięcznych przychodów dla wybranego roku i typu dokumentu.

## Elementy UI

| Element | Opis |
|---|---|
| Selektor roku | `mat-select` — ostatnie 10 lat; domyślnie bieżący rok |
| Selektor typu dokumentu | `mat-select` — `Factura` (1), `Factura Proforma` (2), `Factura Storno` (3); domyślnie `1` |
| Licznik dokumentów | `TotalDocuments` z API |
| Licznik klientów | `TotalClients` z API |
| Licznik produktów | `TotalProducts` z API |
| Licznik kont bankowych | `TotalBankAccounts` z API |
| Wykres liniowy | ng2-charts `line` — 12 miesięcy, 2 serie: invoiceAmount + incomeAmount |

## Pola (state)

| Pole | Typ | Wartość domyślna | Opis |
|---|---|---|---|
| `documentTypes` | `{id, name}[]` | hardcoded 3 typy | Opcje selektora |
| `years` | `number[]` | ostatnie 10 lat | Opcje selektora roku |
| `selectedYear` | `number` | `new Date().getFullYear()` | Wybrany rok |
| `selectedDocumentType` | `number` | `1` | Wybrany typ |
| `dashboardStats` | `IDashboardStats` | — | Dane z API |
| `lineChartData` | `any[]` | — | Dane wykresu |
| `lineChartLabels` | `string[]` | 12 miesięcy ang. | Etykiety osi X |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie danych | `GET /api/Document/GetDashboardStats/{year}/{documentType}` |

Wywoływane w `ngOnInit()` i przy `onSelectionChange()`.

## Metody

| Metoda | Opis |
|---|---|
| `getDashboardData()` | Wywołuje API, aktualizuje `dashboardStats`, wywołuje `updateChartData()` |
| `onSelectionChange()` | Wywoływana przy zmianie selektora roku lub typu |
| `updateChartData(monthlyTotals)` | Mapuje `monthlyTotals` na dane wykresu Chart.js |

## Anomalie

| # | Anomalia |
|---|---|
| DA-01 | `console.log(invoiceAmounts)` i `console.log(incomeAmounts)` w `updateChartData()` — aktywne w produkcji |
| DA-02 | `monthlyTotals` zwracany tylko dla miesięcy z dokumentami — wykres pokazuje tylko bary dla niepustych miesięcy |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
