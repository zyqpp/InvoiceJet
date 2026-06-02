# Scenariusze testowe manualne: Firma i klienci

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-MAN-FIRMA |
| Typ dokumentu | scenariusze testowe manualne |
| Wersja | 0.1 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Scenariusze testowe obejmują dodanie i edycję własnej firmy (profil użytkownika) oraz zarządzanie firmami klientów — zarówno ręcznie jak i przez integrację z rumuńskim rejestrem ANAF. Powiązane z endpointami API-03 – API-09.

## Powiązane algorytmy

| Algorytm | Testowane przez |
|---|---|
| [ALG-06 Integracja ANAF](../../../03_algorytmy/dedykowane/integracja_anaf.md) | TC-111 — autouzupełnienie przez CUI, TC-116 — klient przez ANAF |
| [dedykowane/zarzadzanie_relacja_userfirm](../../../03_algorytmy/dedykowane/zarzadzanie_relacja_userfirm.md) | TC-110 — ManageUserFirmRelation przy AddFirm |
| [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | TC-114/115 — klienci widoczni tylko dla bieżącego użytkownika |

## Selektory CSS / Angular Material

| Element | Selektor |
|---|---|
| Pole Nazwa firmy | `input[formControlName="firmName"]` |
| Pole CUI | `input[formControlName="cuiValue"]` |
| Ikona chmury ANAF | `button[mat-icon-button][matSuffix]` lub `button` z `mat-icon` `cloud_download` |
| Pole Reg. Com | `input[formControlName="regCom"]` |
| Pole Adres | `input[formControlName="address"]` |
| Pole Okręg | `input[formControlName="county"]` |
| Pole Miasto | `input[formControlName="city"]` |
| Przycisk Zapisz | `button[type="submit"]` lub `button` z tekstem „Save" |
| Dialog Dodaj/Edytuj klienta | `mat-dialog-container` |
| Input w dialogu (Nazwa klienta) | `mat-dialog-container input[formControlName="firmName"]` |

---

## TC-110: Dodanie własnej firmy (happy path)

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** API-03 (`POST /api/Firm/AddFirm/false`)

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Zaloguj się i przejdź do sekcji „Moja firma" | e-mail: `test@example.com` | Formularz danych firmy widoczny, pola puste |
| 2 | Wypełnij formularz danych firmy | Nazwa: `TEST SRL`, CUI: `12345678`, Nr. reg.: `J40/1234/2020`, Adres: `Str. Testului 1, Bucuresti` | Formularz wypełniony |
| 3 | Kliknij „Zapisz" | — | Wywołanie `POST /api/Firm/AddFirm/false` — status 201 Created |
| 4 | Sprawdź potwierdzenie | — | Komunikat o pomyślnym zapisaniu danych firmy |
| 5 | Odśwież stronę i sprawdź dane | — | Dane firmy wyświetlone zgodnie z wprowadzonymi; `GET /api/Firm/GetUserActiveFirm` zwraca obiekt firmy |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-111: Autouzupełnienie danych firmy z ANAF po CUI

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** API-04 (`GET /api/Firm/GetFirmFromAnaf`), integracja z ANAF

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Zaloguj się i przejdź do formularza firmy (własna lub klient) | — | Formularz widoczny z polem „CUI" i przyciskiem „Wyszukaj w ANAF" lub równoważnym |
| 2 | Wpisz CUI istniejącej rumuńskiej firmy | CUI: `14942091` (przykładowy CUI aktywnej spółki) | Pole CUI wypełnione |
| 3 | Kliknij przycisk autouzupełnienia ANAF | — | Wywołanie `GET /api/Firm/GetFirmFromAnaf?cui=14942091` |
| 4 | Sprawdź odpowiedź | — | Status 200 OK; pola formularza (nazwa, adres, nr rej.) zostają automatycznie wypełnione danymi z ANAF |
| 5 | Sprawdź wypełnione pola | — | Nazwa firmy, adres i numer rejestracyjny zgodne z danymi publicznymi ANAF |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-112: Edycja danych firmy

**Typ:** Happy path
**Priorytet:** Średni
**Powiązane:** API-05 (`PUT /api/Firm/EditFirm`)

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Upewnij się, że firma istnieje (po TC-110) | — | Dane firmy widoczne |
| 2 | Przejdź do sekcji edycji firmy | — | Formularz edycji z aktualnymi danymi |
| 3 | Zmień adres firmy | Nowy adres: `Str. Modificata 5, Cluj-Napoca` | Pole adresu zaktualizowane |
| 4 | Kliknij „Zapisz" | — | Wywołanie `PUT /api/Firm/EditFirm` — status 200 OK |
| 5 | Sprawdź zaktualizowane dane | — | Nowy adres widoczny na stronie; `GET /api/Firm/GetUserActiveFirm` zwraca nowy adres |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-113: Dodanie klienta ręcznie

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** API-03 (`POST /api/Firm/AddFirm/true`), API-07

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Zaloguj się i przejdź do sekcji „Klienci" | — | Lista klientów widoczna (może być pusta) |
| 2 | Kliknij „Dodaj klienta" | — | Formularz dodawania klienta widoczny |
| 3 | Wypełnij dane klienta ręcznie | Nazwa: `KLIENT TESTOWY SRL`, CUI: `99999999`, Adres: `Str. Clientului 10, Timisoara` | Formularz wypełniony |
| 4 | Kliknij „Zapisz" | — | Wywołanie `POST /api/Firm/AddFirm/true` — status 201 Created |
| 5 | Sprawdź listę klientów | — | Nowy klient widoczny na liście; `GET /api/Firm/GetUserClientFirms` zawiera dodanego klienta |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## TC-114: Dodanie klienta przez ANAF

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane:** API-03, API-04, API-07

| # | Akcja | Dane testowe | Oczekiwany wynik |
|---|---|---|---|
| 1 | Przejdź do sekcji „Klienci" i kliknij „Dodaj klienta" | — | Formularz dodawania klienta widoczny |
| 2 | Wpisz CUI i użyj autouzupełnienia ANAF | CUI: `14942091` | Wywołanie `GET /api/Firm/GetFirmFromAnaf?cui=14942091`; pola formularza wypełnione automatycznie |
| 3 | Sprawdź dane w formularzu | — | Nazwa, adres, numer rejestracyjny zgodne z ANAF |
| 4 | Kliknij „Zapisz" | — | Wywołanie `POST /api/Firm/AddFirm/true` — status 201 Created |
| 5 | Sprawdź listę klientów | — | Klient z danymi z ANAF widoczny na liście |

**Wynik rzeczywisty:** [Do wypełnienia przez testera]
**Status:** [Nie przetestowany]

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
