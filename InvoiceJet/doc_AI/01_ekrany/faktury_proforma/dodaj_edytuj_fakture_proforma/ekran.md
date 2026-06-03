# AddOrEditInvoiceProformaComponent — Formularz faktury proforma

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-FormularzProformy |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran tworzenia i edycji faktury proforma (DocumentTypeId=2). Komponent dziedziczy z `BaseInvoiceComponent` — całość logiki UI i wywołań API zdefiniowana w klasie bazowej. `AddOrEditInvoiceProformaComponent` implementuje wyłącznie `getDocumentTypeId()` → `2` i `getNavigationUrl()` → `"/dashboard/invoice-proformas"`. Formularz jest identyczny wizualnie z formularzem faktury zwykłej (EKRAN-FormularzFaktury). Chroniony przez AuthGuard (rola: User).

## Wizualizacja układu

Identyczna z `../faktury/dodaj_edytuj_fakture/ekran.md` — patrz dokumentacja `BaseInvoiceComponent`.

```
┌────────────────────────────────────────────────────────┐
│ Dodaj proformę / Edytuj proformę                       │
├────────────────────────────────────────────────────────┤
│ Klient (autocomplete) | Seria dok. | Data wyst. | Term.│
├────────────────────────────────────────────────────────┤
│ Konto bankowe | Waluta | Status dokumentu              │
├────────────────────────────────────────────────────────┤
│ Tabela pozycji (FormArray)                             │
├────────────────────────────────────────────────────────┤
│ Suma netto: ... | VAT: ... | Brutto: ...               │
├────────────────────────────────────────────────────────┤
│ [Generuj PDF] [Podgląd PDF] [Anuluj] [     Zapisz   ] │
└────────────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/add-invoice-proforma` (dodaj), `/dashboard/edit-invoice-proforma/:id` (edytuj) |
| Wymagana rola/uprawnienie | User (AuthGuard) |
| Punkty wejścia | Klik „Dodaj proformę" z listy; klik wiersza na liście (edycja) |
| Powiązany kod komponentu | `src/app/components/invoice-proformas/add-or-edit-invoice-proforma/add-or-edit-invoice-proforma.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| `/dashboard/invoice-proformas` | Sukces zapisu (onSubmit) | Formularz poprawny + API sukces | User |
| `/dashboard/invoice-proformas` | Klik „Anuluj" | Zawsze | User |
| `PdfViewerComponent` | Klik „Podgląd PDF" | Zawsze | User |

## Sekcje ekranu

Identyczne z `../faktury/dodaj_edytuj_fakture/ekran.md` — patrz dokumentacja `BaseInvoiceComponent`.

### Pola

Identyczne pola jak `EKRAN-FormularzFaktury` — patrz `../../00_wspolne/base_invoice_component/ekran.md`.

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-FormularzProformy-Zapisz | Zapisz | [ALG-02 Generowanie numeru](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) · [wyliczeniowe/aktualizacja_produktow_dokumentu](../../../03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md) |
| OP-FormularzProformy-Anuluj | Anuluj | — |
| OP-FormularzProformy-GenerujPdf | Generuj PDF | [ALG-07 Generuj PDF na dysk](../../../03_algorytmy/generowania_pdf/generuj_pdf_na_dysk.md) ⚠️ BUG A-KRIT-04: hardcoded InvoiceDocument — zamiast ProformaDocument |
| OP-FormularzProformy-PodgladPdf | Podgląd PDF | [ALG-07 Generuj PDF stream](../../../03_algorytmy/generowania_pdf/generuj_pdf_stream.md) (poprawna fabryka) |

### Modale

| ID modalu | Nazwa | Wywołane przez | Link do dokumentu |
|---|---|---|---|
| MODAL-Wspolne-PdfViewer | Podgląd PDF | OP-FormularzProformy-PodgladPdf | `../../00_wspolne/modale_wspolne/pdf_viewer/modal.md` |

## Tryby działania

| Tryb | URL | Zachowanie |
|---|---|---|
| Dodawanie | `/dashboard/add-invoice-proforma` | `isEditMode = false` |
| Edycja | `/dashboard/edit-invoice-proforma/:id` | `isEditMode = true`; ładuje dokument przez API |

## Wywołania API

Identyczne jak `EKRAN-FormularzFaktury`, ale `GetDocumentAutofillInfo/2` (DocumentTypeId=2).

| Akcja | Endpoint |
|---|---|
| Załadowanie autofill (ngOnInit) | [GET /api/Document/GetAutofillInfo](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetAutofillInfo.md) |
| Załadowanie dokumentu (tryb edycji) | [GET /api/Document/GetById](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetById.md) |
| Submit (dodanie) | [POST /api/Document/Add](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md) |
| Submit (edycja) | [PUT /api/Document/Edit](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Edit.md) |
| Generowanie PDF | [POST /api/Document/GeneratePdf](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GeneratePdf.md) |
| Podgląd PDF | [POST /api/Document/GetPdfStream](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) |

## Powiązania

- Klasa bazowa: [BaseInvoiceComponent](../../../01_ekrany/00_wspolne/base_invoice_component/ekran.md)
- Powiązane procesy: [dodaj_dokument](../../../02_procesy/dokumenty/dodaj_dokument/proces.md), [edytuj_dokument](../../../02_procesy/dokumenty/edytuj_dokument/proces.md)
- Powiązane API: [POST /api/Document/Add](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md)
- Powiązane UC: Brak

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| Pola formularza (pozycje) | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) | Identyczne jak faktura: `UnitPrice × Qty × (1 + VAT/100)` — wyliczenie brutto pozycji |
| Podsumowanie sum | [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) | `calculateTotals()` z BaseInvoiceComponent — netto / VAT / brutto |
| OP-FormularzProformy-Zapisz | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | DocumentTypeId=2 → seria PRF; numer PRF0001, PRF0002… |
| OP-FormularzProformy-Zapisz | [wyliczeniowe/aktualizacja_produktow_dokumentu](../../../03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md) | Backend: zapis pozycji i sum do DB |
| OP-FormularzProformy-GenerujPdf | [ALG-07 Generuj PDF na dysk](../../../03_algorytmy/generowania_pdf/generuj_pdf_na_dysk.md) | ⚠️ **BUG A-KRIT-04:** hardcoded `InvoiceDocument` — dla proformy generuje szablon faktury zamiast proformy |
| OP-FormularzProformy-PodgladPdf | [ALG-07 Generuj PDF stream](../../../03_algorytmy/generowania_pdf/generuj_pdf_stream.md) | Poprawna implementacja — fabryka wybiera `ProformaDocument` dla DocumentTypeId=2 |

## Powiązania z kodem

- Komponent: `src/app/components/invoice-proformas/add-or-edit-invoice-proforma/add-or-edit-invoice-proforma.component.ts`
- Szablon HTML: `src/app/components/invoice-proformas/add-or-edit-invoice-proforma/add-or-edit-invoice-proforma.component.html`
- Klasa bazowa: `src/app/components/invoices/add-or-edit-invoice/base-invoice.component.ts`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

Patrz anomalie `BaseInvoiceComponent`: BA-01, BA-02, BA-03 w `../../00_wspolne/base_invoice_component/ekran.md`.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `invoice_proformas/add-or-edit-invoice-proforma.md`. |
