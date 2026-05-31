# Scenariusze testowe manualne: Dokumenty

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-MAN-DOKUMENTY |
| Typ dokumentu | scenariusze testowe manualne |
| Wersja | 0.1 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Scenariusze testowe obejmują pełny cykl życia dokumentów — faktur i proform: wystawianie, edycję, konwersję na storno, generowanie PDF oraz podgląd statystyk na dashboardzie. Szczególnie istotny jest TC-154, który weryfikuje anomalię niepoprawnego szablonu PDF dla proformy. Powiązane z endpointami API-22 – API-31.

---

## TC-150: Wystawienie faktury (happy path)

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** UC-Dokumenty-Faktury, API-22 (`POST /api/Document/AddDocument`), API-27

**Warunki wstępne:** Firma, seria `FV` (documentTypeId=1), konto bankowe i klient muszą istnieć.

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Zaloguj się i przejdź do `/dashboard/invoices` | e-mail: `test@example.com` | Lista faktur widoczna |
| 2 | Kliknij „Nowa faktura" | — | Przekierowanie na `/dashboard/add-invoice`; formularz z autouzupełnionymi selektorami |
| 3 | Sprawdź autouzupełnienie | — | `GET /api/Document/GetDocumentAutofillInfo/1` zwrócił serie, klientów i konta bankowe |
| 4 | Wybierz serię, klienta, konto bankowe i wypełnij daty | Seria: `FV`, klient: `KLIENT TESTOWY SRL`, konto: `RO49AAAA1B31007593840000`, data wystawienia: `2026-05-31`, termin płatności: `2026-06-14` | Formularz wypełniony |
| 5 | Dodaj pozycję faktury | Produkt: `Servicii consultanta`, ilość: `2`, cena: `500.00 RON`, VAT: `19%` | Pozycja dodana; netto: `1000.00`, VAT: `190.00`, brutto: `1190.00` |
| 6 | Kliknij „Zapisz" | — | Wywołanie `POST /api/Document/AddDocument` z documentTypeId=1 — status 201 Created |
| 7 | Sprawdź numer faktury | — | Faktura otrzymuje numer `FV0001`; licznik serii inkrementowany do 2 |
| 8 | Sprawdź przekierowanie i listę | — | Użytkownik na `/dashboard/invoices`; faktura `FV0001` widoczna |

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
**Powiązane:** UC-Dokumenty-FakturyStorno, API-31 (`PUT /api/Document/TransformToStorno`)

**Warunki wstępne:** Dokument (faktura lub proforma) musi istnieć.

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Przejdź do listy faktur lub proform | — | Lista dokumentów widoczna |
| 2 | Wybierz dokument do stornoowania | Faktura: `FV0001` | Dokument zaznaczony lub widoczny z opcją konwersji |
| 3 | Kliknij „Przekształć na storno" lub równoważną opcję | — | Dialog potwierdzenia lub bezpośrednie wywołanie |
| 4 | Potwierdź konwersję | — | Wywołanie `PUT /api/Document/TransformToStorno` — status 200 OK |
| 5 | Sprawdź listę dokumentów | — | Dokument stornoowy widoczny na liście; typ dokumentu zmieniony na storno |
| 6 | Sprawdź dane storno | — | Wartości w dokumencie storno są ujemne (odwrócone) |

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
