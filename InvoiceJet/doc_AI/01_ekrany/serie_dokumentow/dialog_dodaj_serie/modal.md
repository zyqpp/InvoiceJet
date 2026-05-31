# AddOrEditDocumentSeriesDialogComponent — Dialog dodaj/edytuj serię dokumentów

| Pole | Wartość |
|---|---|
| ID dokumentu | MODAL-SerieDokumentow-DodajSerie |
| Typ dokumentu | modal |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Modal Angular Material do dodawania i edycji serii numeracji dokumentów. Otwierany z ekranu listy serii przez `MatDialog.open()`. Dane serii przekazywane przez `MAT_DIALOG_DATA`. Seria definiuje prefiks (`seriesName`) i bieżący licznik (`currentNumber`) — backend generuje numer dokumentu jako `SeriesName + CurrentNumber.ToString("D4")`. Uwaga: anomalia race condition przy równoległym wystawianiu dokumentów.

## Charakterystyka modalu

| Atrybut | Wartość |
|---|---|
| ID modalu | MODAL-SerieDokumentow-DodajSerie |
| Nazwa / tytuł w UI | Dodaj serię / Edytuj serię |
| Wywołany przez operację | OP-SerieDokumentow-DodajSerie, OP-SerieDokumentow-EdytujSerie |
| Ekran nadrzędny | `../ekran.md` (DocumentSeriesComponent) |
| Typ modalu | formularz |
| Zamknięcie przez Escape | tak |
| Zamknięcie przez klik tła | tak |

## Wizualizacja układu

```
┌──────────────────────────────────────────┐
│ Dodaj serię / Edytuj serię           [X] │
├──────────────────────────────────────────┤
│ Nazwa serii (prefiks): [_________________]│
│ Bieżący numer:         [_________________]│
│ Typ dokumentu:         [Factura ▼]       │
├──────────────────────────────────────────┤
│ [Anuluj]                    [Zapisz]     │
└──────────────────────────────────────────┘
```

## Pola modalu

| ID pola | Nazwa w UI | Typ | Wymagalność | Link do dokumentu |
|---|---|---|---|---|
| POLE-DodajSerie-seriesName | Nazwa serii (prefiks) | mat-form-field (input) | wymagane | — |
| POLE-DodajSerie-currentNumber | Bieżący numer | mat-form-field (input number) | wymagane, min=1 | — |
| POLE-DodajSerie-documentTypeId | Typ dokumentu | mat-select | wymagane | — |

## Dane wejściowe (MAT_DIALOG_DATA)

| Pole | Typ | Opis |
|---|---|---|
| `documentSeries` | `IDocumentSeries \| null` | `null` = tryb dodawania; obiekt = tryb edycji |

## Operacje modalu

| Przycisk | Akcja | Wywołuje operację | Zamyka modal |
|---|---|---|---|
| Zapisz (tryb dodaj) | Wywołuje `POST /api/DocumentSeries/Add` | Tak | tak (z wynikiem) |
| Zapisz (tryb edytuj) | Wywołuje `PUT /api/DocumentSeries/Update` | Tak | tak (z wynikiem) |
| Anuluj | Zamknięcie bez zmian | Nie | tak |

## Przepływ

### Tryb dodawania
1. Formularz pusty; `currentNumber` domyślnie `1`
2. Submit → `POST /api/DocumentSeries/Add`
3. Dialog zamknięty z wynikiem → lista serii odświeżona

### Tryb edycji
1. Formularz wypełniony danymi serii
2. Submit → `PUT /api/DocumentSeries/Update`
3. Dialog zamknięty z wynikiem → lista serii odświeżona

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
- `SeriesName=FV`, `CurrentNumber=5` → `FV0005`
- `SeriesName=PRF`, `CurrentNumber=12` → `PRF0012`

## Typy dokumentów (documentTypeId)

| ID | Nazwa |
|---|---|
| `1` | Factura (faktura zwykła) |
| `2` | Factura Proforma (proforma) |
| `3` | Factura Storno (storno) |

## Możliwe wyniki

| Wynik | Warunki | Komunikat | Następna akcja |
|---|---|---|---|
| Sukces dodania | API zwróci 200/201 | Brak komunikatu | Modal zamknięty; lista serii odświeżona |
| Sukces edycji | API zwróci 200 | Brak komunikatu | Modal zamknięty; lista serii odświeżona |
| Błąd API | API zwróci 400/500 | Brak komunikatu (anomalia) | Modal pozostaje otwarty |
| Anulowanie | Użytkownik klika Anuluj lub Escape | Brak | Modal zamknięty, brak zmian |

## Powiązania z kodem

- Komponent modalu: `src/app/components/document-series/add-or-edit-document-series-dialog/add-or-edit-document-series-dialog.component.ts`
- Szablon HTML: `src/app/components/document-series/add-or-edit-document-series-dialog/add-or-edit-document-series-dialog.component.html`

## Wątpliwości i braki

- DS-01: Brak mechanizmu blokującego (lock/transaction) przy inkrementacji `CurrentNumber` — race condition przy równoległym wystawianiu dokumentów przez wielu użytkowników w tej samej firmie jest możliwy. Może to prowadzić do duplikacji numerów dokumentów.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `document_series/add-or-edit-document-series-dialog.md`. |
