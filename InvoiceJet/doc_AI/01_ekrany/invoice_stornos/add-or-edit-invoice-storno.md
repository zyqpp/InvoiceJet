# Ekran: Formularz storna (Add/Edit Invoice Storno)

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-14 |
| Trasy | `/dashboard/add-invoice-storno`, `/dashboard/edit-invoice-storno/:id` |
| Komponent | `AddOrEditInvoiceStornosComponent` extends `BaseInvoiceComponent` |
| Plik | `src/app/components/invoice-stornos/add-or-edit-invoice-storno/add-or-edit-invoice-stornos.component.ts` |
| AuthGuard | TAK |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Formularz tworzenia/edycji faktury storno. Identyczny z EKRAN-10 i EKRAN-12, różni się tylko typem dokumentu.

- `getDocumentTypeId()` → `3`
- `getNavigationUrl()` → `"/dashboard/invoice-stornos"`
- Całość logiki w `BaseInvoiceComponent`

## Wywołania API

Identyczne jak EKRAN-10, ale `GetDocumentAutofillInfo/3` (DocumentTypeId=3).

## Specyfika storna

Storno może powstać:
1. Ręcznie — przez formularz (EKRAN-14)
2. Automatycznie — przez `PUT /api/Document/TransformToStorno` z listy EKRAN-13 (zaznaczenie istniejących dokumentów i ich konwersja)

W przypadku automatycznej konwersji komponent nie jest używany — akcja odbywa się bezpośrednio z listy.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
