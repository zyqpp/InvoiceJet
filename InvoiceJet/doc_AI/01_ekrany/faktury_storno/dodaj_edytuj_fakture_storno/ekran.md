# AddOrEditInvoiceStornosComponent — Formularz faktury storno

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-FormularzStorna |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran tworzenia i edycji faktury storno (DocumentTypeId=3). Komponent dziedziczy z `BaseInvoiceComponent` — całość logiki UI i wywołań API zdefiniowana w klasie bazowej. `AddOrEditInvoiceStornosComponent` implementuje wyłącznie `getDocumentTypeId()` → `3` i `getNavigationUrl()` → `"/dashboard/invoice-stornos"`. Formularz identyczny wizualnie z formularzem faktury zwykłej i proformy. Specyfika: storno może powstać ręcznie (przez ten formularz) lub automatycznie (przez `TransformToStorno` z listy faktur — wtedy formularz nie jest używany). Chroniony przez AuthGuard (rola: User).

## Wizualizacja układu

Identyczna z `../faktury/dodaj_edytuj_fakture/ekran.md` — patrz dokumentacja `BaseInvoiceComponent`.

```
┌────────────────────────────────────────────────────────┐
│ Dodaj storno / Edytuj storno                           │
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
| Ścieżka URL | `/dashboard/add-invoice-storno` (dodaj), `/dashboard/edit-invoice-storno/:id` (edytuj) |
| Wymagana rola/uprawnienie | User (AuthGuard) |
| Punkty wejścia | Klik wiersza na liście storn (edycja); URL bezpośredni (dodawanie — nie eksponowane w UI) |
| Powiązany kod komponentu | `src/app/components/invoice-stornos/add-or-edit-invoice-storno/add-or-edit-invoice-stornos.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| `/dashboard/invoice-stornos` | Sukces zapisu (onSubmit) | Formularz poprawny + API sukces | User |
| `/dashboard/invoice-stornos` | Klik „Anuluj" | Zawsze | User |
| `PdfViewerComponent` | Klik „Podgląd PDF" | Zawsze | User |

## Sekcje ekranu

Identyczne z `../faktury/dodaj_edytuj_fakture/ekran.md` — patrz dokumentacja `BaseInvoiceComponent`.

### Pola

Identyczne pola jak `EKRAN-FormularzFaktury` — patrz `../../00_wspolne/base_invoice_component/ekran.md`.

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-FormularzStorna-Zapisz | Zapisz | [ALG-02 Generowanie numeru](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) · [wyliczeniowe/aktualizacja_produktow_dokumentu](../../../03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md) |
| OP-FormularzStorna-Anuluj | Anuluj | — |
| OP-FormularzStorna-GenerujPdf | Generuj PDF | [ALG-07 Generuj PDF na dysk](../../../03_algorytmy/generowania_pdf/generuj_pdf_na_dysk.md) |
| OP-FormularzStorna-PodgladPdf | Podgląd PDF | [ALG-07 Generuj PDF stream](../../../03_algorytmy/generowania_pdf/generuj_pdf_stream.md) |

### Modale

| ID modalu | Nazwa | Wywołane przez | Link do dokumentu |
|---|---|---|---|
| MODAL-Wspolne-PdfViewer | Podgląd PDF | OP-FormularzStorna-PodgladPdf | `../../00_wspolne/modale_wspolne/pdf_viewer/modal.md` |

## Tryby działania

| Tryb | URL | Zachowanie |
|---|---|---|
| Dodawanie (ręczne) | `/dashboard/add-invoice-storno` | `isEditMode = false`; nie eksponowane w UI listy storn |
| Edycja | `/dashboard/edit-invoice-storno/:id` | `isEditMode = true`; dostępne z listy storn |

## Specyfika storna

Storno może powstać:
1. Ręcznie — przez formularz (ten ekran, tryb dodawania)
2. Automatycznie — przez [PUT /api/Document/TransformToStorno](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_TransformToStorno.md) z [listy faktur](../../../01_ekrany/faktury/lista_faktur/ekran.md); w tym przypadku komponent nie jest używany — akcja odbywa się bezpośrednio z listy

## Wywołania API

Identyczne jak `EKRAN-FormularzFaktury`, ale `GetDocumentAutofillInfo/3` (DocumentTypeId=3).

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
- Powiązane procesy: [dodaj_dokument](../../../02_procesy/dokumenty/dodaj_dokument/proces.md), [edytuj_dokument](../../../02_procesy/dokumenty/edytuj_dokument/proces.md), [transformuj_na_storno](../../../02_procesy/dokumenty/transformuj_na_storno/proces.md)
- Powiązane API: [POST /api/Document/Add](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md)
- Powiązane UC: Brak

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| Pola i tabela pozycji | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) | Identyczne jak faktura: wyliczenie brutto pozycji na frontendzie |
| Podsumowanie sum | [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) | `calculateTotals()` z BaseInvoiceComponent |
| OP-FormularzStorna-Zapisz | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | DocumentTypeId=3 → seria STN; numer STN0001… |
| OP-FormularzStorna-Zapisz | [wyliczeniowe/aktualizacja_produktow_dokumentu](../../../03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md) | Backend: zapis pozycji i sum do DB |
| OP-FormularzStorna-GenerujPdf | [ALG-07 Generuj PDF na dysk](../../../03_algorytmy/generowania_pdf/generuj_pdf_na_dysk.md) | Generowanie PDF i zapis na dysk |
| OP-FormularzStorna-PodgladPdf | [ALG-07 Generuj PDF stream](../../../03_algorytmy/generowania_pdf/generuj_pdf_stream.md) | Podgląd PDF przez stream |
| Automatyczne storno (TransformToStorno) | [ALG-08 Transformacja na storno](../../../03_algorytmy/dedykowane/transformacja_na_storno.md) | Storno tworzone z listy faktur — formularz nie używany w tym ścieżce |

## Powiązania z kodem

- Komponent: `src/app/components/invoice-stornos/add-or-edit-invoice-storno/add-or-edit-invoice-stornos.component.ts`
- Szablon HTML: `src/app/components/invoice-stornos/add-or-edit-invoice-storno/add-or-edit-invoice-stornos.component.html`
- Klasa bazowa: `src/app/components/invoices/add-or-edit-invoice/base-invoice.component.ts`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

- Trasa `/dashboard/add-invoice-storno` istnieje w routingu i jest obsługiwana przez komponent, ale UI listy storn nie eksponuje przycisku „Dodaj storno". Niespójność — celowa decyzja projektowa (storno tylko przez TransformToStorno) czy przeoczenie?
- Patrz anomalie `BaseInvoiceComponent`: BA-01, BA-02, BA-03 w `../../00_wspolne/base_invoice_component/ekran.md`.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `invoice_stornos/add-or-edit-invoice-storno.md`. |
