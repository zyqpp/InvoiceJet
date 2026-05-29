# Wystawienie nowej faktury - Scenariusze testowe E2E

## 1. Scenariusz pozytywny: wystawienie faktury

| Krok | Akcja testera | Oczekiwany wynik |
|---|---|---|
| 1 | Tester loguje sie i przechodzi do `/dashboard/invoices`. | Widoczny jest grid faktur. |
| 2 | Tester uruchamia dodanie faktury. | Aplikacja przechodzi do `/dashboard/add-invoice`. |
| 3 | Formularz pobiera dane pomocnicze. | API wywoluje `GET /api/Document/GetDocumentAutofillInfo/1`. |
| 4 | Tester wybiera klienta z listy. | Pole `client` zawiera obiekt `IFirm`. |
| 5 | Tester wybiera serie dokumentu. | Pole `documentSeries` zawiera obiekt `DocumentSeriesDto`. |
| 6 | Tester wybiera produkt i ustawia ilosc. | UI przelicza `totalPrice`. |
| 7 | Tester klika `Issue`. | Frontend wysyla `POST /api/Document/AddDocument`. |
| 8 | Backend zapisuje dokument. | W bazie powstaje rekord `Document`. |
| 9 | Backend zapisuje pozycje. | W bazie powstaja rekordy `DocumentProduct`. |
| 10 | Backend aktualizuje serie. | `DocumentSeries.CurrentNumber` zwieksza sie o `1`. |
| 11 | API zwraca `200 OK`. | UI pokazuje toastr i wraca do `/dashboard/invoices`. |

## 2. Scenariusz negatywny: brak klienta

| Krok | Akcja testera | Oczekiwany wynik |
|---|---|---|
| 1 | Tester otwiera `/dashboard/add-invoice`. | Formularz jest widoczny. |
| 2 | Tester zostawia puste pole klienta. | `invoiceForm.invalid` ma wartosc `true`. |
| 3 | Tester klika `Issue`. | `onSubmit()` konczy dzialanie bez wywolania API. |

## 3. Scenariusz negatywny: brak aktywnego konta bankowego

| Krok | Akcja testera | Oczekiwany wynik |
|---|---|---|
| 1 | Tester wypelnia poprawny formularz. | Formularz jest `valid`. |
| 2 | Tester klika `Issue`. | Frontend wysyla `POST /api/Document/AddDocument`. |
| 3 | Backend nie znajduje aktywnego konta. | `DocumentService.AddDocument()` rzuca `NoBankAccountAddedException`. |
| 4 | UI otrzymuje blad HTTP. | Komunikat zalezy od konfiguracji `ErrorInterceptor`. |

## 4. Scenariusz: podglad PDF w edycji

| Krok | Akcja testera | Oczekiwany wynik |
|---|---|---|
| 1 | Tester otwiera `/dashboard/edit-invoice/:id`. | Formularz laduje dokument przez `GET /api/Document/GetDocumentById/{documentId}`. |
| 2 | Tester klika `Preview`. | Frontend wysyla `POST /api/Document/GetInvoicePdfStream`. |
| 3 | Backend generuje PDF. | API zwraca plik `application/pdf`. |
| 4 | UI otwiera dialog. | `PdfViewerComponent` wyswietla blob PDF. |

## 5. Dane testowe minimalne

| Obiekt | Wymagane dane |
|---|---|
| Klient | Rekord `Firm` powiazany z uzytkownikiem przez `UserFirm.IsClient = true`. |
| Seria | Rekord `DocumentSeries` dla `DocumentTypeId = 1`. |
| Produkt | Rekord `Product` powiazany z aktywna firma. |
| Konto bankowe | Rekord `BankAccount` z `IsActive = true`. |
