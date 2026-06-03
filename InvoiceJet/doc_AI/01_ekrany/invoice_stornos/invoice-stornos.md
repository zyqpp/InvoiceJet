# Ekran: Lista storn (Invoice Stornos)

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-13 |
| Trasa | `/dashboard/invoice-stornos` |
| Komponent | `InvoiceStornosComponent` |
| Plik | `src/app/components/invoice-stornos/invoice-stornos.component.ts` |
| AuthGuard | TAK |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Lista faktur storno (DocumentTypeId=3). Brak możliwości tworzenia nowego storno z tego ekranu — storno tworzone jest wyłącznie przez `TransformToStorno` z ekranu faktur.

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie | `GET /api/Document/GetDocumentTableRecords/3` |
| Usunięcie | `PUT /api/Document/DeleteDocuments` |

## Nawigacja

| Akcja | Cel |
|---|---|
| Edycja storno | `/dashboard/edit-invoice-storno/:id` |

**Brak** `openNewInvoiceStornoDialog()` / trasy `/add-invoice-storno`.

## Anomalie

- `console.log(this.selection.selected)` i `console.log(documentIds)` w `deleteSelected()`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
