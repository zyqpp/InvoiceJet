# E-10 AddOrEditInvoiceComponent — Formularz faktury

| Pole | Wartość |
|---|---|
| ID dokumentu | E-10 |
| Typ dokumentu | ekran |
| Wersja | 1.0 |
| Status | zweryfikowany |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran tworzenia i edycji faktury zwykłej (`DocumentTypeId = 1`). Logika formularza pochodzi z klasy abstrakcyjnej `BaseInvoiceComponent`; `AddOrEditInvoiceComponent` dostarcza tylko `getDocumentTypeId() = 1` i `getNavigationUrl() = "/dashboard/invoices"`. W trybie dodawania URL to `/dashboard/add-invoice`, w trybie edycji `/dashboard/edit-invoice/:id`. Formularz zawiera dane dokumentu, autocomplete klienta i produktów oraz dynamiczną tabelę pozycji z obliczaniem cen w czasie rzeczywistym.

---

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────────────────┐
│ ← [Wróć]   Invoice Details - FV0007   [Unpaid chip]             │
├──────────────────────────────────────────────────────────────────┤
│ [Client Name or CUI*] [Issue Date*] [Due Date] [Status*]        │
├──────────────────────────────────────────────────────────────────┤
│ Tabela pozycji:                                                  │
│ Name | Unit Price | Qty | U.M. | TVA% | Contains TVA | Total | ✕│
│ [Wiersz 1]                                                       │
│ [+ Dodaj pozycję]                                               │
├──────────────────────────────────────────────────────────────────┤
│ [Save / Update]    [Preview PDF]    [Generate PDF]              │
└──────────────────────────────────────────────────────────────────┘
```

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL (dodaj) | `/dashboard/add-invoice` |
| Ścieżka URL (edycja) | `/dashboard/edit-invoice/:id` |
| Wymagana rola | `User` (AuthGuard JWT) |
| Punkty wejścia | [OP-E09-01 New Invoice](../E-09_InvoicesComponent/E-09_ekran.md#op-e09-01-new-invoice); klik wiersza [OP-E09-02 Edytuj](../E-09_InvoicesComponent/E-09_ekran.md#op-e09-02-edytuj-fakture) |
| Komponent Angular | [`AddOrEditInvoiceComponent`](../../../../InvoiceJetUI/src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.ts) |
| Klasa bazowa | [`BaseInvoiceComponent`](../../../../InvoiceJetUI/src/app/components/invoices/base-invoice/base-invoice.component.ts) |
| Szablon HTML | [`add-or-edit-invoice.component.html`](../../../../InvoiceJetUI/src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.html) |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek | Uprawnienie |
|---|---|---|---|
| `/dashboard/invoices` | [OP-E10-03 Save / Update](#op-e10-03-save--update) sukces | formularz poprawny | User |
| `/dashboard/invoices` | [OP-E10-06 Wróć](#op-e10-06-wróć) | zawsze | User |
| Modal PdfViewer | [OP-E10-04 Preview PDF](#op-e10-04-preview-pdf) | zawsze | User |

---

## Tryby działania

| Tryb | URL | `isEditMode` | Zachowanie |
|---|---|---|---|
| Dodawanie | `/dashboard/add-invoice` | `false` | pusty formularz, `addDocument()` na submit |
| Edycja | `/dashboard/edit-invoice/:id` | `true` | ładuje dokument przez `loadDocument(id)`, `updateDocument()` na submit |

Tryb ustalany w `ngOnInit()` przez `+params["id"]` — jeśli `id` jest w route params, `isEditMode = true`.

---

## Filtry (autocomplete)

### FILTR-E10-01 Autocomplete klienta (Client Name or CUI)

| Atrybut | Wartość |
|---|---|
| ID | FILTR-E10-01 |
| Etykieta UI | „Client Name or CUI" |
| Nazwa w kodzie | `invoiceForm.get('client')` |
| Typ kontrolki | `mat-autocomplete` (input z podpowiedziami) |
| Zawęża | lista podpowiedzi klientów |
| Parametr API | brak — filtrowanie klienckie na `invoiceAutofillData.clients` |
| Pole DTO autofill | [DTO-10 DocumentAutofillInfoDto](../../../05_model_danych/02_dto/DTO-10_DocumentAutofillInfoDto.md) → `Clients[]` |
| Pola filtrowane | `Firm.Name` (contains, case-insensitive) + `Firm.Cui` (contains, case-insensitive) |
| Wartości dopuszczalne | dowolny string; obsługuje zarówno obiekt `IFirm` jak i string |
| Domyślna wartość | `null` (wymagane) |
| Wymagany | tak |

**Zachowanie:**

| Aspekt | Opis |
|---|---|
| Moment zastosowania | `valueChanges` → `filterClients()` — na bieżąco przy wpisywaniu |
| Filtrowanie | `firm.name.includes(value) OR firm.cui.includes(value)` |
| Po wyborze | `displayFn(firm)` wyświetla `firm.name` |
| Efekt na formularz | `invoiceForm.client` = `IFirm` object |

**Dane testowe:**

| Scenariusz | Dane wejściowe | Oczekiwany efekt |
|---|---|---|
| Filtr po nazwie | `"ABC"` | lista firm zawierających „ABC" |
| Filtr po CUI | `"12345"` | lista firm z CUI zawierającym „12345" |
| Wybór firmy | klik na podpowiedź | `client` = `IFirm` object, pole pokazuje `firm.name` |
| Puste pole | submit bez wyboru | błąd walidacji Validators.required |

---

### FILTR-E10-02 Autocomplete produktu (Name — per wiersz pozycji)

| Atrybut | Wartość |
|---|---|
| ID | FILTR-E10-02 |
| Etykieta UI | „Name" (w każdym wierszu tabeli pozycji) |
| Nazwa w kodzie | `productsFormArray.at(i).get('name')` |
| Typ kontrolki | `mat-autocomplete` per wiersz |
| Zawęża | lista produktów z katalogu |
| Parametr API | brak — filtrowanie klienckie na `invoiceAutofillData.products` |
| Pole DTO autofill | [DTO-10](../../../05_model_danych/02_dto/DTO-10_DocumentAutofillInfoDto.md) → `Products[]` |
| Pola filtrowane | `Product.Name` (contains, case-insensitive) |
| Domyślna wartość | `null` (wymagane) |
| Wymagany | tak |

**Zachowanie po wyborze produktu (onProductSelected):**
Autouzupełnia pozostałe pola wiersza danymi z katalogu:
- `unitPrice` ← `product.price`
- `unitOfMeasurement` ← `product.unitOfMeasurement`
- `tvaValue` ← `product.tvaValue`
- `containsTva` ← `product.containsTva`
- Wywołuje `calculateTotalPrice(index)`

---

## Pola formularza

### POLE-E10-01 Client (klient)

| Atrybut | Wartość |
|---|---|
| ID | POLE-E10-01 |
| Etykieta UI | „Client Name or CUI" |
| Nazwa w kodzie | `invoiceForm.get('client')` |
| Typ pola UI | `mat-autocomplete` |
| Źródło danych | autofill: [GET /api/Document/GetDocumentAutofillInfo/1](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetAutofillInfo.md) |
| Pole DTO | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) → `Client: FirmRequestDto` |
| Pole DB | `Document.ClientId` → `Firm.Id` | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Typ danych | `IFirm` (obiekt) |
| Walidacja | `Validators.required` |
| Wymagalność | wymagane |
| Domyślna wartość | `null` |

---

### POLE-E10-02 Issue Date (data wystawienia)

| Atrybut | Wartość |
|---|---|
| ID | POLE-E10-02 |
| Etykieta UI | „Issue Date" |
| Nazwa w kodzie | `invoiceForm.get('issueDate')` |
| Typ pola UI | `mat-datepicker` |
| Pole DTO | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) → `IssueDate: DateTime` |
| Pole DB | `Document.IssueDate` | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Typ danych | `DateTime` |
| Walidacja | `Validators.required` |
| Domyślna wartość | `new Date()` (dzisiaj) |

---

### POLE-E10-03 Due Date (termin płatności)

| Atrybut | Wartość |
|---|---|
| ID | POLE-E10-03 |
| Etykieta UI | „Due Date" |
| Nazwa w kodzie | `invoiceForm.get('dueDate')` |
| Typ pola UI | `mat-datepicker` |
| Pole DTO | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) → `DueDate: DateTime` |
| Pole DB | `Document.DueDate` (nullable) | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Typ danych | `DateTime` nullable |
| Walidacja | `dueDateValidator` (custom — musi być po Issue Date) |
| Wymagalność | opcjonalne |
| Domyślna wartość | `null` |

---

### POLE-E10-04 Document Series (seria dokumentu)

| Atrybut | Wartość |
|---|---|
| ID | POLE-E10-04 |
| Etykieta UI | „Document Series" |
| Nazwa w kodzie | `invoiceForm.get('documentSeries')` |
| Typ pola UI | `mat-select` |
| Źródło danych | autofill: `invoiceAutofillData.documentSeries` (filtrowane po `DocumentTypeId=1`) |
| Pole DTO | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) → `DocumentSeries: DocumentSeriesRequestDto` |
| Pole DB | brak FK w Document (numer generowany jako string) → `DocumentSeries.SeriesName + CurrentNumber` |
| Walidacja | brak (nie jest wymagane przez Validators — anomalia BA-05) |
| Domyślna wartość | `null` |

---

### POLE-E10-05 Document Status (status)

| Atrybut | Wartość |
|---|---|
| ID | POLE-E10-05 |
| Etykieta UI | „Status" |
| Nazwa w kodzie | `invoiceForm.get('documentStatus')` |
| Typ pola UI | `mat-select` |
| Źródło danych | autofill: `invoiceAutofillData.documentStatuses` |
| Pole DTO | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) → `DocumentStatusId: int` |
| Pole DB | `Document.DocumentStatusId` → `DocumentStatus.Id` | [dbo.DocumentStatus](../../../05_model_danych/01_db/dbo/dbo.DocumentStatus.md) |
| Wartości | `Unpaid` (id=1), `Paid` (id=2) — seedowane |
| Walidacja | brak (nie jest wymagane — anomalia BA-05) |
| Domyślna wartość | `null` (backend ustawia `DocumentStatusEnum.Unpaid` przy dodaniu) |

---

## Tabele i listy

### TAB-E10-01 Tabela pozycji dokumentu (Products)

| Atrybut | Wartość |
|---|---|
| ID | TAB-E10-01 |
| Nazwa w UI | brak nagłówka nad tabelą |
| Źródło danych | `FormArray` (`invoiceForm.get('products')`) — nie API |
| Typ Angular | `MatTableDataSource` z danymi z `FormArray.controls` |
| Paginacja | nie |
| Sortowanie | nie |
| Selekcja | nie (brak checkboxów) |

#### Kolumny tabeli pozycji

| ID | Nagłówek UI | Pole FormGroup | Pole DTO | Pole DB | Typ | Opis |
|---|---|---|---|---|---|---|
| KOL-E10-01 | Name | `name` | `DocumentProductRequestDto.Name` | `Product.Name` (snapshot) | string | autocomplete z katalogu produktów |
| KOL-E10-02 | Unit Price | `unitPrice` | `DocumentProductRequestDto.UnitPrice` | `DocumentProduct.UnitPrice` | decimal | cena netto jednostkowa; przelicza `totalPrice` |
| KOL-E10-03 | Quantity | `quantity` | `DocumentProductRequestDto.Quantity` | `DocumentProduct.Quantity` | decimal | min=1; przelicza `totalPrice` |
| KOL-E10-04 | U.M. | `unitOfMeasurement` | `DocumentProductRequestDto.UnitOfMeasurement` | brak w DB (snapshot) | string | domyślnie „buc" |
| KOL-E10-05 | TVA Value | `tvaValue` | `DocumentProductRequestDto.TvaValue` | brak w DB — nie persystowane | decimal | stawka VAT %; domyślnie 19 |
| KOL-E10-06 | Contains TVA | `containsTva` | `DocumentProductRequestDto.ContainsTva` | brak bezpośrednio | bool | checkbox; przelicza `unitPrice` gdy zmiana |
| KOL-E10-07 | Total Price | `totalPrice` | `DocumentProductRequestDto.TotalPrice` | `DocumentProduct.TotalPrice` | decimal | obliczane przez frontend: `unitPrice×qty×(1+tva/100)` |
| KOL-E10-08 | Actions | — | — | — | — | przycisk usuń wiersz (✕) → `deleteProduct(i)` |

**Obliczenia w tabeli:**
→ [ALG-Wyliczeniowe-ObliczanieCenyPozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) — wzór: `unitPrice × qty × (1 + tvaValue/100)`

---

## Operacje

### OP-E10-01 Dodaj pozycję (Add Product)

| Atrybut | Wartość |
|---|---|
| ID | OP-E10-01 |
| Etykieta UI | „+" lub „Add Product" (ikona/przycisk) |
| Wyzwalacz | `(click)` → `addProduct()` |
| Wywoływane API | brak |
| Efekt | dodaje nowy `FormGroup` do `productsFormArray` z wartościami domyślnymi; odświeża `dataSource` |

**Wartości domyślne nowego wiersza:**

| Pole | Domyślna wartość |
|---|---|
| `id` | `0` |
| `name` | `null` (wymagane) |
| `unitPrice` | `null` (wymagane, min=0) |
| `totalPrice` | `null` (wymagane, min=0) |
| `quantity` | `1` (wymagane, min=1) |
| `unitOfMeasurement` | `"buc"` (wymagane) |
| `tvaValue` | `19` (wymagane, min=0) |
| `containsTva` | `false` |

---

### OP-E10-02 Usuń pozycję

| Atrybut | Wartość |
|---|---|
| ID | OP-E10-02 |
| Etykieta UI | ✕ w kolumnie „Actions" wiersza |
| Wyzwalacz | `(click)` → `deleteProduct(index)` |
| Wywoływane API | brak (operacja na FormArray) |
| Efekt | `productsFormArray.removeAt(index)` + odświeżenie `dataSource` |

---

### OP-E10-03 Save / Update

| Atrybut | Wartość |
|---|---|
| ID | OP-E10-03 |
| Etykieta UI | „Save" (dodawanie) / „Update" (edycja) |
| Wyzwalacz | `(click)` → `onSubmit()` |
| Walidacja pre-submit | `invoiceForm.invalid` → return (bez akcji) |
| Wywoływane API (dodaj) | [POST /api/Document/AddDocument](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md) |
| Wywoływane API (edycja) | [PUT /api/Document/EditDocument](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Edit.md) |
| DTO żądania | [DTO-07 DocumentRequestDto](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Powiązany proces (dodaj) | [dodaj_dokument](../../../02_procesy/dokumenty/dodaj_dokument/proces.md) |
| Powiązany proces (edycja) | [edytuj_dokument](../../../02_procesy/dokumenty/edytuj_dokument/proces.md) |
| Wymagana rola | User |

**Pola wejściowe (z formularza do DTO):**

| Pole formularza | Pole DTO | Pole DB | Walidacja |
|---|---|---|---|
| `client` | `Client: FirmRequestDto` | `Document.ClientId` | wymagane |
| `issueDate` | `IssueDate: DateTime` | `Document.IssueDate` | wymagane |
| `dueDate` | `DueDate: DateTime` | `Document.DueDate` | po issueDate (dueDateValidator) |
| `documentSeries` | `DocumentSeries: DocumentSeriesRequestDto` | używany do generowania numeru | opcjonalne (anomalia) |
| `documentStatus` | `DocumentStatusId: int` | `Document.DocumentStatusId` | opcjonalne (anomalia) |
| `products[]` | `Products: DocumentProductRequestDto[]` | `DocumentProduct.*` | każdy wiersz: name/unitPrice/quantity wymagane |

**Możliwe wyniki:**

| Wynik | Warunek | Komunikat | Akcja UI |
|---|---|---|---|
| Sukces | HTTP 200 | toastr: „Document added/updated successfully" | `router.navigateByUrl("/dashboard/invoices")` |
| Błąd walidacji | `invoiceForm.invalid` | brak komunikatu (cichy return) | formularz pozostaje |
| Błąd serwera | HTTP 4xx/5xx | brak obsługi (anomalia BA-06) | brak reakcji UI |

**Dane testowe:**

| Pole | Wartość testowa | Uwagi |
|---|---|---|
| `client.id` | `2` | id istniejącej firmy klienta |
| `issueDate` | `"2026-05-31"` | ISO date |
| `dueDate` | `"2026-06-30"` | musi być po issueDate |
| `documentSeries.id` | `1` | id serii dla DocumentTypeId=1 |
| `documentStatus.id` | `1` | 1=Unpaid (seedowane) |
| `products[0].name` | `"Consulting"` | string |
| `products[0].unitPrice` | `100.00` | decimal min=0 |
| `products[0].quantity` | `2` | int min=1 |
| `products[0].tvaValue` | `19` | % |
| `products[0].totalPrice` | `238.00` | 100×2×1.19 |
| JWT | `Authorization: Bearer <token>` rola User | prereq |

---

### OP-E10-04 Preview PDF

| Atrybut | Wartość |
|---|---|
| ID | OP-E10-04 |
| Etykieta UI | „Preview" |
| Wyzwalacz | `(click)` → `getInvoicePdfStream()` |
| Wywoływane API | [POST /api/Document/GetInvoicePdfStream](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) |
| DTO żądania | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) + `documentType`, `documentNumber`, `documentStatus` |
| Efekt | otwiera [MODAL-E10-01 PdfViewer](#modale) z blob URL |
| Wymagana rola | User |

> ⚠️ Anomalia BA-01: `// if (this.invoiceForm.invalid) return;` zakomentowane — Preview działa nawet dla niepoprawnego formularza.

