# Invoice Stornos - Elementy elementarne

| Element | Typ | Komponent | Opis |
|---|---|---|---|
| Lista storn | ekran | `InvoiceStornosComponent` | Grid dokumentow typu `3`. |
| Formularz storna | ekran potomny | `AddOrEditInvoiceStornosComponent` | Edycja dokumentu storno. |
| Podglad PDF | dialog | `PdfViewerComponent` | Podglad wygenerowanego PDF. |
| Usuwanie | operacja masowa | `deleteSelected()` | Wywoluje `DeleteDocuments`. |
