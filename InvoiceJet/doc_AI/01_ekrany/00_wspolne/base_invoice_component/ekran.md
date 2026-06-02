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
| POLE-BaseInvoice-documentSeriesId | Seria dokumentu | wymagane | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) — wybrana seria determinuje format numeru |
| POLE-BaseInvoice-clientId | Klient | wymagane | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) — autocomplete filtruje klientów bieżącej firmy |
| POLE-BaseInvoice-bankAccountId | Konto bankowe | wymagane | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) — autocomplete filtruje konta bieżącej firmy |
| POLE-BaseInvoice-issueDate | Data wystawienia | wymagane | — |
| POLE-BaseInvoice-dueDate | Termin płatności | wymagane | — |
| POLE-BaseInvoice-currency | Waluta | wymagane | — |
| POLE-BaseInvoice-documentStatus | Status dokumentu | wymagane | — |
| POLE-BaseInvoice-products | Tabela pozycji (FormArray) | wymagane (min. 1) | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) · [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) |

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
| OP-BaseInvoice-Zapisz | Zapisz / Submit | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) · [wyliczeniowe/aktualizacja_produktow_dokumentu](../../../03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md) |
| OP-BaseInvoice-GenerujPdf | Generuj PDF | [ALG-07 Generuj PDF na dysk](../../../03_algorytmy/generowania_pdf/generuj_pdf_na_dysk.md) ⚠️ BUG: hardcoded InvoiceDocument |
| OP-BaseInvoice-PodgladPdf | Podgląd PDF | [ALG-07 Generuj PDF stream](../../../03_algorytmy/generowania_pdf/generuj_pdf_stream.md) (poprawna fabryka) |
| OP-BaseInvoice-DodajPozycje | Dodaj pozycję (do tabeli) | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) · [ALG-05 Obliczanie wartości](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) |
| OP-BaseInvoice-UsunPozycje | Usuń pozycję (z tabeli) | [ALG-05 Obliczanie wartości](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) — sumy przeliczane po usunięciu |

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

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| POLE-BaseInvoice-documentSeriesId | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | Wybrana seria → format numeru: `SeriesName + CurrentNumber.PadLeft(4,'0')`; licznik rośnie przy każdym zapisie |
| Pola pozycji: `quantity`, `price`, `vatRate` | [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) | `price × quantity × (1 + vatRate/100)` — wylicza `totalPrice` wiersza w czasie rzeczywistym |
| Stan: `totalNetAmount`, `totalVatAmount`, `totalGrossAmount` | [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) | `calculateTotals()` — reaktywna subskrypcja na `valueChanges` FormArray; aktualizacja przy każdej zmianie |
| OP-BaseInvoice-Zapisz (backend) | [wyliczeniowe/aktualizacja_produktow_dokumentu](../../../03_algorytmy/wyliczeniowe/aktualizacja_produktow_dokumentu.md) | Backend: `UpdateDocumentProducts` — iteracja po pozycjach DTO, obliczenie sum netto i brutto, zapis do `Document.UnitPrice` + `TotalPrice` |
| OP-BaseInvoice-GenerujPdf | [ALG-07 Generuj PDF na dysk](../../../03_algorytmy/generowania_pdf/generuj_pdf_na_dysk.md) | ⚠️ **BUG:** hardcoded template `InvoiceDocument` — dla proformy (TypeId=2) generuje szablon faktury |
| OP-BaseInvoice-PodgladPdf | [ALG-07 Generuj PDF stream](../../../03_algorytmy/generowania_pdf/generuj_pdf_stream.md) | Poprawna implementacja — fabryka szablonów wybiera szablon na podstawie `DocumentTypeId` |
| POLE-BaseInvoice-clientId / bankAccountId | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Autofill ładuje tylko dane bieżącego UserFirm przez `GetAutofillInfo` |

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
