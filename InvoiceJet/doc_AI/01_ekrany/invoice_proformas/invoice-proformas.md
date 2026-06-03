# Ekran: Lista proform (Invoice Proformas)

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-11 |
| Trasa | `/dashboard/invoice-proformas` |
| Komponent | `InvoiceProformasComponent` |
| Plik | `src/app/components/invoice-proformas/invoice-proformas.component.ts` |
| AuthGuard | TAK |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Lista faktur proforma (DocumentTypeId=2). Identyczna struktura jak `InvoicesComponent`, bez funkcji TransformToStorno.

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie | `GET /api/Document/GetDocumentTableRecords/2` |
| Usunięcie | `PUT /api/Document/DeleteDocuments` |

## Nawigacja

| Akcja | Cel |
|---|---|
| Nowa proforma | `/dashboard/add-invoice-proforma` |
| Edycja | `/dashboard/edit-invoice-proforma/:id` |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
