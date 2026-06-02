# Scenariusze testów automatycznych E2E: Faktury

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-AUTO-E2E-FAKTURY |
| Typ dokumentu | scenariusze testów automatycznych E2E |
| Wersja | 1.0 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-06-02 |
| Narzędzie | Playwright (TypeScript) |

## Streszczenie

Scenariusze pokrywają wystawianie faktur (z weryfikacją obliczeń ALG-05), walidację formularza, konwersję na storno (ALG-08), podgląd PDF (ALG-07) oraz weryfikację buga A-KRIT-04 dla proformy. Selektory zweryfikowane w `add-or-edit-invoice.component.html` i `invoices.component.html`.

> **Uwaga architektoniczna:** Strona `/dashboard/invoices` nie ma przycisku "PDF" per wiersz — otwarcie PDF odbywa się przez kliknięcie wiersza (-> ekran edycji) i kliknięcie przycisku "Preview" (`button[mat-raised-button]:has-text("Preview")`). Uwzględnione w TC-AUTO-013.

---

## TC-AUTO-010: Wystawienie faktury z weryfikacją obliczeń pozycji i sumy

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane algorytmy:**
- [ALG-05 Document Total Calculation](../../03_algorytmy/ALG-05_DocumentTotalCalculation.md)
- [ALG-02 Document Number Generation](../../03_algorytmy/ALG-02_DocumentNumberGeneration.md)

**Powiązane API:**
- `GET /api/Document/GetDocumentAutofillInfo/1`
- `POST /api/Document/AddDocument`

**Prereq w DB:**
- Zalogowany użytkownik z kontem `auto_invoice_010@invoicejet.test` / `Invoice010!`
- Rekord `UserFirm` z powiązaną firmą (`firmName = "FIRMA TESTOWA SRL"`, `cuiValue = "12345678"`)
- Seria dokumentów: `seriesName = "FV"`, `currentNumber = 1`, `documentTypeId = 1` (Invoice), powiązana z `UserFirm`
- Klient (`isClient = true`): `name = "KLIENT TESTOWY SRL"`, `cui = "87654321"`, powiązany z `UserFirm`
- Konto bankowe: `iban = "RO49AAAA1B31007593840000"`, powiązane z `UserFirm`

