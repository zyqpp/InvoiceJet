# Rejestr przepływów aplikacji

**Aplikacja:** InvoiceJet
**Status:** Roboczy
**Data utwórzenia:** 2026-05-29

## 1. Lista przepływów

| ID | Nazwa | Sekcja menu | Ekran frontend | Proces backend | Status |
|---|---|---|---|---|---|
| `A-00` | AppShell | Global | `E-00_AppShell` | `P-04_LoginUser` | Do przygotowania |
| `A-01` | Dashboard | Dashboard | `E-01_Dashboard` | `P-18_GetDashboardStats` | Do przygotowania |
| `A-02` | Invoices | Documents | `E-02_Invoices` | `P-14`, `P-15`, `P-19` | Do przygotowania |
| `A-03` | Invoice Proformas | Documents | `E-03_InvoiceProformas` | `P-14`, `P-15` | Do przygotowania |
| `A-04` | Invoice Stornos | Documents | `E-04_InvoiceStornos` | `P-14`, `P-15` | Do przygotowania |
| `A-05` | Issue New Invoice | Documents | `E-05_InvoiceDetails` | `P-01_IssueNewInvoice` | Utwórzony |
| `A-06` | Clients | Inventory | `E-06_Clients` | `P-08_ManageClientFirms`, `P-05_GetFirmFromAnaf` | Do przygotowania |
| `A-07` | Products | Inventory | `E-07_Products` | `P-09_ManageProducts` | Do przygotowania |
| `A-08` | Firm Details | Settings | `E-08_FirmDetails` | `P-02_AddFirm`, `P-06_EditFirm`, `P-07_GetUserActiveFirm` | Do przygotowania |
| `A-09` | Bank Accounts | Settings | `E-09_BankAccounts` | `P-10_ManageBankAccounts` | Do przygotowania |
| `A-10` | Document Series | Settings | `E-10_DocumentSeries` | `P-11_ManageDocumentSeries` | Do przygotowania |
| `A-11` | Login | Public | `E-11_Login` | `P-04_LoginUser` | Do przygotowania |
| `A-12` | Register | Public | `E-12_Register` | `P-03_RegisterUser` | Do przygotowania |

## 2. Linki główne

| Dokument | Link |
|---|---|
| Mapa Nawigacji i Makiet | [MAPA_NAWIGACJI_I_MAKIET.md](./MAPA_NAWIGACJI_I_MAKIET.md) |
| Pierwszy pełny przepływ | [A-05_IssueNewInvoice](./flows/A-05_IssueNewInvoice/00_METADANE.md) |
| Wytyczne agenta | [FullStackAgentAI](../../FullStackAgentAI/01_ZASADY_AOS_APLIKACYJNEGO.md) |
