# E-12 AddOrEditInvoiceProformaComponent — Formularz faktury proforma

| Pole | Wartość |
|---|---|
| ID dokumentu | E-12 |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 |
| Data ostatniej modyfikacji | 2026-06-02 |

## Streszczenie

Ekran tworzenia i edycji faktury proforma (`DocumentTypeId = 2`). Komponent dziedziczy z `BaseInvoiceComponent` — całość logiki UI i wywołań API zdefiniowana w klasie bazowej. `AddOrEditInvoiceProformaComponent` implementuje wyłącznie `getDocumentTypeId() = 2` i `getNavigationUrl() = "/dashboard/invoice-proformas"`. Formularz jest identyczny wizualnie z formularzem faktury zwykłej (E-10). Zawiera dynamiczną tabelę pozycji z obliczaniem cen w czasie rzeczywistym.

**UWAGA:** Operacja „Generuj PDF" zawiera krytyczny błąd BUG A-KRIT-04 — hardcoded `InvoiceDocument` zamiast `ProformaDocument`, przez co PDF tytułuje się „Factura" zamiast „Factura Proforma".

---

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────────────────┐
│ ← [Wróć]   Proforma Details - PRF0007   [Unpaid chip]           │
├──────────────────────────────────────────────────────────────────┤
│ [Client Name or CUI*] [Issue Date*] [Due Date] [Status*]        │
├──────────────────────────────────────────────────────────────────┤
│ [Document Series*]    [Bank Account]                             │
├──────────────────────────────────────────────────────────────────┤
│ Name | Unit Price | Qty | U.M. | TVA% | Contains TVA | Total | ✕│
│ [Wiersz 1]                                                       │
│ [+ Dodaj pozycję]                                               │
├──────────────────────────────────────────────────────────────────┤
│ Netto: ...  VAT: ...  Brutto: ...                                │
├──────────────────────────────────────────────────────────────────┤
│ [Generate PDF ⚠️]  [Preview PDF]  [Cancel]  [Save / Update]     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| URL (dodaj) | `/dashboard/add-invoice-proforma` |
| URL (edycja) | `/dashboard/edit-invoice-proforma/:id` |
| Wymagana rola | `User` (AuthGuard JWT) |
| Punkty wejścia | [OP-E11-01](../E-11_InvoiceProformasComponent/E-11_OP-01.md); [OP-E11-02](../E-11_InvoiceProformasComponent/E-11_OP-02.md) |
| Komponent Angular | [`AddOrEditInvoiceProformaComponent`](../../../../InvoiceJetUI/src/app/components/invoice-proformas/add-or-edit-invoice-proforma/add-or-edit-invoice-proforma.component.ts) |
| Klasa bazowa | [`BaseInvoiceComponent`](../../../../InvoiceJetUI/src/app/components/invoices/base-invoice/base-invoice.component.ts) |

## Tryby działania

| Tryb | URL | `isEditMode` | Zachowanie |
|---|---|---|---|
| Dodawanie | `/dashboard/add-invoice-proforma` | `false` | pusty formularz; `addDocument()` |
| Edycja | `/dashboard/edit-invoice-proforma/:id` | `true` | ładuje proformę; `updateDocument()` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek |
|---|---|---|
| [E-11 Lista proform](../E-11_InvoiceProformasComponent/E-11_ekran.md) | [OP-E12-03](E-12_OP-03.md) sukces | formularz poprawny |
| [E-11 Lista proform](../E-11_InvoiceProformasComponent/E-11_ekran.md) | [OP-E12-06](E-12_OP-06.md) | zawsze (Anuluj) |
| [MODAL-E12-01 PdfViewer](E-12_MODAL-01.md) | [OP-E12-04](E-12_OP-04.md) | zawsze (Preview PDF) |

---

## Filtry (autocomplete)

| ID | Etykieta UI | Typ | Dokument |
|---|---|---|---|
| FILTR-E12-01 | Client Name or CUI | mat-autocomplete, kliencki | [E-12_FILTR-01.md](E-12_FILTR-01.md) |
| FILTR-E12-02 | Name (per wiersz pozycji) | mat-autocomplete, kliencki | [E-12_FILTR-02.md](E-12_FILTR-02.md) |

## Pola formularza

→ [E-12_POLA.md](E-12_POLA.md) — wszystkie pola: Client, Issue Date, Due Date, Document Series (PRF), Bank Account, Status

## Tabele i listy

| ID | Nazwa | Dokument |
|---|---|---|
| TAB-E12-01 | Tabela pozycji dokumentu | [E-12_TAB-01.md](E-12_TAB-01.md) |

## Operacje

| ID | Etykieta UI | Dokument |
|---|---|---|
| OP-E12-01 | + Add Product | [E-12_OP-01.md](E-12_OP-01.md) |
| OP-E12-02 | ✕ Usuń wiersz pozycji | [E-12_OP-02.md](E-12_OP-02.md) |
| OP-E12-03 | Save / Update | [E-12_OP-03.md](E-12_OP-03.md) |
| OP-E12-04 | Preview PDF | [E-12_OP-04.md](E-12_OP-04.md) |
| OP-E12-05 | Generate PDF ⚠️ BUG A-KRIT-04 | [E-12_OP-05.md](E-12_OP-05.md) |
| OP-E12-06 | Cancel (Anuluj) | [E-12_OP-06.md](E-12_OP-06.md) |

