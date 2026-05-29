# Documents - Diagram sekcji

## 1. Diagram

```mermaid
flowchart TD
  Documents["Menu: Documents"]
  Documents --> Invoices["Invoices"]
  Documents --> Proformas["Invoice Proformas"]
  Documents --> Stornos["Invoice Stornos"]
  Invoices --> AddInvoice["Add invoice"]
  Invoices --> EditInvoice["Edit invoice"]
  Invoices --> Transform["Transform to storno"]
  Proformas --> AddProforma["Add proforma"]
  Proformas --> EditProforma["Edit proforma"]
  Stornos --> EditStorno["Edit storno"]
```

## 2. Linki

| Pozycja | Route | Dokument pozycji |
|---|---|---|
| Invoices | `/dashboard/invoices` | [Invoices](./Invoices/01_MAPA_MAKIET_POZYCJI.md) |
| Invoice Proformas | `/dashboard/invoice-proformas` | [InvoiceProformas](./InvoiceProformas/01_MAPA_MAKIET_POZYCJI.md) |
| Invoice Stornos | `/dashboard/invoice-stornos` | [InvoiceStornos](./InvoiceStornos/01_MAPA_MAKIET_POZYCJI.md) |
