# BaseInvoiceComponent — Abstrakcyjna klasa bazowa formularzy dokumentów

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-BaseInvoiceComponent |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Abstrakcyjna klasa bazowa (`abstract`) dla formularzy tworzenia i edycji dokumentów: faktury zwykłej, proformy i storna. Zawiera całą logikę UI i wywołania API wspólne dla wszystkich trzech typów dokumentów. Klasy pochodne dostarczają wyłącznie `getDocumentTypeId()` (identyfikator typu dokumentu: 1, 2 lub 3) oraz `getNavigationUrl()` (URL powrotu po zapisaniu). Nie jest samodzielnym ekranem — zawsze używany przez konkretne komponenty dziedziczące.

## Wizualizacja układu

```
┌─────────────────────────────────────────────────────┐
│ Nagłówek: Dodaj / Edytuj [typ dokumentu]            │
├─────────────────────────────────────────────────────┤
│ Klient (autocomplete) | Seria | Data wyst. | Termin │
├─────────────────────────────────────────────────────┤
│ Konto bankowe | Waluta | Status dokumentu           │
├─────────────────────────────────────────────────────┤
│ Tabela pozycji dokumentu                            │
│  name | cena | ilość | j.m. | VAT | brutto | akcje  │
├─────────────────────────────────────────────────────┤
│ Suma netto: ...  |  VAT: ...  |  Brutto: ...        │
├─────────────────────────────────────────────────────┤
│ [Generuj PDF]  [Podgląd PDF]  [Zapisz]  [Anuluj]   │
└─────────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | Niesamodzielny — używany przez: `/dashboard/add-invoice`, `/dashboard/edit-invoice/:id`, `/dashboard/add-invoice-proforma`, `/dashboard/edit-invoice-proforma/:id`, `/dashboard/edit-invoice-storno/:id` |
| Wymagana rola/uprawnienie | User (przez `AuthGuard`) |
| Punkty wejścia | Lista faktur, proform lub storn + nawigacja przez URL |
| Powiązany kod komponentu | `src/app/components/invoices/add-or-edit-invoice/base-invoice.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| `getNavigationUrl()` (lista dokumentów) | Sukces zapisu (onSubmit) | Formularz poprawny + API sukces | User |
| `PdfViewerComponent` | Klik „Podgląd PDF" | Zawsze | User |

## Sekcje ekranu

### Filtry

Brak.

### Tabele i listy

| ID tabeli | Nazwa | Link do dokumentu |
|---|---|---|
| TAB-BaseInvoice-Pozycje | Tabela pozycji dokumentu (FormArray) | — |

### Pola

| ID pola | Nazwa w UI | Wymagalność | Link do dokumentu |
|---|---|---|---|
| POLE-BaseInvoice-documentSeriesId | Seria dokumentu | wymagane | — |
| POLE-BaseInvoice-clientId | Klient | wymagane | — |
| POLE-BaseInvoice-bankAccountId | Konto bankowe | wymagane | — |
| POLE-BaseInvoice-issueDate | Data wystawienia | wymagane | — |
| POLE-BaseInvoice-dueDate | Termin płatności | wymagane | — |
| POLE-BaseInvoice-currency | Waluta | wymagane | — |
| POLE-BaseInvoice-documentStatus | Status dokumentu | wymagane | — |
| POLE-BaseInvoice-products | Tabela pozycji (FormArray) | wymagane (min. 1) | — |

### Pola w tabeli pozycji (FormArray)

| Pole | Kontrolka | Opis |
|---|---|---|
| `productId` | `mat-select` | Wybór produktu z katalogu |
| `quantity` | `input[type=number]` | Ilość |
| `price` | `input[type=number]` | Cena jednostkowa (autouzupełniana) |
| `vatRate` | `mat-select` | Stawka VAT (autouzupełniana) |
| `name` | `input` | Nazwa (autouzupełniana z produktu) |
| `measureUnit` | `input` | Jednostka miary (autouzupełniana) |

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-BaseInvoice-Zapisz | Zapisz / Submit | — |
| OP-BaseInvoice-GenerujPdf | Generuj PDF | — |
| OP-BaseInvoice-PodgladPdf | Podgląd PDF | — |
| OP-BaseInvoice-DodajPozycje | Dodaj pozycję (do tabeli) | — |
| OP-BaseInvoice-UsunPozycje | Usuń pozycję (z tabeli) | — |

### Modale

