# ManageDocumentSeries — Dane, modele i mapowania

## 1. DTO

### `DocumentSeriesDto` (wejście: AddDocumentSeries, UpdateDocumentSeries; wyjście: GetAllDocumentSeriesForUserId)

Źródło: `DocumentSeriesDto.cs`

| Pole | Typ | Wymagane | Opis / źródło wartości |
|---|---|---|---|
| `Id` | `int` | tak (Update/Delete), nie (Add) | Identyfikator serii; przy Add nadawany przez DB |
| `SeriesName` | `string` | tak | Nazwa serii (np. `"2026"`); inicjalizator `string.Empty` |
| `FirstNumber` | `int` | tak | Numer pierwszego dokumentu w serii |
| `CurrentNumber` | `int` | tak | Aktualny numer serii (inkrementowany przy wystawieniu faktury) |
| `IsDefault` | `bool` | nie | Czy seria jest domyślna dla danego typu dokumentu |
| `DocumentTypeId` | `int?` | nie | ID typu dokumentu (nullable); może być przesłany bezpośrednio |
| `DocumentType` | `DocumentType?` | nie | Nawigacja — obiekt encji `DocumentType` osadzony w DTO; serwis pobiera z niego `DocumentType.Id` |

> [UWAGA: `DocumentSeriesDto` zawiera pole `DocumentType` o typie `InvoiceJet.Domain.Models.DocumentType` — bezpośrednia encja domenowa zamiast dedykowanego DTO. Narusza separację warstw (DTO powinno używać uproszczonego DTO, nie encji). Kotwica: `DocumentSeriesDto.cs` — `public DocumentType? DocumentType { get; set; }`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

> Atrybuty walidacyjne DTO: brak atrybutów z przestrzeni `System.ComponentModel.DataAnnotations`. Cała walidacja realizowana w `DocumentSeriesService` lub przez controller's try/catch.

---

## 2. Encje i kolumny

### Encja `DocumentSeries` → tabela `DocumentSeries`

Kotwica: `DocumentSeries.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("InvoiceJet.Domain.Models.DocumentSeries", b => ...)`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | nie | PK | — |
| `SeriesName` | `nvarchar(max)` | nie | — | — |
| `FirstNumber` | `int` | nie | — | — |
| `CurrentNumber` | `int` | nie | — | — |
| `IsDefault` | `bit` | nie | — | — |
| `DocumentTypeId` | `int` | tak | FK→`DocumentType` | tak |
| `UserFirmId` | `int` | tak | FK→`UserFirm` | tak |

Uwagi do schematu:
- `UserFirmId` jest nullable — seria może teoretycznie istnieć bez przypisania do firmy (choć serwis zawsze ustawia `UserFirmId` przy tworzeniu).
- `DocumentTypeId` nullable — seria może być bez przypisanego typu (choć serwis pobiera go z `documentSeriesDto.DocumentType!.Id` — null ref przy braku `DocumentType` w DTO).
- Brak indeksu unikalnego: wiele serii o tej samej `SeriesName` może istnieć w obrębie tej samej firmy.

> Pełne definicje: `../../SLOWNIK_DANYCH.md#DocumentSeries`.

### Encja `DocumentType` → tabela `DocumentType` (lookup — seed)

Kotwica: `DocumentType.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("InvoiceJet.Domain.Models.DocumentType", b => ...)`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | nie | PK | — |
| `Name` | `nvarchar(max)` | nie | — | — |

Wartości seed (z `DbSeeder.SeedDocumentTypes`): `Id=1 → "Factura"`, `Id=2 → "Factura Proforma"`, `Id=3 → "Factura Storno"`.

> Pełne definicje: `../../SLOWNIK_DANYCH.md#DocumentType`.

---

## 3. Relacje i kaskady

| Z encji | Pole FK | Do encji | Kierunek | Kaskada |
|---|---|---|---|---|
| `DocumentSeries` | `DocumentTypeId` | `DocumentType` | N..1 | brak jawnej kaskady (nullable FK) |
| `DocumentSeries` | `UserFirmId` | `UserFirm` | N..1 | brak jawnej kaskady (nullable FK); `WithMany("DocumentSeries")` |

Uwaga: usunięcie `UserFirm` ani `DocumentType` nie kaskaduje automatycznie usunięcia `DocumentSeries` — brak `OnDelete(DeleteBehavior.Cascade)` dla tych relacji w snapshosie.

> [UWAGA: `DeleteDocumentSeries` nie sprawdza, czy usuwana seria jest powiązana z istniejącymi dokumentami (`Document.DocumentSeriesId` — jeśli taka relacja istnieje). Brak WAL analogicznego do WAL-04 z P-10 (BankAccountAssociatedWithDocumentsException). — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 4. Mapowania AutoMapper

Źródło: `DocumentSeriesProfile.cs › DocumentSeriesProfile`

```csharp
public class DocumentSeriesProfile : Profile
{
    public DocumentSeriesProfile()
    {
        CreateMap<DocumentSeries, DocumentSeriesDto>();

        CreateMap<DocumentSeriesDto, DocumentSeries>()
            .ForMember(dest => dest.DocumentTypeId, opt => opt.MapFrom(src => src.DocumentType!.Id))
            .ForMember(dest => dest.DocumentType, opt => opt.Ignore());
    }
}
```

| Źródło | Cel | Profil | Uwagi |
|---|---|---|---|
| `DocumentSeries` | `DocumentSeriesDto` | `DocumentSeriesProfile` | Wszystkie pola 1:1; `DocumentType` mapowane przez nawigację EF (Include w repozytorium) |
| `DocumentSeriesDto` | `DocumentSeries` | `DocumentSeriesProfile` | `DocumentTypeId` mapowany z `src.DocumentType!.Id`; `DocumentType` navigation ignorowana (`opt.Ignore()`); `UserFirmId` **nie jest** w DTO — ustawiany ręcznie po mapowaniu |

> Uwaga do `AddDocumentSeries` i `UpdateDocumentSeries`: AutoMapper mapuje `DocumentTypeId = src.DocumentType!.Id`, ale serwis **dodatkowo ręcznie** ustawia `documentSeries.DocumentTypeId = documentSeriesDto.DocumentType!.Id` — zduplikowane przypisanie. Kotwica: `DocumentSeriesService.cs › DocumentSeriesService.AddDocumentSeries` (linia `documentSeries.DocumentTypeId = documentSeriesDto.DocumentType!.Id`) i `DocumentSeriesService.UpdateDocumentSeries`.

> [UWAGA: Ręczne `documentSeries.DocumentTypeId = documentSeriesDto.DocumentType!.Id` w serwisie jest nadmiarowe względem mapowania AutoMapper (`MapFrom(src => src.DocumentType!.Id)`). Oba przypisania dają ten sam wynik, ale drugie jest zbędne i potencjalnie mylące. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 5. Zapytania (LINQ/SQL)

### Query 1: Pobranie serii aktywnej firmy użytkownika (`GetAllDocumentSeriesForUserId`)

Kotwica: `DocumentSeriesRepository.cs › DocumentSeriesRepository.GetAllDocumentSeriesForActiveUserFirm`

```csharp
return _dbSet
    .Include(ds => ds.UserFirm)
    .ThenInclude(uf => uf!.User)
    .Include(ds => ds.DocumentType)
    .Where(ds => ds.UserFirm!.UserId.Equals(userId) && ds.UserFirm.User.ActiveUserFirmId == ds.UserFirmId)
    .ToListAsync();
```

Semantyka: pobiera serie z Include `UserFirm+User` (do filtrowania po aktywnej firmie) i Include `DocumentType` (do wypełnienia pola nawigacji w DTO). Filtruje per aktywna firma użytkownika.

### Query 2: Pobranie serii do edycji (`UpdateDocumentSeries`)

Kotwica: `DocumentSeriesService.cs › DocumentSeriesService.UpdateDocumentSeries`

```csharp
var documentSeries = await _unitOfWork.DocumentSeries.Query()
    .FirstOrDefaultAsync(ds => ds.Id == documentSeriesDto.Id);
```

Semantyka: pobiera jedną serię po `Id`. Brak Include — tracked encja bez nawigacji.

### Query 3: Pobranie serii do usunięcia (`DeleteDocumentSeries`)

Kotwica: `DocumentSeriesService.cs › DocumentSeriesService.DeleteDocumentSeries`

```csharp
var documentSeries = await _unitOfWork.DocumentSeries.Query()
    .Where(d => documentSeriesIds.Contains(d.Id))
    .ToListAsync();
```

Semantyka: pobiera listę serii, których `Id` zawiera się w tablicy `documentSeriesIds`. Jeśli żaden ID nie istnieje — zwraca pustą listę (brak wyjątku). `RemoveRangeAsync` na pustej liście — brak DELETE, `CompleteAsync` bez zmian.

---

## 6. Użyte enumy i lookupy

| Element | Rodzaj | Plik | Wartości |
|---|---|---|---|
| `DocumentType` (seed) | tabela słownikowa | `InvoiceJet.Domain/Models/DocumentType.cs` + `DbSeeder.cs` | `Id=1 → "Factura"`, `Id=2 → "Factura Proforma"`, `Id=3 → "Factura Storno"` |

> Wartości `DocumentType` są seedowane przy starcie przez `DbSeeder.SeedDocumentTypes`. Pełna definicja: `../../SLOWNIK_DANYCH.md#DocumentType`.
