# Ekran: Formularz proformy (Add/Edit Invoice Proforma)

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-12 |
| Trasy | `/dashboard/add-invoice-proforma`, `/dashboard/edit-invoice-proforma/:id` |
| Komponent | `AddOrEditInvoiceProformaComponent` extends `BaseInvoiceComponent` |
| Plik | `src/app/components/invoice-proformas/add-or-edit-invoice-proforma/add-or-edit-invoice-proforma.component.ts` |
| AuthGuard | TAK |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Formularz tworzenia/edycji proformy. Identyczny z EKRAN-10, różni się tylko typem dokumentu.

- `getDocumentTypeId()` → `2`
- `getNavigationUrl()` → `"/dashboard/invoice-proformas"`
- Całość logiki w `BaseInvoiceComponent`

## Wywołania API

Identyczne jak EKRAN-10, ale `GetDocumentAutofillInfo/2` (DocumentTypeId=2).

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
