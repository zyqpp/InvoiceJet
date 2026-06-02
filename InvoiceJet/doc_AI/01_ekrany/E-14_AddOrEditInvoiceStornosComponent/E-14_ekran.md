# E-14 AddOrEditInvoiceStornosComponent — Formularz faktury storno

| Pole | Wartość |
|---|---|
| ID dokumentu | E-14 |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 |
| Data ostatniej modyfikacji | 2026-06-02 |

## Streszczenie

Ekran tworzenia i edycji faktury storno (`DocumentTypeId = 3`). Komponent dziedziczy z `BaseInvoiceComponent` — całość logiki UI i wywołań API zdefiniowana w klasie bazowej. `AddOrEditInvoiceStornosComponent` implementuje wyłącznie `getDocumentTypeId() = 3` i `getNavigationUrl() = "/dashboard/invoice-stornos"`. Formularz jest identyczny wizualnie z formularzem faktury zwykłej (E-10) i proformy (E-12). Specyfika: storno najczęściej tworzone jest automatycznie przez operację TransformToStorno z [E-09](../E-09_InvoicesComponent/E-09_ekran.md) — w tym przypadku formularz nie jest używany. Dostępny z UI wyłącznie w trybie edycji (klik wiersza z [E-13](../E-13_InvoiceStornosComponent/E-13_ekran.md)).

