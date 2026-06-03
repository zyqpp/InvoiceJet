# Dialog: Dodaj/Edytuj serię dokumentów (Add/Edit Document Series Dialog)

| Atrybut | Wartość |
|---|---|
| ID | DIALOG-04 |
| Komponent | `AddOrEditDocumentSeriesDialogComponent` |
| Plik | `src/app/components/document-series/add-or-edit-document-series-dialog/add-or-edit-document-series-dialog.component.ts` |
| Otwierany z | EKRAN-08 (lista serii dokumentów) |
| Typ | `MatDialog` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Modal Angular Material do dodawania i edycji serii numeracji dokumentów. Dane serii przekazywane przez `MAT_DIALOG_DATA`.

## Pola formularza

| Pole | Kontrolka | Walidacja | Opis |
|---|---|---|---|
| `seriesName` | `mat-form-field` | required | Prefiks serii (np. "FV", "PRF", "STORNO") |
| `currentNumber` | `mat-form-field` | required, min=1 | Bieżący numer (counter) |
| `documentTypeId` | `mat-select` | required | Typ dokumentu (Factura=1, Proforma=2, Storno=3) |

## Dane wejściowe (MAT_DIALOG_DATA)

| Pole | Typ | Opis |
|---|---|---|
| `documentSeries` | `IDocumentSeries \| null` | `null` = tryb dodawania; obiekt = tryb edycji |

## Przepływ

### Tryb dodawania
1. Formularz pusty, domyślnie `currentNumber = 1`
2. Submit → `POST /api/DocumentSeries/Add`
3. Dialog zamknięty z wynikiem → lista odświeżona

### Tryb edycji
1. Formularz wypełniony danymi serii
2. Submit → `PUT /api/DocumentSeries/Update`
3. Dialog zamknięty z wynikiem → lista odświeżona

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Dodanie serii | `POST /api/DocumentSeries/Add` |
| Edycja serii | `PUT /api/DocumentSeries/Update` |

## Format numeru dokumentu

Numer dokumentu generowany przez backend jako:
```
SeriesName + CurrentNumber.ToString("D4")
```
Przykłady:
- SeriesName=`FV`, CurrentNumber=`5` → `FV0005`
- SeriesName=`PRF`, CurrentNumber=`12` → `PRF0012`

## Anomalie

| # | Anomalia |
|---|---|
| DS-01 | Brak mechanizmu blokującego (lock/transaction) przy inkrementacji `CurrentNumber` — race condition przy równoległym wystawianiu dokumentów możliwy |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
