# Katalog API — InvoiceJetAPI

Kompletna lista endpointów udokumentowanych w ramach AOS (etap backend).  
Zakres: **API-01 – API-31** (31 endpointów, 19 procesów, 5 kontrolerów).

> Autoryzacja: o ile nie zaznaczono inaczej, każdy endpoint oznaczony `[Authorize]`
> wymaga nagłówka `Authorization: Bearer <JWT>` z rolą `User`.

---

## Spis endpointów

| ID API | Metoda | Ścieżka | Kontroler.Metoda | Auth | Proces |
|---|---|---|---|---|---|
| `API-01` | `POST` | `/api/Auth/register` | `AuthController.Register` | publiczny | [P-01](processes/Authentication/P-01_RegisterUser/) |
| `API-02` | `POST` | `/api/Auth/login` | `AuthController.Login` | publiczny | [P-02](processes/Authentication/P-02_LoginUser/) |
| `API-03` | `POST` | `/api/Firm/AddFirm/{isClient}` | `FirmController.AddFirm` | `[Authorize]` | [P-03](processes/FirmManagement/P-03_AddFirm/) |
| `API-04` | `GET` | `/api/Firm/fromAnaf/{cui}` | `FirmController.GetFirmDataFromAnaf` | `[Authorize]` | [P-04](processes/FirmManagement/P-04_GetFirmFromAnaf/) |
| `API-05` | `PUT` | `/api/Firm/EditFirm/{isClient}` | `FirmController.EditFirm` | `[Authorize]` | [P-05](processes/FirmManagement/P-05_EditFirm/) |
| `API-06` | `GET` | `/api/Firm/GetUserActiveFirm` | `FirmController.GetUserActiveFirm` | `[Authorize]` | [P-06](processes/FirmManagement/P-06_GetUserActiveFirm/) |
| `API-07` | `GET` | `/api/Firm/GetUserClientFirms` | `FirmController.GetUserClientFirms` | `[Authorize]` | [P-07](processes/FirmManagement/P-07_GetUserClientFirms/) |
| `API-08` | `GET` | `/api/Firm/GetUserClientFirms` | `FirmController.GetUserClientFirms` | `[Authorize]` | [P-08](processes/FirmManagement/P-08_ManageClientFirms/) |
| `API-09` | `PUT` | `/api/Firm/DeleteFirms` | `FirmController.DeleteFirms` | `[Authorize]` | [P-08](processes/FirmManagement/P-08_ManageClientFirms/) |
| `API-10` | `GET` | `/api/Product/GetAllProductsForUserId` | `ProductController.GetAllProductsForUserId` | `[Authorize]` | [P-09](processes/ProductManagement/P-09_ManageProducts/) |
| `API-11` | `POST` | `/api/Product/AddProduct` | `ProductController.AddProduct` | `[Authorize]` | [P-09](processes/ProductManagement/P-09_ManageProducts/) |
| `API-12` | `PUT` | `/api/Product/EditProduct` | `ProductController.EditProduct` | `[Authorize]` | [P-09](processes/ProductManagement/P-09_ManageProducts/) |
| `API-13` | `PUT` | `/api/Product/DeleteProducts` | `ProductController.DeleteProducts` | `[Authorize]` | [P-09](processes/ProductManagement/P-09_ManageProducts/) |
| `API-14` | `GET` | `/api/BankAccount/GetUserFirmBankAccounts` | `BankAccountController.GetUserFirmBankAccounts` | `[Authorize]` | [P-10](processes/BankAccountManagement/P-10_ManageBankAccounts/) |
| `API-15` | `POST` | `/api/BankAccount/AddUserFirmBankAccount` | `BankAccountController.AddUserFirmBankAccount` | `[Authorize]` | [P-10](processes/BankAccountManagement/P-10_ManageBankAccounts/) |
| `API-16` | `PUT` | `/api/BankAccount/EditUserFirmBankAccount` | `BankAccountController.EditUserFirmBankAccount` | `[Authorize]` | [P-10](processes/BankAccountManagement/P-10_ManageBankAccounts/) |
| `API-17` | `PUT` | `/api/BankAccount/DeleteUserFirmBankAccounts` | `BankAccountController.DeleteUserFirmBankAccounts` | `[Authorize]` | [P-10](processes/BankAccountManagement/P-10_ManageBankAccounts/) |
| `API-18` | `GET` | `/api/DocumentSeries/GetAllDocumentSeriesForUserId` | `DocumentSeriesController.GetAllDocumentSeriesForUserId` | `[Authorize]` | [P-11](processes/DocumentSeriesManagement/P-11_ManageDocumentSeries/) |
| `API-19` | `POST` | `/api/DocumentSeries/AddDocumentSeries` | `DocumentSeriesController.AddDocumentSeries` | `[Authorize]` | [P-11](processes/DocumentSeriesManagement/P-11_ManageDocumentSeries/) |
| `API-20` | `PUT` | `/api/DocumentSeries/UpdateDocumentSeries` | `DocumentSeriesController.UpdateDocumentSeries` | `[Authorize]` | [P-11](processes/DocumentSeriesManagement/P-11_ManageDocumentSeries/) |
| `API-21` | `PUT` | `/api/DocumentSeries/DeleteDocumentSeries` | `DocumentSeriesController.DeleteDocumentSeries` | `[Authorize]` | [P-11](processes/DocumentSeriesManagement/P-11_ManageDocumentSeries/) |
| `API-22` | `POST` | `/api/Document/AddDocument` | `DocumentController.AddDocument` | `[Authorize]` | [P-12](processes/DocumentManagement/P-12_AddDocument/) |
| `API-23` | `PUT` | `/api/Document/EditDocument` | `DocumentController.EditDocument` | `[Authorize]` | [P-13](processes/DocumentManagement/P-13_EditDocument/) |
| `API-24` | `GET` | `/api/Document/GetDocumentTableRecords/{documentTypeId}` | `DocumentController.GetDocumentTableRecords` | `[Authorize]` | [P-14](processes/DocumentManagement/P-14_GetDocuments/) |
| `API-25` | `GET` | `/api/Document/GetDocumentById/{documentId}` | `DocumentController.GetDocumentById` | `[Authorize]` | [P-14](processes/DocumentManagement/P-14_GetDocuments/) |
| `API-26` | `PUT` | `/api/Document/DeleteDocuments` | `DocumentController.DeleteDocuments` | `[Authorize]` | [P-15](processes/DocumentManagement/P-15_DeleteDocuments/) |
| `API-27` | `GET` | `/api/Document/GetDocumentAutofillInfo/{documentTypeId}` | `DocumentController.GetDocumentAutofillInfo` | `[Authorize]` | [P-16](processes/DocumentManagement/P-16_GetDocumentAutofillInfo/) |
| `API-28` | `POST` | `/api/Document/GenerateDocumentPdf` | `DocumentController.GenerateDocument` | `[Authorize]` | [P-17](processes/DocumentManagement/P-17_ManageDocumentPdf/) |
| `API-29` | `POST` | `/api/Document/GetInvoicePdfStream` | `DocumentController.GetInvoicePdfStream` | `[Authorize]` | [P-17](processes/DocumentManagement/P-17_ManageDocumentPdf/) |
| `API-30` | `GET` | `/api/Document/GetDashboardStats/{year}/{documentType}` | `DocumentController.GetDashboardStats` | `[Authorize]` | [P-18](processes/DocumentManagement/P-18_GetDashboardStats/) |
| `API-31` | `PUT` | `/api/Document/TransformToStorno` | `DocumentController.TransformToStorno` | `[Authorize]` | [P-19](processes/DocumentManagement/P-19_TransformToStorno/) |

