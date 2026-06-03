# Scenariusze testowe manualne: Serie dokumentów

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-MAN-SERIE-DOKUMENTOW |
| Typ dokumentu | scenariusze testowe manualne |
| Wersja | 0.1 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Scenariusze testowe obejmują zarządzanie seriami numeracji dokumentów: dodawanie, edycję, usuwanie oraz weryfikację automatycznego generowania kolejnych numerów dokumentów. Serie są wymagane do wystawienia faktur i proform. Powiązane z endpointami API-18 – API-21.

## Powiązane algorytmy

| Algorytm | Testowane przez |
|---|---|
| [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | TC-141 — weryfikacja formatu "FV" + currentNumber.D4 = "FV0001"; inkrementacja |
| [dedykowane/inicjalizacja_serii_dokumentow](../../../03_algorytmy/dedykowane/inicjalizacja_serii_dokumentow.md) | TC-140 krok 7 — domyślne serie FV/PRF/STN tworzone po rejestracji |

## Selektory CSS / Angular Material

| Element | Selektor |
|---|---|
| Przycisk Dodaj serię | `button[mat-raised-button]` z tekstem „Add Series" |
| Dialog Dodaj/Edytuj serię | `mat-dialog-container` |
| Pole Nazwa serii | `mat-dialog-container input[formControlName="seriesName"]` |
| Select Typ dokumentu | `mat-dialog-container mat-select[formControlName="documentType"]` |
| Pole Numer startowy | `mat-dialog-container input[formControlName="firstNumber"]` lub `currentNumber` |
| Przycisk Save w dialogu | `mat-dialog-container button[type="submit"]` |
| Wiersze tabeli | `mat-row` lub `tr` z danymi serii |

---

## TC-140: Dodanie serii dokumentów (happy path)

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** API-19 (`POST /api/DocumentSeries/AddDocumentSeries`), API-18

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Zaloguj się i przejdź do sekcji „Serie dokumentów" | e-mail: `test@example.com` | Lista serii widoczna (może być pusta) |
| 2 | Kliknij „Dodaj serię" | — | Formularz dodawania serii widoczny z polami: nazwa, typ dokumentu, numer startowy |
| 3 | Wypełnij dane serii dla faktur | Nazwa: `FV`, typ: `Faktura` (documentTypeId=1), numer startowy: `1` | Formularz wypełniony |
| 4 | Kliknij „Zapisz" | — | Wywołanie `POST /api/DocumentSeries/AddDocumentSeries` — status 201 Created |
| 5 | Sprawdź listę serii | — | Nowa seria `FV` widoczna na liście; `GET /api/DocumentSeries/GetAll` zawiera serię z `currentNumber=1` |
| 6 | Dodaj drugą serię dla proform | Nazwa: `PRF`, typ: `Proforma` (documentTypeId=2), numer startowy: `1` | Seria `PRF` widoczna na liście |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-141: Edycja serii dokumentów

**Typ:** Happy path
**Priorytet:** Średni
**Powiązane:** API-20 (`PUT /api/DocumentSeries/UpdateDocumentSeries`)

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Upewnij się, że seria `FV` istnieje (po TC-140) | — | Seria `FV` na liście |
| 2 | Kliknij „Edytuj" przy serii | — | Formularz edycji z aktualnymi danymi serii |
| 3 | Zmień numer startowy (currentNumber) | Nowy currentNumber: `100` | Pole numeru zaktualizowane |
| 4 | Kliknij „Zapisz" | — | Wywołanie `PUT /api/DocumentSeries/UpdateDocumentSeries` — status 200 OK |
| 5 | Sprawdź zaktualizowane dane | — | Seria `FV` ma `currentNumber=100` na liście |
| 6 | Sprawdź czy następna faktura otrzyma numer FV0100 | Wystaw nową fakturę z serią `FV` | Faktura otrzymuje numer `FV0100` |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-142: Usunięcie serii dokumentów

**Typ:** Happy path
**Priorytet:** Średni
**Powiązane:** API-21 (`PUT /api/DocumentSeries/DeleteDocumentSeries`)

> **Uwaga:** Usunięcie serii dokumentów to operacja soft-delete. Sprawdź zachowanie systemu, gdy do serii są przypisane istniejące faktury.

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Dodaj nową serię pomocniczą do usunięcia | Nazwa: `TEST-DEL`, typ: `Faktura`, numer startowy: `1` | Seria widoczna na liście |
| 2 | Upewnij się, że do serii nie są przypisane żadne dokumenty | — | Brak faktur z serią `TEST-DEL` |
| 3 | Zaznacz serię `TEST-DEL` i kliknij „Usuń" | — | Dialog potwierdzenia |
| 4 | Potwierdź usunięcie | — | Wywołanie `PUT /api/DocumentSeries/DeleteDocumentSeries` — status 200 OK |
| 5 | Sprawdź listę serii | — | Seria `TEST-DEL` nie jest już widoczna na liście |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-143: Generowanie kolejnych numerów dokumentów

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** API-22 (`POST /api/Document/AddDocument`), API-18, anomalia A-02 (race condition) z `plan_testow.md`

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Upewnij się, że seria `FV` istnieje z `currentNumber=1` | — | Seria widoczna; currentNumber=1 |
| 2 | Wystaw pierwszą fakturę z serią `FV` | Seria: `FV`, klient, konto bankowe, pozycja faktury | Wywołanie `POST /api/Document/AddDocument` — faktura z numerem `FV0001` |
| 3 | Sprawdź licznik serii po wystawieniu | — | `GET /api/DocumentSeries/GetAll` zwraca serię `FV` z `currentNumber=2` |
| 4 | Wystaw drugą fakturę z serią `FV` | Seria: `FV`, dane faktury | Faktura z numerem `FV0002` |
| 5 | Sprawdź licznik serii | — | `currentNumber=3` |
| 6 | Sprawdź listę faktur | — | Dwie faktury: `FV0001` i `FV0002`, numery unikalne |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
