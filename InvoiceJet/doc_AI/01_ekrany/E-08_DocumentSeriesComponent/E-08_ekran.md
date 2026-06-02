# E-08 DocumentSeriesComponent — Lista serii dokumentów

| Pole | Wartość |
|---|---|
| ID dokumentu | E-08 |
| Typ dokumentu | ekran |
| Wersja | 1.0 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 |
| Data ostatniej modyfikacji | 2026-06-02 |

## Streszczenie

Ekran zarządzania seriami numeracji dokumentów. Każda seria definiuje prefiks i aktualny licznik, z których generowany jest numer kolejnego dokumentu. Aplikacja posiada domyślne serie FV (faktura), PRF (proforma), STN (storno) tworzone automatycznie po rejestracji. Operacje CRUD przez dialog Angular Material. Chroniony przez `AuthGuard` (rola: User).

---

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────────┐
│ Serie dokumentów                       [+ Dodaj serię]   │
├──┬──────────────┬───────────────┬────────────────────────┤
│☐ │ Nazwa serii  │ Typ dokumentu │ Aktualny numer          │
├──┼──────────────┼───────────────┼────────────────────────┤
│☐ │ FV           │ Faktura       │ 1                       │
│☐ │ PRF          │ Proforma      │ 1                       │
│☐ │ STN          │ Storno        │ 1                       │
├──┴──────────────┴───────────────┴────────────────────────┤
│ [Usuń zaznaczone]                        [Paginacja]      │
└──────────────────────────────────────────────────────────┘
```

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/document-series` |
| Wymagana rola | `User` (AuthGuard JWT) |
| Punkty wejścia | Klik „Document Series" w Sidebar |
| Komponent Angular | `DocumentSeriesComponent` |
| Plik | `src/app/components/document-series/document-series.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek |
|---|---|---|
| Dialog `AddOrEditDocumentSeriesDialogComponent` | Klik „Dodaj serię" | Zawsze |
| Dialog `AddOrEditDocumentSeriesDialogComponent` | Klik „Edytuj" przy wierszu | Zawsze |

---

## Filtry

| ID | Nazwa w UI | Typ | Opis |
|---|---|---|---|
| FILTR-E08-01 | Search | input, kliencki MatTableDataSource | Filtr po nazwie serii i typie dokumentu |

## Tabele i listy

| ID | Nazwa | Opis |
|---|---|---|
| TAB-E08-01 | Lista serii dokumentów | Tabela z sortowaniem i paginacją |

### Kolumny tabeli

| Kolumna | Opis | Algorytm |
|---|---|---|
| Checkbox | Zaznaczanie do operacji batch | — |
| `seriesName` | Nazwa serii (prefiks numeru) | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) — `seriesName + currentNumber.PadLeft(4)` |
| `documentType` | Typ dokumentu (Faktura/Proforma/Storno) | — |
| `currentNumber` | Aktualny licznik (inkrementowany przy każdym dokumencie) | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) |

## Operacje

| ID | Etykieta UI | Opis | Algorytm |
|---|---|---|---|
| OP-E08-01 | Dodaj serię | Otwiera dialog dodania | [ALG-02 Generowanie numeru](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) |
| OP-E08-02 | Edytuj (klik wiersza) | Otwiera dialog edycji | [ALG-02 Generowanie numeru](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) |
| OP-E08-03 | Usuń zaznaczone | Batch soft-delete | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) |

## Scenariusze testowe

→ [E-08_TC.md](E-08_TC.md)

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint |
|---|---|---|
| Załadowanie listy | GET | `/api/DocumentSeries/GetAll` |
| Dodanie serii | POST | `/api/DocumentSeries/AddDocumentSeries` |
| Edycja serii | PUT | `/api/DocumentSeries/EditDocumentSeries` |
| Usunięcie zaznaczonych | PUT | `/api/DocumentSeries/DeleteDocumentSeries` |

---

## Powiązania

| Typ | Dokument |
|---|---|
| Algorytm | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) — `SeriesName + CurrentNumber.PadLeft(4, '0')` → np. FV0001 |
| Algorytm | [dedykowane/inicjalizacja_serii_dokumentow](../../../03_algorytmy/dedykowane/inicjalizacja_serii_dokumentow.md) — domyślne serie FV/PRF/STN tworzone po rejestracji |
| Algorytm | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) — serie izolowane per UserFirm |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | `src/app/components/document-series/document-series.component.ts` |
| Dialog | `src/app/components/document-series/add-or-edit-document-series-dialog/add-or-edit-document-series-dialog.component.ts` |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| DS-01 | Brak walidacji unikalności `seriesName` per UserFirm — możliwe duplikaty serii |
| DS-02 | Brak `data-cy` / `data-testid` — selektory nieodporne na zmiany UI |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
