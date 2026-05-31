# AutoMapper Profile: DocumentSeriesProfile

| Atrybut | Wartość |
|---|---|
| ID | AM-05 |
| Plik | `InvoiceJet.Application/MappingProfiles/DocumentSeriesProfile.cs` |
| Dotyczy | Serie numeracji dokumentów |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Mapowania

### DocumentSeriesRequestDto → DocumentSeries

```csharp
CreateMap<DocumentSeriesRequestDto, DocumentSeries>();
```

| Pole DTO | Pole Encji |
|---|---|
| `Id` | `DocumentSeries.Id` |
| `SeriesName` | `DocumentSeries.SeriesName` |
| `CurrentNumber` | `DocumentSeries.CurrentNumber` |
| `DocumentTypeId` | `DocumentSeries.DocumentTypeId` |

`UserFirmId` nie jest w DTO — ustawiane ręcznie po mapowaniu.

### DocumentSeries → DocumentSeriesRequestDto

```csharp
CreateMap<DocumentSeries, DocumentSeriesRequestDto>();
```

## Użycie w AddDocument

W procesie tworzenia dokumentu `DocumentSeries` jest przekazywany z frontendu jako zagnieżdżony obiekt w `DocumentRequestDto`. Backend pobiera aktualny numer z DB, nie z DTO (ale praktycznie używa `CurrentNumber` z DTO — anomalia!).

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
