# Inwentaryzacja API — endpointy

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Źródło | Kontrolery w `InvoiceJetAPI/InvoiceJet.Presentation/Controllers/` |

## Lista endpointów (31)

| ID | Metoda | URL | Kontroler.Metoda | Auth | Dokument | Status |
|---|---|---|---|---|---|---|
| API-01 | POST | `/api/Auth/register` | `AuthController.Register` | publiczny | [link](../04_api_i_integracje/01_api_frontend/auth/POST_Auth_register.md) | szkic |
| API-02 | POST | `/api/Auth/login` | `AuthController.Login` | publiczny | [link](../04_api_i_integracje/01_api_frontend/auth/POST_Auth_login.md) | szkic |
| API-03 | POST | `/api/Firm/AddFirm/{isClient}` | `FirmController.AddFirm` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/firm/POST_Firm_AddFirm.md) | szkic |
| API-04 | GET | `/api/Firm/fromAnaf/{cui}` | `FirmController.GetFirmDataFromAnaf` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/firm/GET_Firm_fromAnaf.md) | szkic |
| API-05 | PUT | `/api/Firm/EditFirm/{isClient}` | `FirmController.EditFirm` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/firm/PUT_Firm_EditFirm.md) | szkic |
| API-06 | GET | `/api/Firm/GetUserActiveFirm` | `FirmController.GetUserActiveFirm` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/firm/GET_Firm_GetUserActiveFirm.md) | szkic |
| API-07/08 | GET | `/api/Firm/GetUserClientFirms` | `FirmController.GetUserClientFirms` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/firm/GET_Firm_GetUserClientFirms.md) | szkic |
| API-09 | PUT | `/api/Firm/DeleteFirms` | `FirmController.DeleteFirms` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/firm/PUT_Firm_DeleteFirms.md) | szkic |
| API-10 | GET | `/api/Product/GetAllProductsForUserId` | `ProductController.GetAllProductsForUserId` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/product/GET_Product_GetAll.md) | szkic |
| API-11 | POST | `/api/Product/AddProduct` | `ProductController.AddProduct` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/product/POST_Product_Add.md) | szkic |
| API-12 | PUT | `/api/Product/EditProduct` | `ProductController.EditProduct` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/product/PUT_Product_Edit.md) | szkic |
| API-13 | PUT | `/api/Product/DeleteProducts` | `ProductController.DeleteProducts` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/product/PUT_Product_Delete.md) | szkic |
| API-14 | GET | `/api/BankAccount/GetUserFirmBankAccounts` | `BankAccountController.GetUserFirmBankAccounts` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/bank_account/GET_BankAccount_GetAll.md) | szkic |
| API-15 | POST | `/api/BankAccount/AddUserFirmBankAccount` | `BankAccountController.AddUserFirmBankAccount` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/bank_account/POST_BankAccount_Add.md) | szkic |
| API-16 | PUT | `/api/BankAccount/EditUserFirmBankAccount` | `BankAccountController.EditUserFirmBankAccount` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/bank_account/PUT_BankAccount_Edit.md) | szkic |
| API-17 | PUT | `/api/BankAccount/DeleteUserFirmBankAccounts` | `BankAccountController.DeleteUserFirmBankAccounts` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/bank_account/PUT_BankAccount_Delete.md) | szkic |
| API-18 | GET | `/api/DocumentSeries/GetAllDocumentSeriesForUserId` | `DocumentSeriesController.GetAllDocumentSeriesForUserId` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document_series/GET_DocumentSeries_GetAll.md) | szkic |
| API-19 | POST | `/api/DocumentSeries/AddDocumentSeries` | `DocumentSeriesController.AddDocumentSeries` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document_series/POST_DocumentSeries_Add.md) | szkic |
| API-20 | PUT | `/api/DocumentSeries/UpdateDocumentSeries` | `DocumentSeriesController.UpdateDocumentSeries` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document_series/PUT_DocumentSeries_Update.md) | szkic |
| API-21 | PUT | `/api/DocumentSeries/DeleteDocumentSeries` | `DocumentSeriesController.DeleteDocumentSeries` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document_series/PUT_DocumentSeries_Delete.md) | szkic |
| API-22 | POST | `/api/Document/AddDocument` | `DocumentController.AddDocument` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md) | szkic |
| API-23 | PUT | `/api/Document/EditDocument` | `DocumentController.EditDocument` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document/PUT_Document_Edit.md) | szkic |
| API-24 | GET | `/api/Document/GetDocumentTableRecords/{documentTypeId}` | `DocumentController.GetDocumentTableRecords` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md) | szkic |
| API-25 | GET | `/api/Document/GetDocumentById/{documentId}` | `DocumentController.GetDocumentById` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document/GET_Document_GetById.md) | szkic |
| API-26 | PUT | `/api/Document/DeleteDocuments` | `DocumentController.DeleteDocuments` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document/PUT_Document_Delete.md) | szkic |
| API-27 | GET | `/api/Document/GetDocumentAutofillInfo/{documentTypeId}` | `DocumentController.GetDocumentAutofillInfo` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document/GET_Document_GetAutofillInfo.md) | szkic |
| API-28 | POST | `/api/Document/GenerateDocumentPdf` | `DocumentController.GenerateDocument` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document/POST_Document_GeneratePdf.md) | szkic |
| API-29 | POST | `/api/Document/GetInvoicePdfStream` | `DocumentController.GetInvoicePdfStream` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) | szkic |
| API-30 | GET | `/api/Document/GetDashboardStats/{year}/{documentType}` | `DocumentController.GetDashboardStats` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document/GET_Document_GetDashboardStats.md) | szkic |
| API-31 | PUT | `/api/Document/TransformToStorno` | `DocumentController.TransformToStorno` | `[Authorize]` | [link](../04_api_i_integracje/01_api_frontend/document/PUT_Document_TransformToStorno.md) | szkic |

## Anomalie

| # | Anomalia |
|---|---|
| A-01 | Brak `DELETE` HTTP — wszystkie usunięcia przez `PUT` z body `int[]` |
| A-02 | `API-07` i `API-08` to ten sam fizyczny endpoint (duplikat numeracji) |
| A-03 | `API-21` używa `PUT` zamiast `DELETE` dla usunięcia serii |
| A-04 | `API-28` — `DocumentController.GenerateDocument` ma własny try/catch → omija ExceptionMiddleware |
| A-05 | `API-19` — `DocumentSeriesController.AddDocumentSeries` ma własny try/catch → odpowiedź błędu to plain string (nie JSON) |
| A-06 | `API-28` — `PdfGenerationService.GenerateInvoicePdf` hardcodes `new InvoiceDocument()` — zawsze generuje fakturę zwykłą |
| A-07 | `int[]` parametry delete bez `[FromBody]` → binding z query string (nie body) dla API-09, API-13, API-21 |
