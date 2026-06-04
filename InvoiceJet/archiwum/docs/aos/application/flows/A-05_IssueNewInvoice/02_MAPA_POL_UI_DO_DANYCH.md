# Wystawienie nowej faktury - Mapa pól UI do danych

## 1. Pola naglowka dokumentu

| Element makiety | Frontend | Endpoint | DTO backendu | Encja | Tabela.kolumna | Uwagi |
|---|---|---|---|---|---|---|
| Pole Client Name or CUI | `formControlName="client"`, `IFirm` | `POST /api/Document/AddDocument` | `DocumentRequestDto.Client.Id` | `Document` / `Firm` | `Document.ClientId`, `Firm.Id` | Lista klientow pochodzi z `GET /api/Document/GetDocumentAutofillInfo/1`. |
| Pole Issue Date | `formControlName="issueDate"` | `POST /api/Document/AddDocument` | `DocumentRequestDto.IssueDate` | `Document` | `Document.IssueDate` | Wymagane w formularzu. |
| Pole Due Date | `formControlName="dueDate"` | `POST /api/Document/AddDocument` | `DocumentRequestDto.DueDate` | `Document` | `Document.DueDate` | Walidowane przez `dueDateValidator`. |
| Pole Document Series | `formControlName="documentSeries"` | `POST /api/Document/AddDocument` | `DocumentRequestDto.DocumentSeries` | `Document`, `DocumentSeries` | `Document.DocumentNumber`, `Document.DocumentTypeId`, `DocumentSeries.CurrentNumber` | Widoczne tylko w trybie dodawania. |
| Pole Status | `formControlName="documentStatus"` | `PUT /api/Document/EditDocument` | `DocumentRequestDto.DocumentStatus.Id` | `Document` | `Document.DocumentStatusId` | Widoczne tylko w trybie edycji. |

## 2. Pola pozycji dokumentu

| Element makiety | Frontend | Endpoint | DTO backendu | Encja | Tabela.kolumna | Uwagi |
|---|---|---|---|---|---|---|
| Kolumna Product Name | `products[].name` | `POST /api/Document/AddDocument` | `DocumentProductRequestDto.Name` | `Product` | `Product.Name` | Dla `Id > 0` backend wyszukuje produkt po nazwie i `UserFirmId`. |
| Kolumna Unit Price | `products[].unitPrice` | `POST /api/Document/AddDocument` | `DocumentProductRequestDto.UnitPrice` | `DocumentProduct`, `Product` | `DocumentProduct.UnitPrice`, `Product.Price` | Dla nowego produktu mapper zapisuje cene w `Product.Price`. |
| Kolumna Quantity | `products[].quantity` | `POST /api/Document/AddDocument` | `DocumentProductRequestDto.Quantity` | `DocumentProduct` | `DocumentProduct.Quantity` | Minimalna wartość w UI: `1`. |
| Kolumna U.M. | `products[].unitOfMeasurement` | `POST /api/Document/AddDocument` | `DocumentProductRequestDto.UnitOfMeasurement` | `Product` | `Product.UnitOfMeasurement` | W trybie edycji pole jest `readonly`. |
| Kolumna TVA Value | `products[].tvaValue` | `POST /api/Document/AddDocument` | `DocumentProductRequestDto.TvaValue` | `Product` | `Product.TvaValue` | W trybie edycji pole jest `readonly`. |
| Kolumna Contains TVA | `products[].containsTva` | `POST /api/Document/AddDocument` | `DocumentProductRequestDto.ContainsTva` | `Product` | `Product.ContainsTva` | W `DocumentProduct` nie istnieje osobną kolumna dla tej wartości. |
| Kolumna Total Price | `products[].totalPrice` | `POST /api/Document/AddDocument` | `DocumentProductRequestDto.TotalPrice` | `DocumentProduct`, `Document` | `DocumentProduct.TotalPrice`, `Document.TotalPrice` | W UI pole jest tylko do odczytu. |

## 3. Dane pomocnicze formularza

| Dane | Endpoint | Backend | Tabele |
|---|---|---|---|
| Klienci | `GET /api/Document/GetDocumentAutofillInfo/1` | `GetDocumentAutofillInfo(1)` | `Firm`, `UserFirm` |
| Serie dokumentów | `GET /api/Document/GetDocumentAutofillInfo/1` | `GetDocumentAutofillInfo(1)` | `DocumentSeries`, `DocumentType` |
| Statusy dokumentów | `GET /api/Document/GetDocumentAutofillInfo/1` | `GetDocumentAutofillInfo(1)` | `DocumentStatus` |
| Produkty | `GET /api/Document/GetDocumentAutofillInfo/1` | `GetDocumentAutofillInfo(1)` | `Product` |
