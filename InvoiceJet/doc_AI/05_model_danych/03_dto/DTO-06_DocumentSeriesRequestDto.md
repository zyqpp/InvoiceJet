# DTO: DocumentSeriesRequestDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-06 |
| Plik | `InvoiceJet.Application/DTOs/DocumentSeriesRequestDto.cs` |
| Kierunek | Request + Response (dwukierunkowy) |
| Endpointy | `GET /api/DocumentSeries/GetAll`, `POST /api/DocumentSeries/Add`, `PUT /api/DocumentSeries/Update` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `Id` | `int` | NIE | ID serii (0 przy dodawaniu) |
| `SeriesName` | `string` | NIE | Prefiks serii (np. "FV", "PRF") |
| `CurrentNumber` | `int` | NIE | Bieżący numer counter (min 1) |
| `DocumentTypeId` | `int` | NIE | Typ dokumentu: 1=Faktura, 2=Proforma, 3=Storno |

## Rola w generowaniu numeru dokumentu

`DocumentNumber = SeriesName + CurrentNumber.ToString("D4")`

Po wystawieniu dokumentu `CurrentNumber` jest inkrementowany przez backend.

## Mapowanie AutoMapper

| Kierunek | Profile |
|---|---|
| `DocumentSeriesRequestDto` → `DocumentSeries` | `DocumentSeriesProfile` |
| `DocumentSeries` → `DocumentSeriesRequestDto` | `DocumentSeriesProfile` |

## Przykład JSON

```json
{
  "id": 1,
  "seriesName": "FV",
  "currentNumber": 15,
  "documentTypeId": 1
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