### Kroki

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | login helper | — | `auto_invoice_010@invoicejet.test` / `Invoice010!` | Token JWT w localStorage; na `/dashboard` |
| 2 | navigate | URL bar | `/dashboard/invoices` | Lista faktur załadowana; widoczny nagłówek "Invoices" |
| 3 | click | `button[mat-raised-button]:has-text("New Invoice")` | — | Redirect na `/dashboard/add-invoice`; `GET /api/Document/GetDocumentAutofillInfo/1` wywołany (status 200) |
| 4 | verify loading | `mat-progress-bar` | — | Progress bar znika; formularz `[formGroup="invoiceForm"]` aktywny |
| 5 | fill autocomplete | `mat-form-field input[formControlName="client"]` | `KLIENT` | Pole tekstowe wypełnione; po chwili panel autocomplete `mat-autocomplete-panel` pojawia się |
| 6 | click autocomplete option | `mat-autocomplete-panel mat-option:first-child` | — | Klient "KLIENT TESTOWY SRL (87654321)" wybrany; pole wypełnione obiektem klienta |
| 7 | fill datepicker | `mat-form-field input[formControlName="issueDate"]` | `2026-06-02` | Data wystawienia ustawiona; format wyświetlania: "Jun 2, 2026" |
| 8 | fill datepicker | `mat-form-field input[formControlName="dueDate"]` | `2026-06-16` | Termin płatności ustawiony |
| 9 | click mat-select | `mat-select[formControlName="documentSeries"]` | — | Dropdown otwarty; widoczne opcje serii dokumentów |
| 10 | click mat-option | `mat-option:has-text("FV - 1")` | — | Seria "FV" z numerem bieżącym 1 wybrana |
| 11 | fill | `table[mat-table] tr[mat-row]:first-child mat-form-field input[formControlName="name"]` | `Servicii consultanta` | Pole nazwy produktu wypełnione w wierszu 1 |
| 12 | fill | `table[mat-table] tr[mat-row]:first-child mat-form-field input[formControlName="unitPrice"]` | `500` | Cena jednostkowa = 500.00; zdarzenie `change` wyzwolone |
| 13 | fill | `table[mat-table] tr[mat-row]:first-child mat-form-field input[formControlName="quantity"]` | `2` | Ilość = 2; zdarzenie `change` wyzwolone |
| 14 | fill | `table[mat-table] tr[mat-row]:first-child mat-form-field input[formControlName="unitOfMeasurement"]` | `buc` | Jednostka miary ustawiona |
| 15 | fill | `table[mat-table] tr[mat-row]:first-child mat-form-field input[formControlName="tvaValue"]` | `19` | TVA = 19%; zdarzenie `change` wyzwolone |
| 16 | verify totalPrice row 1 | `table[mat-table] tr[mat-row]:first-child input[formControlName="totalPrice"]` | `1190` | **[ALG-05]** Total Price wiersza 1 = 500 × 2 × (1 + 19/100) = 1190.00; pole `readonly` wyświetla 1190 |
| 17 | click | `button[mat-icon-button]:has(mat-icon:text("add_circle_outline"))` | — | Nowy wiersz pozycji dodany do tabeli |
| 18 | fill | `table[mat-table] tr[mat-row]:nth-child(2) mat-form-field input[formControlName="name"]` | `Transport` | Pole nazwy produktu wypełnione w wierszu 2 |
| 19 | fill | `table[mat-table] tr[mat-row]:nth-child(2) mat-form-field input[formControlName="unitPrice"]` | `100` | Cena jednostkowa = 100.00 |
| 20 | fill | `table[mat-table] tr[mat-row]:nth-child(2) mat-form-field input[formControlName="quantity"]` | `3` | Ilość = 3; zdarzenie `change` wyzwolone |
| 21 | fill | `table[mat-table] tr[mat-row]:nth-child(2) mat-form-field input[formControlName="unitOfMeasurement"]` | `buc` | Jednostka miary ustawiona |
| 22 | fill | `table[mat-table] tr[mat-row]:nth-child(2) mat-form-field input[formControlName="tvaValue"]` | `9` | TVA = 9%; zdarzenie `change` wyzwolone |
| 23 | verify totalPrice row 2 | `table[mat-table] tr[mat-row]:nth-child(2) input[formControlName="totalPrice"]` | `327` | **[ALG-05]** Total Price wiersza 2 = 100 × 3 × (1 + 9/100) = 327.00; pole `readonly` wyświetla 327 |
| 24 | click submit | `button[mat-raised-button]:has-text("Issue")` | — | `POST /api/Document/AddDocument` wywołany z `documentTypeId=1`; status 201 Created |
| 25 | expect redirect | URL bar | `/dashboard/invoices` | Redirect na listę faktur po pomyślnym zapisie |
| 26 | verify row visible | `table[mat-table] td[mat-cell]:has-text("FV0001")` | — | **[ALG-02]** Wiersz z numerem "FV0001" widoczny w tabeli faktur |

### Walidacja algorytmu

| Weryfikacja | Oczekiwana wartość | Jak sprawdzić |
|---|---|---|
| [ALG-05] totalPrice wiersza 1 = 500 × 2 × 1.19 | 1190.00 | Wartość inputa `[formControlName="totalPrice"]` w wierszu 1 = 1190 (krok 16) |
| [ALG-05] totalPrice wiersza 2 = 100 × 3 × 1.09 | 327.00 | Wartość inputa `[formControlName="totalPrice"]` w wierszu 2 = 327 (krok 23) |
| [ALG-05] Suma netto całego dokumentu | 500×2 + 100×3 = 1300.00 (netto) | Brak dedykowanego pola sumy netto na UI (CALC-01 — patrz doc ALG-05); zweryfikuj przez API: `GET /api/Document/GetById/{id}` → `unitPrice = 1300.00` |
| [ALG-05] Suma brutto całego dokumentu | 1190 + 327 = 1517.00 (brutto) | API: `GET /api/Document/GetById/{id}` → `totalPrice = 1517.00` |
| [ALG-02] Numer dokumentu = "FV0001" | `documentNumber = "FV0001"` (SeriesName="FV" + CurrentNumber=1 w formacie D4) | Wiersz "FV0001" w tabeli faktur (krok 26) |
| [ALG-02] Licznik serii inkrementowany | Seria "FV" ma `currentNumber = 2` po zapisie | API: `GET /api/DocumentSeries/GetAll` → seria FV ma `currentNumber = 2` |

