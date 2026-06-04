# ManageDocumentSeries — Logika aplikacyjna

Proces `P-11` obsługuje cztery endpointy CRUD dla zasobu `DocumentSeries`. Każdy ma osobną sekcję.

---

## Endpoint A — `GET /api/DocumentSeries/GetAllDocumentSeriesForUserId`

### 0. Algorytm w skrócie

1. Kontroler odbiera GET bez parametrów, wywołuje `_documentSeriesService.GetAllDocumentSeriesForUserId()`.
2. Serwis pobiera `userFirmId` → jeśli null → zwraca pustą listę (bez wyjątku).
3. Serwis wywołuje `DocumentSeriesRepository.GetAllDocumentSeriesForActiveUserFirm(userId)` z Include `DocumentType`.
4. AutoMapper mapuje `List<DocumentSeries>` → `List<DocumentSeriesDto>`.
5. Kontroler zwraca `200 OK` z listą DTO.

### 1. Wejście do procesu

Kotwica: `DocumentSeriesController.cs › DocumentSeriesController.GetAllDocumentSeriesForUserId`

```csharp
[HttpGet("GetAllDocumentSeriesForUserId")]
public async Task<ActionResult<DocumentSeriesDto>> GetAllDocumentSeriesForUserId()
{
    var bankAccountDto = await _documentSeriesService.GetAllDocumentSeriesForUserId();
    return Ok(bankAccountDto);
}
```

> Uwaga: lokalna zmienna nazywa się `bankAccountDto` (copy-paste artifact) — faktycznie zawiera `List<DocumentSeriesDto>`.

### 2. Walidacje (faza wejściowa)

> Wymiar nie dotyczy tego endpointu. `GetAllDocumentSeriesForUserId`: jeśli `userFirmId == null` (brak aktywnej firmy) → serwis zwraca `new List<DocumentSeriesDto>()` — brak wyjątku, brak `400`. Kotwica: `DocumentSeriesService.cs › DocumentSeriesService.GetAllDocumentSeriesForUserId`:

```csharp
var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
if (!userFirmId.HasValue)
{
    return new List<DocumentSeriesDto>();
}
```

### 3. Logika biznesowa

Kotwica: `DocumentSeriesService.cs › DocumentSeriesService.GetAllDocumentSeriesForUserId`

**Krok 1:** `GetUserFirmIdAsync(userId)` — sprawdzenie istnienia aktywnej firmy. Jeśli brak → pusta lista.

**Krok 2:** `DocumentSeriesRepository.GetAllDocumentSeriesForActiveUserFirm(userId)` — pobiera serie z Include `DocumentType`. Kotwica: `DocumentSeriesRepository.cs › DocumentSeriesRepository.GetAllDocumentSeriesForActiveUserFirm`:

```csharp
return _dbSet
    .Include(ds => ds.UserFirm)
    .ThenInclude(uf => uf!.User)
    .Include(ds => ds.DocumentType)
    .Where(ds => ds.UserFirm!.UserId.Equals(userId) && ds.UserFirm.User.ActiveUserFirmId == ds.UserFirmId)
    .ToListAsync();
```

**Krok 3:** `_mapper.Map<List<DocumentSeries>, List<DocumentSeriesDto>>(documentSeries)`.

### 4. Zapisy do bazy i transakcje

> Wymiar nie dotyczy. Endpoint read-only — brak zapisów, brak `CompleteAsync()`.

### 5. Odpowiedź

HTTP `200 OK`. Ciało: `List<DocumentSeriesDto>` z zagnieżdżonym obiektem `DocumentType` (encja).

---

## Endpoint B — `POST /api/DocumentSeries/AddDocumentSeries`

### 0. Algorytm w skrócie

1. Kontroler odbiera `DocumentSeriesDto` z body `[FromBody]`, owija wywołanie w własny `try/catch`.
2. Serwis pobiera `userFirmId` → null → `UserHasNoAssociatedFirmException` → wychwycony przez kontroler → **`400 Bad Request`** z `ex.Message`.
3. Serwis mapuje DTO → `DocumentSeries` przez AutoMapper.
4. Serwis ręcznie ustawia `DocumentTypeId` i `UserFirmId`.
5. `AddAsync(documentSeries)` + `CompleteAsync()`.
6. Kontroler zwraca `200 OK` (puste ciało).

