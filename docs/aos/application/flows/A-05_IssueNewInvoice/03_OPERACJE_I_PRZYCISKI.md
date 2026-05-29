# Wystawienie nowej faktury - Operacje i przyciski

## 1. Tabela operacji

| Operacja | Element UI | Handler frontend | Endpoint | Backend | Skutek |
|---|---|---|---|---|---|
| Ladowanie formularza | wejscie na route | `loadAutofillData()` | `GET /api/Document/GetDocumentAutofillInfo/1` | `GetDocumentAutofillInfo()` | Formularz otrzymuje klientow, serie, statusy i produkty. |
| Dodanie pozycji | przycisk z ikona `add_circle_outline` | `addProduct()` | N/D | N/D | Dodaje nowy `FormGroup` w `products`. |
| Usuniecie pozycji | przycisk z ikona `delete` | `deleteProduct(i)` | N/D | N/D | Usuwa wiersz z `products`. |
| Przeliczenie ceny | zmiana ceny, ilosci albo TVA | `calculateTotalPrice(i)` | N/D | N/D | Aktualizuje `totalPrice` w UI. |
| Wystawienie faktury | przycisk `Issue` | `onSubmit()` | `POST /api/Document/AddDocument` | `AddDocument()` | Tworzy dokument i pozycje w bazie. |
| Aktualizacja faktury | przycisk `Update` | `onSubmit()` | `PUT /api/Document/EditDocument` | `EditDocument()` | Aktualizuje dokument i odtwarza pozycje. |
| Podglad PDF | przycisk `Preview` | `getInvoicePdfStream()` | `POST /api/Document/GetInvoicePdfStream` | `GetInvoicePdfStream()` | Otwiera `PdfViewerComponent`. |
| Powrot | przycisk z ikona `arrow_back` | `goBack()` | N/D | N/D | Przechodzi do `/dashboard/invoices`. |

## 2. Operacja wystawienia faktury

| Krok | Warstwa | Opis |
|---|---|---|
| 1 | UI | `onSubmit()` przerywa dzialanie, gdy `invoiceForm.invalid`. |
| 2 | UI | Komponent ustawia `documentData.documentType = { id: 1, name: "" }`. |
| 3 | Frontend HTTP | `DocumentService.addDocument()` wysyla `POST /api/Document/AddDocument`. |
| 4 | API | `DocumentController.AddDocument()` przyjmuje `DocumentRequestDto`. |
| 5 | Backend | `DocumentService.AddDocument()` pobiera `userFirmId`. |
| 6 | Backend | Backend wybiera aktywne konto bankowe firmy. |
| 7 | Baza | Backend zapisuje `Document`. |
| 8 | Baza | Backend usuwa istniejace pozycje dla dokumentu i zapisuje `DocumentProduct`. |
| 9 | Baza | Backend zwieksza `DocumentSeries.CurrentNumber`. |
| 10 | UI | Po sukcesie pojawia sie toastr i route wraca do `/dashboard/invoices`. |

## 3. Uwagi techniczne

| Obszar | Uwaga |
|---|---|
| Produkt istniejacy | Przy `DocumentProductRequestDto.Id > 0` backend wyszukuje `Product` po `Name` i `UserFirmId`. |
| Produkt nowy | Przy `Id == 0` backend mapuje `DocumentProductRequestDto` na `Product` i zapisuje go w `Product`. |
| Numer dokumentu | `DocumentNumber` powstaje z `DocumentSeries.SeriesName` oraz `CurrentNumber` formatowanego jako cztery cyfry. |
| Konto bankowe | Konto nie pochodzi z formularza. Backend wybiera pierwsze aktywne konto firmy. |
