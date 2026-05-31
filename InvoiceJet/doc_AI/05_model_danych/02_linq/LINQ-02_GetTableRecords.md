# LINQ: GetTableRecords (lista dokumentów)

| Atrybut | Wartość |
|---|---|
| ID | LINQ-02 |
| Serwis | `DocumentService.GetDocumentTableRecords()` |
| Endpoint | `GET /api/Document/GetTableRecords/{documentTypeId}` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Pobranie listy dokumentów w formacie tabelarycznym — tylko wybrane kolumny, bez zagnieżdżonych obiektów.

## Zapytanie LINQ (szacowane)

```csharp
var documents = await _context.Documents
    .Include(d => d.Client)           // Potrzebne dla ClientName
    .Include(d => d.DocumentStatus)   // Potrzebne dla StatusName
    .Where(d => d.UserFirmId == userFirmId
             && d.DocumentTypeId == documentTypeId)
    .OrderByDescending(d => d.IssueDate)
    .ToListAsync();
```

## Filtrowanie

| Warunek | Pole |
|---|---|
| Izolacja danych | `d.UserFirmId == userFirmId` |
| Typ dokumentu | `d.DocumentTypeId == documentTypeId` |

## Mapowanie (DocumentProfile)

```csharp
CreateMap<Document, DocumentTableRecordDto>()
    .ForMember(dest => dest.ClientName,
        opt => opt.MapFrom(src => src.Client!.Name))
    .ForMember(dest => dest.TotalValue,
        opt => opt.MapFrom(src => src.TotalPrice));
```

## Anomalie

| # | Anomalia |
|---|---|
| LQ02-01 | Brak paginacji — zwraca wszystkie dokumenty naraz; może być wolne przy dużej liczbie |
| LQ02-02 | Brak sortowania lub domyślne sortowanie nieokreślone — kolejność może być niespójna |
| LQ02-03 | `d.Client!.Name` — ryzyko NullReferenceException jeśli dokument nie ma klienta (nullable FK) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
