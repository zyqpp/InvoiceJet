# InvoiceJet — Indeks ekranów dla Figmy

> **Po co ten plik:** mapa „co budujemy i z czego". Agent czyta TEN indeks, a potem
> dla budowanego ekranu otwiera DOKŁADNIE JEDEN dokument źródłowy (kolumna „Doc").
> Nie eksploruje kodu na ślepo. Źródło: `doc_AI/_mapowania/inwentaryzacja_ekranow.md`.

Ścieżki „Doc" są względne wobec `doc_AI/01_ekrany/`.
Status budowy śledzimy w `figma/progress.md`.

## Ekrany z trasą (14)

| ID | Ekran | Trasa | Doc | Strona Figma |
|---|---|---|---|---|
| EKRAN-01 | Login | `/login` | `login/login.md` | 02 · Auth |
| EKRAN-02 | Rejestracja | `/register` | `register/register.md` | 02 · Auth |
| EKRAN-03 | Dashboard | `/dashboard` | `dashboard/dashboard.md` | 04 · Dashboard |
| EKRAN-04 | Dane firmy | `/dashboard/firm-details` | `firm_details/firm-details.md` | 12 · Firma |
| EKRAN-05 | Klienci (lista) | `/dashboard/clients` | `clients/clients.md` | 09 · Klienci |
| EKRAN-06 | Konta bankowe (lista) | `/dashboard/bank-accounts` | `bank_accounts/bank-accounts.md` | 10 · Konta bankowe |
| EKRAN-07 | Produkty (lista) | `/dashboard/products` | `products/products.md` | 08 · Produkty |
| EKRAN-08 | Serie dokumentów (lista) | `/dashboard/document-series` | `document_series/document-series.md` | 11 · Serie |
| EKRAN-09 | Faktury (lista) | `/dashboard/invoices` | `invoices/invoices.md` | 05 · Faktury |
| EKRAN-10 | Faktura — dodaj/edytuj | `/dashboard/add-invoice`, `/edit-invoice/:id` | `invoices/add-or-edit-invoice.md` | 05 · Faktury |
| EKRAN-11 | Proformy (lista) | `/dashboard/invoice-proformas` | `invoice_proformas/invoice-proformas.md` | 06 · Proformy |
| EKRAN-12 | Proforma — dodaj/edytuj | `/dashboard/add-invoice-proforma`, `/edit-...` | `invoice_proformas/add-or-edit-invoice-proforma.md` | 06 · Proformy |
| EKRAN-13 | Storna (lista) | `/dashboard/invoice-stornos` | `invoice_stornos/invoice-stornos.md` | 07 · Storna |
| EKRAN-14 | Storno — edytuj | `/dashboard/edit-invoice-storno/:id` | `invoice_stornos/add-or-edit-invoice-storno.md` | 07 · Storna |

## Modale / dialogi (6)

| ID | Dialog | Otwiera | Doc | Strona Figma |
|---|---|---|---|---|
| DIALOG-01 | Klient — dodaj/edytuj | Klienci | `clients/add-edit-client-dialog.md` | 09 · Klienci |
| DIALOG-02 | Konto bankowe — dodaj/edytuj | Konta bankowe | `bank_accounts/add-or-edit-bank-account-dialog.md` | 10 · Konta bankowe |
| DIALOG-03 | Produkt — dodaj/edytuj | Produkty | `products/add-or-edit-product-dialog.md` | 08 · Produkty |
| DIALOG-04 | Seria — dodaj/edytuj | Serie dokumentów | `document_series/add-or-edit-document-series-dialog.md` | 11 · Serie |
| DIALOG-05 | Podgląd PDF | Formularz faktury | `_wspolne/pdf-viewer.md` | 05 · Faktury |
| DIALOG-06 | Sesja wygasła | AuthInterceptor | `_wspolne/token-expired-dialog.md` | 02 · Auth |

## Layout wspólny (3) + bazowy (1)

| ID | Element | Doc | Strona Figma |
|---|---|---|---|
| LAYOUT-01 | App shell (chowa navbar na login/register) | `_wspolne/app-component.md` | 03 · Layout |
| LAYOUT-02 | Navbar (logout, toggle sidebar, toggle motyw) | `_wspolne/navbar.md` | 03 · Layout |
| LAYOUT-03 | Sidebar (drzewo nawigacji) | `_wspolne/sidebar.md` | 03 · Layout |
| BASE-01 | BaseInvoiceComponent (logika formularza faktury) | `_wspolne/base-invoice-component.md` | (wzorzec dla EKRAN-10/12/14) |

## Uwagi z dokumentacji
- Brak trasy `add-invoice-storno` — nowe storno powstaje przez `PUT /Document/TransformToStorno` z listy faktur.
- Formularze faktury/proformy/storna dzielą `BaseInvoiceComponent` → w Figmie jeden wzorzec formularza, warianty per typ dokumentu.