| ID modalu | Nazwa | Wywołane przez | Link do dokumentu |
|---|---|---|---|
| MODAL-Wspolne-PdfViewer | Podgląd PDF | OP-BaseInvoice-PodgladPdf | `../../modale_wspolne/pdf_viewer/modal.md` |

### Powiadomienia

Brak (komunikaty błędów inline lub przez `console.log` — anomalia).

## Stan komponentu (state)

| Pole | Typ | Opis |
|---|---|---|
| `isEditMode` | `boolean` | `true` gdy URL zawiera `:id` |
| `documentId` | `number` | ID edytowanego dokumentu |
| `autofillInfo` | `IDocumentAutofillInfo` | Dane wstępne (serie, klienci, konta) |
| `invoiceForm` | `FormGroup` | Reaktywny formularz dokumentu |
| `products` | `FormArray` | Tablica pozycji dokumentu |
| `totalNetAmount` | `number` | Suma netto (computed reaktywnie) |
| `totalVatAmount` | `number` | Suma VAT (computed reaktywnie) |
| `totalGrossAmount` | `number` | Suma brutto (computed reaktywnie) |

## Lifecycle

### ngOnInit
1. Sprawdzenie czy URL zawiera `:id` → ustawienie `isEditMode`
2. Wywołanie [GET /api/Document/GetAutofillInfo](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetAutofillInfo.md) → wypełnienie selektorów
3. Jeśli `isEditMode` → [GET /api/Document/GetById](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetById.md) → wstępne wypełnienie formularza

### onSubmit
1. Walidacja formularza (zakomentowana — anomalia BA-01)
2. Jeśli `isEditMode` → [PUT /api/Document/Edit](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Edit.md)
3. Jeśli `!isEditMode` → [POST /api/Document/Add](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md)
4. Sukces → `router.navigate([getNavigationUrl()])`

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Autouzupełnienie selektorów (ngOnInit) | [GET /api/Document/GetAutofillInfo](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetAutofillInfo.md) |
| Załadowanie dokumentu (tryb edycji) | [GET /api/Document/GetById](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetById.md) |
| Dodanie dokumentu | [POST /api/Document/Add](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md) |
| Edycja dokumentu | [PUT /api/Document/Edit](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Edit.md) |
| Generowanie PDF (zapis na dysk) | [POST /api/Document/GeneratePdf](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GeneratePdf.md) |
| Podgląd PDF (strumień) | [POST /api/Document/GetPdfStream](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) |

## Klasy pochodne

| Klasa | Ekran | `documentTypeId` | `navigationUrl` |
|---|---|---|---|
| `AddOrEditInvoiceComponent` | `../../faktury/dodaj_edytuj_fakture/ekran.md` | `1` | `/dashboard/invoices` |
| `AddOrEditInvoiceProformaComponent` | `../../faktury_proforma/dodaj_edytuj_fakture_proforma/ekran.md` | `2` | `/dashboard/invoice-proformas` |
| `AddOrEditInvoiceStornosComponent` | `../../faktury_storno/dodaj_edytuj_fakture_storno/ekran.md` | `3` | `/dashboard/invoice-stornos` |

## Dynamiczne pozycje dokumentu

- Każda pozycja to `FormGroup` w `FormArray`
- Wartości `price`, `vatRate`, `name`, `measureUnit` autouzupełniane po wyborze produktu z katalogu
- Sumy (`totalNetAmount`, `totalVatAmount`, `totalGrossAmount`) przeliczane reaktywnie przy każdej zmianie formularza

## Powiązania

- Powiązane procesy: `../../../02_procesy/dokumenty/dodaj_dokument/proces.md`, `../../../02_procesy/dokumenty/edytuj_dokument/proces.md`
- Powiązane API: `../../../04_api_i_integracje/01_api_frontend/document/`
- Powiązane UC: Brak

## Powiązania z kodem

- Komponent: `src/app/components/invoices/add-or-edit-invoice/base-invoice.component.ts`
- Szablon HTML: `src/app/components/invoices/add-or-edit-invoice/base-invoice.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

- BA-01: Walidacja formularza zakomentowana: `// if (this.invoiceForm.invalid) return;` w `getInvoicePdfStream()` — możliwe wywołanie API z pustym formularzem.
- BA-02: `generateInvoicePdf()` ignoruje odpowiedź API; wyłącznie `console.log("Invoice pdf generated successfully")` — brak informacji dla użytkownika o sukcesie lub błędzie.
- BA-03: 6 aktywnych `console.log` w kodzie produkcyjnym.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `_wspolne/base-invoice-component.md`. |
