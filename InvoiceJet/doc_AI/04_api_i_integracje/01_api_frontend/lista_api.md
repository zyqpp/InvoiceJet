# Lista endpointów API — InvoiceJet

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| Autor | Agent Claudiusz Sonte 4.6 max |
| Wersja | 1.0 |
| Data | 2026-05-31 |
| Status | Obowiązujący |
| Liczba endpointów | 31 |
| Endpointy publiczne | 2 (API-01, API-02) |
| Endpointy chronione | 29 (JWT Bearer + rola `User`) |

## Streszczenie

31 endpointów REST API wystawianych przez backend ASP.NET Core 8 i konsumowanych przez frontend Angular 16. Wszystkie endpointy mają wspólny prefiks `/api/`. Dwa endpointy (rejestracja i logowanie) są publicznie dostępne bez autoryzacji. Wszystkie pozostałe wymagają JWT Bearer Token z claimem `userId` i rolą `User`, egzekwowanym przez atrybut `[Authorize(Roles = "User")]` na kontrolerach.

## Tabela endpointów

| ID | Metoda | URL | Auth | Rola | Opis | Plik dokumentu |
|---|---|---|---|---|---|---|
| API-01 | POST | `/api/Auth/register` | Nie | Brak | Rejestracja nowego użytkownika | [link](auth/POST_Auth_register.md) |
| API-02 | POST | `/api/Auth/login` | Nie | Brak | Logowanie — zwraca JWT | [link](auth/POST_Auth_login.md) |
| API-03 | POST | `/api/Firm/AddFirm/{isClient}` | Tak | User | Dodanie firmy własnej lub klienta | [link](firm/POST_Firm_AddFirm.md) |
| API-04 | GET | `/api/Firm/GetFirmFromAnaf` | Tak | User | Autouzupełnienie danych firmy z ANAF (CUI) | [link](firm/GET_Firm_fromAnaf.md) |
| API-05 | PUT | `/api/Firm/EditFirm` | Tak | User | Edycja danych firmy | [link](firm/PUT_Firm_EditFirm.md) |
| API-06 | GET | `/api/Firm/GetUserActiveFirm` | Tak | User | Pobranie aktywnej firmy użytkownika | [link](firm/GET_Firm_GetUserActiveFirm.md) |
| API-07 | GET | `/api/Firm/GetUserClientFirms` | Tak | User | Pobranie listy firm klientów | [link](firm/GET_Firm_GetUserClientFirms.md) |
| API-08 | GET | `/api/Firm/GetUserClientFirms` | Tak | User | Pobranie listy firm klientów (wariant paginowany) | [link](firm/GET_Firm_GetUserClientFirms.md) |
| API-09 | PUT | `/api/Firm/DeleteFirms` | Tak | User | Usunięcie (soft-delete) firm klientów | [link](firm/PUT_Firm_DeleteFirms.md) |
| API-10 | GET | `/api/Product/GetAll` | Tak | User | Pobranie wszystkich produktów użytkownika | [link](product/GET_Product_GetAll.md) |
| API-11 | POST | `/api/Product/AddProduct` | Tak | User | Dodanie nowego produktu | [link](product/POST_Product_Add.md) |
| API-12 | PUT | `/api/Product/EditProduct` | Tak | User | Edycja produktu | [link](product/PUT_Product_Edit.md) |
| API-13 | PUT | `/api/Product/DeleteProducts` | Tak | User | Usunięcie (soft-delete) produktów | [link](product/PUT_Product_Delete.md) |
| API-14 | GET | `/api/BankAccount/GetAll` | Tak | User | Pobranie wszystkich kont bankowych firmy | [link](bank_account/GET_BankAccount_GetAll.md) |
| API-15 | POST | `/api/BankAccount/AddBankAccount` | Tak | User | Dodanie konta bankowego | [link](bank_account/POST_BankAccount_Add.md) |
| API-16 | PUT | `/api/BankAccount/EditBankAccount` | Tak | User | Edycja konta bankowego | [link](bank_account/PUT_BankAccount_Edit.md) |
| API-17 | PUT | `/api/BankAccount/DeleteBankAccounts` | Tak | User | Usunięcie (soft-delete) kont bankowych | [link](bank_account/PUT_BankAccount_Delete.md) |
| API-18 | GET | `/api/DocumentSeries/GetAll` | Tak | User | Pobranie wszystkich serii dokumentów | [link](document_series/GET_DocumentSeries_GetAll.md) |
| API-19 | POST | `/api/DocumentSeries/AddDocumentSeries` | Tak | User | Dodanie serii dokumentów | [link](document_series/POST_DocumentSeries_Add.md) |
| API-20 | PUT | `/api/DocumentSeries/UpdateDocumentSeries` | Tak | User | Edycja serii dokumentów | [link](document_series/PUT_DocumentSeries_Update.md) |
| API-21 | PUT | `/api/DocumentSeries/DeleteDocumentSeries` | Tak | User | Usunięcie (soft-delete) serii dokumentów | [link](document_series/PUT_DocumentSeries_Delete.md) |
| API-22 | POST | `/api/Document/AddDocument` | Tak | User | Dodanie nowego dokumentu (faktura, proforma) | [link](document/POST_Document_Add.md) |
| API-23 | PUT | `/api/Document/EditDocument` | Tak | User | Edycja dokumentu | [link](document/PUT_Document_Edit.md) |
| API-24 | GET | `/api/Document/GetTableRecords` | Tak | User | Pobranie listy dokumentów (tabela z filtrowaniem) | [link](document/GET_Document_GetTableRecords.md) |
| API-25 | GET | `/api/Document/GetById/{documentId}` | Tak | User | Pobranie szczegółów dokumentu po ID | [link](document/GET_Document_GetById.md) |
| API-26 | PUT | `/api/Document/DeleteDocument` | Tak | User | Usunięcie (soft-delete) dokumentu | [link](document/PUT_Document_Delete.md) |
| API-27 | GET | `/api/Document/GetDocumentAutofillInfo` | Tak | User | Pobranie danych do autouzupełnienia formularza dokumentu | [link](document/GET_Document_GetAutofillInfo.md) |
| API-28 | POST | `/api/Document/GenerateInvoicePdf` | Tak | User | Generowanie PDF dokumentu ⚠️ BUG: hardcoded `InvoiceDocument` — nie obsługuje proformy ani storna | [link](document/POST_Document_GeneratePdf.md) |
| API-29 | POST | `/api/Document/GetPdfStream` | Tak | User | Pobranie strumienia PDF dokumentu | [link](document/POST_Document_GetPdfStream.md) |
| API-30 | GET | `/api/Document/GetDashboardStats` | Tak | User | Pobranie statystyk do dashboardu | [link](document/GET_Document_GetDashboardStats.md) |
| API-31 | PUT | `/api/Document/TransformToStorno` | Tak | User | Konwersja dokumentu na storno | [link](document/PUT_Document_TransformToStorno.md) |

## Legenda

| Kolumna | Opis |
|---|---|
| ID | Unikalny identyfikator endpointu w dokumentacji (API-XX) |
| Metoda | HTTP method: GET, POST, PUT |
| URL | Ścieżka względna od korzenia API |
| Auth | Czy wymagany jest JWT Bearer Token |
| Rola | Rola wymagana przez `[Authorize(Roles = "...")]` |
| Opis | Krótki opis operacji |
| Plik dokumentu | Link do szczegółowego opisu endpointu |

## Uwagi

- Soft-delete: operacje DELETE w InvoiceJet są realizowane przez metodę PUT ustawiającą flagę `IsDeleted = true` — brak fizycznego usunięcia rekordów.
- API-07 i API-08 wskazują na ten sam plik, gdyż oba warianty (z paginacją i bez) są opisane w jednym dokumencie.
- API-28 zawiera znany błąd: metoda generowania PDF jest hardcoded do typu `InvoiceDocument`, co powoduje niepoprawne działanie dla dokumentów proforma i storno.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny — pełna lista 31 endpointów. |
