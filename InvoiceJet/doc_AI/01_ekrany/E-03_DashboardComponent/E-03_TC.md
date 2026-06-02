# TC-E03 — Scenariusze testowe (DashboardComponent)

| Pole | Wartość |
|---|---|
| ID dokumentu | TC-E03 |
| Typ dokumentu | scenariusze testowe |
| Ekran | [E-03 DashboardComponent](E-03_ekran.md) |
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
| `UserFirm` | Aktywny związek użytkownik–firma |
| `Document` | ≥1 faktura dla TC-E03-01; 0 faktur dla TC-E03-02 |

## Selektory CSS/Angular

| Element | Selektor |
|---|---|
| Selektor roku | `mat-select` (pierwszy na stronie) lub `[formControlName="year"]` |
| Selektor typu dokumentu | `mat-select` (drugi na stronie) lub `[formControlName="documentType"]` |
| Licznik dokumentów | `.stat-card:nth-child(1) .stat-value` |
| Licznik klientów | `.stat-card:nth-child(2) .stat-value` |
| Licznik produktów | `.stat-card:nth-child(3) .stat-value` |
| Licznik kont bankowych | `.stat-card:nth-child(4) .stat-value` |
| Wykres liniowy | `canvas` (ng2-charts) |

> Brak `data-cy` — do uzupełnienia.

## Scenariusze e2e

| ID | Opis | Prereq DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E03-01 | Załadowanie dashboardu z danymi | ≥1 faktura TypeId=1 dla UserFirm | 1. Login 2. GET `/dashboard` | Liczniki > 0; wykres widoczny z danymi; izolacja ([ALG-10](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md)) |
| TC-E03-02 | Pusty dashboard (brak faktur) | 0 dokumentów dla UserFirm | 1. Login (nowe konto bez faktur) 2. GET `/dashboard` | Liczniki = 0; wykres pusty / zerowe wartości |
| TC-E03-03 | Zmiana roku/filtru | ≥1 faktura w roku 2025 | 1. Login 2. GET `/dashboard` 3. Zmień selektor roku na 2025 ([OP-E03-01](E-03_OP-01.md)) | Wykres przeładowany z danymi 2025; HTTP GET `/api/Document/GetDashboardStats/2025/1` |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