### 1. Wejście do procesu

Kotwica: `DocumentSeriesController.cs › DocumentSeriesController.AddDocumentSeries`

```csharp
[HttpPost("AddDocumentSeries")]
public async Task<ActionResult> AddDocumentSeries([FromBody] DocumentSeriesDto documentSeriesDto)
{
    try
    {
        await _documentSeriesService.AddDocumentSeries(documentSeriesDto);
        return Ok();
    }
    catch (Exception ex)
    {
        return BadRequest(ex.Message);
    }
}
```

> **KLUCZOWE:** Kontroler ma własny `try/catch (Exception ex)` → przechwytuje WSZYSTKIE wyjątki z serwisu i zwraca `BadRequest(ex.Message)` (`400`). Wyjątki z `AddDocumentSeries` **nie trafiają do `ExceptionMiddleware`**.

### 2. Walidacje (faza wejściowa)

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Użytkownik ma aktywną firmę | `DocumentSeriesService.cs › DocumentSeriesService.AddDocumentSeries` | `UserHasNoAssociatedFirmException` → przechwycony przez `catch (Exception ex)` w kontrolerze → `400 Bad Request(ex.Message)` |

```csharp
var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
if (!userFirmId.HasValue)
{
    throw new UserHasNoAssociatedFirmException();
}
```

### 3. Logika biznesowa

Kotwica: `DocumentSeriesService.cs › DocumentSeriesService.AddDocumentSeries`

**Krok 1:** AutoMapper: `_mapper.Map<DocumentSeries>(documentSeriesDto)` — mapuje pola DTO na nową encję; `DocumentTypeId` ustawiany z `src.DocumentType!.Id`; `DocumentType` navigation ignorowana.

**Krok 2:** Ręczne przypisanie identyfikatorów:
```csharp
documentSeries.UserFirmId = userFirmId.Value;
documentSeries.DocumentTypeId = documentSeriesDto.DocumentType!.Id; // redundantne — AutoMapper już to zrobił
```

### Tabela: pole encji `DocumentSeries` → źródło (AddDocumentSeries)

| Pole encji `DocumentSeries` | Źródło |
|---|---|
| `Id` | generowany przez DB (IDENTITY) po `CompleteAsync()` |
| `SeriesName` | `documentSeriesDto.SeriesName` |
| `FirstNumber` | `documentSeriesDto.FirstNumber` |
| `CurrentNumber` | `documentSeriesDto.CurrentNumber` |
| `IsDefault` | `documentSeriesDto.IsDefault` |
| `DocumentTypeId` | `documentSeriesDto.DocumentType!.Id` (AutoMapper + ręczne przypisanie) |
| `DocumentType` | ignorowane przez AutoMapper; null po mapowaniu |
| `UserFirmId` | `userFirmId.Value` — wynik `Users.GetUserFirmIdAsync(userId)` |

### 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | `CompleteAsync()` |
|---|---|---|---|
| 1 | `AddAsync(documentSeries)` | `GenericRepository.AddAsync` | nie |
| 2 | `CompleteAsync()` | `UnitOfWork.CompleteAsync()` | tak — nadaje `documentSeries.Id` |

### 5. Odpowiedź

HTTP `200 OK`. Puste ciało (`return Ok()` — bez DTO, bez nadanego ID).

### 6. Uwagi techniczne

