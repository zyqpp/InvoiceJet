# Wystawienie nowej faktury - Metadane

| Atrybut | Wartosc |
|---|---|
| Aplikacja | InvoiceJet |
| ID przeplywu | `A-05` |
| Nazwa | Wystawienie nowej faktury |
| Sekcja menu | Documents > Invoices |
| Route | `/dashboard/add-invoice` |
| Route edycji | `/dashboard/edit-invoice/:id` |
| AOS frontend | `E-05_InvoiceDetails` |
| AOS backend | `P-01_IssueNewInvoice`, `P-12_GetDocumentAutofillInfo`, `P-13_EditDocument`, `P-17_GetInvoicePdfStream` |
| Komponenty Angular | `AddOrEditInvoiceComponent`, `BaseInvoiceComponent`, `PdfViewerComponent` |
| Serwis Angular | `DocumentService` |
| Kontroler API | `DocumentController` |
| Serwis backendowy | `DocumentService` |
| Glowne encje | `Document`, `DocumentProduct`, `Product`, `DocumentSeries`, `Firm`, `BankAccount` |
| Status | Roboczy |
| Data utworzenia | 2026-05-29 |