### Cleanup

- Wykonaj `DELETE` na dokumencie FV0001 przez API lub UI (opcja "Delete selected" w menu `mat-menu`)
- Zresetuj `currentNumber` serii FV do 1 w DB: `UPDATE DocumentSeries SET CurrentNumber = 1 WHERE SeriesName = 'FV' AND UserFirmId = {id}`

---

## TC-AUTO-011: Walidacja formularza faktury — przypadki negatywne

**Typ:** Negatywny
**Priorytet:** Wysoki
**Powiązane algorytmy:**
- [ALG-05 Document Total Calculation](../../03_algorytmy/ALG-05_DocumentTotalCalculation.md)

**Powiązane API:**
- `POST /api/Document/AddDocument` (oczekiwany brak wywołania lub 400)

**Prereq w DB:**
- Zalogowany użytkownik z prereqami jak w TC-AUTO-010

### Kroki — podscenariusz A: Pusty formularz

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | login helper | — | `auto_invoice_010@invoicejet.test` / `Invoice010!` | Na `/dashboard` |
| 2 | navigate | URL bar | `/dashboard/add-invoice` | Formularz nowej faktury załadowany |
| 3 | click submit | `button[mat-raised-button]:has-text("Issue")` | — | Formularz NIE jest wysłany do API; nie ma redirect |
| 4 | verify error — client | `mat-form-field:has(input[formControlName="client"]) mat-error` | — | Błąd "CUI Value is required" lub "This field is required" widoczny pod polem client |
| 5 | verify error — issueDate | `mat-form-field:has(input[formControlName="issueDate"]) mat-error` | — | Błąd "Issue Date is required" widoczny |
| 6 | verify no redirect | URL bar | — | URL pozostaje `/dashboard/add-invoice` |

### Kroki — podscenariusz B: Brak klienta (po wcześniejszym wybraniu)

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | navigate | URL bar | `/dashboard/add-invoice` | Formularz załadowany |
| 2 | fill | `mat-form-field input[formControlName="client"]` | `KLIENT` | Autocomplete pojawia się |
| 3 | click autocomplete option | `mat-autocomplete-panel mat-option:first-child` | — | Klient wybrany |
| 4 | clear field | `mat-form-field input[formControlName="client"]` | `` (puste) | Pole klienta wyczyszczone; wartość formGroup["client"] = null lub "" |
| 5 | fill datepicker | `mat-form-field input[formControlName="issueDate"]` | `2026-06-02` | Data ustawiona |
| 6 | click submit | `button[mat-raised-button]:has-text("Issue")` | — | Formularz NIE jest wysłany lub API zwraca 400 |
| 7 | verify error — client | `mat-form-field:has(input[formControlName="client"]) mat-error` | — | Błąd wymagalności pod polem client widoczny |

### Kroki — podscenariusz C: Zapis bez pozycji (tylko nagłówek)

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | navigate | URL bar | `/dashboard/add-invoice` | Formularz załadowany |
| 2 | fill autocomplete | `mat-form-field input[formControlName="client"]` | `KLIENT TESTOWY SRL` | Klient wybrany z autocomplete |
| 3 | fill datepicker | `mat-form-field input[formControlName="issueDate"]` | `2026-06-02` | Data ustawiona |
| 4 | click mat-select | `mat-select[formControlName="documentSeries"]` | — | Dropdown serii otwarty |
| 5 | click mat-option | `mat-option:has-text("FV - 1")` | — | Seria FV wybrana |
| 6 | clear product row | `table[mat-table] tr[mat-row]:first-child input[formControlName="name"]` | `` (puste) | Pole nazwy produktu puste; wiersz bez danych |
| 7 | click submit | `button[mat-raised-button]:has-text("Issue")` | — | `POST /api/Document/AddDocument` wywołany ale serwer zwraca 400 Bad Request LUB brak wywołania API i błąd walidacji na froncie |
| 8 | verify no redirect | URL bar | — | URL pozostaje `/dashboard/add-invoice` |

