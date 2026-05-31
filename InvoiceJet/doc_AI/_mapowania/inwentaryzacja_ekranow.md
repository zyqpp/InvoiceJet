# Inwentaryzacja ekranów — komponenty Angular

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Źródło | `InvoiceJetUI/src/app/app-routing.module.ts` + eksploracja komponentów |

## 1. Trasy aplikacji (17)

| Trasa URL | Komponent | AuthGuard | Typ trasy |
|---|---|---|---|
| `/login` | `LoginComponent` | NIE | strona publiczna |
| `/register` | `RegisterComponent` | NIE | strona publiczna |
| `/dashboard` | `DashboardComponent` | TAK | widok główny |
| `/dashboard/firm-details` | `FirmDetailsComponent` | TAK | ustawienia |
| `/dashboard/clients` | `ClientsComponent` | TAK | lista |
| `/dashboard/bank-accounts` | `BankAccountsComponent` | TAK | lista |
| `/dashboard/products` | `ProductsComponent` | TAK | lista |
| `/dashboard/document-series` | `DocumentSeriesComponent` | TAK | lista |
| `/dashboard/invoices` | `InvoicesComponent` | TAK | lista |
| `/dashboard/add-invoice` | `AddOrEditInvoiceComponent` | TAK | formularz |
| `/dashboard/edit-invoice/:id` | `AddOrEditInvoiceComponent` | TAK | formularz (edycja) |
| `/dashboard/invoice-proformas` | `InvoiceProformasComponent` | TAK | lista |
| `/dashboard/add-invoice-proforma` | `AddOrEditInvoiceProformaComponent` | TAK | formularz |
| `/dashboard/edit-invoice-proforma/:id` | `AddOrEditInvoiceProformaComponent` | TAK | formularz (edycja) |
| `/dashboard/invoice-stornos` | `InvoiceStornosComponent` | TAK | lista |
| `/dashboard/edit-invoice-storno/:id` | `AddOrEditInvoiceStornosComponent` | TAK | formularz (edycja) |
| `**` (wildcard) | `DashboardComponent` | TAK | fallback |

> **Uwaga:** Trasa `/dashboard/add-invoice-storno` nie istnieje. Nowe storno tworzone jest wyłącznie przez `PUT /Document/TransformToStorno` z poziomu `InvoicesComponent`.

## 2. Komponenty z trasą (ekrany)

| ID | Komponent | Trasa | Plik | Dokument | Status |
|---|---|---|---|---|---|
| EKRAN-01 | `LoginComponent` | `/login` | `components/login/login.component.ts` | [link](../01_ekrany/login/login.md) | szkic |
| EKRAN-02 | `RegisterComponent` | `/register` | `components/register/register.component.ts` | [link](../01_ekrany/register/register.md) | szkic |
| EKRAN-03 | `DashboardComponent` | `/dashboard` | `components/dashboard/dashboard.component.ts` | [link](../01_ekrany/dashboard/dashboard.md) | szkic |
| EKRAN-04 | `FirmDetailsComponent` | `/dashboard/firm-details` | `components/firm/firm-details/firm-details.component.ts` | [link](../01_ekrany/firm_details/firm-details.md) | szkic |
| EKRAN-05 | `ClientsComponent` | `/dashboard/clients` | `components/firm/clients/clients.component.ts` | [link](../01_ekrany/clients/clients.md) | szkic |
| EKRAN-06 | `BankAccountsComponent` | `/dashboard/bank-accounts` | `components/firm/bank-accounts/bank-accounts.component.ts` | [link](../01_ekrany/bank_accounts/bank-accounts.md) | szkic |
| EKRAN-07 | `ProductsComponent` | `/dashboard/products` | `components/products/products.component.ts` | [link](../01_ekrany/products/products.md) | szkic |
| EKRAN-08 | `DocumentSeriesComponent` | `/dashboard/document-series` | `components/document-series/document-series.component.ts` | [link](../01_ekrany/document_series/document-series.md) | szkic |
| EKRAN-09 | `InvoicesComponent` | `/dashboard/invoices` | `components/invoices/invoices.component.ts` | [link](../01_ekrany/invoices/invoices.md) | szkic |
| EKRAN-10 | `AddOrEditInvoiceComponent` | `/dashboard/add-invoice`, `/dashboard/edit-invoice/:id` | `components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.ts` | [link](../01_ekrany/invoices/add-or-edit-invoice.md) | szkic |
| EKRAN-11 | `InvoiceProformasComponent` | `/dashboard/invoice-proformas` | `components/invoice-proformas/invoice-proformas.component.ts` | [link](../01_ekrany/invoice_proformas/invoice-proformas.md) | szkic |
| EKRAN-12 | `AddOrEditInvoiceProformaComponent` | `/dashboard/add-invoice-proforma`, `/dashboard/edit-invoice-proforma/:id` | `components/invoice-proformas/add-or-edit-invoice-proforma/add-or-edit-invoice-proforma.component.ts` | [link](../01_ekrany/invoice_proformas/add-or-edit-invoice-proforma.md) | szkic |
| EKRAN-13 | `InvoiceStornosComponent` | `/dashboard/invoice-stornos` | `components/invoice-stornos/invoice-stornos.component.ts` | [link](../01_ekrany/invoice_stornos/invoice-stornos.md) | szkic |
| EKRAN-14 | `AddOrEditInvoiceStornosComponent` | `/dashboard/edit-invoice-storno/:id` | `components/invoice-stornos/add-or-edit-invoice-stornos/add-or-edit-invoice-stornos.component.ts` | [link](../01_ekrany/invoice_stornos/add-or-edit-invoice-storno.md) | szkic |

