# Ekran: Formularz faktury (Add/Edit Invoice)

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-10 |
| Trasy | `/dashboard/add-invoice`, `/dashboard/edit-invoice/:id` |
| Komponent | `AddOrEditInvoiceComponent` extends `BaseInvoiceComponent` |
| Plik | `src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.ts` |
| Klasa bazowa | `src/app/components/invoices/base-invoice/base-invoice.component.ts` |
| AuthGuard | TAK |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Formularz tworzenia i edycji faktury zwykłej (DocumentTypeId=1). Logika w klasie abstrakcyjnej `BaseInvoiceComponent`. `AddOrEditInvoiceComponent` implementuje tylko `getDocumentTypeId()` → `1` i `getNavigationUrl()` → `"/dashboard/invoices"`.

## Tryby działania

| Tryb | URL | Zachowanie |
|---|---|---|
| Dodawanie | `/dashboard/add-invoice` | `isEditMode = false`; brak `id` w route |
| Edycja | `/dashboard/edit-invoice/:id` | `isEditMode = true`; ładuje dokument przez API |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie autofill (ngOnInit) | `GET /api/Document/GetDocumentAutofillInfo/1` |
| Załadowanie dokumentu (tryb edycji) | `GET /api/Document/GetDocumentById/{id}` |
| Submit (dodanie) | `POST /api/Document/AddDocument` |
| Submit (edycja) | `PUT /api/Document/EditDocument` |
| Generowanie PDF (zapis na dysk) | `POST /api/Document/GenerateDocumentPdf` |
| Podgląd PDF (strumień) | `POST /api/Document/GetInvoicePdfStream` → otwiera `PdfViewerComponent` |

## Pola formularza (BaseInvoiceComponent)

| Pole | Opis |
|---|---|
| Klient | `mat-autocomplete` — filtrowanie po nazwie firmy |
| Seria dokumentu | `mat-select` — wybór serii (wg DocumentTypeId) |
| Data wystawienia | `mat-datepicker` |
| Termin płatności | `mat-datepicker` |
| Status | `mat-select` — `Unpaid`/`Paid` |
| Tabela produktów | `MatTableDataSource` — dynamiczna lista pozycji |

## Kolumny tabeli produktów

`name`, `unitPrice`, `quantity`, `unitOfMeasurement`, `tvaValue`, `containsTva`, `totalPrice`, `actions`

## Anomalie (BaseInvoiceComponent)

| # | Anomalia |
|---|---|
| BA-01 | Zakomentowana walidacja: `// if (this.invoiceForm.invalid) return;` w `getInvoicePdfStream()` |
| BA-02 | `generateInvoicePdf()` — ignoruje odpowiedź API; wyłącznie `console.log("Invoice pdf generated successfully")` |
| BA-03 | 6 aktywnych `console.log` w kodzie |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
