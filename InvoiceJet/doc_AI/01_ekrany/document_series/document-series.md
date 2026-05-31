# Ekran: Serie dokumentów (Document Series)

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-08 |
| Trasa | `/dashboard/document-series` |
| Komponent | `DocumentSeriesComponent` |
| Plik | `src/app/components/document-series/document-series.component.ts` |
| AuthGuard | TAK |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Lista serii dokumentów z autonumeracją. Dla każdego typu dokumentu można zdefiniować prefiks i pierwszą liczbę.

## Kolumny tabeli

`select`, `documentType`, `seriesName`, `firstNumber`, `currentNumber`, `isDefault`

## Dialogi

| Dialog | Cel |
|---|---|
| `AddOrEditDocumentSeriesDialogComponent` | Dodanie / edycja serii |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie (ngOnInit) | `GET /api/DocumentSeries/GetAllDocumentSeriesForUserId` |
| Usunięcie zaznaczonych | `PUT /api/DocumentSeries/DeleteDocumentSeries?documentSeriesIds=...` (query string) |

## Anomalie

- `console.log(series)` w `getDocumentSeries()`
- `console.log(selectedIds)` w `deleteSelected()`
- Podwójne `selection.clear()` w `deleteSelected()`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
