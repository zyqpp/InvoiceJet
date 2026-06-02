# DocumentSeriesComponent — Lista serii dokumentów

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-SerieDokumentow |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran zarządzania seriami numeracji dokumentów. Seria definiuje prefiks i bieżący licznik dla automatycznego generowania numerów dokumentów (np. `FV0005`, `PRF0012`). Dla każdego typu dokumentu (faktura, proforma, storno) można zdefiniować wiele serii z różnymi prefiksami. Ekran zawiera tabelę z sortowaniem, paginacją i operacje CRUD przez dialog Angular Material. Chroniony przez AuthGuard (rola: User).

## Wizualizacja układu

```
┌───────────────────────────────────────────────────────────────┐
│ Serie dokumentów                          [+ Dodaj serię]     │
├──┬──────────────┬─────────────┬───────────┬──────────┬────────┤
│☐ │ Typ dokumentu│ Nazwa serii │ Pierwszy  │ Bieżący  │Domyślna│
│  │              │             │ numer     │ numer    │        │
├──┼──────────────┼─────────────┼───────────┼──────────┼────────┤
│☐ │ Factura      │ FV          │ 1         │ 5        │ Tak    │
├──┴──────────────┴─────────────┴───────────┴──────────┴────────┤
│ [Usuń zaznaczone]                             [Paginacja]      │
└───────────────────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/document-series` |
| Wymagana rola/uprawnienie | User (AuthGuard) |
| Punkty wejścia | Klik „Serie dokumentów" w Sidebar |
| Powiązany kod komponentu | `src/app/components/document-series/document-series.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| Modal AddOrEditDocumentSeriesDialog | Klik „Dodaj serię" | Zawsze | User |
| Modal AddOrEditDocumentSeriesDialog (edycja) | Klik „Edytuj" przy wierszu | Zawsze | User |

## Sekcje ekranu

### Filtry

Brak.

### Tabele i listy

| ID tabeli | Nazwa | Link do dokumentu |
|---|---|---|
| TAB-SerieDokumentow-ListaSerii | Lista serii dokumentów | — |

### Kolumny tabeli

| Kolumna | Źródło danych | Opis |
|---|---|---|
| Checkbox (select) | `selection` | Zaznaczanie do operacji batch |
| `documentType` | `IDocumentSeries.documentTypeId` | Typ dokumentu (Factura/Proforma/Storno) |
| `seriesName` | `IDocumentSeries.seriesName` | Prefiks serii (np. `FV`, `PRF`) |
| `firstNumber` | `IDocumentSeries.firstNumber` | Pierwsza liczba w serii |
| `currentNumber` | `IDocumentSeries.currentNumber` | Bieżący licznik |
| `isDefault` | `IDocumentSeries.isDefault` | Czy domyślna seria dla typu |

### Pola

Brak (ekran listowy).

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-SerieDokumentow-DodajSerie | Dodaj serię | [ALG-GEN Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) |
| OP-SerieDokumentow-EdytujSerie | Edytuj (przy wierszu) | [ALG-GEN Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) |
| OP-SerieDokumentow-UsunZaznaczone | Usuń zaznaczone | [ALG-IZO Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) |

### Modale

| ID modalu | Nazwa | Wywołane przez | Link do dokumentu |
|---|---|---|---|
| MODAL-SerieDokumentow-DodajSerie | AddOrEditDocumentSeriesDialog (dodaj) | OP-SerieDokumentow-DodajSerie | `dialog_dodaj_serie/modal.md` |
| MODAL-SerieDokumentow-EdytujSerie | AddOrEditDocumentSeriesDialog (edytuj) | OP-SerieDokumentow-EdytujSerie | `dialog_dodaj_serie/modal.md` |

### Powiadomienia

Brak.

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie (ngOnInit) | [GET /api/DocumentSeries/GetAll](../../../04_api_i_integracje/01_api_frontend/document_series/GET_DocumentSeries_GetAll.md) |
| Usunięcie zaznaczonych | [PUT /api/DocumentSeries/Delete](../../../04_api_i_integracje/01_api_frontend/document_series/PUT_DocumentSeries_Delete.md) (query string) |

## Powiązania

- Powiązane procesy: [pobierz_serie](../../../02_procesy/serie_dokumentow/pobierz_serie/proces.md), [usun_serie](../../../02_procesy/serie_dokumentow/usun_serie/proces.md)
- Powiązane API: [GET /api/DocumentSeries/GetAll](../../../04_api_i_integracje/01_api_frontend/document_series/GET_DocumentSeries_GetAll.md)
- Powiązane UC: Brak

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| OP-SerieDokumentow-DodajSerie | [ALG-GEN Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | Dodanie serii definiuje prefiks (SeriesName) i licznik startowy (CurrentNumber) używane do generowania numeru dokumentu w formacie SeriesName + CurrentNumber.D4 (np. FV0001) |
| OP-SerieDokumentow-EdytujSerie | [ALG-GEN Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | Edycja serii zmienia parametry (prefiks, bieżący numer) wpływające bezpośrednio na format kolejnych generowanych numerów dokumentów |
| Kolumna `seriesName` / `currentNumber` | [ALG-GEN Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | Pola widoczne w tabeli prezentują dane wejściowe algorytmu generowania numeru: prefiks serii i bieżący licznik |
| Domyślne serie FV / PRF / STN | [ALG-INI Inicjalizacja serii dokumentów](../../../03_algorytmy/dedykowane/inicjalizacja_serii_dokumentow.md) | Serie tworzone automatycznie podczas inicjalizacji konta użytkownika — ekran umożliwia ich przegląd i modyfikację |
| OP-SerieDokumentow-UsunZaznaczone | [ALG-IZO Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Usunięcie działa tylko na seriach należących do UserFirm aktualnie zalogowanego użytkownika |

## Powiązania z kodem

- Komponent: `src/app/components/document-series/document-series.component.ts`
- Szablon HTML: `src/app/components/document-series/document-series.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

- `console.log(series)` aktywny w metodzie `getDocumentSeries()`.
- `console.log(selectedIds)` aktywny w metodzie `deleteSelected()`.
- Podwójne wywołanie `selection.clear()` w metodzie `deleteSelected()` — potencjalnie niegroźne, ale sugeruje błąd w logice.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `document_series/document-series.md`. |
