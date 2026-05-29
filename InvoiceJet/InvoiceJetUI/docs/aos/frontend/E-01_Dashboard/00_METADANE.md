# Dashboard — Metadane

**Dokument:** Metadane ekranu  
**Aplikacja:** InvoiceJet  
**Moduł:** Dashboard  
**Klasyfikacja:** Standardowy  
**Data utworzenia:** 2026-05-29  
**Status:** Do weryfikacji technicznej

---

## Metadane ekranu

| Atrybut | Wartość |
|---|---|
| **Nazwa biznesowa ekranu** | Dashboard |
| **Ścieżka URL** | `/dashboard` |
| **Guard dostępu** | `AuthGuard` |
| **Lazy loading** | Nie |
| **Plik komponentu** | `src/app/components/dashboard/dashboard.component.ts` |
| **Plik szablonu** | `src/app/components/dashboard/dashboard.component.html` |
| **Plik stylów** | `src/app/components/dashboard/dashboard.component.scss` |
| **Wersja dokumentu** | 1.0 |
| **Autor dokumentu** | Agent AI |
| **Ostatnia aktualizacja** | 2026-05-29 |

---

## Krótki opis

Ekran Dashboard prezentuje podsumowanie liczby klientów, kont bankowych, dokumentów i produktów. Ekran zawiera wykres liniowy z wartościami miesięcznymi dla wybranego roku i typu dokumentu.

---

## Powiązane dokumenty

| Dokument | Link |
|---|---|
| Przegląd ekranu | [01_PRZEGLĄD.md](01_PRZEGLĄD.md) |
| Dane i operacje | [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md) |
| Logika frontendowa | [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md) |
| Scenariusze testowe | [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md) |
| Historia zmian | [HISTORIA_ZMIAN.md](HISTORIA_ZMIAN.md) |

---

## Szybkie odniesienia

### Główne serwisy

- `DocumentService` — pobiera statystyki dashboardu przez `getDashboardData(year, documentType)`.

### Modele danych

- `IDashboardStats` — liczby zbiorcze i lista wartości miesięcznych.
- `IMonthlyTotal` — dane miesięczne dla wykresu.

### Biblioteki UI

- Angular Material `mat-card`, `mat-select`, `mat-option`.
- `ng2-charts` i `chart.js` dla wykresu liniowego.

---

## Notatki

- Dokument opisuje zachowanie warstwy frontendowej.
- Endpoint jest podany wyłącznie jako adres wywoływany przez `DocumentService`.