**Dane testowe:**

| Scenariusz | Prereq | Oczekiwany wynik |
|---|---|---|
| Preview istniejącej faktury | id=42, tryb edycji | otwiera modal z PDF |
| Preview nowej (niezapisanej) | tryb dodawania, formularz wypełniony | otwiera modal (walidacja pominięta) |

---

### OP-E10-05 Generate PDF

| Atrybut | Wartość |
|---|---|
| ID | OP-E10-05 |
| Etykieta UI | „Generate" |
| Wyzwalacz | `(click)` → `generateInvoicePdf()` |
| Wywoływane API | [POST /api/Document/GenerateDocumentPdf](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GeneratePdf.md) |
| DTO żądania | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Efekt | PDF zapisywany na dysku serwera; klient nie dostaje pliku |
| Wymagana rola | User |

> ⚠️ Anomalia BA-02: odpowiedź API jest ignorowana — tylko `console.log("Invoice pdf generated successfully")`. Brak potwierdzenia w UI.
> ⚠️ Anomalia PDF-01: hardcodes `new InvoiceDocument()` — zawsze faktura, nawet dla proformy/storna.

---

### OP-E10-06 Wróć

| Atrybut | Wartość |
|---|---|
| ID | OP-E10-06 |
| Etykieta UI | „←" (strzałka/ikona wstecz) |
| Wyzwalacz | `(click)` → `goBack()` |
| Wywoływane API | brak |
| Efekt | `router.navigateByUrl("/dashboard/invoices")` |

