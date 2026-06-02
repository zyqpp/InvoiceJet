# TC-E12 — Scenariusze testowe (AddOrEditInvoiceProformaComponent)

| Pole | Wartość |
|---|---|
| ID dokumentu | TC-E12 |
| Typ dokumentu | scenariusze testowe |
| Ekran | [E-12 AddOrEditInvoiceProformaComponent](E-12_ekran.md) |
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
| `Firm` (własna) | aktywna firma UserFirm (sprzedawca) |
| `Firm` (klient) | ≥1 firma z `UserFirm.IsClient=true` |
| `DocumentSeries` | seria z `DocumentTypeId=2` (PRF), `currentNumber=1` dla aktywnego UserFirm |
| `BankAccount` | ≥1 konto bankowe dla aktywnego UserFirm |
| `DocumentStatus` | seedowane: Unpaid(id=1), Paid(id=2) |
| `Product` | opcjonalnie — dla autocomplete produktów |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Pole Client | `input[placeholder*="CUI"]` |
| Issue Date | pierwszy `input[matDatepicker]` |
| Due Date | drugi `input[matDatepicker]` |
| Select Document Series | `mat-select` z etykietą „Document Series" |
| Select Bank Account | `mat-select` z etykietą „Bank Account" |
| Select Status | `mat-select` z etykietą „Status" |
| Przycisk Add Product | `button` z tekstem „+" / „Add Product" |
| Unit Price (wiersz 1) | pierwszy `input[placeholder*="Unit Price"]` |
| Quantity (wiersz 1) | pierwszy `input[placeholder*="Qty"]` |
| VAT Rate (wiersz 1) | pierwszy `mat-select` w wierszu pozycji (VAT%) |
| Total wiersza (obliczony) | pierwszy `td` z klasą `total-price` |
| Suma netto | element z id/klasą `total-net` lub tekst pod tabelą |
| Suma VAT | element z id/klasą `total-vat` |
| Suma Brutto | element z id/klasą `total-gross` |
| Przycisk Save/Update | `button` z `(click)=onSubmit()` |
| Przycisk Preview PDF | `button` z tekstem „Preview" |
| Przycisk Generate PDF | `button` z tekstem „Generate" |
| Przycisk Cancel | `button` z tekstem „Cancel" lub „Anuluj" |

> Brak `data-cy` — anomalia BA-07.

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E12-01 | Dodanie proformy (happy path) | firma, seria PRF (currentNumber=1), klient, konto bankowe | 1. GET /dashboard/add-invoice-proforma 2. Wybierz klienta 3. Wybierz serię PRF 4. Ustaw issueDate=2026-06-02, dueDate=2026-06-16 5. Wybierz konto bankowe 6. Klik „Add Product" 7. Wpisz UnitPrice=200.00, Qty=3, VAT=19% 8. **Weryfikacja [obliczanie_ceny_pozycji]:** totalPrice wiersza = 200 × 3 × (1 + 19/100) = 200 × 3 × 1.19 = **714.00** 9. **Weryfikacja [ALG-05]:** Suma netto=**600.00**, VAT=**114.00**, Brutto=**714.00** 10. Klik „Save" | toastr „Document added successfully"; redirect do [E-11](../E-11_InvoiceProformasComponent/E-11_ekran.md); **Weryfikacja [ALG-02]:** documentNumber = „PRF0001" |
| TC-E12-02 | Edycja istniejącej proformy | proforma id=7 TypeId=2 | 1. GET /dashboard/edit-invoice-proforma/7 2. Zmień dueDate 3. Klik „Update" | toastr „Document updated successfully"; redirect do [E-11](../E-11_InvoiceProformasComponent/E-11_ekran.md); proforma 7 zaktualizowana w DB |
| TC-E12-03 | Podgląd PDF proformy | proforma id=7 TypeId=2 | 1. GET /dashboard/edit-invoice-proforma/7 2. Klik „Preview PDF" | [MODAL-E12-01](E-12_MODAL-01.md) otwiera się z PDF; tytuł PDF zawiera „Factura Proforma" (stream używa poprawnej fabryki ProformaDocument) |
| TC-E12-04 | Generowanie PDF proformy — TEST ANOMALII BUG A-KRIT-04 | proforma id=7 TypeId=2 | 1. GET /dashboard/edit-invoice-proforma/7 2. Klik „Generate PDF" | **Oczekiwany wynik (bieżący, błędny):** PDF zapisywany na dysk; tytuł PDF to „**Factura**" — BUG A-KRIT-04 (hardcoded InvoiceDocument). Oczekiwany wynik po naprawie: tytuł „Factura Proforma" |
| TC-E12-05 | Anulowanie formularza | — | 1. GET /dashboard/add-invoice-proforma 2. Wypełnij częściowo formularz 3. Klik „Cancel" | redirect do `/dashboard/invoice-proformas` bez zapisu; żaden dokument nie dodany do DB |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — adaptacja z wzorca TC-E10; dodano weryfikacje algorytmów i test BUG A-KRIT-04. |
