# TC-E10 — Scenariusze testowe (AddOrEditInvoiceComponent)

| Pole | Wartość |
|---|---|
| ID | TC-E10 |
| Ekran | [E-10 Formularz faktury](E-10_ekran.md) |
| Wersja | 1.0 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Prereq — autoryzacja

| Wymaganie | Szczegół |
|---|---|
| Typ | JWT Bearer token |
| Rola | `"User"` |
| Nagłówek HTTP | `Authorization: Bearer <token>` |
| Uzyskanie | [POST /api/Auth/login](../../../04_api_i_integracje/01_api_frontend/auth/POST_Auth_login.md) |

## Prereq — dane w DB

| Encja | Minimum |
|---|---|
| `Firm` (klient) | ≥1 firma z `UserFirm.IsClient=true` |
| `DocumentSeries` | seria z `DocumentTypeId=1` dla aktywnego UserFirm |
| `DocumentStatus` | seedowane: Unpaid(id=1), Paid(id=2) |
| `Product` | opcjonalnie — dla autocomplete |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Pole Client | `input[placeholder*="CUI"]` |
| Issue Date | pierwszy `input[matDatepicker]` |
| Due Date | drugi `input[matDatepicker]` |
| Select Status | `mat-select` z etykietą „Status" |
| Przycisk Add Product | `button` z tekstem „+" / „Add Product" |
| Przycisk Save/Update | `button` z `(click)=onSubmit()` |
| Przycisk Preview | `button` z tekstem „Preview" |
| Przycisk Generate | `button` z tekstem „Generate" |
| Przycisk Wróć | `button` z ikoną `arrow_back` |

> Brak `data-cy` — anomalia BA-07.

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E10-01 | Formularz dodaj — pusty | seria TypeId=1, klient | GET /add-invoice | formularz z domyślnym issueDate=dzisiaj |
| TC-E10-02 | Formularz edycja — załadowanie | faktura id=42 | GET /edit-invoice/42 | formularz z danymi faktury 42 |
| TC-E10-03 | Dodaj fakturę (happy path) | klient id=2, seria id=1 | wypełnij → [OP-E10-03](E-10_OP-03.md) | toastr success + [E-09](../E-09_InvoicesComponent/E-09_ekran.md) |
| TC-E10-04 | Walidacja — brak klienta | — | submit bez klienta | błąd walidacji |
| TC-E10-05 | Walidacja — due date przed issue date | — | issueDate=2026-06-01, dueDate=2026-05-01 | błąd (dueDateValidator) |
| TC-E10-06 | Dodaj pozycję | — | klik [OP-E10-01](E-10_OP-01.md) | nowy wiersz w [TAB-E10-01](E-10_TAB-01.md) |
| TC-E10-07 | Usuń pozycję | ≥2 wiersze | klik ✕ [OP-E10-02](E-10_OP-02.md) | wiersz znika |
| TC-E10-08 | Autocomplete klienta | klient „ABC SRL" | wpisz „ABC" → [FILTR-E10-01](E-10_FILTR-01.md) | podpowiedź „ABC SRL" |
| TC-E10-09 | Autocomplete produktu | produkt „Consulting" | wpisz „Con" → [FILTR-E10-02](E-10_FILTR-02.md) | podpowiedź + autouzupełnienie pól |
| TC-E10-10 | Preview PDF | faktura id=42, edycja | klik [OP-E10-04](E-10_OP-04.md) | [MODAL-E10-01](E-10_MODAL-01.md) z PDF |
| TC-E10-11 | Wróć | dowolny stan | klik [OP-E10-06](E-10_OP-06.md) | redirect [E-09](../E-09_InvoicesComponent/E-09_ekran.md) |
| TC-E10-12 | Brak autoryzacji | brak tokenu | GET /add-invoice | redirect do /login |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Wydzielony z E-10_ekran.md. |
