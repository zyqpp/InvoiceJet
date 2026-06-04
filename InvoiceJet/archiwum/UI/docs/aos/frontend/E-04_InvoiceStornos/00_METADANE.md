# Invoice Stornos — Metadane

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
| **Nazwa biznesowa ekranu** | Invoice Stornos |
| **Ścieżka URL** | `/dashboard/invoice-stornos` |
| **Guard dostępu** | `AuthGuard` |
| **Lazy loading** | Nie |
| **Plik komponentu** | `src/app/components/invoice-stornos/invoice-stornos.component.ts` |
| **Plik szablonu** | `src/app/components/invoice-stornos/invoice-stornos.component.html` |
| **Plik stylów** | `src/app/components/invoice-stornos/invoice-stornos.component.scss` |
| **Ekran powiązany** | Formularz edycji storna: `/dashboard/edit-invoice-storno/:id` |
| **Makieta** | `mockup.svg` |
| **Wersja dokumentu** | 1.0 |
| **Autor dokumentu** | Agent AI |
| **Ostatnia aktualizacja** | 2026-05-29 |

---

## Krótki opis

Ekran Invoice Stornos wyświetla grid dokumentów typu storno. Ekran umożliwia filtrowanie tekstowe, sortowanie, paginację, zaznaczanie wierszy, przejście do edycji storna i usunięcie zaznaczonych dokumentów.

W aktualnym szablonie komponentu nie ma aktywnego przycisku dodawania nowego storna. Fragment przycisku `New Storno` istnieje w HTML jako zakomentowany kod.

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

- `InvoiceStornosComponent` — komponent listy dokumentów storno.
- `DocumentService` — pobiera dokumenty przez `getDocuments(3)` i usuwa zaznaczone rekordy.
- `Router` — nawiguje do formularza edycji storna.
- `IDocumentTableRecord` — model wiersza gridu.
- `IDocumentStatus` — model statusu renderowanego w `mat-chip`.

---

## Notatki

- Dokument opisuje zachowanie warstwy frontendowej.
- Ekran nie ma dostarczonego screenshotu. Makieta `mockup.svg` została przygotowana na podstawie kodu komponentu i układu istniejących ekranów list dokumentów.
