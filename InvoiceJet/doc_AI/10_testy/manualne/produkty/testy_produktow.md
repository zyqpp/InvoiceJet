# Scenariusze testowe manualne: Produkty

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-MAN-PRODUKTY |
| Typ dokumentu | scenariusze testowe manualne |
| Wersja | 0.1 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Scenariusze testowe obejmują dodawanie, edycję i usuwanie produktów z katalogu użytkownika oraz weryfikację globalnego ograniczenia UNIQUE INDEX na nazwie produktu (anomalia). Powiązane z endpointami API-10 – API-13.

## Powiązane algorytmy

| Algorytm | Testowane przez |
|---|---|
| [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | TC-120 — produkty widoczne tylko dla bieżącej firmy |
| [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) | Pośrednio — cena i VAT produktu → autouzupełnianie w formularzu faktury |

## Selektory CSS / Angular Material

| Element | Selektor |
|---|---|
| Przycisk Dodaj produkt | `button[mat-raised-button]` z tekstem „Add Product" |
| Dialog | `mat-dialog-container` |
| Pole Nazwa produktu | `mat-dialog-container input[formControlName="name"]` |
| Pole Cena | `mat-dialog-container input[formControlName="price"]` lub `unitPrice` |
| Select Stawka VAT | `mat-dialog-container mat-select[formControlName="vatRate"]` lub `tvaValue` |
| Pole Jednostka miary | `mat-dialog-container input[formControlName="unitOfMeasurement"]` |
| Filter / Szukaj | `input[matInput]` z placeholder „Search" |
| Przycisk Save | `mat-dialog-container button[type="submit"]` |

> ⚠️ **ANOMALIA A-03:** Globalny UNIQUE INDEX na nazwie produktu — dwóch użytkowników nie może mieć produktu o tej samej nazwie!

---

## TC-120: Dodanie produktu (happy path)

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** API-11 (`POST /api/Product/AddProduct`), API-10

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Zaloguj się i przejdź do sekcji „Produkty" | e-mail: `test@example.com` | Lista produktów widoczna (może być pusta) |
| 2 | Kliknij „Dodaj produkt" | — | Formularz dodawania produktu widoczny |
| 3 | Wypełnij dane produktu | Nazwa: `Servicii consultanta`, Cena jednostkowa: `500.00`, Waluta: `RON`, VAT: `19%` | Formularz wypełniony |
| 4 | Kliknij „Zapisz" | — | Wywołanie `POST /api/Product/AddProduct` — status 201 Created |
| 5 | Sprawdź listę produktów | — | Nowy produkt widoczny na liście; `GET /api/Product/GetAll` zawiera dodany produkt |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-121: Edycja produktu

**Typ:** Happy path
**Priorytet:** Średni
**Powiązane:** API-12 (`PUT /api/Product/EditProduct`)

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Upewnij się, że produkt `Servicii consultanta` istnieje (po TC-120) | — | Produkt na liście |
| 2 | Kliknij „Edytuj" przy produkcie | — | Formularz edycji z aktualnymi danymi produktu |
| 3 | Zmień cenę jednostkową | Nowa cena: `600.00 RON` | Pole ceny zaktualizowane |
| 4 | Kliknij „Zapisz" | — | Wywołanie `PUT /api/Product/EditProduct` — status 200 OK |
| 5 | Sprawdź zaktualizowane dane | — | Nowa cena widoczna na liście produktów |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-122: Usunięcie produktu

**Typ:** Happy path
**Priorytet:** Średni
**Powiązane:** API-13 (`PUT /api/Product/DeleteProducts`)

> **Uwaga:** Usunięcie produktu w InvoiceJet jest operacją soft-delete (flaga `IsDeleted = true`). Produkt nie jest fizycznie kasowany z bazy danych.

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Upewnij się, że na liście istnieje przynajmniej jeden produkt | — | Lista zawiera produkt do usunięcia |
| 2 | Zaznacz produkt do usunięcia na liście | Produkt: `Servicii consultanta` | Produkt zaznaczony (checkbox) |
| 3 | Kliknij „Usuń" i potwierdź | — | Wywołanie `PUT /api/Product/DeleteProducts` — status 200 OK |
| 4 | Sprawdź listę produktów | — | Usunięty produkt nie jest już widoczny na liście |
| 5 | Sprawdź czy produkt jest nadal dostępny w dokumentach historycznych | — | Istniejące faktury z tym produktem nadal zawierają jego dane (soft-delete, brak utraty danych) |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-123: Próba dodania produktu z istniejącą nazwą (ANOMALIA — globalny UNIQUE INDEX)

**Typ:** Anomalia krytyczna
**Priorytet:** Wysoki
**Powiązane:** API-11, anomalia bazy danych — UNIQUE INDEX na kolumnie `Name` w tabeli `Products`

> **ANOMALIA:** W bazie danych InvoiceJet istnieje globalny UNIQUE INDEX na kolumnie `Name` w tabeli `Products`. Oznacza to, że dwóch różnych użytkowników NIE MOŻE mieć produktu o tej samej nazwie — ograniczenie działa między wszystkimi użytkownikami, a nie tylko w obrębie konta. Jest to prawdopodobnie błąd projektowy — powinien to być indeks unikalny na parze `(UserId, Name)`.

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Zaloguj się jako Użytkownik A i dodaj produkt | e-mail: `test@example.com`, produkt: `Produs Unic Test` | Produkt dodany — status 201 Created |
| 2 | Wyloguj się i zaloguj jako Użytkownik B (inne konto) | e-mail: `test2@example.com`, hasło: `Test@123` | Zalogowano jako Użytkownik B |
| 3 | Przejdź do produktów i dodaj produkt o tej samej nazwie | Nazwa: `Produs Unic Test` (ta sama co u Użytkownika A) | Formularz wypełniony |
| 4 | Kliknij „Zapisz" | — | Wywołanie `POST /api/Product/AddProduct` |
| 5 | Sprawdź odpowiedź | — | **Bug:** Backend zwraca błąd 500 Internal Server Error lub 400 z powodu naruszenia UNIQUE KEY (zamiast poprawnego zachowania: każdy użytkownik powinien móc mieć produkt o tej samej nazwie) |
| 6 | Sprawdź komunikat dla użytkownika | — | Komunikat błędu (jeśli w ogóle wyświetlony) może być niezrozumiały dla użytkownika |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
