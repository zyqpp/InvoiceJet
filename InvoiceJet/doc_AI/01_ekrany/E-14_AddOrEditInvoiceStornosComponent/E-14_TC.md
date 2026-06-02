# TC-E14 — Scenariusze testowe (AddOrEditInvoiceStornosComponent)

| Pole | Wartość |
|---|---|
| ID dokumentu | TC-E14 |
| Typ dokumentu | scenariusze testowe |
| Ekran | [E-14 AddOrEditInvoiceStornosComponent](E-14_ekran.md) |
| Wersja | 0.1 |
| Autor | Agent Claudiusz Sonte 4.6 |
| Data | 2026-06-02 |

## Prereq — autoryzacja (wymagane dla każdego testu)

| Wymaganie | Szczegół |
|---|---|
| Typ | JWT Bearer token |
| Rola | `"User"` w claims |
| Nagłówek HTTP | `Authorization: Bearer <token>` |
| Uzyskanie tokenu | [POST /api/Auth/login](../../../04_api_i_integracje/01_api_frontend/auth/POST_Auth_login.md) |

## Prereq — dane w DB

| Encja | Minimum |
|---|---|
| `Document` (TypeId=3) | ≥1 storno dla aktywnego UserFirm — najczęściej stworzone przez TransformToStorno z faktury TypeId=1 |
| `Document` (TypeId=1) źródłowe | faktura z `totalValue=600` (używana w TC-E14-03) |
| `Firm` (własna) | aktywna firma UserFirm (sprzedawca) |
| `Firm` (klient) | ≥1 firma z `UserFirm.IsClient=true` |
| `DocumentSeries` | seria z `DocumentTypeId=3` (STN) dla aktywnego UserFirm |
| `BankAccount` | ≥1 konto bankowe dla aktywnego UserFirm |
| `DocumentStatus` | seedowane: Unpaid(id=1), Paid(id=2) |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Pole Client | `input[placeholder*="CUI"]` |
| Issue Date | pierwszy `input[matDatepicker]` |
| Due Date | drugi `input[matDatepicker]` |
| Select Document Series | `mat-select` z etykietą „Document Series" |
| Select Bank Account | `mat-select` z etykietą „Bank Account" |
| Select Status | `mat-select` z etykietą „Status" |
| Wiersze pozycji tabeli | `tr` w `mat-table` pozycji |
| Total wiersza (obliczony) | `td` z klasą `total-price` |
| Suma netto | element z klasą/id `total-net` |
| Suma VAT | element z klasą/id `total-vat` |
| Suma Brutto | element z klasą/id `total-gross` |
| Przycisk Save/Update | `button` z `(click)=onSubmit()` |
| Przycisk Preview PDF | `button` z tekstem „Preview" |
| Przycisk Generate PDF | `button` z tekstem „Generate" |
| Przycisk Cancel | `button` z tekstem „Cancel" lub „Anuluj" |

> Brak `data-cy` — anomalia BA-07.

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E14-01 | Edycja istniejącego storna (załadowany przez /dashboard/edit-invoice-storno/:id) | storno id=10 TypeId=3 | 1. GET /dashboard/edit-invoice-storno/10 2. Zmień Status na „Paid" 3. Klik „Update" | toastr „Document updated successfully"; redirect do [E-13](../E-13_InvoiceStornosComponent/E-13_ekran.md); storno id=10 zaktualizowane w DB |
| TC-E14-02 | Podgląd PDF storna | storno id=10 TypeId=3 | 1. GET /dashboard/edit-invoice-storno/10 2. Klik „Preview PDF" | [MODAL-E14-01](E-14_MODAL-01.md) otwiera się z PDF storna; PDF generowany przez [ALG-07 generuj_pdf_stream](../../../03_algorytmy/generowania_pdf/generuj_pdf_stream.md) |
| TC-E14-03 | Weryfikacja wartości pozycji storna (stworzonego przez TransformToStorno) | storno id=10 stworzone z faktury totalValue=600 | 1. GET /dashboard/edit-invoice-storno/10 2. Odczytaj wiersze w tabeli pozycji i wartości sum | Pozycje tabeli zawierają wartości z faktury źródłowej; Suma Brutto wyświetla wartość ujemną = -600; zgodnie z [ALG-08 TransformToStorno](../../../03_algorytmy/dedykowane/transformacja_na_storno.md) |
| TC-E14-04 | Anulowanie formularza | storno id=10 TypeId=3 | 1. GET /dashboard/edit-invoice-storno/10 2. Zmień dueDate 3. Klik „Cancel" | redirect do `/dashboard/invoice-stornos` bez zapisu; storno id=10 nie zmienione w DB |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — adaptacja z wzorca TC-E10/TC-E12; uwzględniono specyfikę storna i weryfikację ALG-08. |