---

## Modale

| ID | Nazwa | Wywołane przez | Link |
|---|---|---|---|
| MODAL-E10-01 | PdfViewerComponent | [OP-E10-04 Preview PDF](#op-e10-04-preview-pdf) | [E-DIALOG-05 PdfViewer](../E-DIALOG-05_PdfViewerComponent/E-DIALOG-05_modal.md) |

---

## Powiadomienia

| ID | Typ | Treść | Kiedy |
|---|---|---|---|
| POW-E10-01 | toastr success | „Document added successfully" | po sukcesie `addDocument()` |
| POW-E10-02 | toastr success | „Document updated successfully" | po sukcesie `updateDocument()` |

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint | DTO | Proces |
|---|---|---|---|---|
| Załadowanie autofill | GET | [/api/Document/GetDocumentAutofillInfo/1](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetAutofillInfo.md) | [DTO-10](../../../05_model_danych/02_dto/DTO-10_DocumentAutofillInfoDto.md) | — |
| Załadowanie dokumentu (edycja) | GET | [/api/Document/GetDocumentById/{id}](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetById.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) | — |
| Zapisz nową fakturę | POST | [/api/Document/AddDocument](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) | [dodaj_dokument](../../../02_procesy/dokumenty/dodaj_dokument/proces.md) |
| Zaktualizuj fakturę | PUT | [/api/Document/EditDocument](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Edit.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) | [edytuj_dokument](../../../02_procesy/dokumenty/edytuj_dokument/proces.md) |
| Podgląd PDF | POST | [/api/Document/GetInvoicePdfStream](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) | — |
| Generuj PDF | POST | [/api/Document/GenerateDocumentPdf](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GeneratePdf.md) | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) | — |

