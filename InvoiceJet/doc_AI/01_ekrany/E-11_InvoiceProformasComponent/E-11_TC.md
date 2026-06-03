# TC-E11 — Scenariusze testowe (InvoiceProformasComponent)

| Pole | Wartość |
|---|---|
| ID dokumentu | TC-E11 |
| Typ dokumentu | scenariusze testowe |
| Ekran | [E-11 InvoiceProformasComponent](E-11_ekran.md) |
| Wersja | 0.1 |
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
| `Document` (TypeId=2) | ≥1 proforma dla aktywnego UserFirm |
| `Firm` (klient) | ≥1 firma z `UserFirm.IsClient=true` |
| `DocumentSeries` | ≥1 seria z `DocumentTypeId=2` (PRF) dla aktywnego UserFirm |
| `DocumentStatus` | seedowane: Unpaid(id=1), Paid(id=2) |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Przycisk New Proforma | `button[mat-raised-button]` z tekstem „New Proforma" |
| Menu ⋮ | `button[mat-stroked-button]` z `mat-icon` `more_vert` |
| „Delete selected" | `button[mat-menu-item]` z ikoną `delete` |
| Pole Search | `input[matInput]` z placeholder „Search" |
| Wiersze tabeli | `tr.clickable` |
| Checkbox wiersza | `mat-checkbox` w `td.select-column` |
| Checkbox nagłówka | `mat-checkbox` w `th.select-column` |
| Paginator | `mat-paginator` |

> Brak `data-cy` — anomalia IA-04.

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E11-01 | Załadowanie listy proform | ≥1 proforma TypeId=2 | 1. Login 2. GET /dashboard/invoice-proformas | [TAB-E11-01](E-11_TAB-01.md) z proformami; kolumna Document Nr zawiera wartości z serii PRF |
| TC-E11-02 | Wyszukiwanie po numerze | proforma „PRF0001" | wpisz „PRF0001" w [FILTR-E11-01](E-11_FILTR-01.md) | tylko wiersz PRF0001 widoczny w tabeli |
| TC-E11-03 | Nawigacja do dodania proformy | — | klik [OP-E11-01](E-11_OP-01.md) „New Proforma" | URL = `/dashboard/add-invoice-proforma`; ekran [E-12](../E-12_AddOrEditInvoiceProformaComponent/E-12_ekran.md) |
| TC-E11-04 | Edycja proformy | proforma id=7 TypeId=2 | klik wiersz id=7 [OP-E11-02](E-11_OP-02.md) | URL = `/dashboard/edit-invoice-proforma/7`; ekran [E-12](../E-12_AddOrEditInvoiceProformaComponent/E-12_ekran.md) z danymi proformy 7 |
| TC-E11-05 | Usuń zaznaczone proformy | proforma id=7 TypeId=2 | zaznacz checkbox id=7 → menu ⋮ → [OP-E11-03](E-11_OP-03.md) „Delete selected" | id=7 znika z tabeli; PUT /api/Document/DeleteDocuments z `[7]` |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — adaptacja z wzorca TC-E09. |