---

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────────────────┐
│ ← [Wróć]   Storno Details - STORNO0001   [Unpaid chip]          │
├──────────────────────────────────────────────────────────────────┤
│ [Client Name or CUI*] [Issue Date*] [Due Date] [Status*]        │
├──────────────────────────────────────────────────────────────────┤
│ [Document Series*]    [Bank Account]                             │
├──────────────────────────────────────────────────────────────────┤
│ Name | Unit Price | Qty | U.M. | TVA% | Contains TVA | Total | ✕│
│ [Wiersz 1 — wartości ze źródłowej faktury, mogą być ujemne]     │
│ [+ Dodaj pozycję]                                               │
├──────────────────────────────────────────────────────────────────┤
│ Netto: ...  VAT: ...  Brutto: ...                                │
├──────────────────────────────────────────────────────────────────┤
│ [Generate PDF]  [Preview PDF]  [Cancel]  [Save / Update]        │
└──────────────────────────────────────────────────────────────────┘
```

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| URL (edycja) | `/dashboard/edit-invoice-storno/:id` |
| URL (dodaj — nie eksponowane w UI) | `/dashboard/add-invoice-storno` |
| Wymagana rola | `User` (AuthGuard JWT) |
| Punkty wejścia | [OP-E13-01](../E-13_InvoiceStornosComponent/E-13_OP-01.md) klik wiersza z E-13 (edycja); URL bezpośredni (dodawanie — nie eksponowane w UI) |
| Komponent Angular | [`AddOrEditInvoiceStornosComponent`](../../../../InvoiceJetUI/src/app/components/invoice-stornos/add-or-edit-invoice-storno/add-or-edit-invoice-stornos.component.ts) |
| Klasa bazowa | [`BaseInvoiceComponent`](../../../../InvoiceJetUI/src/app/components/invoices/base-invoice/base-invoice.component.ts) |

## Tryby działania

| Tryb | URL | `isEditMode` | Zachowanie |
|---|---|---|---|
| Edycja | `/dashboard/edit-invoice-storno/:id` | `true` | ładuje storno; `updateDocument()`; dostępne z E-13 |
| Dodawanie (ręczne) | `/dashboard/add-invoice-storno` | `false` | pusty formularz; `addDocument()`; nie eksponowane w UI |

## Specyfika storna

Storno może powstać:
1. Automatycznie — przez [ALG-08 TransformToStorno](../../../03_algorytmy/dedykowane/transformacja_na_storno.md) z [E-09 Lista faktur](../E-09_InvoicesComponent/E-09_ekran.md); komponent nie używany w tej ścieżce — storno tworzone bezpośrednio przez API
2. Ręcznie — przez ten formularz (tryb dodawania, nie eksponowany w UI)

Pozycje storna stworzonego przez TransformToStorno mają wartości z faktury źródłowej (mogą być ujemne po odwróceniu znaków przez ALG-08).

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek |
|---|---|---|
| [E-13 Lista storn](../E-13_InvoiceStornosComponent/E-13_ekran.md) | [OP-E14-03](E-14_OP-03.md) sukces | formularz poprawny |
| [E-13 Lista storn](../E-13_InvoiceStornosComponent/E-13_ekran.md) | [OP-E14-04](E-14_OP-04.md) | zawsze (Anuluj) |
| [MODAL-E14-01 PdfViewer](E-14_MODAL-01.md) | [OP-E14-02](E-14_OP-02.md) | zawsze (Preview PDF) |

---

## Filtry (autocomplete)

| ID | Etykieta UI | Typ | Dokument |
|---|---|---|---|
| FILTR-E14-01 | Client Name or CUI | mat-autocomplete, kliencki | [E-14_FILTR-01.md](E-14_FILTR-01.md) |
| FILTR-E14-02 | Name (per wiersz pozycji) | mat-autocomplete, kliencki | [E-14_FILTR-02.md](E-14_FILTR-02.md) |

## Pola formularza

→ [E-14_POLA.md](E-14_POLA.md) — wszystkie pola: Client, Issue Date, Due Date, Document Series (STN), Bank Account, Status

## Tabele i listy

| ID | Nazwa | Dokument |
|---|---|---|
| TAB-E14-01 | Tabela pozycji dokumentu | [E-14_TAB-01.md](E-14_TAB-01.md) |

## Operacje

| ID | Etykieta UI | Dokument |
|---|---|---|
| OP-E14-01 | + Add Product | [E-14_OP-01.md](E-14_OP-01.md) |
| OP-E14-02 | Preview PDF | [E-14_OP-02.md](E-14_OP-02.md) |
| OP-E14-03 | Save / Update | [E-14_OP-03.md](E-14_OP-03.md) |
| OP-E14-04 | Cancel (Anuluj) | [E-14_OP-04.md](E-14_OP-04.md) |
| OP-E14-05 | Generate PDF | [E-14_OP-05.md](E-14_OP-05.md) |
| OP-E14-06 | ✕ Usuń wiersz pozycji | [E-14_OP-06.md](E-14_OP-06.md) |

## Modale

| ID | Nazwa | Dokument |
|---|---|---|
| MODAL-E14-01 | PdfViewerComponent | [E-14_MODAL-01.md](E-14_MODAL-01.md) |

## Powiadomienia

| ID | Typ | Treść | Kiedy |
|---|---|---|---|
| POW-E14-01 | toastr success | „Document updated successfully" | [OP-E14-03](E-14_OP-03.md) sukces (edycja) |
| POW-E14-02 | toastr success | „Document added successfully" | [OP-E14-03](E-14_OP-03.md) sukces (dodaj — ręczne) |

## Scenariusze testowe

→ [E-14_TC.md](E-14_TC.md) — prereq JWT, prereq DB, selektory CSS, 4 scenariusze e2e

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint | DTO |
|---|---|---|---|
| Autofill (DocumentTypeId=3) | GET | [/api/Document/GetDocumentAutofillInfo/3](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetAutofillInfo.md) | [DTO-10](../../../05_model_danych/02_dto/DTO-10_DocumentAutofillInfoDto.md) |
| Ładowanie (edycja) | GET | [/api/Document/GetDocumentById/{id}](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetById.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Zapisz nowe storno | POST | [/api/Document/AddDocument](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Zaktualizuj storno | PUT | [/api/Document/EditDocument](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Edit.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Podgląd PDF | POST | [/api/Document/GetInvoicePdfStream](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Generuj PDF | POST | [/api/Document/GenerateDocumentPdf](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GeneratePdf.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |

---

## Powiązania

| Typ | Dokument |
|---|---|
| Ekran poprzedni | [E-13 InvoiceStornosComponent](../E-13_InvoiceStornosComponent/E-13_ekran.md) |
| Ekran wzorzec | [E-10 AddOrEditInvoiceComponent](../E-10_AddOrEditInvoiceComponent/E-10_ekran.md) |
| Ekran wzorzec | [E-12 AddOrEditInvoiceProformaComponent](../E-12_AddOrEditInvoiceProformaComponent/E-12_ekran.md) |
| DTO | [DTO-07 DocumentRequestDto](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| DTO | [DTO-10 DocumentAutofillInfoDto](../../../05_model_danych/02_dto/DTO-10_DocumentAutofillInfoDto.md) |
| Model DB | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Model DB | [dbo.DocumentProduct](../../../05_model_danych/01_db/dbo/dbo.DocumentProduct.md) |

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| Pola tabeli pozycji (quantity, price, vatRate) | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) | `UnitPrice × Qty × (1 + VAT/100)` — wyliczenie brutto pozycji w czasie rzeczywistym |
| Suma netto/VAT/Brutto | [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) | `calculateTotals()` z BaseInvoiceComponent |
| OP-E14-03 Zapisz (documentSeriesId) | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | DocumentTypeId=3 → seria STN; numer STN0001, STN0002… |
| OP-E14-03 Zapisz (pozycje) | [wyliczeniowe/aktualizacja_produktow_dokumentu](../../../03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md) | Backend: zapis pozycji i sum do DB |
| OP-E14-05 Generuj PDF | [ALG-07 generuj_pdf_na_dysk](../../../03_algorytmy/generowania_pdf/generuj_pdf_na_dysk.md) | Generowanie PDF i zapis na dysk |
| OP-E14-02 Podgląd PDF | [ALG-07 generuj_pdf_stream](../../../03_algorytmy/generowania_pdf/generuj_pdf_stream.md) | Podgląd PDF przez stream |
| Automatyczne storno (nie przez formularz) | [ALG-08 Transformacja na storno](../../../03_algorytmy/dedykowane/transformacja_na_storno.md) | Storno tworzone z [E-09](../E-09_InvoicesComponent/E-09_ekran.md) przez TransformToStorno — komponent nie używany w tej ścieżce |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`add-or-edit-invoice-stornos.component.ts`](../../../../InvoiceJetUI/src/app/components/invoice-stornos/add-or-edit-invoice-storno/add-or-edit-invoice-stornos.component.ts) |
| Klasa bazowa TS | [`base-invoice.component.ts`](../../../../InvoiceJetUI/src/app/components/invoices/base-invoice/base-invoice.component.ts) |
| Szablon HTML | [`add-or-edit-invoice-stornos.component.html`](../../../../InvoiceJetUI/src/app/components/invoice-stornos/add-or-edit-invoice-storno/add-or-edit-invoice-stornos.component.html) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| BA-01 | Walidacja zakomentowana w Preview PDF (dziedziczone z BaseInvoiceComponent) |
| BA-02 | `generateInvoicePdf()` ignoruje odpowiedź API |
| BA-03 | Brak `.error()` handlera dla save/update |
| BA-05 | `documentSeries` i `documentStatus` bez `Validators.required` |
| BA-07 | Brak `data-cy` / `data-testid` |
| IA-07 | Trasa `/dashboard/add-invoice-storno` istnieje w routingu, ale UI listy storn nie eksponuje przycisku „Dodaj storno" — celowa decyzja projektowa czy przeoczenie? |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — adaptacja z wzorca E-10/E-12 i źródła faktury_storno/dodaj_edytuj_fakture_storno/ekran.md. |
