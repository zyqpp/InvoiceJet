# Invoice Proformas - Elementy elementarne

| Element | Typ | Komponent | Opis |
|---|---|---|---|
| Lista proform | ekran | `InvoiceProformasComponent` | Grid dokumentów typu `2`. |
| Formularz proformy | ekran potomny | `AddOrEditInvoiceProformaComponent` | Dodanie albo edycja proformy. |
| Podgląd PDF | dialog | `PdfViewerComponent` | Podgląd wygenerowanego PDF. |
| Usuwanie | operacja masowa | `deleteSelected()` | Wywołuje `DeleteDocuments`. |
