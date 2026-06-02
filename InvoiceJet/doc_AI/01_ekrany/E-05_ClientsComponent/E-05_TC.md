# TC-E05 — Scenariusze testowe (ClientsComponent)

| Pole | Wartość |
|---|---|
| ID dokumentu | TC-E05 |
| Typ dokumentu | scenariusze testowe |
| Ekran | [E-05 ClientsComponent](E-05_ekran.md) |
| Wersja | 1.0 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 |
| Data | 2026-06-02 |

## Prereq — autoryzacja (wymagane dla każdego testu)

| Wymaganie | Szczegół |
|---|---|
| Typ | JWT Bearer token |
| Rola | `"User"` w claims |
| Nagłówek HTTP | `Authorization: Bearer <token>` |
| Uzyskanie tokenu | POST `/api/Auth/login` |

## Prereq — dane w DB

| Encja | Minimum |
|---|---|
| `User` | ≥1 zalogowany użytkownik |
| `Firm` (klient, IsClient=true) | ≥1 klient dla aktywnego UserFirm (TC-E05-01, TC-E05-02, TC-E05-04, TC-E05-05) |
| `Firm` (klient z nazwą „ABC") | Dla TC-E05-02 |
| `Firm` (klient id=42) | Dla TC-E05-04, TC-E05-05 |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Przycisk Dodaj klienta | `button[mat-raised-button]` z tekstem „Dodaj klienta" |
| Pole filtra | `input[matInput]` z placeholder „Filter" lub podobnym |
| Wiersze tabeli | `tr[mat-row]` |
| Checkbox wiersza | `mat-checkbox` w `td` |
| Checkbox nagłówka (zaznacz wszystkie) | `mat-checkbox` w `th` |
| Przycisk Edytuj przy wierszu | `button[mat-icon-button]` z `mat-icon` `edit` |
| Przycisk Usuń zaznaczone | `button[mat-raised-button]` lub `button[mat-button]` z tekstem „Usuń zaznaczone" |
| Paginator | `mat-paginator` |

> Brak `data-cy` — do uzupełnienia.

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E05-01 | Załadowanie listy klientów | ≥1 klient IsClient=true dla UserFirm | 1. Login 2. GET `/dashboard/clients` | [TAB-E05-01](E-05_TAB-01.md) z klientami; izolacja UserFirm ([ALG-10](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md)) |
| TC-E05-02 | Filtrowanie listy | Klient o nazwie „ABC SRL" | 1. Login 2. GET `/dashboard/clients` 3. Wpisz „ABC" w [FILTR-E05-01](E-05_FILTR-01.md) | Tabela pokazuje tylko wiersze zawierające „ABC"; filtr po stronie klienta |
| TC-E05-03 | Dodaj klienta (dialog) | — | 1. Login 2. GET `/dashboard/clients` 3. Klik [OP-E05-01] 4. Wypełnij dialog (firmName) 5. Klik Save w dialogu | Nowy wiersz pojawia się w tabeli; HTTP POST `/api/Firm/AddFirm` (isClient=true) |
| TC-E05-04 | Edytuj klienta | Klient id=42 istnieje | 1. Login 2. GET `/dashboard/clients` 3. Klik [OP-E05-02] Edytuj przy kliencie id=42 | Dialog z wypełnionymi danymi klienta; po Save HTTP PUT `/api/Firm/EditFirm`; dane zaktualizowane |
| TC-E05-05 | Usuń zaznaczone | ≥1 klient id=42 | 1. Login 2. GET `/dashboard/clients` 3. Zaznacz klienta id=42 4. Klik [OP-E05-03] Usuń zaznaczone | HTTP PUT `/api/Firm/DeleteFirms?ids=42`; wiersz id=42 znika z tabeli ([ALG-10](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md)) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
