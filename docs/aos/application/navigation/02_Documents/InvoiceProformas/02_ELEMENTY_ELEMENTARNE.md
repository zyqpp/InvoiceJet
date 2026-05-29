# Invoice Proformas - Elementy elementarne

| Element | Typ | Komponent | Opis |
|---|---|---|---|
| Lista proform | ekran | `InvoiceProformasComponent` | Grid dokumentow typu `2`. |
| Formularz proformy | ekran potomny | `AddOrEditInvoiceProformaComponent` | Dodanie albo edycja proformy. |
| Podglad PDF | dialog | `PdfViewerComponent` | Podglad wygenerowanego PDF. |
| Usuwanie | operacja masowa | `deleteSelected()` | Wywoluje `DeleteDocuments`. |
