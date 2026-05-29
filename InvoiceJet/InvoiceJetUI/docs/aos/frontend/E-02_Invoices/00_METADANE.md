# Invoices — Metadane

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
| **Nazwa biznesowa ekranu** | Invoices |
| **Ścieżka URL** | `/dashboard/invoices` |
| **Guard dostępu** | `AuthGuard` |
| **Lazy loading** | Nie |
| **Plik komponentu** | `src/app/components/invoices/invoices.component.ts` |
| **Plik szablonu** | `src/app/components/invoices/invoices.component.html` |
| **Plik stylów** | `src/app/components/invoices/invoices.component.scss` |
| **Ekran powiązany** | `E-03_InvoiceDetails` dla `/dashboard/add-invoice` i `/dashboard/edit-invoice/:id` |
| **Wersja dokumentu** | 1.0 |
| **Autor dokumentu** | Agent AI |
| **Ostatnia aktualizacja** | 2026-05-29 |

---

## Krótki opis

Ekran Invoices wyświetla grid faktur typu `Factura`. Ekran umożliwia filtrowanie tekstowe, sortowanie, paginację, zaznaczanie wierszy, przejście do nowej faktury, przejście do edycji faktury, usunięcie zaznaczonych dokumentów i transformację zaznaczonych dokumentów do storna.

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

- `DocumentService` — wywołania HTTP dla listy faktur, usuwania i transformacji do storna.
- `Router` — nawigacja do dodawania i edycji faktury.

### Modele danych

- `IDocumentTableRecord` — model wiersza gridu faktur.
- `IDocumentStatus` — model statusu dokumentu pokazywany w kolumnie `Status`.

---

## Notatki

- Dokument opisuje zachowanie warstwy frontendowej wynikające z komponentów Angular i serwisów UI.
- Endpointy są podane wyłącznie jako adresy wywoływane przez `DocumentService`.