---

## Informacje dla testów automatycznych

### Autoryzacja (prereq dla każdego testu)

| Wymaganie | Szczegół |
|---|---|
| Typ autoryzacji | JWT Bearer token |
| Rola wymagana | `"User"` |
| Nagłówek HTTP | `Authorization: Bearer <token>` |
| Uzyskanie tokenu | [POST /api/Auth/login](../../../04_api_i_integracje/01_api_frontend/auth/POST_Auth_login.md) |

### Prereq w DB (dane potrzebne do testów)

| Encja | Minimalne dane |
|---|---|
| Firma klienta | `Firm` z `UserFirm.IsClient=true` (z `Firm.Id`) |
| Seria dokumentów | `DocumentSeries` z `DocumentTypeId=1`, `UserFirmId=aktywny` |
| Statuses | seedowane: `Unpaid` (id=1), `Paid` (id=2) |
| Produkt (opcjonalnie) | `Product` z `UserFirmId=aktywny` (dla autocomplete) |

### Selektory komponentów

| Element | Selektor CSS | Uwagi |
|---|---|---|
| Pole Client | `input[placeholder*="CUI"]` lub `mat-autocomplete` | — |
| Pole Issue Date | `input[matDatepicker]` (pierwszy) | — |
| Pole Due Date | `input[matDatepicker]` (drugi) | — |
| Select Status | `mat-select` z etykietą „Status" | — |
| Wiersze pozycji | `tr` w `mat-table` formularza | — |
| Przycisk Add Product | `button` z tekstem „+" / „Add Product" | — |
| Przycisk Save/Update | `button[type=submit]` lub `(click)=onSubmit()` | — |
| Przycisk Preview | `button` z tekstem „Preview" | — |
| Przycisk Generate | `button` z tekstem „Generate" | — |
| Przycisk Wróć | `button` z ikoną `arrow_back` | — |

