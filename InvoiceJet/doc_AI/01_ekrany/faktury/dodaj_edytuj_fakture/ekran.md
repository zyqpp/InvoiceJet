# AddOrEditInvoiceComponent — Formularz faktury

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-FormularzFaktury |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran tworzenia i edycji faktury zwykłej (DocumentTypeId=1). Komponent dziedziczy z `BaseInvoiceComponent`, który zawiera całą logikę UI i wywołania API. `AddOrEditInvoiceComponent` implementuje tylko `getDocumentTypeId()` → `1` i `getNavigationUrl()` → `"/dashboard/invoices"`. Formularz zawiera pola nagłówka dokumentu oraz dynamiczną tabelę pozycji (produktów). Chroniony przez AuthGuard (rola: User).

## Wizualizacja układu

```
┌────────────────────────────────────────────────────────┐
│ Dodaj fakturę / Edytuj fakturę                         │
├────────────────────────────────────────────────────────┤
│ Klient (autocomplete) | Seria dok. | Data wyst. | Term.│
├────────────────────────────────────────────────────────┤
│ Konto bankowe | Waluta | Status dokumentu              │
├────────────────────────────────────────────────────────┤
│ Tabela pozycji:                                        │
│  Produkt | Cena | Ilość | J.m. | VAT | Brutto | [Del] │
├────────────────────────────────────────────────────────┤
│ Suma netto: ... | VAT: ... | Brutto: ...               │
├────────────────────────────────────────────────────────┤
│ [Generuj PDF] [Podgląd PDF] [Anuluj] [     Zapisz   ] │
└────────────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/add-invoice` (dodaj), `/dashboard/edit-invoice/:id` (edytuj) |
| Wymagana rola/uprawnienie | User (AuthGuard) |
| Punkty wejścia | Klik „Dodaj fakturę" z listy; klik wiersza na liście (edycja) |
| Powiązany kod komponentu | `src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| `/dashboard/invoices` | Sukces zapisu (onSubmit) | Formularz poprawny + API sukces | User |
| `/dashboard/invoices` | Klik „Anuluj" | Zawsze | User |
| `PdfViewerComponent` | Klik „Podgląd PDF" | Zawsze | User |

## Sekcje ekranu

### Filtry

Brak.

### Tabele i listy

| ID tabeli | Nazwa | Link do dokumentu |
|---|---|---|
| TAB-FormularzFaktury-PozycjeDokumentu | Tabela pozycji dokumentu (FormArray) | `../../00_wspolne/base_invoice_component/ekran.md` |

### Pola

| ID pola | Nazwa w UI | Wymagalność | Link do dokumentu |
|---|---|---|---|
| POLE-FormularzFaktury-clientId | Klient | wymagane | — |
| POLE-FormularzFaktury-documentSeriesId | Seria dokumentu | wymagane | — |
| POLE-FormularzFaktury-issueDate | Data wystawienia | wymagane | — |
| POLE-FormularzFaktury-dueDate | Termin płatności | wymagane | — |
| POLE-FormularzFaktury-bankAccountId | Konto bankowe | wymagane | — |
| POLE-FormularzFaktury-currency | Waluta | wymagane | — |
| POLE-FormularzFaktury-documentStatus | Status dokumentu | wymagane | — |

### Kolumny tabeli pozycji

| Kolumna | Opis |
|---|---|
| `name` | Nazwa produktu/usługi |
| `unitPrice` | Cena jednostkowa |
| `quantity` | Ilość |
| `unitOfMeasurement` | Jednostka miary |
| `tvaValue` | Stawka VAT |
| `containsTva` | Czy zawiera VAT |
| `totalPrice` | Cena brutto pozycji (wyliczana) |
| `actions` | Usuń pozycję |

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-FormularzFaktury-Zapisz | Zapisz | — |
| OP-FormularzFaktury-Anuluj | Anuluj | — |
| OP-FormularzFaktury-GenerujPdf | Generuj PDF | — |
| OP-FormularzFaktury-PodgladPdf | Podgląd PDF | — |
| OP-FormularzFaktury-DodajPozycje | Dodaj pozycję | — |
| OP-FormularzFaktury-UsunPozycje | Usuń pozycję | — |

### Modale

| ID modalu | Nazwa | Wywołane przez | Link do dokumentu |
|---|---|---|---|
| MODAL-Wspolne-PdfViewer | Podgląd PDF | OP-FormularzFaktury-PodgladPdf | `../../00_wspolne/modale_wspolne/pdf_viewer/modal.md` |

### Powiadomienia

Brak (anomalia: brak widocznych komunikatów sukcesu/błędu).

## Tryby działania

| Tryb | URL | Zachowanie |
|---|---|---|
| Dodawanie | `/dashboard/add-invoice` | `isEditMode = false`; brak `:id` w route |
| Edycja | `/dashboard/edit-invoice/:id` | `isEditMode = true`; ładuje dokument przez API |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie autofill (ngOnInit) | `GET /api/Document/GetDocumentAutofillInfo/1` |
| Załadowanie dokumentu (tryb edycji) | `GET /api/Document/GetDocumentById/{id}` |
| Submit (dodanie) | `POST /api/Document/AddDocument` |
| Submit (edycja) | `PUT /api/Document/EditDocument` |
| Generowanie PDF (zapis na dysk) | `POST /api/Document/GenerateDocumentPdf` |
| Podgląd PDF (strumień) | `POST /api/Document/GetInvoicePdfStream` |

## Powiązania

- Klasa bazowa: `../../00_wspolne/base_invoice_component/ekran.md`
- Powiązane procesy: `../../02_procesy/dokumenty/dodaj_dokument/proces.md`, `../../02_procesy/dokumenty/edytuj_dokument/proces.md`, `../../02_procesy/dokumenty/generuj_pdf/proces.md`
- Powiązane API: `../../04_api_i_integracje/01_api_frontend/document/`
- Powiązane UC: Brak

## Powiązania z kodem

- Komponent: `src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.ts`
- Szablon HTML: `src/app/components/invoices/add-or-edit-invoice/add-or-edit-invoice.component.html`
- Klasa bazowa: `src/app/components/invoices/add-or-edit-invoice/base-invoice.component.ts`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

- BA-01: Walidacja formularza zakomentowana w `getInvoicePdfStream()` — możliwe wywołanie API z niekompletnym formularzem.
- BA-02: `generateInvoicePdf()` ignoruje odpowiedź API — brak komunikatu dla użytkownika.
- BA-03: 6 aktywnych `console.log` w kodzie produkcyjnym.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `invoices/add-or-edit-invoice.md`. |
