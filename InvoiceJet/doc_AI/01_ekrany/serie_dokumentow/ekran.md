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
| OP-SerieDokumentow-DodajSerie | Dodaj serię | — |
| OP-SerieDokumentow-EdytujSerie | Edytuj (przy wierszu) | — |
| OP-SerieDokumentow-UsunZaznaczone | Usuń zaznaczone | — |

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