## 3. Komponenty dialogowe (6)

| ID | Komponent | Otwiera | Plik | Dokument | Status |
|---|---|---|---|---|---|
| DIALOG-01 | `AddEditClientDialogComponent` | `ClientsComponent` | `components/firm/add-edit-client-dialog/add-edit-client-dialog.component.ts` | [link](../01_ekrany/clients/add-edit-client-dialog.md) | szkic |
| DIALOG-02 | `AddOrEditBankAccountDialogComponent` | `BankAccountsComponent` | `components/firm/bank-accounts/add-or-edit-bank-account-dialog/add-or-edit-bank-account-dialog.component.ts` | [link](../01_ekrany/bank_accounts/add-or-edit-bank-account-dialog.md) | szkic |
| DIALOG-03 | `AddOrEditProductDialogComponent` | `ProductsComponent` | `components/products/add-or-edit-product-dialog/add-or-edit-product-dialog.component.ts` | [link](../01_ekrany/products/add-or-edit-product-dialog.md) | szkic |
| DIALOG-04 | `AddOrEditDocumentSeriesDialogComponent` | `DocumentSeriesComponent` | `components/document-series/add-or-edit-document-series-dialog/add-or-edit-document-series-dialog.component.ts` | [link](../01_ekrany/document_series/add-or-edit-document-series-dialog.md) | szkic |
| DIALOG-05 | `PdfViewerComponent` | `BaseInvoiceComponent` | `components/pdf-viewer/pdf-viewer.component.ts` | [link](../01_ekrany/shared/pdf-viewer.md) | szkic |
| DIALOG-06 | `TokenExpiredDialogComponent` | `AuthInterceptor` | `components/token-expired-dialog/token-expired-dialog.component.ts` | [link](../01_ekrany/shared/token-expired-dialog.md) | szkic |

## 4. Komponenty layout (3)

| ID | Komponent | Rola | Plik | Dokument | Status |
|---|---|---|---|---|---|
| LAYOUT-01 | `AppComponent` | root shell, chowa navbar na login/register | `app.component.ts` | [link](../01_ekrany/shared/app.md) | szkic |
| LAYOUT-02 | `NavbarComponent` | górna belka, logout, toggle sidebar, toggle theme | `components/navbar/navbar.component.ts` | [link](../01_ekrany/shared/navbar.md) | szkic |
| LAYOUT-03 | `SidebarComponent` | boczne drzewo nawigacji z filtrowaniem | `components/sidebar/sidebar.component.ts` | [link](../01_ekrany/shared/sidebar.md) | szkic |

## 5. Komponenty abstrakcyjne / bazowe (1)

| ID | Komponent | Rola | Plik |
|---|---|---|---|
| BASE-01 | `BaseInvoiceComponent` | klasa bazowa dla AddOrEditInvoice/Proforma/Storno; zawiera całą logikę formularza faktury | `components/invoices/base-invoice/base-invoice.component.ts` |

## 6. Anomalie UI

| # | Anomalia |
|---|---|
| UI-A01 | `addNewClient()` w `FirmDetailsComponent` zawiera tylko `console.log("Add new client")` — niezaimplementowana funkcja |
| UI-A02 | `initForm()` w `AddOrEditProductDialogComponent` — pusta metoda, martwy kod |
| UI-A03 | `isFormChanged()` w `FirmDetailsComponent` — błędna logika: porównuje `initialFormValues.value` (undefined) z `initialFormValues`; wynik zawsze `false` |
| UI-A04 | `ngOnInit()` puste (bez ciała) w `NavbarComponent` i `PdfViewerComponent` |
| UI-A05 | Podwójne `selection.clear()` w `DocumentSeriesComponent.deleteSelected()` |
| UI-A06 | Zakomentowana walidacja `// if (this.invoiceForm.invalid) return;` w `BaseInvoiceComponent.getInvoicePdfStream()` |
| UI-A07 | `generateInvoicePdf()` ignoruje odpowiedź serwera — wyłącznie `console.log("Invoice pdf generated successfully")` |
| UI-A08 | `UserService.getUserByEmail()` — wstrzykiwany w `AuthService` jako `public userService`, nigdy niewywoływany |
| UI-A09 | `MatSnackBar` wstrzykiwany w `AddOrEditBankAccountDialogComponent` ale nieużywany |
| UI-A10 | `Subject` importowany w `FirmService` ale nieużywany |
| UI-A11 | `MatDialog` importowany (nie wstrzykiwany) w `AuthGuard` — zbędny import |
| UI-A12 | Co najmniej 19 aktywnych wywołań `console.log` w kodzie produkcyjnym |
| UI-A13 | `IDocumentProduct.document?: Document` — pole typowane jako globalny typ DOM `Document`, nie jako `IDocument` — błąd typowania |
| UI-A14 | `IDocumentProductRequest.id?: 0` — typ pola `id` to literał `0`, nie `number` — błąd TypeScript |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Inwentaryzacja na podstawie eksploracji kodu Angular. |
