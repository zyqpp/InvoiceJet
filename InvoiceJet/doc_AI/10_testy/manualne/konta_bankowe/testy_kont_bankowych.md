# Scenariusze testowe manualne: Konta bankowe

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-MAN-KONTA-BANKOWE |
| Typ dokumentu | scenariusze testowe manualne |
| Wersja | 0.1 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Scenariusze testowe obejmują dodawanie, edycję oraz usuwanie kont bankowych firmy. Szczególnie istotny jest TC-132, który weryfikuje krytyczną anomalię kaskadowego usuwania faktur powiązanych z usuwanym kontem bankowym. Powiązane z endpointami API-14 – API-17.

---

## TC-130: Dodanie konta bankowego (happy path)

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** API-15 (`POST /api/BankAccount/AddBankAccount`), API-14

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Zaloguj się i przejdź do sekcji „Konta bankowe" | e-mail: `test@example.com` | Lista kont bankowych widoczna (może być pusta) |
| 2 | Kliknij „Dodaj konto" | — | Formularz dodawania konta bankowego widoczny |
| 3 | Wypełnij dane konta | IBAN: `RO49AAAA1B31007593840000`, waluta: `RON`, nazwa banku: `Banca Test SA` | Formularz wypełniony |
| 4 | Kliknij „Zapisz" | — | Wywołanie `POST /api/BankAccount/AddBankAccount` — status 201 Created |
| 5 | Sprawdź listę kont | — | Nowe konto widoczne na liście; `GET /api/BankAccount/GetAll` zawiera dodane konto |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-131: Edycja konta bankowego

**Typ:** Happy path
**Priorytet:** Średni
**Powiązane:** API-16 (`PUT /api/BankAccount/EditBankAccount`)

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Upewnij się, że konto bankowe istnieje (po TC-130) | — | Konto widoczne na liście |
| 2 | Kliknij „Edytuj" przy koncie bankowym | — | Formularz edycji z aktualnymi danymi |
| 3 | Zmień nazwę banku | Nowa nazwa banku: `Banca Modificata SA` | Pole nazwy banku zaktualizowane |
| 4 | Kliknij „Zapisz" | — | Wywołanie `PUT /api/BankAccount/EditBankAccount` — status 200 OK |
| 5 | Sprawdź zaktualizowane dane | — | Nowa nazwa banku widoczna na liście kont |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-132: Usunięcie konta bankowego — kaskadowe usunięcie faktur (ANOMALIA KRYTYCZNA A-KRIT-01)

**Typ:** Anomalia krytyczna
**Priorytet:** Wysoki
**Powiązane:** API-17 (`PUT /api/BankAccount/DeleteBankAccounts`), anomalia A-KRIT-01 z `plan_testow.md` (TC-01)

> **ANOMALIA KRYTYCZNA A-KRIT-01:** W bazie danych InvoiceJet relacja między `BankAccounts` a `Documents` skonfigurowana jest z regułą `CASCADE DELETE`. Oznacza to, że usunięcie konta bankowego powoduje automatyczne, bezpowrotne usunięcie wszystkich faktur powiązanych z tym kontem — bez ostrzeżenia dla użytkownika. Jest to krytyczny błąd utraty danych.

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Zaloguj się i upewnij się, że istnieje konto bankowe | IBAN: `RO49AAAA1B31007593840000` | Konto widoczne na liście |
| 2 | Wystaw fakturę przypisaną do tego konta | Faktura z kontem IBAN: `RO49AAAA1B31007593840000`, seria: `FV`, nr: `FV0001` | Faktura widoczna na liście faktur |
| 3 | Przejdź do kont bankowych i usuń konto | IBAN: `RO49AAAA1B31007593840000` | Wywołanie `PUT /api/BankAccount/DeleteBankAccounts` — status 200 OK |
| 4 | Sprawdź listę faktur | — | **Bug:** Faktura `FV0001` zniknęła z listy — CASCADE DELETE usunął fakturę wraz z kontem bankowym |
| 5 | Sprawdź oczekiwane zachowanie | — | **Oczekiwane (poprawne):** Usunięcie konta bankowego powinno być zablokowane, jeśli istnieją faktury do niego przypisane, lub konto powinno być zachowane w dokumentach historycznych (soft-delete bez kaskady) |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
