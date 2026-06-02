# TC-E07 — Scenariusze testowe (ProductsComponent)

| Pole | Wartość |
|---|---|
| ID dokumentu | TC-E07 |
| Typ dokumentu | scenariusze testowe |
| Ekran | [E-07 ProductsComponent](E-07_ekran.md) |
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
| Uzyskanie tokenu | [POST /api/Auth/login](../../../04_api_i_integracje/01_api_frontend/auth/POST_Auth_login.md) |

## Prereq — dane w DB

| Encja | Minimum |
|---|---|
| `User` + `Firm` + `UserFirm` | ≥1 aktywny UserFirm |
| `Product` | Dla TC-E07-03/04: ≥1 produkt przypisany do UserFirm |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Przycisk Dodaj produkt | `button[mat-raised-button]` z tekstem „Add Product" |
| Pole Search | `input[matInput]` z placeholder „Search" |
| Wiersze tabeli | `mat-row` lub `tr` w tabeli produktów |
| Checkbox wiersza | `mat-checkbox` w wierszu |
| Przycisk Usuń zaznaczone | `button` z tekstem „Delete selected" lub ikoną `delete` |
| Dialog Dodaj/Edytuj | `mat-dialog-container` |
| Pole Nazwa (dialog) | `mat-dialog-container input[formControlName="name"]` |
| Pole Cena (dialog) | `mat-dialog-container input[formControlName="price"]` |
| Select VAT (dialog) | `mat-dialog-container mat-select[formControlName="tvaValue"]` |
| Pole J.m. (dialog) | `mat-dialog-container input[formControlName="unitOfMeasurement"]` |
| Przycisk Save (dialog) | `mat-dialog-container button[type="submit"]` |

> Brak `data-cy` — do uzupełnienia.

## Powiązane algorytmy

| Algorytm | Powiązanie |
|---|---|
| [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Lista produktów filtrowana per UserFirm |
| [wyliczeniowe/obliczanie_ceny_pozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md) | Cena i VAT produktu → autouzupełnienie w formularzu faktury |

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E07-01 | Załadowanie listy produktów | ≥1 produkt UserFirm | 1. Login 2. GET `/dashboard/products` | Tabela z produktami; `GET /api/Product/GetAll` HTTP 200 |
| TC-E07-02 | Wyszukiwanie produktu | produkt „Servicii consultanta" | 1. Login 2. GET `/dashboard/products` 3. Wpisz „Servicii" w Search | Tylko „Servicii consultanta" widoczny |
| TC-E07-03 | Dodanie nowego produktu | UserFirm istnieje | 1. Login 2. GET `/dashboard/products` 3. Klik „Add Product" 4. Wypełnij: name=„Servicii consultanta", price=500.00, tvaValue=19, unitOfMeasurement=„ore" 5. Save | HTTP POST `/api/Product/Add` 201; produkt w tabeli |
| TC-E07-04 | Edycja produktu | ≥1 produkt | 1. Login 2. Klik wiersz → dialog 3. Zmień price=600.00 4. Save | HTTP PUT `/api/Product/Edit` 200; cena zaktualizowana |
| TC-E07-05 | Usuń zaznaczone | ≥2 produkty | 1. Login 2. Zaznacz 2 checkboxy 3. Klik „Delete selected" | HTTP PUT `/api/Product/Delete` `[id1, id2]` 200; produkty znikają |
| TC-E07-06 | Anomalia: globalny UNIQUE INDEX nazwy | Konto User B | 1. Login jako A 2. Dodaj „TestProduct" 3. Login jako B 4. Próba dodania „TestProduct" | **Bug A-03:** HTTP 500 — globalny UNIQUE INDEX uniemożliwia tę samą nazwę u dwóch użytkowników |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
