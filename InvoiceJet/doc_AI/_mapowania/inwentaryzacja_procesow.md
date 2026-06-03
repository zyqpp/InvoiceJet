# Inwentaryzacja procesów technicznych

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Źródło | `InvoiceJetAPI/InvoiceJet.Presentation/Controllers/`, `InvoiceJet.Application/Services/Impl/` |

## Lista procesów (15)

| ID | Nazwa procesu | Kontroler | Endpointy API | Serwis | Dokument | Status |
|---|---|---|---|---|---|---|
| P-01 | Auth | `AuthController` | API-01, API-02 | `IAuthService` | [link](../02_procesy/P-01_Auth.md) | szkic |
| P-02 | ManageOwnFirm | `FirmController` | API-03 (false), API-05 (false), API-06 | `IFirmService` | [link](../02_procesy/P-02_ManageOwnFirm.md) | szkic |
| P-03 | GetFirmFromAnaf | `FirmController` | API-04 | `IFirmService` | [link](../02_procesy/P-03_GetFirmFromAnaf.md) | szkic |
| P-04 | ManageClientFirms | `FirmController` | API-03 (true), API-05 (true), API-07/08, API-09 | `IFirmService` | [link](../02_procesy/P-04_ManageClientFirms.md) | szkic |
| P-05 | ManageBankAccounts | `BankAccountController` | API-14, API-15, API-16, API-17 | `IBankAccountService` | [link](../02_procesy/P-05_ManageBankAccounts.md) | szkic |
| P-06 | ManageProducts | `ProductController` | API-10, API-11, API-12, API-13 | `IProductService` | [link](../02_procesy/P-06_ManageProducts.md) | szkic |
| P-07 | ManageDocumentSeries | `DocumentSeriesController` | API-18, API-19, API-20, API-21 | `IDocumentSeriesService` | [link](../02_procesy/P-07_ManageDocumentSeries.md) | szkic |
| P-08 | AddEditDocument | `DocumentController` | API-22, API-23 | `IDocumentService` | [link](../02_procesy/P-08_AddEditDocument.md) | szkic |
| P-09 | GetDocuments | `DocumentController` | API-24, API-25 | `IDocumentService` | [link](../02_procesy/P-09_GetDocuments.md) | szkic |
| P-10 | DeleteDocuments | `DocumentController` | API-26 | `IDocumentService` | [link](../02_procesy/P-10_DeleteDocuments.md) | szkic |
| P-11 | GetDocumentAutofillInfo | `DocumentController` | API-27 | `IDocumentService` | [link](../02_procesy/P-11_GetDocumentAutofillInfo.md) | szkic |
| P-12 | GetDashboardStats | `DocumentController` | API-30 | `IDocumentService` | [link](../02_procesy/P-12_GetDashboardStats.md) | szkic |
| P-13 | TransformToStorno | `DocumentController` | API-31 | `IDocumentService` | [link](../02_procesy/P-13_TransformToStorno.md) | szkic |
| P-14 | GenerateDocumentPdf | `DocumentController` | API-28 | `IDocumentService`, `IPdfGenerationService` | [link](../02_procesy/P-14_GenerateDocumentPdf.md) | szkic |
| P-15 | GetInvoicePdfStream | `DocumentController` | API-29 | `IDocumentService`, `IPdfGenerationService` | [link](../02_procesy/P-15_GetInvoicePdfStream.md) | szkic |

## Opis procesów

### P-01 Auth

**Cel:** Rejestracja nowego użytkownika i logowanie. Oba endpointy zwracają JWT Bearer Token.

**Przepływ rejestracji:**
1. Sprawdzenie czy email jest zajęty → `UserAlreadyExistsException` jeśli tak
2. Walidacja hasła regexem (min 8 znaków, duże/małe litery, cyfra, znak specjalny)
3. Walidacja zgodności `Password` z `PasswordConfirmation`
4. Hashowanie hasła BCrypt → zapis do DB
5. Generowanie JWT (ważny **10 minut**)
6. Zwrot tokenu jako `string`

**Przepływ logowania:**
1. Szukanie usera po email → `UserNotFoundException` jeśli nie znaleziony
2. Weryfikacja hasła BCrypt → `IncorrectPasswordException` jeśli niezgodne
3. Generowanie JWT (ważny **10 minut**)
4. Zwrot tokenu jako `string`

**Uwaga:** JWT wygasa po 10 minutach — bardzo krótki czas sesji.

---

### P-02 ManageOwnFirm

**Cel:** Zarządzanie własną firmą użytkownika (wystawiającego). Parametr `isClient=false` w URL.

**Endpointy:**
- `GET /api/Firm/GetUserActiveFirm` — pobiera aktywną firmę zalogowanego usera
- `POST /api/Firm/AddFirm/false` — dodaje własną firmę (pierwsze użycie)
- `PUT /api/Firm/EditFirm/false` — edytuje własną firmę

---

### P-03 GetFirmFromAnaf

**Cel:** Pobiera dane firmy z zewnętrznego API ANAF (rumuński urząd skarbowy) na podstawie CUI.

**Endpoint:** `GET /api/Firm/fromAnaf/{cui}`

**Przepływ:** HTTP GET do ANAF API → mapowanie odpowiedzi → zwrot `FirmDto`

---

### P-04 ManageClientFirms

**Cel:** Zarządzanie firmami klientów (odbiorcami faktur). Parametr `isClient=true` w URL.

