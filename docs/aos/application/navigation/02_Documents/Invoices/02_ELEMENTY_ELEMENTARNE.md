# Invoices - Elementy elementarne

| Element | Typ | Komponent | Opis |
|---|---|---|---|
| Lista faktur | ekran | `InvoicesComponent` | Grid dokumentow typu `1`. |
| Formularz faktury | ekran potomny | `AddOrEditInvoiceComponent` | Dodanie albo edycja faktury. |
| Grid pozycji | fragment formularza | `BaseInvoiceComponent` | Pozycje dokumentu w `FormArray`. |
| Podglad PDF | dialog | `PdfViewerComponent` | Wyswietla blob PDF z API. |
| Transformacja do storna | operacja masowa | `InvoicesComponent.transformToStorno()` | Zmienia typ dokumentu na storno. |
