# AddOrEditInvoiceComponent — Formularz faktury

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-FormularzFaktury |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran tworzenia i edycji faktury zwykłej (DocumentTypeId=1). Komponent dziedziczy z `BaseInvoiceComponent`, który zawiera całą logikę UI i wywołania API. `AddOrEditInvoiceComponent` implementuje tylko `getDocumentTypeId()` → `1` i `getNavigationUrl()` → `"/dashboard/invoices"`. Formularz zawiera pola nagłówka dokumentu oraz dynamiczną tabelę pozycji (produktów). Chroniony przez AuthGuard (rola: User).

## Wizualizacja układu

```
┌────────────────────────────────────────────────────────┐
│ Dodaj fakturę / Edytuj fakturę                         │
├────────────────────────────────────────────────────────┤
│ Klient (autocomplete) | Seria dok. | Data wyst. | Term.│
├────────────────────────────────────────────────────────┤
│ Konto bankowe | Waluta | Status dokumentu              │
├────────────────────────────────────────────────────────┤
│ Tabela pozycji:                                        │
│  Produkt | Cena | Ilość | J.m. | VAT | Brutto | [Del] │
├────────────────────────────────────────────────────────┤
│ Suma netto: ... | VAT: ... | Brutto: ...               │
├────────────────────────────────────────────────────────┤
│ [Generuj PDF] [Podgląd PDF] [Anuluj] [     Zapisz   ] │
└────────────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/add-invoice` (dodaj), `/dashboard/edit-invoice/:id` (edytuj) |
| Wymagana rola/uprawnienie | User (AuthGuard) |
| Punkty wejścia | Klik „Dodaj fakturę" z listy; klik wiersza na liście (edycja) |
| Powiązany kod komponentu | `src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| `/dashboard/invoices` | Sukces zapisu (onSubmit) | Formularz poprawny + API sukces | User |
| `/dashboard/invoices` | Klik „Anuluj" | Zawsze | User |
| `PdfViewerComponent` | Klik „Podgląd PDF" | Zawsze | User |

## Sekcje ekranu

### Filtry

Brak.

### Tabele i listy

| ID tabeli | Nazwa | Link do dokumentu |
|---|---|---|
| TAB-FormularzFaktury-PozycjeDokumentu | Tabela pozycji dokumentu (FormArray) | `../../00_wspolne/base_invoice_component/ekran.md` |

### Pola

| ID pola | Nazwa w UI | Wymagalność | Link do dokumentu |
|---|---|---|---|
| POLE-FormularzFaktury-clientId | Klient | wymagane | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) — autocomplete filtruje klientów bieżącej firmy |
| POLE-FormularzFaktury-documentSeriesId | Seria dokumentu | wymagane | [ALG-02 Generowanie numeru](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) — wybór serii decyduje o formacie numeru (SeriesName + CurrentNumber.D4) |
| POLE-FormularzFaktury-issueDate | Data wystawienia | wymagane | — |
| POLE-FormularzFaktury-dueDate | Termin płatności | wymagane | — |
| POLE-FormularzFaktury-bankAccountId | Konto bankowe | wymagane | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) — autocomplete filtruje konta bieżącej firmy |
| POLE-FormularzFaktury-currency | Waluta | wymagane | — |
| POLE-FormularzFaktury-documentStatus | Status dokumentu | wymagane | — |

### Kolumny tabeli pozycji

| Kolumna | Opis | Algorytm |
|---|---|---|
| `name` | Nazwa produktu/usługi | — |
| `unitPrice` | Cena jednostkowa (netto) | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) — wejście do wzoru |
| `quantity` | Ilość | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) — wejście do wzoru |
| `unitOfMeasurement` | Jednostka miary | — |
| `tvaValue` | Stawka VAT (%) | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) — wejście do wzoru `UnitPrice × Qty × (1 + VAT/100)` |
| `containsTva` | Czy podana cena jest brutto | — |
| `totalPrice` | Cena brutto pozycji (wyliczana live) | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) — **obliczana automatycznie** na frontendzie |
| `actions` | Usuń pozycję | — |

> **Podsumowanie sum dokumentu** (Suma netto / VAT / Brutto wyświetlane pod tabelą):
> → [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) — `totalNetAmount`, `totalVatAmount`, `totalGrossAmount` wyliczane w `BaseInvoiceComponent.calculateTotals()`

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-FormularzFaktury-Zapisz | Zapisz | [ALG-02 Generowanie numeru](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) (numer nadawany przy zapisie) · [wyliczeniowe/aktualizacja_produktow_dokumentu](../../../03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md) (zapis pozycji + sum do DB) |
| OP-FormularzFaktury-Anuluj | Anuluj | — |
| OP-FormularzFaktury-GenerujPdf | Generuj PDF | [ALG-07 Generuj PDF na dysk](../../../03_algorytmy/generowania_pdf/generuj_pdf_na_dysk.md) ⚠️ BUG: hardcoded InvoiceDocument |
| OP-FormularzFaktury-PodgladPdf | Podgląd PDF | [ALG-07 Generuj PDF stream](../../../03_algorytmy/generowania_pdf/generuj_pdf_stream.md) (poprawna ścieżka z fabryką) |
| OP-FormularzFaktury-DodajPozycje | Dodaj pozycję | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) (po dodaniu pozycji przeliczane sumy) |
| OP-FormularzFaktury-UsunPozycje | Usuń pozycję | [ALG-05 Obliczanie wartości](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) (sumy przeliczane po usunięciu) |

### Modale

| ID modalu | Nazwa | Wywołane przez | Link do dokumentu |
|---|---|---|---|
| MODAL-Wspolne-PdfViewer | Podgląd PDF | OP-FormularzFaktury-PodgladPdf | `../../00_wspolne/modale_wspolne/pdf_viewer/modal.md` |

### Powiadomienia

Brak (anomalia: brak widocznych komunikatów sukcesu/błędu).

## Tryby działania

| Tryb | URL | Zachowanie |
|---|---|---|
| Dodawanie | `/dashboard/add-invoice` | `isEditMode = false`; brak `:id` w route |
| Edycja | `/dashboard/edit-invoice/:id` | `isEditMode = true`; ładuje dokument przez API |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie autofill (ngOnInit) | [GET /api/Document/GetAutofillInfo](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetAutofillInfo.md) |
| Załadowanie dokumentu (tryb edycji) | [GET /api/Document/GetById](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetById.md) |
| Submit (dodanie) | [POST /api/Document/Add](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md) |
| Submit (edycja) | [PUT /api/Document/Edit](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Edit.md) |
| Generowanie PDF (zapis na dysk) | [POST /api/Document/GeneratePdf](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GeneratePdf.md) |
| Podgląd PDF (strumień) | [POST /api/Document/GetPdfStream](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) |

## Powiązania

- Klasa bazowa: [BaseInvoiceComponent](../../../01_ekrany/00_wspolne/base_invoice_component/ekran.md)
- Powiązane procesy: [dodaj_dokument](../../../02_procesy/dokumenty/dodaj_dokument/proces.md), [edytuj_dokument](../../../02_procesy/dokumenty/edytuj_dokument/proces.md), [generuj_pdf](../../../02_procesy/dokumenty/generuj_pdf/proces.md)
- Powiązane API: [POST /api/Document/Add](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md)
- Powiązane UC: Brak

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| POLE-FormularzFaktury-documentSeriesId | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | Wybrana seria determinuje format numeru (SeriesName + CurrentNumber.D4); licznik inkrementowany przy zapisie |
| Kolumna `unitPrice`, `quantity`, `tvaValue` | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) | `UnitPrice × Qty × (1 + VAT/100)` — wyliczenie brutto wiersza na frontendzie |
| Kolumna `totalPrice` (wyliczana) | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) | Automatycznie wyliczana cena brutto pozycji po każdej zmianie |
| Podsumowanie: Suma netto / VAT / Brutto | [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) | `calculateTotals()` w BaseInvoiceComponent — aktualizacja na żywo przy każdej zmianie w FormArray |
| OP-FormularzFaktury-Zapisz | [wyliczeniowe/aktualizacja_produktow_dokumentu](../../../03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md) | Backend: `UpdateDocumentProducts` — zapis pozycji do DB i wyliczenie `UnitPrice` (netto) + `TotalPrice` (brutto) dokumentu |
| OP-FormularzFaktury-Zapisz | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | Przy dodaniu nowego dokumentu: numer = `SeriesName + CurrentNumber.PadLeft(4)`, następnie `CurrentNumber++` |
| OP-FormularzFaktury-GenerujPdf | [ALG-07 Generuj PDF na dysk](../../../03_algorytmy/generowania_pdf/generuj_pdf_na_dysk.md) | ⚠️ BUG: hardcoded template `InvoiceDocument` niezależnie od DocumentTypeId |
| OP-FormularzFaktury-PodgladPdf | [ALG-07 Generuj PDF stream](../../../03_algorytmy/generowania_pdf/generuj_pdf_stream.md) | Poprawna implementacja — fabryka szablonów na podstawie DocumentTypeId |
| POLE-FormularzFaktury-clientId / bankAccountId | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Autocomplete ładuje tylko dane bieżącej firmy (UserFirm filter) |

## Powiązania z kodem

- Komponent: `src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.ts`
- Szablon HTML: `src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.html`
- Klasa bazowa: `src/app/components/invoices/add-or-edit-invoice/base-invoice.component.ts`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

- BA-01: Walidacja formularza zakomentowana w `getInvoicePdfStream()` — możliwe wywołanie API z niekompletnym formularzem.
- BA-02: `generateInvoicePdf()` ignoruje odpowiedź API — brak komunikatu dla użytkownika.
- BA-03: 6 aktywnych `console.log` w kodzie produkcyjnym.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `invoices/add-or-edit-invoice.md`. |