- [UWAGA: `AddDocumentSeries` zwraca `200 OK` z pustym ciałem — klient nie otrzymuje `Id` nowo utworzonej serii. Aby pobrać ID trzeba wywołać `GetAllDocumentSeriesForUserId`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Własny `try/catch (Exception ex)` w kontrolerze przechwytuje WSZYSTKIE wyjątki z serwisu (w tym `UserHasNoAssociatedFirmException`) i zwraca `400 BadRequest(ex.Message)` zamiast delegowania do `ExceptionMiddleware`. Niespójność z innymi kontrolerami (które nie mają własnego try/catch). — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Ręczne `documentSeries.DocumentTypeId = documentSeriesDto.DocumentType!.Id` jest redundantne — AutoMapper już mapuje to pole przez `MapFrom(src => src.DocumentType!.Id)`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## Endpoint C — `PUT /api/DocumentSeries/UpdateDocumentSeries`

### 0. Algorytm w skrócie

1. Kontroler odbiera `DocumentSeriesDto` z body `[FromBody]`, wywołuje `_documentSeriesService.UpdateDocumentSeries(documentSeriesDto)`.
2. Serwis pobiera serię z DB po `documentSeriesDto.Id` → brak → `Exception("Document Series not found")` → trafia do `ExceptionMiddleware` → **`500 ⚠️`**.
3. AutoMapper mapuje DTO na tracked encję.
4. Serwis ręcznie ustawia `DocumentTypeId`.
5. `UpdateAsync(documentSeries)` + `CompleteAsync()`.
6. Kontroler zwraca `200 OK` (puste ciało).

### 1. Wejście do procesu

Kotwica: `DocumentSeriesController.cs › DocumentSeriesController.UpdateDocumentSeries`

```csharp
[HttpPut("UpdateDocumentSeries")]
public async Task<ActionResult> UpdateDocumentSeries([FromBody] DocumentSeriesDto documentSeriesDto)
{
    await _documentSeriesService.UpdateDocumentSeries(documentSeriesDto);
    return Ok();
}
```

Brak try/catch — wyjątki z serwisu trafiają do `ExceptionMiddleware`.

### 2. Walidacje (faza wejściowa)

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Seria o danym `Id` istnieje w DB | `DocumentSeriesService.cs › DocumentSeriesService.UpdateDocumentSeries` | `Exception("Document Series not found")` (WAL-02 → **500 ⚠️**) |

```csharp
var documentSeries = await _unitOfWork.DocumentSeries.Query()
    .FirstOrDefaultAsync(ds => ds.Id == documentSeriesDto.Id);

if (documentSeries == null)
{
    throw new Exception("Document Series not found");
}
```

### 3. Logika biznesowa

Kotwica: `DocumentSeriesService.cs › DocumentSeriesService.UpdateDocumentSeries`

**Krok 1:** `_mapper.Map(documentSeriesDto, documentSeries)` — mapuje pola DTO na tracked encję EF Core.

**Krok 2:** Ręczne przypisanie `DocumentTypeId`:
```csharp
documentSeries.DocumentTypeId = documentSeriesDto.DocumentType!.Id;
```

### Tabela: pole encji `DocumentSeries` → źródło (UpdateDocumentSeries)

| Pole encji `DocumentSeries` | Źródło |
|---|---|
| `Id` | bez zmian (tracked przez EF Core) |
| `SeriesName` | `documentSeriesDto.SeriesName` |
| `FirstNumber` | `documentSeriesDto.FirstNumber` |
| `CurrentNumber` | `documentSeriesDto.CurrentNumber` |
| `IsDefault` | `documentSeriesDto.IsDefault` |
| `DocumentTypeId` | `documentSeriesDto.DocumentType!.Id` (AutoMapper + ręczne przypisanie) |
| `UserFirmId` | bez zmian (pole nie istnieje w `DocumentSeriesDto` jako FK) |

### 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | `CompleteAsync()` |
|---|---|---|---|
| 1 | `UpdateAsync(documentSeries)` | `GenericRepository.UpdateAsync` | nie |
| 2 | `CompleteAsync()` | `UnitOfWork.CompleteAsync()` | tak |

### 5. Odpowiedź

HTTP `200 OK`. Puste ciało.

### 6. Uwagi techniczne

- [UWAGA: Generyczny `Exception("Document Series not found")` (WAL-02) trafia do catch-all w `ExceptionMiddleware` → `500 Internal Server Error` zamiast `400`/`404`. Brak dedykowanego `DocumentSeriesNotFoundException`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `UpdateDocumentSeries` nie weryfikuje, czy edytowana seria należy do aktywnej firmy bieżącego użytkownika. `Query().FirstOrDefaultAsync(ds => ds.Id == documentSeriesDto.Id)` pobiera każdą serię z DB po `Id` — możliwa edycja serii innego użytkownika. Brak ownership check. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## Endpoint D — `PUT /api/DocumentSeries/DeleteDocumentSeries`

### 0. Algorytm w skrócie

1. Kontroler odbiera `int[] documentSeriesIds` z **query string** (brak `[FromBody]`), wywołuje `_documentSeriesService.DeleteDocumentSeries(documentSeriesIds)`.
2. Serwis pobiera z DB listę serii, których `Id` zawiera się w tablicy — nieistniejące IDs są **po cichu ignorowane** (brak wyjątku).
3. `RemoveRangeAsync(documentSeries)` + `CompleteAsync()`.
4. Kontroler zwraca `200 OK` (puste ciało).

### 1. Wejście do procesu

Kotwica: `DocumentSeriesController.cs › DocumentSeriesController.DeleteDocumentSeries`

```csharp
[HttpPut("DeleteDocumentSeries")]
public async Task<ActionResult> DeleteDocumentSeries(int[] documentSeriesIds)
{
    await _documentSeriesService.DeleteDocumentSeries(documentSeriesIds);
    return Ok();
}
```

> **Brak `[FromBody]`** — parametr `int[] documentSeriesIds` jest bindowany z **query string** (np. `?documentSeriesIds=1&documentSeriesIds=2`). Różni się od `BankAccountController.DeleteUserFirmBankAccounts`, który używa `[FromBody]`.

### 2. Walidacje (faza wejściowa)

> Wymiar nie dotyczy tego endpointu. `DeleteDocumentSeries` nie ma żadnych walidacji: nieistniejące IDs są po cichu ignorowane (brak wyjątku). Kotwica: `DocumentSeriesService.cs › DocumentSeriesService.DeleteDocumentSeries`:

```csharp
var documentSeries = await _unitOfWork.DocumentSeries.Query()
    .Where(d => documentSeriesIds.Contains(d.Id))
    .ToListAsync();

await _unitOfWork.DocumentSeries.RemoveRangeAsync(documentSeries);
await _unitOfWork.CompleteAsync();
```

Jeśli żaden ID nie istnieje → `documentSeries = []` → `RemoveRangeAsync([])` → `CompleteAsync()` bez zmian w DB.

### 3. Logika biznesowa

`RemoveRangeAsync(documentSeries)` — oznacza wszystkie znalezione serie do usunięcia jednocześnie (batch). EF Core generuje `DELETE` per rekord przy `CompleteAsync()`.

### Tabela: pole encji → źródło

> Wymiar nie dotyczy — encje są usuwane, nie tworzone ani modyfikowane.

### 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | `CompleteAsync()` |
|---|---|---|---|
| 1 | `RemoveRangeAsync(documentSeries)` (batch) | `GenericRepository.RemoveRangeAsync` | nie — tylko oznaczenie |
| 2 | `CompleteAsync()` | `UnitOfWork.CompleteAsync()` | tak |

> `RemoveRangeAsync` w odróżnieniu od `RemoveAsync` (P-09, P-10) operuje na całej liście naraz, nie w pętli per element. Atomowość jest taka sama (jeden `CompleteAsync()`).

### 5. Odpowiedź

HTTP `200 OK`. Puste ciało.

### 6. Uwagi techniczne

- [UWAGA: `DeleteDocumentSeries` używa `PUT` zamiast `DELETE` — niezgodność z konwencją REST. Kotwica: `DocumentSeriesController.cs` — `[HttpPut("DeleteDocumentSeries")]`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Nieistniejące IDs w `documentSeriesIds` są po cichu ignorowane — klient otrzymuje `200 OK` nawet gdy żadna seria nie istnieje. Brak informacji zwrotnej dla klienta o tym, które IDs zostały faktycznie usunięte. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `DeleteDocumentSeries` nie sprawdza, czy usuwana seria jest powiązana z dokumentami (brak WAL analogicznego do `BankAccountAssociatedWithDocumentsException`). Usunięcie serii może osierocić dokumenty, które odwołują się do tej serii. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `DeleteDocumentSeries` nie weryfikuje, czy usuwane serie należą do aktywnej firmy bieżącego użytkownika. Możliwe usunięcie serii innego użytkownika znając `Id`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Brak `[FromBody]` na parametrze `int[] documentSeriesIds` — bindowanie z query string. Różnica względem `BankAccountController.DeleteUserFirmBankAccounts` (body) i `ProductController.DeleteProducts` (query string). — WYMAGA WERYFIKACJI Z ZESPOŁEM]
