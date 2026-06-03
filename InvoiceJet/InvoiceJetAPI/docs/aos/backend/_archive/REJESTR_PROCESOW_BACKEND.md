# Rejestr procesów backendowych — InvoiceJetAPI

**Data utworzenia:** 2026-05-29
**Status:** Roboczy
**Źródło:** `InvoiceJetAPI`

---

## Procesy udokumentowane

| Nr | Proces | Katalog | Endpoint główny | Status |
|---|---|---|---|---|
| P-01 | Wystawienie nowej faktury | [P-01_IssueNewInvoice](processes/P-01_IssueNewInvoice) | `POST /api/Document/AddDocument` | Do weryfikacji technicznej |
| P-02 | Dodanie firmy | [P-02_AddFirm](processes/P-02_AddFirm) | `POST /api/Firm/AddFirm/{isClient}` | Do weryfikacji technicznej |
| P-03 | Rejestracja użytkownika | [P-03_RegisterUser](processes/P-03_RegisterUser) | `POST /api/Auth/register` | Do weryfikacji technicznej |
| P-04 | Logowanie użytkownika | [P-04_LoginUser](processes/P-04_LoginUser) | `POST /api/Auth/login` | Do weryfikacji technicznej |
| P-05 | Pobranie firmy z ANAF | [P-05_GetFirmFromAnaf](processes/P-05_GetFirmFromAnaf) | `GET /api/Firm/fromAnaf/{cui}` | Do weryfikacji technicznej |
| P-06 | Edycja firmy | [P-06_EditFirm](processes/P-06_EditFirm) | `PUT /api/Firm/EditFirm/{isClient}` | Do weryfikacji technicznej |
| P-07 | Pobranie aktywnej firmy użytkownika | [P-07_GetUserActiveFirm](processes/P-07_GetUserActiveFirm) | `GET /api/Firm/GetUserActiveFirm` | Do weryfikacji technicznej |
| P-08 | Zarządzanie firmami-klientami | [P-08_ManageClientFirms](processes/P-08_ManageClientFirms) | `GET /api/Firm/GetUserClientFirms`, `PUT /api/Firm/DeleteFirms` | Do weryfikacji technicznej |
| P-09 | Zarządzanie produktami | [P-09_ManageProducts](processes/P-09_ManageProducts) | `GET/POST/PUT /api/Product/*` | Do weryfikacji technicznej |
| P-10 | Zarządzanie kontami bankowymi | [P-10_ManageBankAccounts](processes/P-10_ManageBankAccounts) | `GET/POST/PUT /api/BankAccount/*` | Do weryfikacji technicznej |
| P-11 | Zarządzanie seriami dokumentów | [P-11_ManageDocumentSeries](processes/P-11_ManageDocumentSeries) | `GET/POST/PUT /api/DocumentSeries/*` | Do weryfikacji technicznej |
| P-12 | Dane autouzupełniania dokumentu | [P-12_GetDocumentAutofillInfo](processes/P-12_GetDocumentAutofillInfo) | `GET /api/Document/GetDocumentAutofillInfo/{documentTypeId}` | Do weryfikacji technicznej |
| P-13 | Edycja dokumentu | [P-13_EditDocument](processes/P-13_EditDocument) | `PUT /api/Document/EditDocument` | Do weryfikacji technicznej |
| P-14 | Lista i szczegóły dokumentów | [P-14_GetDocumentListAndDetails](processes/P-14_GetDocumentListAndDetails) | `GET /api/Document/GetDocumentTableRecords/{documentTypeId}`, `GET /api/Document/GetDocumentById/{documentId}` | Do weryfikacji technicznej |
| P-15 | Usuwanie dokumentów | [P-15_DeleteDocuments](processes/P-15_DeleteDocuments) | `PUT /api/Document/DeleteDocuments` | Do weryfikacji technicznej |
| P-16 | Generowanie dokumentu PDF | [P-16_GenerateDocumentPdf](processes/P-16_GenerateDocumentPdf) | `POST /api/Document/GenerateDocumentPdf` | Do weryfikacji technicznej |
| P-17 | Pobranie strumienia PDF faktury | [P-17_GetInvoicePdfStream](processes/P-17_GetInvoicePdfStream) | `POST /api/Document/GetInvoicePdfStream` | Do weryfikacji technicznej |
| P-18 | Statystyki dashboardu | [P-18_GetDashboardStats](processes/P-18_GetDashboardStats) | `GET /api/Document/GetDashboardStats/{year}/{documentType}` | Do weryfikacji technicznej |
| P-19 | Transformacja faktury do storna | [P-19_TransformInvoiceToStorno](processes/P-19_TransformInvoiceToStorno) | `PUT /api/Document/TransformToStorno` | Do weryfikacji technicznej |

---

## Procesy do przygotowania

Brak. Lista `P-01` do `P-19` została utworzona.

---

## Zasady numeracji

Procesy numerowane są w kolejności dokumentowania. Numer nie musi odpowiadać kolejności kontrolerów w projekcie.

---

## Zakres źródeł

- `InvoiceJet.Presentation/Controllers`
- `InvoiceJet.Application/Services/Impl`
- `InvoiceJet.Application/DTOs`
- `InvoiceJet.Application/MappingProfiles`
- `InvoiceJet.Domain/Models`
- `InvoiceJet.Domain/Exceptions`
- `InvoiceJet.Infrastructure/Persistence`
