# Products — Metadane

**Dokument:** Metadane ekranu  
**Aplikacja:** InvoiceJet  
**Moduł:** Inventory  
**Klasyfikacja:** Standardowy  
**Data utworzenia:** 2026-05-29  
**Status:** Do weryfikacji technicznej

---

## Metadane ekranu

| Atrybut | Wartość |
|---|---|
| **Nazwa biznesowa ekranu** | Products |
| **Ścieżka URL** | `/dashboard/products` |
| **Guard dostępu** | `AuthGuard` |
| **Lazy loading** | Nie |
| **Plik komponentu** | `src/app/components/products/products.component.ts` |
| **Plik szablonu** | `src/app/components/products/products.component.html` |
| **Plik stylów** | `src/app/components/products/products.component.scss` |
| **Komponent dialogu** | `src/app/components/products/add-or-edit-product-dialog/add-or-edit-product-dialog.component.ts` |
| **Szablon dialogu** | `src/app/components/products/add-or-edit-product-dialog/add-or-edit-product-dialog.component.html` |
| **Wersja dokumentu** | 1.0 |
| **Autor dokumentu** | Agent AI |
| **Ostatnia aktualizacja** | 2026-05-29 |

---

## Krótki opis

Ekran Products wyświetla grid produktów zalogowanego użytkownika. Ekran umożliwia filtrowanie tekstowe, sortowanie, paginację, zaznaczanie wierszy, dodawanie produktu, edycję produktu i usuwanie zaznaczonych produktów.

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

- `ProductService` — wywołania HTTP dla listy produktów, dodawania, edycji i usuwania.
- `MatDialog` — otwieranie dialogu Dodawanie/Edycja produktu.
- `ToastrService` — wyświetlanie komunikatów sukcesu.
- `LiveAnnouncer` — komunikaty dostępności dla zmiany sortowania.

### Modele danych

- `IProduct` — model produktu używany przez grid i formularz dialogu.

### Dialogi

- Dialog Dodawanie/Edycja produktu: `AddOrEditProductDialogComponent`.

---

## Notatki

- Dokument opisuje zachowanie warstwy frontendowej wynikające z komponentów Angular i serwisów UI.
- Dokument nie opisuje implementacji backendu ani logiki bazy danych.
- Endpointy są podane wyłącznie jako adresy wywoływane przez `ProductService`.