## Modale

| ID | Nazwa | Dokument |
|---|---|---|
| MODAL-E12-01 | PdfViewerComponent | [E-12_MODAL-01.md](E-12_MODAL-01.md) |

## Powiadomienia

| ID | Typ | Treść | Kiedy |
|---|---|---|---|
| POW-E12-01 | toastr success | „Document added successfully" | [OP-E12-03](E-12_OP-03.md) sukces (dodaj) |
| POW-E12-02 | toastr success | „Document updated successfully" | [OP-E12-03](E-12_OP-03.md) sukces (edycja) |

## Scenariusze testowe

→ [E-12_TC.md](E-12_TC.md) — prereq JWT, prereq DB, selektory CSS, 5 scenariuszy e2e (w tym weryfikacja BUG A-KRIT-04)

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint | DTO |
|---|---|---|---|
| Autofill (DocumentTypeId=2) | GET | [/api/Document/GetDocumentAutofillInfo/2](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetAutofillInfo.md) | [DTO-10](../../../05_model_danych/02_dto/DTO-10_DocumentAutofillInfoDto.md) |
| Ładowanie (edycja) | GET | [/api/Document/GetDocumentById/{id}](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetById.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Zapisz nową proformę | POST | [/api/Document/AddDocument](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Zaktualizuj proformę | PUT | [/api/Document/EditDocument](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Edit.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Podgląd PDF | POST | [/api/Document/GetInvoicePdfStream](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Generuj PDF ⚠️ | POST | [/api/Document/GenerateDocumentPdf](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GeneratePdf.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |

---

## Powiązania

| Typ | Dokument |
|---|---|
| Ekran poprzedni | [E-11 InvoiceProformasComponent](../E-11_InvoiceProformasComponent/E-11_ekran.md) |
| Ekran wzorzec | [E-10 AddOrEditInvoiceComponent](../E-10_AddOrEditInvoiceComponent/E-10_ekran.md) |
| DTO | [DTO-07 DocumentRequestDto](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| DTO | [DTO-10 DocumentAutofillInfoDto](../../../05_model_danych/02_dto/DTO-10_DocumentAutofillInfoDto.md) |
| Model DB | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Model DB | [dbo.DocumentProduct](../../../05_model_danych/01_db/dbo/dbo.DocumentProduct.md) |

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| Pola tabeli pozycji (quantity, price, vatRate) | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) | `UnitPrice × Qty × (1 + VAT/100)` — wyliczenie brutto pozycji w czasie rzeczywistym |
| Suma netto/VAT/Brutto | [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) | `calculateTotals()` z BaseInvoiceComponent |
| OP-E12-03 Zapisz (documentSeriesId) | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | DocumentTypeId=2 → seria PRF; numer PRF0001, PRF0002… |
| OP-E12-03 Zapisz (pozycje) | [wyliczeniowe/aktualizacja_produktow_dokumentu](../../../03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md) | Backend: zapis pozycji i sum do DB |
| OP-E12-05 Generuj PDF | [ALG-07 generuj_pdf_na_dysk](../../../03_algorytmy/generowania_pdf/generuj_pdf_na_dysk.md) | **⚠️ BUG A-KRIT-04:** hardcoded `InvoiceDocument` — generuje szablon „Factura" zamiast „Factura Proforma" |
| OP-E12-04 Podgląd PDF | [ALG-07 generuj_pdf_stream](../../../03_algorytmy/generowania_pdf/generuj_pdf_stream.md) | Poprawna fabryka — wybiera `ProformaDocument` dla DocumentTypeId=2 |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`add-or-edit-invoice-proforma.component.ts`](../../../../InvoiceJetUI/src/app/components/invoice-proformas/add-or-edit-invoice-proforma/add-or-edit-invoice-proforma.component.ts) |
| Klasa bazowa TS | [`base-invoice.component.ts`](../../../../InvoiceJetUI/src/app/components/invoices/base-invoice/base-invoice.component.ts) |
| Szablon HTML | [`add-or-edit-invoice-proforma.component.html`](../../../../InvoiceJetUI/src/app/components/invoice-proformas/add-or-edit-invoice-proforma/add-or-edit-invoice-proforma.component.html) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| A-KRIT-04 | **KRYTYCZNY BUG:** `Generate PDF` używa hardcoded `InvoiceDocument` zamiast `ProformaDocument` — PDF proformy tytułuje się „Factura" zamiast „Factura Proforma" |
| BA-01 | Walidacja zakomentowana w Preview PDF (dziedziczone z BaseInvoiceComponent) |
| BA-02 | `generateInvoicePdf()` ignoruje odpowiedź API |
| BA-03 | Brak `.error()` handlera dla save/update |
| BA-05 | `documentSeries` i `documentStatus` bez `Validators.required` |
| BA-07 | Brak `data-cy` / `data-testid` |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — adaptacja z wzorca E-10 i źródła faktury_proforma/dodaj_edytuj_fakture_proforma/ekran.md. |
