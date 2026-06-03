# TC-E09 — Scenariusze testowe (InvoicesComponent)

| Pole | Wartość |
|---|---|
| ID dokumentu | TC-E09 |
| Typ dokumentu | scenariusze testowe |
| Ekran | [E-09 InvoicesComponent](E-09_ekran.md) |
| Wersja | 1.0 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

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
| `Document` (TypeId=1) | ≥1 faktura dla aktywnego UserFirm |
| `Firm` (klient) | ≥1 firma z `UserFirm.IsClient=true` |
| `DocumentStatus` | seedowane: Unpaid(id=1), Paid(id=2) |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Przycisk New Invoice | `button[mat-raised-button]` z tekstem „New Invoice" |
| Menu ⋮ | `button[mat-stroked-button]` z `mat-icon` `more_vert` |
| „Delete selected" | `button[mat-menu-item]` z ikoną `delete` |
| „Transform to storno" | `button[mat-menu-item]` z ikoną `swap_vert` |
| Pole Search | `input[matInput]` z placeholder „Search" |
| Wiersze tabeli | `tr.clickable` |
| Checkbox wiersza | `mat-checkbox` w `td.select-column` |
| Checkbox nagłówka | `mat-checkbox` w `th.select-column` |
| Paginator | `mat-paginator` |

> Brak `data-cy` — anomalia IA-04.

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E09-01 | Załadowanie listy | ≥1 faktura TypeId=1 | 1. Login 2. GET /dashboard/invoices | [TAB-E09-01](E-09_TAB-01.md) z fakturami |
| TC-E09-02 | Wyszukiwanie | faktura „FV0001" | wpisz „FV0001" w [FILTR-E09-01](E-09_FILTR-01.md) | tylko FV0001 |
| TC-E09-03 | Clear Search | po TC-E09-02 | klik × | pełna lista |
| TC-E09-04 | New Invoice | — | klik [OP-E09-01](E-09_OP-01.md) | URL = `/dashboard/add-invoice` |
| TC-E09-05 | Edycja faktury | faktura id=42 | klik wiersz id=42 [OP-E09-02](E-09_OP-02.md) | URL = `/dashboard/edit-invoice/42` |
| TC-E09-06 | Usuń fakturę | id=42 istnieje | zaznacz → menu ⋮ → [OP-E09-03](E-09_OP-03.md) | id=42 znika |
| TC-E09-07 | Transform to Storno | id=42 TypeId=1 | zaznacz → menu ⋮ → [OP-E09-04](E-09_OP-04.md) | id=42 znika; w [E-13](../E-13_InvoiceStornosComponent/E-13_ekran.md) |
| TC-E09-08 | Brak autoryzacji | brak tokenu | GET /dashboard/invoices | redirect do /login |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Wydzielony z E-09_ekran.md. |