> Brak `data-cy` — anomalia BA-07.

### Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E10-01 | Wyświetlenie pustego formularza (dodaj) | seria TypeId=1, klient, status | GET /add-invoice | formularz z domyślnym issueDate=dzisiaj |
| TC-E10-02 | Załadowanie istniejącej faktury (edycja) | faktura id=42 | GET /edit-invoice/42 | formularz wypełniony danymi faktury 42 |
| TC-E10-03 | Dodanie faktury (happy path) | klient id=2, seria id=1 | wypełnij formularz → Save | toastr success + redirect do /invoices |
| TC-E10-04 | Walidacja — brak klienta | — | submit bez klienta | formularz nie wysyła, pole client w błędzie |
| TC-E10-05 | Walidacja — due date przed issue date | — | issueDate=2026-06-01, dueDate=2026-05-01 | pole dueDate w błędzie (dueDateValidator) |
| TC-E10-06 | Dodanie pozycji | — | klik Add Product | nowy wiersz z domyślnymi wartościami |
| TC-E10-07 | Usunięcie pozycji | ≥2 wiersze | klik ✕ na wierszu | wiersz znika z tabeli |
| TC-E10-08 | Autocomplete klienta | klient „ABC SRL" w DB | wpisz „ABC" | podpowiedź z „ABC SRL" |
| TC-E10-09 | Autocomplete produktu | produkt „Consulting" w DB | wpisz „Con" | podpowiedź z „Consulting" |
| TC-E10-10 | Preview PDF | faktura id=42, tryb edycja | klik Preview | otwiera modal PdfViewer |
| TC-E10-11 | Wróć | dowolny stan | klik ← | redirect do /invoices |
| TC-E10-12 | Brak autoryzacji | brak tokenu | GET /add-invoice | redirect do /login |

