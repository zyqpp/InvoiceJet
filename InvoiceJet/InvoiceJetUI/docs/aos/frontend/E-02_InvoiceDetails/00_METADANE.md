# Invoice Details — Metadane

**Dokument:** Metadane ekranu  
**Aplikacja:** InvoiceJet  
**Moduł:** Documents  
**Klasyfikacja:** Duży  
**Data utworzenia:** 2026-05-29  
**Status:** Do weryfikacji technicznej

---

## Metadane ekranu

| Atrybut | Wartość |
|---|---|
| **Nazwa biznesowa ekranu** | Invoice Details |
| **Ścieżka URL — dodawanie** | `/dashboard/add-invoice` |
| **Ścieżka URL — edycja** | `/dashboard/edit-invoice/:id` |
| **Guard dostępu** | `AuthGuard` |
| **Lazy loading** | Nie |
| **Plik komponentu** | `src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.ts` |
| **Plik szablonu** | `src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.html` |
| **Plik stylów** | `src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.scss` |
| **Klasa bazowa** | `src/app/components/invoices/base-invoice/base-invoice.component.ts` |
| **Walidator daty** | `src/app/components/invoices/base-invoice/date-validator.ts` |
| **Dialog podglądu PDF** | `src/app/components/pdf-viewer/pdf-viewer.component.ts` |
| **Wersja dokumentu** | 1.0 |
| **Autor dokumentu** | Agent AI |
| **Ostatnia aktualizacja** | 2026-05-29 |

---

## Krótki opis

Ekran Invoice Details umożliwia dodanie albo edycję faktury. Ekran zawiera formularz danych dokumentu, grid pozycji dokumentu, przeliczanie wartości pozycji, wybór klienta i produktu przez autouzupełnianie oraz podgląd PDF w trybie edycji.

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

- `DocumentService` — wywołania HTTP dla autouzupełniania, pobrania dokumentu, dodania, edycji i podglądu PDF.
- `MatDialog` — otwarcie dialogu `PdfViewerComponent`.
- `ToastrService` — komunikaty sukcesu po dodaniu i edycji dokumentu.
- `Router` — powrót do listy faktur po zapisie lub kliknięciu przycisku Wstecz.

### Modele danych

- `IDocumentRequest` — model formularza dokumentu.
- `IDocumentProductRequest` — model pozycji dokumentu.
- `IDocumentAutofill` — dane do autouzupełniania klientów, produktów, serii i statusów.
- `IFirm` — klient dokumentu.
- `IProduct` — produkt używany do wypełnienia pozycji dokumentu.

### Dialogi

- Dialog Podgląd PDF: `PdfViewerComponent`.

---

## Notatki

- Dokument opisuje zachowanie frontendu wynikające z komponentów Angular i serwisów UI.
- Dokument nie opisuje implementacji backendu, generowania numeru dokumentu po stronie API ani zapisu w bazie danych.
- Ekran faktury jest specjalizacją klasy `BaseInvoiceComponent`; typ dokumentu faktury jest ustawiany przez `getDocumentTypeId()` zwracające `1`.
