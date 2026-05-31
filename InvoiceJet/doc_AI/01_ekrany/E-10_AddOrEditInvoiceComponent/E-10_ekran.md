# E-10 AddOrEditInvoiceComponent — Formularz faktury

| Pole | Wartość |
|---|---|
| ID dokumentu | E-10 |
| Typ dokumentu | ekran |
| Wersja | 1.1 |
| Status | zweryfikowany |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran tworzenia i edycji faktury zwykłej (`DocumentTypeId = 1`). Logika pochodzi z `BaseInvoiceComponent`; `AddOrEditInvoiceComponent` dostarcza tylko `getDocumentTypeId() = 1` i `getNavigationUrl()`. Formularz zawiera autocomplete klienta i produktów oraz dynamiczną tabelę pozycji z obliczaniem cen w czasie rzeczywistym.

---

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────────────────┐
│ ← [Wróć]   Invoice Details - FV0007   [Unpaid chip]             │
├──────────────────────────────────────────────────────────────────┤
│ [Client Name or CUI*] [Issue Date*] [Due Date] [Status*]        │
├──────────────────────────────────────────────────────────────────┤
│ Name | Unit Price | Qty | U.M. | TVA% | Contains TVA | Total | ✕│
│ [Wiersz 1]                                                       │
│ [+ Dodaj pozycję]                                               │
├──────────────────────────────────────────────────────────────────┤
│ [Save / Update]    [Preview PDF]    [Generate PDF]              │
└──────────────────────────────────────────────────────────────────┘
```

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| URL (dodaj) | `/dashboard/add-invoice` |
| URL (edycja) | `/dashboard/edit-invoice/:id` |
| Wymagana rola | `User` (AuthGuard JWT) |
| Punkty wejścia | [OP-E09-01](../E-09_InvoicesComponent/E-09_OP-01.md); [OP-E09-02](../E-09_InvoicesComponent/E-09_OP-02.md) |
| Komponent Angular | [`AddOrEditInvoiceComponent`](../../../../InvoiceJetUI/src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.ts) |
| Klasa bazowa | [`BaseInvoiceComponent`](../../../../InvoiceJetUI/src/app/components/invoices/base-invoice/base-invoice.component.ts) |

## Tryby działania

| Tryb | URL | `isEditMode` | Zachowanie |
|---|---|---|---|
| Dodawanie | `/dashboard/add-invoice` | `false` | pusty formularz; `addDocument()` |
| Edycja | `/dashboard/edit-invoice/:id` | `true` | ładuje dokument; `updateDocument()` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek |
|---|---|---|
| [E-09 Lista faktur](../E-09_InvoicesComponent/E-09_ekran.md) | [OP-E10-03](E-10_OP-03.md) sukces | formularz poprawny |
| [E-09 Lista faktur](../E-09_InvoicesComponent/E-09_ekran.md) | [OP-E10-06](E-10_OP-06.md) | zawsze |
| [MODAL-E10-01 PdfViewer](E-10_MODAL-01.md) | [OP-E10-04](E-10_OP-04.md) | zawsze |

---

## Filtry (autocomplete)

| ID | Etykieta UI | Typ | Dokument |
|---|---|---|---|
| FILTR-E10-01 | Client Name or CUI | mat-autocomplete, kliencki | [E-10_FILTR-01.md](E-10_FILTR-01.md) |
| FILTR-E10-02 | Name (per wiersz pozycji) | mat-autocomplete, kliencki | [E-10_FILTR-02.md](E-10_FILTR-02.md) |

## Pola formularza

→ [E-10_POLA.md](E-10_POLA.md) — wszystkie 5 pól: Client, Issue Date, Due Date, Document Series, Status

## Tabele i listy

| ID | Nazwa | Dokument |
|---|---|---|
| TAB-E10-01 | Tabela pozycji dokumentu | [E-10_TAB-01.md](E-10_TAB-01.md) |

## Operacje

| ID | Etykieta UI | Dokument |
|---|---|---|
| OP-E10-01 | + Add Product | [E-10_OP-01.md](E-10_OP-01.md) |
| OP-E10-02 | ✕ Usuń wiersz pozycji | [E-10_OP-02.md](E-10_OP-02.md) |
| OP-E10-03 | Save / Update | [E-10_OP-03.md](E-10_OP-03.md) |
| OP-E10-04 | Preview PDF | [E-10_OP-04.md](E-10_OP-04.md) |
| OP-E10-05 | Generate PDF | [E-10_OP-05.md](E-10_OP-05.md) |
| OP-E10-06 | ← Wróć | [E-10_OP-06.md](E-10_OP-06.md) |

## Modale

| ID | Nazwa | Dokument |
|---|---|---|
| MODAL-E10-01 | PdfViewerComponent | [E-10_MODAL-01.md](E-10_MODAL-01.md) |

## Powiadomienia

| ID | Typ | Treść | Kiedy |
|---|---|---|---|
| POW-E10-01 | toastr success | „Document added successfully" | [OP-E10-03](E-10_OP-03.md) sukces (dodaj) |
| POW-E10-02 | toastr success | „Document updated successfully" | [OP-E10-03](E-10_OP-03.md) sukces (edycja) |

## Scenariusze testowe

→ [E-10_TC.md](E-10_TC.md) — prereq JWT, prereq DB, selektory CSS, 12 scenariuszy e2e

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint | DTO |
|---|---|---|---|
| Autofill | GET | [/api/Document/GetDocumentAutofillInfo/1](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetAutofillInfo.md) | [DTO-10](../../../05_model_danych/02_dto/DTO-10_DocumentAutofillInfoDto.md) |
| Ładowanie (edycja) | GET | [/api/Document/GetDocumentById/{id}](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetById.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Zapisz nową | POST | [/api/Document/AddDocument](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Zaktualizuj | PUT | [/api/Document/EditDocument](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Edit.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Podgląd PDF | POST | [/api/Document/GetInvoicePdfStream](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Generuj PDF | POST | [/api/Document/GenerateDocumentPdf](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GeneratePdf.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |

---

## Powiązania

| Typ | Dokument |
|---|---|
| Ekran poprzedni | [E-09 InvoicesComponent](../E-09_InvoicesComponent/E-09_ekran.md) |
| DTO | [DTO-07 DocumentRequestDto](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| DTO | [DTO-10 DocumentAutofillInfoDto](../../../05_model_danych/02_dto/DTO-10_DocumentAutofillInfoDto.md) |
| Model DB | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Model DB | [dbo.DocumentProduct](../../../05_model_danych/01_db/dbo/dbo.DocumentProduct.md) |
| Algorytm | [ALG-Wyliczeniowe-ObliczanieCenyPozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`add-or-edit-invoice.component.ts`](../../../../InvoiceJetUI/src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.ts) |
| Klasa bazowa TS | [`base-invoice.component.ts`](../../../../InvoiceJetUI/src/app/components/invoices/base-invoice/base-invoice.component.ts) |
| Walidator daty | [`date-validator.ts`](../../../../InvoiceJetUI/src/app/components/invoices/base-invoice/date-validator.ts) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| BA-01 | Walidacja zakomentowana w Preview PDF |
| BA-02 | `generateInvoicePdf()` ignoruje odpowiedź API |
| BA-03 | Brak `.error()` handlera dla save/update |
| BA-05 | `documentSeries` i `documentStatus` bez `Validators.required` |
| BA-07 | Brak `data-cy` / `data-testid` |
| BA-08 | `getInvoicePdfStream()` może użyć `undefined` `documentNumber` przy dodawaniu |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pełna wersja inline. |
| 1.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Podział na pliki — ekran.md jako indeks. |