---

## Grupowanie według kontrolera

### AuthController (2 endpointy)

| ID API | Metoda | Ścieżka |
|---|---|---|
| `API-01` | `POST` | `/api/Auth/register` |
| `API-02` | `POST` | `/api/Auth/login` |

### FirmController (7 endpointów)

| ID API | Metoda | Ścieżka |
|---|---|---|
| `API-03` | `POST` | `/api/Firm/AddFirm/{isClient}` |
| `API-04` | `GET` | `/api/Firm/fromAnaf/{cui}` |
| `API-05` | `PUT` | `/api/Firm/EditFirm/{isClient}` |
| `API-06` | `GET` | `/api/Firm/GetUserActiveFirm` |
| `API-07` | `GET` | `/api/Firm/GetUserClientFirms` |
| `API-08` | `GET` | `/api/Firm/GetUserClientFirms` ⚠️ |
| `API-09` | `PUT` | `/api/Firm/DeleteFirms` |

> ⚠️ `API-07` i `API-08` wskazują na ten sam fizyczny endpoint `GET /api/Firm/GetUserClientFirms`.
> `API-07` pochodzi z dokumentu P-07 (proces read-only); `API-08` z P-08 (zarządzanie = GET + DELETE).
> To duplikat numeracji spowodowany sposobem dekompozycji procesów — **wymaga weryfikacji z zespołem**.

