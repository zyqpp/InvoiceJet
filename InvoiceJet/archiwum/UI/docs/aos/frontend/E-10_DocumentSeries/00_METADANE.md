# Document Series — Metadane

**Dokument:** Metadane ekranu  
**Aplikacja:** InvoiceJet  
**Moduł:** Settings  
**Klasyfikacja:** Standardowy  
**Data utworzenia:** 2026-05-29  
**Status:** Do weryfikacji technicznej

---

## Metadane ekranu

| Atrybut | Wartość |
|---|---|
| **Nazwa biznesowa ekranu** | Document Series |
| **Ścieżka URL** | `/dashboard/document-series` |
| **Guard dostępu** | `AuthGuard` |
| **Lazy loading** | Nie |
| **Plik komponentu** | `src/app/components/document-series/document-series.component.ts` |
| **Plik szablonu** | `src/app/components/document-series/document-series.component.html` |
| **Plik stylów** | `src/app/components/document-series/document-series.component.scss` |
| **Komponent dialogu** | `src/app/components/document-series/add-or-edit-document-series-dialog/add-or-edit-document-series-dialog.component.ts` |
| **Szablon dialogu** | `src/app/components/document-series/add-or-edit-document-series-dialog/add-or-edit-document-series-dialog.component.html` |
| **Wersja dokumentu** | 1.0 |
| **Autor dokumentu** | Agent AI |
| **Ostatnia aktualizacja** | 2026-05-29 |

---

## Krótki opis

Ekran Document Series wyświetla grid serii dokumentów użytkownika. Ekran umożliwia filtrowanie tekstowe, sortowanie, paginację, zaznaczanie wierszy, dodawanie serii, edycję serii i usuwanie zaznaczonych serii.

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

- `DocumentSeriesService` — wywołania HTTP dla listy serii, dodawania, edycji i usuwania.
- `MatDialog` — otwieranie dialogu Dodawanie/Edycja serii dokumentów.
- `ToastrService` — wyświetlanie komunikatów sukcesu.
- `LiveAnnouncer` — komunikaty dostępności dla zmiany sortowania.

### Modele danych

- `IDocumentSeries` — model serii dokumentów używany przez grid i formularz dialogu.
- `IDocumentType` — model typu dokumentu używany w kolumnie i liście rozwijanej.

### Dialogi

- Dialog Dodawanie/Edycja serii dokumentów: `AddOrEditDocumentSeriesDialogComponent`.

---

## Notatki

- Dokument opisuje zachowanie warstwy frontendowej wynikające z komponentów Angular i serwisów UI.
- Endpointy są podane wyłącznie jako adresy wywoływane przez `DocumentSeriesService`.
