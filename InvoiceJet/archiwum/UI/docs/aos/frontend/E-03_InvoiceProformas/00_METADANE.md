# Invoice Proformas — Metadane

**Dokument:** Metadane ekranu
**Aplikacja:** InvoiceJet
**Moduł:** Documents
**Klasyfikacja:** Standardowy
**Data utworzenia:** 2026-05-29
**Status:** Do weryfikacji technicznej

---

## Metadane ekranu

| Atrybut | Wartość |
|---|---|
| **Nazwa biznesowa ekranu** | Invoice Proformas |
| **Ścieżka URL** | `/dashboard/invoice-proformas` |
| **Guard dostępu** | `AuthGuard` |
| **Lazy loading** | Nie |
| **Plik komponentu** | `src/app/components/invoice-proformas/invoice-proformas.component.ts` |
| **Plik szablonu** | `src/app/components/invoice-proformas/invoice-proformas.component.html` |
| **Plik stylów** | `src/app/components/invoice-proformas/invoice-proformas.component.scss` |
| **Ekran powiązany** | Formularz proformy: `/dashboard/add-invoice-proforma`, `/dashboard/edit-invoice-proforma/:id` |
| **Makieta** | `mockup.svg` |
| **Wersja dokumentu** | 1.0 |
| **Autor dokumentu** | Agent AI |
| **Ostatnia aktualizacja** | 2026-05-29 |

---

## Krótki opis

Ekran Invoice Proformas wyświetla grid dokumentów typu proforma. Ekran umożliwia filtrowanie tekstowe, sortowanie, paginację, zaznaczanie wierszy, przejście do nowej proformy, przejście do edycji proformy i usunięcie zaznaczonych dokumentów.

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

- `InvoiceProformasComponent` — komponent listy proform.
- `DocumentService` — pobiera dokumenty przez `getDocuments(2)` i usuwa zaznaczone rekordy.
- `Router` — nawiguje do formularza dodawania i edycji proformy.
- `IDocumentTableRecord` — model wiersza gridu.
- `IDocumentStatus` — model statusu renderowanego w `mat-chip`.

---

## Notatki

- Dokument opisuje zachowanie warstwy frontendowej.
- Ekran nie ma dostarczonego screenshotu. Makieta `mockup.svg` została przygotowana na podstawie kodu komponentu i układu istniejących ekranów list dokumentów.