**Endpointy:**
- `GET /api/Firm/GetUserClientFirms` — lista klientów
- `POST /api/Firm/AddFirm/true` — dodanie klienta
- `PUT /api/Firm/EditFirm/true` — edycja klienta
- `PUT /api/Firm/DeleteFirms` — soft-usuwanie (lub hard-delete — do weryfikacji)

---

### P-05 ManageBankAccounts

**Cel:** CRUD kont bankowych powiązanych z aktywną firmą użytkownika.

**Endpointy:** API-14 (list), API-15 (add), API-16 (edit), API-17 (delete)

---

### P-06 ManageProducts

**Cel:** CRUD produktów/usług katalogowych powiązanych z aktywną firmą.

**Endpointy:** API-10 (list), API-11 (add), API-12 (edit), API-13 (delete)

---

### P-07 ManageDocumentSeries

**Cel:** CRUD serii dokumentów (np. "FV", "PRO", "STORNO") z automatycznym numerowaniem.

**Endpointy:** API-18 (list), API-19 (add), API-20 (edit), API-21 (delete)

---

### P-08 AddEditDocument

**Cel:** Tworzenie i edycja dokumentu (faktura / proforma / storno).

**Przepływ AddDocument:**
1. Pobranie `userFirmId` z JWT → `UserHasNoAssociatedFirmException` jeśli brak
2. Pobranie aktywnego konta bankowego (WHERE `IsActive=true`) → `NoBankAccountAddedException` jeśli brak
3. Generowanie numeru: `SeriesName + CurrentNumber.ToString("D4")`
4. Zapis dokumentu do DB
5. `UpdateDocumentProducts()`: usuń istniejące produkty, dodaj nowe; jeśli produkt ma `Id > 0` → lookup po nazwie, else → utwórz nowy produkt
6. Inkrementacja `DocumentSeries.CurrentNumber`
7. Zapis zmian

**Przepływ EditDocument:**
1. Pobranie `userFirmId` z JWT
2. Pobranie dokumentu po Id → wyjątek jeśli nie znaleziony (plain `Exception`, nie domenowy)
3. Aktualizacja pól daty, statusu, klienta
4. `UpdateDocumentProducts()`: reset i ponowne dodanie produktów
5. Zapis zmian

---

### P-09 GetDocuments

**Cel:** Pobieranie listy dokumentów (tabela) lub pojedynczego dokumentu.

- `GET /api/Document/GetDocumentTableRecords/{documentTypeId}` → lista `DocumentTableRecordDto`
- `GET /api/Document/GetDocumentById/{documentId}` → pełny `DocumentRequestDto`

---

### P-10 DeleteDocuments

**Cel:** Fizyczne (hard) usunięcie dokumentów i ich pozycji produktowych.

**Przepływ:**
1. Pobranie dokumentów z `DocumentProducts` (Include)
2. `RemoveRangeAsync(DocumentProducts)` — fizyczne usunięcie pozycji
3. `RemoveRangeAsync(Documents)` — fizyczne usunięcie dokumentów
4. `CompleteAsync()`

**Uwaga:** Brak soft-delete — dane są trwale usuwane.

---

### P-11 GetDocumentAutofillInfo

**Cel:** Pobieranie danych potrzebnych do wypełnienia formularza faktury (klienci, serie, statusy, produkty) jednym zapytaniem.

**Endpoint:** `GET /api/Document/GetDocumentAutofillInfo/{documentTypeId}`

---

### P-12 GetDashboardStats

**Cel:** Dane statystyczne dla dashboardu (liczniki + sumy miesięczne dla wykresu).

**Endpoint:** `GET /api/Document/GetDashboardStats/{year}/{documentType}`

**Dane zwracane:** `TotalDocuments`, `TotalClients`, `TotalProducts`, `TotalBankAccounts`, `MonthlyTotals` (12 miesięcy).

---

### P-13 TransformToStorno

**Cel:** Zmiana istniejącej faktury na fakturę storno przez zmianę `DocumentTypeId=3`.

**Endpoint:** `PUT /api/Document/TransformToStorno`

**Przepływ:** iteracja po tablicy `documentIds[]`, dla każdego: szukanie w DB → zmiana `DocumentTypeId = 3` → zapis. Brak transakcji — każdy dokument zapisywany osobno w pętli.

**Uwaga:** Brak transakcji ogarniającej całą operację — przy błędzie w środku pętli część dokumentów może być już przetransformowana.

---

### P-14 GenerateDocumentPdf

**Cel:** Generowanie pliku PDF faktury i zapis na dysku serwera.

**Endpoint:** `POST /api/Document/GenerateDocumentPdf`

**Uwaga:** Używa `PdfGenerationService.GenerateInvoicePdf()` który hardcoduje `new InvoiceDocument()` (faktura zwykła) — ignoruje `DocumentType`. Zwraca `DocumentRequestDto` z uzupełnionym `Seller`.

---

### P-15 GetInvoicePdfStream

**Cel:** Generowanie PDF faktury i zwrot jako strumień bajtów do przeglądarki.

**Endpoint:** `POST /api/Document/GetInvoicePdfStream`

**Przepływ:**
1. Pobranie aktywnej firmy i konta bankowego dokumentu
2. Uzupełnienie `Seller` i `BankAccount` w DTO
3. Wywołanie `IPdfGenerationService.GetInvoicePdfStream()` (factory pattern — typy dokumentów)
4. Zwrot `DocumentStreamDto { DocumentNumber, PdfContent (byte[]) }`

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Inwentaryzacja 15 procesów z opisami przepływów. |
