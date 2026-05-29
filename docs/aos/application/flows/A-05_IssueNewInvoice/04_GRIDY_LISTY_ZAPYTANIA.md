# Wystawienie nowej faktury - Gridy, listy i zapytania

## 1. Grid pozycji dokumentu

| Atrybut | Wartosc |
|---|---|
| Komponent | `BaseInvoiceComponent` |
| Zrodlo danych | `MatTableDataSource` z `productsFormArray.controls` |
| Kolumny | `name`, `unitPrice`, `quantity`, `unitOfMeasurement`, `tvaValue`, `containsTva`, `totalPrice`, `actions` |
| Paginacja | N/D |
| Sortowanie | N/D |
| Zapis do API | `DocumentRequestDto.Products` |
| Encja pozycji | `DocumentProduct` |

## 2. Lista klientow w autouzupelnianiu

| Atrybut | Wartosc |
|---|---|
| Pole | `client` |
| Zrodlo UI | `invoiceAutofillData.clients` |
| Filtrowanie UI | `filterClients()` po `firm.name` i `firm.cui` |
| Endpoint | `GET /api/Document/GetDocumentAutofillInfo/1` |
| Zapytanie backend | `Firms.Query().Where(f => f.UserFirms.Any(uf => uf.UserId == userId && uf.IsClient))` |
| Tabele | `Firm`, `UserFirm` |

## 3. Lista produktow w autouzupelnianiu

| Atrybut | Wartosc |
|---|---|
| Pole | `products[].name` |
| Zrodlo UI | `invoiceAutofillData.products` |
| Filtrowanie UI | `filterProducts()` po `product.name` |
| Endpoint | `GET /api/Document/GetDocumentAutofillInfo/1` |
| Zapytanie backend | `Products.Query().Where(p => p.UserFirmId == userFirmId)` |
| Tabela | `Product` |

## 4. Lista serii dokumentu

| Atrybut | Wartosc |
|---|---|
| Pole | `documentSeries` |
| Zrodlo UI | `invoiceAutofillData.documentSeries` |
| Endpoint | `GET /api/Document/GetDocumentAutofillInfo/1` |
| Zapytanie backend | `DocumentSeries.Query().Where(ds => ds.UserFirmId == userFirmId && ds.DocumentTypeId == documentTypeId).Include(ds => ds.DocumentType)` |
| Tabele | `DocumentSeries`, `DocumentType` |

## 5. Lista statusow

| Atrybut | Wartosc |
|---|---|
| Pole | `documentStatus` |
| Widocznosc | Tylko tryb edycji |
| Endpoint | `GET /api/Document/GetDocumentAutofillInfo/1` |
| Zapytanie backend | `DocumentStatuses.Query().ToListAsync()` |
| Tabela | `DocumentStatus` |
