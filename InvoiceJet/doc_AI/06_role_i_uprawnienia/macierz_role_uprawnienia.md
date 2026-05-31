# Macierz ról i uprawnień

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Macierz: Rola × Endpoint × Operacja

| Endpoint | Anonimowy | User (zalogowany) |
|---|---|---|
| `POST /api/Auth/register` | ✅ | ✅ |
| `POST /api/Auth/login` | ✅ | ✅ |
| `POST /api/Firm/AddFirm/{isClient}` | ❌ | ✅ |
| `GET /api/Firm/fromAnaf/{cui}` | ❌ | ✅ |
| `PUT /api/Firm/EditFirm/{isClient}` | ❌ | ✅ |
| `GET /api/Firm/GetUserActiveFirm` | ❌ | ✅ |
| `GET /api/Firm/GetUserClientFirms` | ❌ | ✅ |
| `PUT /api/Firm/DeleteFirms` | ❌ | ✅ |
| `GET /api/Product/GetAllProductsForUserId` | ❌ | ✅ |
| `POST /api/Product/AddProduct` | ❌ | ✅ |
| `PUT /api/Product/EditProduct` | ❌ | ✅ |
| `PUT /api/Product/DeleteProducts` | ❌ | ✅ |
| `GET /api/BankAccount/GetUserFirmBankAccounts` | ❌ | ✅ |
| `POST /api/BankAccount/AddUserFirmBankAccount` | ❌ | ✅ |
| `PUT /api/BankAccount/EditUserFirmBankAccount` | ❌ | ✅ |
| `PUT /api/BankAccount/DeleteUserFirmBankAccounts` | ❌ | ✅ |
| `GET /api/DocumentSeries/GetAllDocumentSeriesForUserId` | ❌ | ✅ |
| `POST /api/DocumentSeries/AddDocumentSeries` | ❌ | ✅ |
| `PUT /api/DocumentSeries/UpdateDocumentSeries` | ❌ | ✅ |
| `PUT /api/DocumentSeries/DeleteDocumentSeries` | ❌ | ✅ |
| `POST /api/Document/AddDocument` | ❌ | ✅ |
| `PUT /api/Document/EditDocument` | ❌ | ✅ |
| `GET /api/Document/GetDocumentTableRecords/{documentTypeId}` | ❌ | ✅ |
| `GET /api/Document/GetDocumentById/{documentId}` | ❌ | ✅ |
| `PUT /api/Document/DeleteDocuments` | ❌ | ✅ |
| `GET /api/Document/GetDocumentAutofillInfo/{documentTypeId}` | ❌ | ✅ |
| `POST /api/Document/GenerateDocumentPdf` | ❌ | ✅ |
| `POST /api/Document/GetInvoicePdfStream` | ❌ | ✅ |
| `GET /api/Document/GetDashboardStats/{year}/{documentType}` | ❌ | ✅ |
| `PUT /api/Document/TransformToStorno` | ❌ | ✅ |

## Macierz: Rola × Ekran

| Ekran | Anonimowy | User |
|---|---|---|
| `/login` | ✅ | ✅ |
| `/register` | ✅ | ✅ |
| `/dashboard/**` (wszystkie) | ❌ → redirect `/login` | ✅ |

## Mechanizm egzekwowania

| Warstwa | Mechanizm |
|---|---|
| Backend API | `[Authorize(Roles = "User")]` na kontrolerach; JWT middleware |
| Frontend routing | `AuthGuard.canActivate()` sprawdza `authService.isLoggedIn()` |
| Frontend HTTP | `AuthInterceptor` dodaje Bearer token; przy 401 logout |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