### Walidacja algorytmu

| Weryfikacja | Oczekiwana wartość | Jak sprawdzić |
|---|---|---|
| [ALG-05] Brak pozycji = brak obliczeń | totalPrice dokumentu = 0 lub błąd API | Brak redirect na listę faktur po submicie bez pozycji |
| Angular Reactive Forms — required | `mat-error` widoczny po próbie submit z pustym polem | Obecność `mat-error` w DOM dla pola `client` i `issueDate` |

### Cleanup

- Brak (test nie tworzy danych)

---

## TC-AUTO-012: Przekształcenie faktury w storno

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane algorytmy:**
- [ALG-08 Transform To Storno](../../03_algorytmy/ALG-08_TransformToStorno.md)
- [ALG-02 Document Number Generation](../../03_algorytmy/ALG-02_DocumentNumberGeneration.md)

**Powiązane API:**
- `PUT /api/Document/TransformToStorno`
- `GET /api/Document/GetTableRecords` (documentTypeId=3)

**Prereq w DB:**
- Faktura FV0001 istnieje (po TC-AUTO-010 lub wstawiona przez fixture)
- Faktura ma `documentTypeId = 1` i `id = {invoiceId}`
- Zalogowany użytkownik będący właścicielem FV0001

### Kroki

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | login helper | — | `auto_invoice_010@invoicejet.test` / `Invoice010!` | Na `/dashboard` |
| 2 | navigate | URL bar | `/dashboard/invoices` | Lista faktur załadowana; wiersz "FV0001" widoczny |
| 3 | verify row exists | `table[mat-table] td[mat-cell]:has-text("FV0001")` | — | Wiersz FV0001 widoczny w tabeli |
| 4 | click checkbox in row | `table[mat-table] tr[mat-row]:has(td:has-text("FV0001")) mat-checkbox` | — | Checkbox przy FV0001 zaznaczony; `selection.isSelected(row)` = true |
| 5 | click more options button | `button[mat-stroked-button]:has(mat-icon:text("more_vert"))` | — | Menu `mat-menu` otwarte z opcjami: "Transform to storno", "Delete selected" |
| 6 | click menu item | `button[mat-menu-item]:has-text("Transform to storno")` | — | `PUT /api/Document/TransformToStorno` wywołany z tablicą ID faktur; status 200 OK |
| 7 | verify FV0001 absent | `table[mat-table] td[mat-cell]:has-text("FV0001")` | — | Wiersz FV0001 **NIE jest już** widoczny na liście faktur (documentTypeId zmieniony z 1 na 3) |
| 8 | navigate | URL bar | `/dashboard/invoice-stornos` | Lista storn załadowana |
| 9 | verify storno visible | `table[mat-table] td[mat-cell]:has-text("FV0001")` | — | **[ALG-08]** Dokument FV0001 widoczny na liście storn; documentTypeId = 3 |

### Walidacja algorytmu

| Weryfikacja | Oczekiwana wartość | Jak sprawdzić |
|---|---|---|
| [ALG-08] Mutacja istniejącego dokumentu — nie nowy | Ten sam `Id` dokumentu; tylko `DocumentTypeId` zmieniony z 1 na 3 | API: `GET /api/Document/GetById/{invoiceId}` → `documentTypeId = 3`; `id` niezmieniony |
| [ALG-08] Wartości TotalPrice pozostają dodatnie w DB | `TotalPrice` w DB = 1517.00 (ta sama wartość co przed konwersją) | API: `GET /api/Document/GetById/{invoiceId}` → `totalPrice = 1517.00` |
| [ALG-08] Dokument znika z listy faktur | `GET /api/Document/GetTableRecords?documentTypeId=1` nie zawiera FV0001 | Lista faktur na `/dashboard/invoices` nie pokazuje FV0001 (krok 7) |
| [ALG-08] Dokument widoczny na liście storn | `GET /api/Document/GetTableRecords?documentTypeId=3` zawiera FV0001 | Lista storn na `/dashboard/invoice-stornos` pokazuje FV0001 (krok 9) |
| [ALG-08] Wartości ujemne tylko na PDF | PDF storna pokazuje `-2`, `-1190.00` itp. (efekt szablonu) | Weryfikacja przez TC-AUTO-013 (PDF storna) |

