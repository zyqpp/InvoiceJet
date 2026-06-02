# TC-E04 — Scenariusze testowe (FirmDetailsComponent)

| Pole | Wartość |
|---|---|
| ID dokumentu | TC-E04 |
| Typ dokumentu | scenariusze testowe |
| Ekran | [E-04 FirmDetailsComponent](E-04_ekran.md) |
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
| `Firm` (własna) | Dla TC-E04-02: brak firmy; dla TC-E04-03: firma już istnieje |
| ANAF | Dla TC-E04-01/04: zewnętrzne API dostępne (lub mock) |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Pole Nazwa firmy | `input[formControlName="firmName"]` |
| Pole CUI | `input[formControlName="cuiValue"]` |
| Przycisk ANAF ☁ | `button[mat-icon-button]` z `mat-icon` `cloud_download` |
| Pole Reg. handlowy | `input[formControlName="regCom"]` |
| Pole Adres | `input[formControlName="address"]` |
| Pole Okręg | `input[formControlName="county"]` |
| Pole Miasto | `input[formControlName="city"]` |
| Przycisk Zapisz | `button[type="submit"]` lub `button[mat-raised-button]` z tekstem „Zapisz" |

> Brak `data-cy` — do uzupełnienia.

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E04-01 | Autouzupełnienie z ANAF | Brak lub istniejąca firma | 1. Login 2. GET `/dashboard/firm-details` 3. Wpisz CUI `12345678` 4. Klik [OP-E04-02] ☁ | Pola firmName, regCom, address, county, city wypełnione danymi z [ALG-06](../../../03_algorytmy/dedykowane/integracja_anaf.md); HTTP GET `/api/Firm/fromAnaf?cui=12345678` |
| TC-E04-02 | Zapisanie nowej firmy | Brak firmy dla UserFirm | 1. Login (konto bez firmy) 2. GET `/dashboard/firm-details` 3. Wypełnij firmName 4. Klik [OP-E04-01] Zapisz | HTTP POST `/api/Firm/AddFirm`; relacja UserFirm stworzona ([ALG-07](../../../03_algorytmy/dedykowane/zarzadzanie_relacja_userfirm.md)); ekran odświeżony |
| TC-E04-03 | Edycja istniejącej firmy | Firma istnieje w UserFirm | 1. Login 2. GET `/dashboard/firm-details` 3. Pola wstępnie wypełnione 4. Zmień firmName 5. Klik [OP-E04-01] Zapisz | HTTP PUT `/api/Firm/EditFirm`; dane zaktualizowane; ekran odświeżony |
| TC-E04-04 | Błąd ANAF (nieprawidłowy CUI) | — | 1. Login 2. GET `/dashboard/firm-details` 3. Wpisz CUI `00000000` (nieistniejący) 4. Klik [OP-E04-02] ☁ | Błąd z ANAF API wyświetlony; pola NIE wypełnione |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
