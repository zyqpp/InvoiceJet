# Scenariusze testowe manualne: Dokumenty

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-MAN-DOKUMENTY |
| Typ dokumentu | scenariusze testowe manualne |
| Wersja | 0.2 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-06-02 |

## Streszczenie

Scenariusze testowe obejmują pełny cykl życia dokumentów — faktur i proform: wystawianie, edycję, konwersję na storno, generowanie PDF oraz podgląd statystyk na dashboardzie. Szczególnie istotny jest TC-154, który weryfikuje anomalię niepoprawnego szablonu PDF dla proformy. Powiązane z endpointami API-22 – API-31.

## Powiązane algorytmy

| Algorytm | Testowane przez |
|---|---|
| [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | TC-150 krok 7 (numer FV0001), TC-151 krok 6 (PRF0001) |
| [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) | TC-150 krok 5 (netto 1000, VAT 190, brutto 1190) |
| [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) | TC-150 krok 5 (`500 × 2 × 1.19 = 1190.00`) |
| [ALG-07 Generowanie PDF — stream](../../../03_algorytmy/generowania_pdf/generuj_pdf_stream.md) | TC-153 (Preview PDF — poprawna ścieżka) |
| [ALG-07 Generowanie PDF — na dysk](../../../03_algorytmy/generowania_pdf/generuj_pdf_na_dysk.md) | TC-154 ⚠️ BUG A-KRIT-04 — hardcoded szablon |
| [ALG-08 Transformacja na storno](../../../03_algorytmy/dedykowane/transformacja_na_storno.md) | TC-152 (konwersja faktury/proformy w storno) |

## Selektory CSS / Angular Material

| Element | Selektor |
|---|---|
| Przycisk „Nowa faktura" | `button[mat-raised-button]` z tekstem „New Invoice" |
| Pole klienta (autocomplete) | `mat-form-field input[formControlName="clientId"]` lub `[formControlName="client"]` |
| Dropdown seria dokumentów | `mat-select[formControlName="documentSeriesId"]` |
| Data wystawienia | `mat-form-field input[formControlName="issueDate"]` |
| Data płatności | `mat-form-field input[formControlName="dueDate"]` |
| Wiersz tabeli pozycji | `mat-row` lub `tr` w tabeli pozycji FormArray |
| Cena jedn. pozycji | `input[formControlName="price"]` lub `input[formControlName="unitPrice"]` |
| Ilość pozycji | `input[formControlName="quantity"]` |
| Stawka VAT | `mat-select[formControlName="vatRate"]` lub `[formControlName="tvaValue"]` |
| Brutto pozycji (wyliczane) | wyświetlone w kolumnie `totalPrice` — pole readonly |
| Suma netto pod tabelą | element z binding `totalNetAmount` |
| Suma VAT | element z binding `totalVatAmount` |
| Suma brutto | element z binding `totalGrossAmount` |
| Przycisk Zapisz | `button[type="submit"]` lub `button` z tekstem „Save" |
| Przycisk Podgląd PDF | `button` z tekstem „Preview PDF" |
| Przycisk Generuj PDF | `button` z tekstem „Generate PDF" |
| Checkbox wiersza (lista) | `mat-checkbox` w wierszu tabeli |
| Przycisk Transform to Storno | `button[mat-menu-item]` z tekstem „Transform to storno" |

---

## TC-150: Wystawienie faktury (happy path)

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** UC-Dokumenty-Faktury, `POST /api/Document/Add`
**Algorytmy:** [ALG-02 Generowanie numeru](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) · [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) · [ALG-05 Obliczanie wartości](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md)

**Prereq:**
- Firma skonfigurowana (`/dashboard/firm-details`)
- Seria `FV` z `currentNumber=1` (DocumentTypeId=1) w `/dashboard/document-series`
- Klient „KLIENT TESTOWY SRL" istnieje w `/dashboard/clients`
- Konto bankowe `RO49AAAA1B31007593840000` istnieje w `/dashboard/bank-accounts`

| # | Akcja | Element UI (selektor) | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | Zaloguj się | `input[formControlName="email"]`, `input[formControlName="password"]` | `test@example.com` / `Test@123` | Przekierowanie na `/dashboard` |
| 2 | Nawiguj | URL | `/dashboard/invoices` | Lista faktur widoczna |
| 3 | Kliknij „Nowa faktura" | `button[mat-raised-button]` z tekstem „New Invoice" | — | Przekierowanie na `/dashboard/add-invoice`; selektory wypełnione przez autofill (`GET /api/Document/GetAutofillInfo/1`) |
| 4 | Wybierz serię | `mat-select[formControlName="documentSeriesId"]` → `mat-option` z „FV" | `FV` | Wybrana seria FV; licznik aktualny = 1 |
| 5 | Wybierz klienta | `mat-form-field input` powiązany z `clientId` → wpisz „KLIENT" → wybierz z autocomplete | `KLIENT TESTOWY SRL` | Pole wypełnione |
| 6 | Wybierz konto bankowe | `mat-select[formControlName="bankAccountId"]` | `RO49AAAA1B31007593840000` | Konto wybrane |
| 7 | Ustaw datę wystawienia | `input[formControlName="issueDate"]` | `2026-06-02` | Data wpisana |
| 8 | Ustaw termin płatności | `input[formControlName="dueDate"]` | `2026-06-16` | Data wpisana (14 dni) |
| 9 | Kliknij „Dodaj pozycję" | `button` z tekstem „Add Product" lub ikona `+` | — | Nowy wiersz w tabeli pozycji |
| 10 | Wybierz produkt | `mat-select[formControlName="productId"]` w nowym wierszu | `Servicii consultanta` | Pola `price`, `vatRate`, `name` autouzupełnione |
| 11 | Wpisz ilość | `input[formControlName="quantity"]` w wierszu | `2` | Pole = 2 |
| 12 | Wpisz cenę jednostkową | `input[formControlName="price"]` lub `unitPrice` | `500.00` | Pole = 500.00 |
| 13 | Wybierz VAT | `mat-select[formControlName="vatRate"]` lub `tvaValue` | `19` | VAT = 19% |
| 14 | **Weryfikacja ALG-obliczanie_ceny_pozycji** | Kolumna `totalPrice` w tabeli | — | **= 500 × 2 × (1 + 19/100) = 500 × 2 × 1.19 = 1190.00** |
| 15 | **Weryfikacja ALG-05** | Pola pod tabelą: Suma netto / VAT / Brutto | — | Netto = **1000.00**, VAT = **190.00**, Brutto = **1190.00** |
| 16 | Kliknij „Zapisz" | `button[type="submit"]` lub „Save" | — | Wywołanie `POST /api/Document/Add` — HTTP 201 Created |
| 17 | **Weryfikacja ALG-02** | URL po przekierowaniu; lista faktur | — | Redirect na `/dashboard/invoices`; nowa faktura z numerem **FV0001**; seria FV `currentNumber` = 2 |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-151: Wystawienie proformy

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** UC-Dokumenty-FakturyProforma, API-22, API-27

**Warunki wstępne:** Firma, seria `PRF` (documentTypeId=2), konto bankowe i klient muszą istnieć.

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Przejdź do `/dashboard/invoice-proformas` | — | Lista proform widoczna |
| 2 | Kliknij „Nowa proforma" | — | Formularz nowego dokumentu; `GET /api/Document/GetDocumentAutofillInfo/2` |
| 3 | Wybierz serię proforma | Seria: `PRF`, klient: `KLIENT TESTOWY SRL`, konto bankowe, daty | Formularz wypełniony |
| 4 | Dodaj pozycję | Produkt: `Servicii consultanta`, ilość: `1`, cena: `500.00 RON`, VAT: `19%` | Pozycja dodana; brutto: `595.00` |
| 5 | Kliknij „Zapisz" | — | Wywołanie `POST /api/Document/AddDocument` z documentTypeId=2 — status 201 Created |
| 6 | Sprawdź numer proformy | — | Proforma z numerem `PRF0001`; licznik serii PRF inkrementowany |
| 7 | Sprawdź listę proform | — | Proforma `PRF0001` widoczna na liście |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-152: Konwersja faktury/proformy na storno

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** UC-Dokumenty-FakturyStorno, `PUT /api/Document/TransformToStorno`
**Algorytm:** [ALG-08 Transformacja na storno](../../../03_algorytmy/dedykowane/transformacja_na_storno.md)

**Prereq:** Faktura FV0001 istnieje (po TC-150).

| # | Akcja | Element UI (selektor) | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | Nawiguj | URL | `/dashboard/invoices` | Lista faktur widoczna |
| 2 | Zaznacz fakturę FV0001 | `mat-checkbox` w wierszu z „FV0001" | klik | Checkbox zaznaczony; wiersz zaznaczony |
| 3 | Otwórz menu akcji | `button[mat-stroked-button]` z ikoną `more_vert` (⋮) | klik | Menu rozwinięte; widoczna opcja „Transform to storno" |
| 4 | Kliknij „Przekształć w storno" | `button[mat-menu-item]` z tekstem „Transform to storno" | klik | Wywołanie `PUT /api/Document/TransformToStorno` z `[FV0001.id]` — HTTP 200 OK |
| 5 | **Weryfikacja ALG-08** | Lista faktur | — | Faktura FV0001 **znikła z listy**; status faktury zmieniony (lub usunięta z widoku) |
| 6 | Nawiguj | URL | `/dashboard/invoice-stornos` | Lista storn widoczna |
| 7 | **Weryfikacja ALG-08** | Wiersz z nowym stornem | — | Storno o numerze (np. „STN0001" lub inny) widoczne; **wartość `totalValue` = -1190.00** (ujemna wartość faktury FV0001) |
| 8 | **Weryfikacja braku atomowości** | — | — | ⚠️ Uwaga: ALG-08 nie jest atomowy — błąd w trakcie może pozostawić niespójny stan |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-153: Generowanie PDF faktury

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** API-29 (`POST /api/Document/GetPdfStream`), UC-Dokumenty-Faktury (scenariusz generowania PDF)

**Warunki wstępne:** Faktura `FV0001` musi istnieć.

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Przejdź do listy faktur | — | Lista faktur z fakturą `FV0001` |
| 2 | Kliknij „PDF" przy fakturze `FV0001` | — | Wywołanie `POST /api/Document/GetPdfStream` z ID faktury |
| 3 | Sprawdź czy PDF jest pobierany | — | Przeglądarka pobiera lub wyświetla plik PDF; status 200 OK ze strumieniem |
| 4 | Otwórz wygenerowany PDF | — | Dokument PDF zawiera: tytuł „Factura", numer dokumentu `FV0001`, dane firmy, dane klienta, pozycje, kwoty, numer konta bankowego |
| 5 | Sprawdź poprawność danych w PDF | — | Wszystkie dane zgodne z fakturą `FV0001` |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-154: Generowanie PDF proformy (ANOMALIA A-KRIT-04 — błędny szablon)

**Typ:** Anomalia krytyczna
**Priorytet:** Wysoki
**Powiązane:** API-28 (`POST /api/Document/GenerateInvoicePdf`), anomalia A-KRIT-04, `plan_testow.md` (TC-03)

> **ANOMALIA KRYTYCZNA A-KRIT-04:** Endpoint `POST /api/Document/GenerateInvoicePdf` (API-28) ma hardcoded szablon `InvoiceDocument`, niezależnie od typu dokumentu. Dla proformy zamiast szablonu „Factura Proforma" generowany jest szablon „Factura". Błąd ten nie dotyczy endpointu `GetPdfStream` (API-29), który może obsługiwać typy poprawnie — należy zweryfikować.

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Upewnij się, że proforma `PRF0001` istnieje (po TC-151) | — | Proforma widoczna |
| 2 | Kliknij opcję generowania PDF przy proformie (przez API-28) | ID proformy `PRF0001` | Wywołanie `POST /api/Document/GenerateInvoicePdf` |
| 3 | Sprawdź odpowiedź | — | Status 200 OK; PDF wygenerowany |
| 4 | Otwórz wygenerowany PDF | — | **Bug:** Tytuł dokumentu w PDF to „Factura" zamiast „Factura Proforma" — niepoprawny typ dokumentu |
| 5 | Zweryfikuj przez API-29 jako obejście | Wywołaj `POST /api/Document/GetPdfStream` dla tej samej proformy | Sprawdź czy GetPdfStream generuje poprawny tytuł „Factura Proforma" |
| 6 | Porównaj wyniki obu endpointów | — | Zidentyfikuj który endpoint generuje poprawny PDF dla proformy |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-155: Edycja faktury

**Typ:** Happy path
**Priorytet:** Średni
**Powiązane:** API-23 (`PUT /api/Document/EditDocument`), API-25

**Warunki wstępne:** Faktura `FV0001` musi istnieć.

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Przejdź do listy faktur | — | Lista faktur widoczna |
| 2 | Kliknij „Edytuj" przy fakturze `FV0001` | — | Przekierowanie na `/dashboard/edit-invoice/:id`; `GET /api/Document/GetDocumentById` załadował dane |
| 3 | Zmodyfikuj termin płatności | Nowy termin płatności: `2026-07-14` | Pole daty zaktualizowane |
| 4 | Kliknij „Zapisz" | — | Wywołanie `PUT /api/Document/EditDocument` — status 200 OK |
| 5 | Sprawdź zaktualizowane dane | — | Faktura `FV0001` ma nowy termin płatności; dane zgodne |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-156: Usunięcie faktury

**Typ:** Happy path
**Priorytet:** Średni
**Powiązane:** API-26 (`PUT /api/Document/DeleteDocument`)

> **Uwaga:** Usunięcie faktury to operacja soft-delete (flaga `IsDeleted = true`). Dokument nie jest fizycznie kasowany.

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Przejdź do listy faktur | — | Lista faktur widoczna |
| 2 | Wybierz fakturę do usunięcia | Faktura: `FV0002` (jeśli istnieje) lub inna testowa | Faktura zaznaczona |
| 3 | Kliknij „Usuń" i potwierdź | — | Dialog potwierdzenia; po potwierdzeniu `PUT /api/Document/DeleteDocument` — status 200 OK |
| 4 | Sprawdź listę faktur | — | Usunięta faktura nie jest już widoczna na liście |
| 5 | Sprawdź licznik serii | — | Licznik serii NIE jest cofany — następna faktura otrzyma kolejny numer |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-157: Dashboard — statystyki roku

**Typ:** Happy path
**Priorytet:** Niski
**Powiązane:** API-30 (`GET /api/Document/GetDashboardStats`)

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Zaloguj się i przejdź do `/dashboard` | e-mail: `test@example.com` | Dashboard widoczny z wykresami i statystykami |
| 2 | Sprawdź wywołanie API statystyk | — | `GET /api/Document/GetDashboardStats` wywołany automatycznie przy załadowaniu dashboardu — status 200 OK |
| 3 | Sprawdź wyświetlane dane | — | Dashboard pokazuje statystyki dla bieżącego roku: łączna wartość faktur, liczba dokumentów, podział miesięczny |
| 4 | Sprawdź poprawność danych | — | Dane na dashboardzie zgodne z wystawionymi fakturami (suma wartości brutto, liczba dokumentów) |
| 5 | Sprawdź zachowanie przy braku faktur | Konto bez faktur | Dashboard wyświetla wartości zerowe lub pusty stan, bez błędu |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
