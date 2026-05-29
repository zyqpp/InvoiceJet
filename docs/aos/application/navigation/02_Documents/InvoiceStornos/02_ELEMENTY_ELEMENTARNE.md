# Invoice Stornos - Elementy elementarne

| Element | Typ | Komponent | Opis |
|---|---|---|---|
| Lista storn | ekran | `InvoiceStornosComponent` | Grid dokumentów typu `3`. |
| Formularz storna | ekran potomny | `AddOrEditInvoiceStornosComponent` | Edycja dokumentu storno. |
| Podgląd PDF | dialog | `PdfViewerComponent` | Podgląd wygenerowanego PDF. |
| Usuwanie | operacja masowa | `deleteSelected()` | Wywołuje `DeleteDocuments`. |
