# TC-E08 — Scenariusze testowe (DocumentSeriesComponent)

| Pole | Wartość |
|---|---|
| ID dokumentu | TC-E08 |
| Typ dokumentu | scenariusze testowe |
| Ekran | [E-08 DocumentSeriesComponent](E-08_ekran.md) |
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
| `DocumentSeries` | Dla TC-E08-01: domyślne serie FV/PRF/STN (inicjalizowane przy rejestracji) |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Przycisk Dodaj serię | `button[mat-raised-button]` z tekstem „Add Series" |
| Pole Search | `input[matInput]` z placeholder „Search" |
| Wiersze tabeli | `mat-row` lub `tr` z seriami |
| Checkbox wiersza | `mat-checkbox` w wierszu |
| Przycisk Usuń zaznaczone | `button` z tekstem „Delete selected" lub ikoną `delete` |
| Dialog Dodaj/Edytuj | `mat-dialog-container` |
| Pole Nazwa serii (dialog) | `mat-dialog-container input[formControlName="seriesName"]` |
| Select Typ dokumentu (dialog) | `mat-dialog-container mat-select[formControlName="documentType"]` |
| Pole Numer startowy (dialog) | `mat-dialog-container input[formControlName="firstNumber"]` |
| Przycisk Save (dialog) | `mat-dialog-container button[type="submit"]` |

> Brak `data-cy` — anomalia DS-02.

## Powiązane algorytmy

| Algorytm | Powiązanie |
|---|---|
| [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | Każda seria definiuje format numeru: `seriesName + currentNumber.PadLeft(4,'0')` |
| [dedykowane/inicjalizacja_serii_dokumentow](../../../03_algorytmy/dedykowane/inicjalizacja_serii_dokumentow.md) | Domyślne serie FV/PRF/STN tworzone automatycznie po rejestracji |

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E08-01 | Załadowanie listy — domyślne serie | Serie FV/PRF/STN (po rejestracji) | 1. Login (nowe konto) 2. GET `/dashboard/document-series` | **Weryfikacja [inicjalizacja_serii]:** tabela zawiera FV (currentNumber=1), PRF (currentNumber=1), STN (currentNumber=1) |
| TC-E08-02 | Dodanie własnej serii | UserFirm istnieje | 1. Login 2. GET `/dashboard/document-series` 3. Klik „Add Series" 4. Wypełnij: seriesName=„TEST", documentType=Faktura, firstNumber=1 5. Save | HTTP POST `/api/DocumentSeries/Add` 201; seria „TEST" widoczna w tabeli |
| TC-E08-03 | Edycja serii | Seria „TEST" istnieje | 1. Login 2. Klik wiersz „TEST" → dialog 3. Zmień firstNumber=5 4. Save | HTTP PUT `/api/DocumentSeries/Edit` 200; currentNumber=5 |
| TC-E08-04 | Weryfikacja generowania numeru po serii | Seria „TEST" (currentNumber=1), firma | 1. Login 2. GET `/dashboard/add-invoice` 3. Wybierz serię „TEST" 4. Dodaj pozycje i Zapisz | **Weryfikacja [ALG-02]:** numer faktury = „TEST0001"; currentNumber serii → 2 |
| TC-E08-05 | Usuń zaznaczone serie | ≥1 seria własna (nie FV/PRF/STN) | 1. Login 2. Zaznacz serię „TEST" 3. Klik „Delete selected" | HTTP PUT `/api/DocumentSeries/Delete` 200; seria znika |
| TC-E08-06 | Brak autoryzacji | — | GET `/dashboard/document-series` bez tokenu | Redirect do `/login` (AuthGuard) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