---

## Powiązania

| Typ | Dokument |
|---|---|
| Ekran poprzedni | [E-09 InvoicesComponent](../E-09_InvoicesComponent/E-09_ekran.md) |
| Modal PdfViewer | [E-DIALOG-05 PdfViewerComponent](../E-DIALOG-05_PdfViewerComponent/E-DIALOG-05_modal.md) |
| API: autofill | [GET /Document/GetDocumentAutofillInfo](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetAutofillInfo.md) |
| API: pobierz dokument | [GET /Document/GetDocumentById](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetById.md) |
| API: dodaj | [POST /Document/AddDocument](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md) |
| API: edytuj | [PUT /Document/EditDocument](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Edit.md) |
| API: PDF stream | [POST /Document/GetInvoicePdfStream](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) |
| DTO | [DTO-07 DocumentRequestDto](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| DTO | [DTO-10 DocumentAutofillInfoDto](../../../05_model_danych/02_dto/DTO-10_DocumentAutofillInfoDto.md) |
| Model DB | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Model DB | [dbo.DocumentProduct](../../../05_model_danych/01_db/dbo/dbo.DocumentProduct.md) |
| Algorytm | [ALG-Wyliczeniowe-ObliczanieCenyPozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) |
| Algorytm | [ALG-Wyliczeniowe-AktualizacjaProduktow](../../../03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md) |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`add-or-edit-invoice.component.ts`](../../../../InvoiceJetUI/src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.ts) |
| Klasa bazowa TS | [`base-invoice.component.ts`](../../../../InvoiceJetUI/src/app/components/invoices/base-invoice/base-invoice.component.ts) |
| Szablon HTML | [`add-or-edit-invoice.component.html`](../../../../InvoiceJetUI/src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.html) |
| Walidator daty | [`date-validator.ts`](../../../../InvoiceJetUI/src/app/components/invoices/base-invoice/date-validator.ts) |
| Model interfejsu | [`IDocumentRequest.ts`](../../../../InvoiceJetUI/src/app/models/IDocumentRequest.ts) |
| Serwis | [`document.service.ts`](../../../../InvoiceJetUI/src/app/services/document.service.ts) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| BA-01 | `// if (this.invoiceForm.invalid) return;` zakomentowane w `getInvoicePdfStream()` — Preview PDF bez walidacji |
| BA-02 | `generateInvoicePdf()` ignoruje odpowiedź API — brak feedbacku dla użytkownika |
| BA-03 | Brak obsługi błędów dla `updateDocument()` i `addDocument()` — błąd serwera cichy |
| BA-04 | `console.log("Filtering products", value)` i inne `console.log` aktywne w produkcji |
| BA-05 | `documentSeries` i `documentStatus` nie mają `Validators.required` — można zapisać fakturę bez serii |
| BA-06 | Brak komunikatu błędu dla `addDocument` / `updateDocument` — nieobsłużony `.error()` handler |
| BA-07 | Brak `data-cy` / `data-testid` — selektory testów nieodporne na zmiany |
| BA-08 | `getInvoicePdfStream()` odczytuje `this.currentDocument.documentNumber` — może być `undefined` w trybie dodawania |

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkic na podstawie kodu. |
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Wersja pełna — pola, filtry autocomplete, tabela pozycji, operacje z API/DTO, testy e2e. |