### Cleanup

- Nie czyść — dokument FV0001 jako storno może być potrzebny dla kolejnych testów
- Alternatywnie: usuń cały dokument przez API `PUT /api/Document/DeleteDocument`

---

## TC-AUTO-013: Podgląd PDF faktury przez stream (PreviewPdf)

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane algorytmy:**
- [ALG-07 PDF Generation](../../03_algorytmy/ALG-07_PdfGeneration.md)

**Powiązane API:**
- `POST /api/Document/GetPdfStream`

**Prereq w DB:**
- Faktura FV0001 istnieje z `documentTypeId = 1` i kompletną strukturą (firma, klient, pozycje)
- Zalogowany użytkownik będący właścicielem FV0001

> **Uwaga implementacyjna:** Przycisk "Preview" PDF jest widoczny **tylko w trybie edycji** (`isEditMode = true`), czyli na ekranie `/dashboard/edit-invoice/{id}`. Nie ma przycisku PDF per wiersz na liście faktur.

### Kroki

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | login helper | — | `auto_invoice_010@invoicejet.test` / `Invoice010!` | Na `/dashboard` |
| 2 | navigate | URL bar | `/dashboard/invoices` | Lista faktur z FV0001 |
| 3 | click row FV0001 | `table[mat-table] tr[mat-row]:has(td:has-text("FV0001"))` | — | Redirect na `/dashboard/edit-invoice/{id}` (kliknięcie wiersza wywołuje `openEditInvoiceDialog(row)`) |
| 4 | verify edit mode | `h1:has-text("Invoice Details")` | — | Nagłówek "Invoice Details - FV0001" widoczny (`isEditMode = true`) |
| 5 | verify preview button | `button[mat-raised-button]:has-text("Preview")` | — | Przycisk "Preview" widoczny (tylko w trybie edycji) |
| 6 | intercept network | Monitoruj `POST /api/Document/GetPdfStream` | — | Przygotowanie przechwycenia żądania |
| 7 | click preview | `button[mat-raised-button]:has-text("Preview")` | — | Metoda `getInvoicePdfStream()` wywołana; `POST /api/Document/GetPdfStream` wysłany z `{id: invoiceId, documentTypeId: 1}` |
| 8 | verify API response | Network: `POST /api/Document/GetPdfStream` | — | Status 200 OK; Content-Type: `application/pdf`; odpowiedź to strumień binarny |
| 9 | expect dialog | `mat-dialog-container` | — | Dialog z komponentem `PdfViewerComponent` pojawia się |
| 10 | verify PDF content | `mat-dialog-container app-pdf-viewer` | — | Komponent PDF viewer załadowany; brak komunikatu błędu |

### Walidacja algorytmu

| Weryfikacja | Oczekiwana wartość | Jak sprawdzić |
|---|---|---|
| [ALG-07] Endpoint GetPdfStream wywołany | `POST /api/Document/GetPdfStream` status 200 | Przechwycony request w Network (krok 6-8) |
| [ALG-07] Content-Type to PDF | `application/pdf` | Nagłówek `Content-Type` odpowiedzi API |
| [ALG-07] PDF zawiera numer dokumentu | Tekst "FV0001" w PDF | Pobranie PDF i analiza: `page.waitForResponse(r => r.url().includes('GetPdfStream'))` + weryfikacja content |
| [ALG-07] PDF zawiera tytuł "Factura" | String "Factura" w bajtach PDF | Analiza odpowiedzi binarnej lub pobranie pliku i sprawdzenie tekstu |

### Cleanup

- Zamknij dialog jeśli otwarty: `page.keyboard.press('Escape')` lub klik poza dialogiem

---

## TC-AUTO-014: Generowanie PDF proformy — weryfikacja buga A-KRIT-04

**Typ:** Anomalia krytyczna — test powinien FAIL do czasu naprawienia buga
**Priorytet:** Wysoki
**Powiązane algorytmy:**
- [ALG-07 PDF Generation](../../03_algorytmy/ALG-07_PdfGeneration.md)