### ProductController (4 endpointy)

| ID API | Metoda | Ścieżka |
|---|---|---|
| `API-10` | `GET` | `/api/Product/GetAllProductsForUserId` |
| `API-11` | `POST` | `/api/Product/AddProduct` |
| `API-12` | `PUT` | `/api/Product/EditProduct` |
| `API-13` | `PUT` | `/api/Product/DeleteProducts` |

### BankAccountController (4 endpointy)

| ID API | Metoda | Ścieżka |
|---|---|---|
| `API-14` | `GET` | `/api/BankAccount/GetUserFirmBankAccounts` |
| `API-15` | `POST` | `/api/BankAccount/AddUserFirmBankAccount` |
| `API-16` | `PUT` | `/api/BankAccount/EditUserFirmBankAccount` |
| `API-17` | `PUT` | `/api/BankAccount/DeleteUserFirmBankAccounts` |

### DocumentSeriesController (4 endpointy)

| ID API | Metoda | Ścieżka |
|---|---|---|
| `API-18` | `GET` | `/api/DocumentSeries/GetAllDocumentSeriesForUserId` |
| `API-19` | `POST` | `/api/DocumentSeries/AddDocumentSeries` |
| `API-20` | `PUT` | `/api/DocumentSeries/UpdateDocumentSeries` |
| `API-21` | `PUT` | `/api/DocumentSeries/DeleteDocumentSeries` |

> ⚠️ `API-21` używa `PUT` zamiast `DELETE`. Kotwica: `DocumentSeriesController.cs` — `[HttpPut("DeleteDocumentSeries")]`. Wymaga weryfikacji z zespołem.

### DocumentController (10 endpointów)

| ID API | Metoda | Ścieżka |
|---|---|---|
| `API-22` | `POST` | `/api/Document/AddDocument` |
| `API-23` | `PUT` | `/api/Document/EditDocument` |
| `API-24` | `GET` | `/api/Document/GetDocumentTableRecords/{documentTypeId}` |
| `API-25` | `GET` | `/api/Document/GetDocumentById/{documentId}` |
| `API-26` | `PUT` | `/api/Document/DeleteDocuments` |
| `API-27` | `GET` | `/api/Document/GetDocumentAutofillInfo/{documentTypeId}` |
| `API-28` | `POST` | `/api/Document/GenerateDocumentPdf` |
| `API-29` | `POST` | `/api/Document/GetInvoicePdfStream` |
| `API-30` | `GET` | `/api/Document/GetDashboardStats/{year}/{documentType}` |
| `API-31` | `PUT` | `/api/Document/TransformToStorno` |

> ⚠️ `API-26` i `API-09` używają `PUT` dla operacji usuwania (semantycznie `DELETE`).
> Wzorzec konsekwentny w całym API — prawdopodobnie celowy (batch delete przez body). Wymaga weryfikacji z zespołem.

---

## Uwagi przekrojowe

| Obserwacja | Dotyczy |
|---|---|
| Brak `DELETE` HTTP — wszystkie usunięcia realizowane przez `PUT` z `int[]` w body | API-09, API-13, API-17, API-21, API-26 |
| Dwa `POST` dla PDF: jeden zapisuje plik na dysk, drugi zwraca strumień | API-28, API-29 |
| Endpoint autouzupełnienia (API-27) zwraca pusty DTO zamiast błędu gdy user nie ma firmy | API-27 |
| `API-07` = `API-08` (ten sam fizyczny endpoint, dwa ID w dokumentacji) | API-07, API-08 |

---

## Metadane katalogu

| Atrybut | Wartość |
|---|---|
| Liczba endpointów | 31 (w tym 1 duplikat fizyczny: API-07/API-08) |
| Kontrolery | 5 (`AuthController`, `FirmController`, `ProductController`, `BankAccountController`, `DocumentSeriesController`, `DocumentController`) |
| Procesy | P-01 – P-19 (19 procesów) |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
