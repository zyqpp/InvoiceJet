# TC-E13 — Scenariusze testowe (InvoiceStornosComponent)

| Pole | Wartość |
|---|---|
| ID dokumentu | TC-E13 |
| Typ dokumentu | scenariusze testowe |
| Ekran | [E-13 InvoiceStornosComponent](E-13_ekran.md) |
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
| `Document` (TypeId=3) | ≥1 storno dla aktywnego UserFirm (stworzone poprzez TransformToStorno z faktury TypeId=1) |
| `Document` (TypeId=1) | ≥1 faktura zwykła — wymagana jako źródło dla TC-E13-01 i TC-E13-02 |
| `Firm` (klient) | ≥1 firma z `UserFirm.IsClient=true` |
| `DocumentStatus` | seedowane: Unpaid(id=1), Paid(id=2) |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Menu ⋮ | `button[mat-stroked-button]` z `mat-icon` `more_vert` |
| „Delete selected" | `button[mat-menu-item]` z ikoną `delete` |
| Pole Search | `input[matInput]` z placeholder „Search" |
| Wiersze tabeli | `tr.clickable` |
| Checkbox wiersza | `mat-checkbox` w `td.select-column` |
| Checkbox nagłówka | `mat-checkbox` w `th.select-column` |
| Kolumna totalValue | `td` w kolumnie „Total" / `totalValue` |
| Paginator | `mat-paginator` |

> Brak `data-cy` — anomalia IA-04.
> Brak przycisku „New Storno" — storna tworzone wyłącznie przez TransformToStorno z E-09.

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E13-01 | Załadowanie listy storn (po poprzednim TransformToStorno) | ≥1 storno TypeId=3 (stworzone przez TransformToStorno z faktury) | 1. Login 2. Z [E-09](../E-09_InvoicesComponent/E-09_ekran.md): zaznacz fakturę id=5, wykonaj „Transform to storno" 3. GET /dashboard/invoice-stornos | [TAB-E13-01](E-13_TAB-01.md) zawiera storno powiązane z fakturą 5; kolumna Document Nr z serii STN |
| TC-E13-02 | Weryfikacja ujemnej wartości totalValue | storno id=10 (TypeId=3) stworzone z faktury o totalValue=600 | 1. GET /dashboard/invoice-stornos 2. Odczytaj kolumnę „Total" dla storna id=10 | Wartość totalValue = -600 (ujemna wartość faktury źródłowej); zgodnie z [ALG-08 TransformToStorno](../../../03_algorytmy/dedykowane/transformacja_na_storno.md) |
| TC-E13-03 | Edycja storna (klik wiersza) | storno id=10 TypeId=3 | klik wiersz id=10 [OP-E13-01](E-13_OP-01.md) | URL = `/dashboard/edit-invoice-storno/10`; ekran [E-14](../E-14_AddOrEditInvoiceStornosComponent/E-14_ekran.md) z danymi storna 10 |
| TC-E13-04 | Usuń zaznaczone storna | storno id=10 TypeId=3 | zaznacz checkbox id=10 → menu ⋮ → [OP-E13-02](E-13_OP-02.md) „Delete selected" | id=10 znika z tabeli; PUT /api/Document/DeleteDocuments z `[10]` |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — adaptacja z wzorca TC-E09/TC-E11; dodano scenariusz weryfikacji ujemnej wartości (ALG-08). |