**Powiązane API:**
- `POST /api/Document/GenerateInvoicePdf` (API z bugiem hardcoded szablonu)
- `POST /api/Document/GetPdfStream` (API bez buga — ścieżka poprawna)

**Prereq w DB:**
- Proforma PRF0001 istnieje z `documentTypeId = 2`
- Seria "PRF" z `currentNumber = 1`, `documentTypeId = 2`
- Zalogowany użytkownik będący właścicielem PRF0001

> **Bug A-KRIT-04:** Endpoint `POST /api/Document/GenerateInvoicePdf` ma hardcoded szablon `InvoiceDocument` niezależnie od `documentTypeId`. Dla proformy (typeId=2) generuje PDF z tytułem "Factura" zamiast "Factura Proforma". Ten test weryfikuje istnienie buga i porównuje zachowanie obu endpointów.

### Kroki — Część 1: Weryfikacja buga w GenerateInvoicePdf (oczekiwane FAIL)

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | login helper | — | `auto_invoice_010@invoicejet.test` / `Invoice010!` | Na `/dashboard` |
| 2 | navigate | URL bar | `/dashboard/invoice-proformas` | Lista proform załadowana; PRF0001 widoczna |
| 3 | click row PRF0001 | `table[mat-table] tr[mat-row]:has(td:has-text("PRF0001"))` | — | Redirect na ekran edycji proformy |
| 4 | intercept network | Monitoruj `POST /api/Document/GenerateInvoicePdf` | — | Przygotowanie przechwycenia |
| 5 | click preview | `button[mat-raised-button]:has-text("Preview")` | — | `POST /api/Document/GetPdfStream` lub `POST /api/Document/GenerateInvoicePdf` wywołany |
| 6 | capture PDF | Pobierz binarną odpowiedź PDF | — | Status 200 OK; plik PDF zwrócony |
| 7 | verify PDF title — BUG | Analiza tekstu PDF | `"Factura Proforma"` | **OCZEKIWANE FAIL (BUG A-KRIT-04):** PDF zawiera "Factura" zamiast "Factura Proforma" — jeśli test PRZECHODZI, bug nadal istnieje; jeśli FAIL — bug naprawiony |

### Kroki — Część 2: Weryfikacja poprawnej ścieżki GetPdfStream

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 8 | API call direct | `POST /api/Document/GetPdfStream` z `{id: proformaId, documentTypeId: 2}` | Body: `{"id": {proformaId}, "documentTypeId": 2}` | Status 200 OK; PDF zwrócony |
| 9 | verify PDF title | Analiza tekstu PDF z GetPdfStream | `"Factura Proforma"` | Zweryfikuj czy GetPdfStream generuje poprawny tytuł "Factura Proforma" dla proformy |

### Walidacja algorytmu

| Weryfikacja | Oczekiwana wartość (stan z bugiem) | Jak sprawdzić |
|---|---|---|
| [ALG-07] GenerateInvoicePdf dla proformy — tytuł PDF | "Factura" (BUG — powinno być "Factura Proforma") | Pobranie PDF i wyszukanie tekstu "Factura Proforma" — test FAIL = bug istnieje |
| [ALG-07] GetPdfStream dla proformy — tytuł PDF | "Factura Proforma" (oczekiwane poprawne zachowanie) | Pobranie PDF przez GetPdfStream i wyszukanie "Factura Proforma" |
| [ALG-07] Porównanie endpointów | GenerateInvoicePdf ≠ GetPdfStream dla documentTypeId=2 | Oba testy porównawcze; różnica w tytule PDF |

> **Instrukcja dla CI/CD:** Ten test należy oznaczyć tagiem `@known-bug` lub `@xfail`. Test w Części 1 (kroki 1-7) powinien być oczekiwanym niepowodzeniem (`expect(pdfTitle).toBe('Factura Proforma')` → FAIL potwierdza bug). Test w Części 2 (kroki 8-9) powinien PRZEJŚĆ — GetPdfStream obsługuje typ poprawnie.

### Cleanup

- Zamknij dialog jeśli otwarty

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. Selektory zweryfikowane w `add-or-edit-invoice.component.html`, `invoices.component.html`, `invoice-proformas.component.html`. Obliczenia ALG-05 zweryfikowane. Bug A-KRIT-04 udokumentowany. |
