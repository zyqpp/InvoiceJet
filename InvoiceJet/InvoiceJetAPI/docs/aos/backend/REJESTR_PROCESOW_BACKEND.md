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

---

## Procesy do przygotowania

| Nr | Proces | Kontroler | Metody / endpointy |
|---|---|---|---|
| P-03 | Rejestracja użytkownika | `AuthController` | `POST /api/Auth/register` |
| P-04 | Logowanie użytkownika | `AuthController` | `POST /api/Auth/login` |
| P-05 | Pobranie firmy z ANAF | `FirmController` | `GET /api/Firm/fromAnaf/{cui}` |
| P-06 | Edycja firmy | `FirmController` | `PUT /api/Firm/EditFirm/{isClient}` |
| P-07 | Pobranie aktywnej firmy użytkownika | `FirmController` | `GET /api/Firm/GetUserActiveFirm` |
| P-08 | Zarządzanie firmami-klientami | `FirmController` | `GET /api/Firm/GetUserClientFirms`, `PUT /api/Firm/DeleteFirms` |
| P-09 | Zarządzanie produktami | `ProductController` | `GET`, `POST`, `PUT` endpointy produktu |
| P-10 | Zarządzanie kontami bankowymi | `BankAccountController` | `GET`, `POST`, `PUT` endpointy kont |
| P-11 | Zarządzanie seriami dokumentów | `DocumentSeriesController` | `GET`, `POST`, `PUT` endpointy serii |
| P-12 | Dane autouzupełniania dokumentu | `DocumentController` | `GET /api/Document/GetDocumentAutofillInfo/{documentTypeId}` |
| P-13 | Edycja dokumentu | `DocumentController` | `PUT /api/Document/EditDocument` |
| P-14 | Lista i szczegóły dokumentów | `DocumentController` | `GET /api/Document/GetDocumentTableRecords/{documentTypeId}`, `GET /api/Document/GetDocumentById/{documentId}` |
| P-15 | Usuwanie dokumentów | `DocumentController` | `PUT /api/Document/DeleteDocuments` |
| P-16 | Generowanie dokumentu PDF | `DocumentController` | `POST /api/Document/GenerateDocumentPdf` |
| P-17 | Pobranie strumienia PDF faktury | `DocumentController` | `POST /api/Document/GetInvoicePdfStream` |
| P-18 | Statystyki dashboardu | `DocumentController` | `GET /api/Document/GetDashboardStats/{year}/{documentType}` |
| P-19 | Transformacja faktury do storna | `DocumentController` | `PUT /api/Document/TransformToStorno` |

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
