# Algorytm: Generowanie numeru dokumentu

| Atrybut | Wartość |
|---|---|
| ID | ALG-02 |
| Nazwa | Document Number Generation |
| Kategoria | Logika biznesowa |
| Pliki | `DocumentService.cs › AddDocument()`, `DocumentSeries` (encja) |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Wygenerowanie unikalnego numeru dokumentu w formacie `<SeriesName><Number:D4>` i automatyczne inkrementowanie licznika serii.

## Schemat

```
DocumentNumber = SeriesName + CurrentNumber.ToString("D4")
```

## Przykłady

| SeriesName | CurrentNumber | DocumentNumber |
|---|---|---|
| `FV` | 1 | `FV0001` |
| `FV` | 15 | `FV0015` |
| `FV` | 999 | `FV0999` |
| `FV` | 1000 | `FV1000` |
| `PRF` | 3 | `PRF0003` |
| `STORNO` | 1 | `STORNO0001` |

## Kod źródłowy

```csharp
// DocumentService › AddDocument
var documentSeries = await _unitOfWork.DocumentSeries.GetByIdAsync(
    documentRequestDto.DocumentSeries!.Id
);

string documentNumber = documentRequestDto.DocumentSeries?.SeriesName +
                        documentRequestDto.DocumentSeries?.CurrentNumber.ToString("D4");

var document = _mapper.Map<Document>(documentRequestDto);
document.DocumentNumber = documentNumber;
// ... zapis dokumentu ...

// Inkrementacja serii po zapisaniu dokumentu
documentSeries.CurrentNumber++;
await _unitOfWork.DocumentSeries.UpdateAsync(documentSeries);
await _unitOfWork.CompleteAsync(); // drugi CompleteAsync!
```

## Sekwencja operacji

```
1. Pobierz DocumentSeries z DB (GetByIdAsync)
2. Oblicz DocumentNumber = SeriesName + CurrentNumber.D4
3. Utwórz Document z DocumentNumber
4. Zapisz Document → CompleteAsync() (1)
5. Inkrementuj DocumentSeries.CurrentNumber++
6. Zapisz DocumentSeries → CompleteAsync() (2)
```

## Anomalie

| # | Anomalia |
|---|---|
| ALG02-01 | **Race condition:** Brak pesymistycznej blokady (`SELECT FOR UPDATE`) ani optymistycznej (ETag/RowVersion) na `CurrentNumber` — możliwe duplikaty numerów przy równoległych żądaniach |
| ALG02-02 | Dwa osobne `CompleteAsync()` — inkrementacja serii w oddzielnej transakcji od zapisu dokumentu; możliwy stan: dokument zapisany, numer nie inkrementowany (lub odwrotnie) |
| ALG02-03 | `CurrentNumber` pobierany z obiektu `DocumentSeries` przekazanego w żądaniu z frontendu — frontend może przekazać zmanipulowany numer; brak re-pobrania aktualnej wartości z DB przed generowaniem numeru |

## Format D4

`ToString("D4")` = minimalna szerokość 4 cyfry, z zerami wiodącymi:
- `1` → `0001`
- `99` → `0099`
- `1000` → `1000` (bez obcinania)
- `9999` → `9999`
- `10000` → `10000` (przekracza 4 cyfry — format nie obcina!)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
