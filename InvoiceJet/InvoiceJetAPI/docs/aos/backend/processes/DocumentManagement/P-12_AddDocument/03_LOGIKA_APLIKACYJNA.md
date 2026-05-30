# AddDocument — Logika aplikacyjna

## 0. Algorytm w skrócie

1. Kontroler odbiera `POST` z `DocumentRequestDto` w body (bez explicit `[FromBody]`), wywołuje `_documentService.AddDocument(documentRequestDto)`.
2. Serwis sprawdza aktywną firmę użytkownika → brak → `UserHasNoAssociatedFirmException` → `400 Bad Request` (WAL-01).
3. Serwis buduje encję `Document` ręcznie (bez AutoMapper): ustawia `DocumentNumber`, `DocumentStatusId = 1`, pobiera aktywne konto bankowe z DB → brak → `NoBankAccountAddedException` → `400` (WAL-02).
4. `Documents.AddAsync(document)` + pierwszy `CompleteAsync()` → nadaje `document.Id`.
5. `UpdateDocumentProducts(document.Id, documentRequestDto.Products, userFirmId)`:
   - Usuwa istniejące `DocumentProduct` (dla nowego dokumentu = brak, więc brak DELETE)
   - Dla każdego produktu: jeśli `Id > 0` → szuka w DB po `Name+UserFirmId` → brak → `Exception("Product not found.")` → `500` ⚠️ (WAL-03); jeśli `Id == 0` → tworzy nowy `Product` przez AutoMapper
   - Tworzy `DocumentProduct` per pozycja; akumuluje sumy
   - Aktualizuje `Document.UnitPrice` i `Document.TotalPrice`
6. `IncreaseDocumentSeriesNumber(documentRequestDto.DocumentSeries.Id)` → pobiera serię; `CurrentNumber++`; `UpdateAsync`
7. Drugi `CompleteAsync()` → zapisuje `DocumentProduct`, zaktualizowane sumy dokumentu, inkrementację serii.
8. Kontroler zwraca `Ok(documentRequestDto)` — oryginalny obiekt żądania, nie encja z DB.

---

## 1. Wejście do procesu

Kotwica: `DocumentController.cs › DocumentController.AddDocument`

```csharp
[HttpPost("AddDocument")]
public async Task<ActionResult<DocumentRequestDto>> AddDocument(DocumentRequestDto documentRequestDto)
{
    await _documentService.AddDocument(documentRequestDto);
    return Ok(documentRequestDto);
}
```

> Brak atrybutu `[FromBody]` — ASP.NET Core inferuje bindowanie z body dla złożonych typów. Brak `try/catch` — wyjątki z serwisu trafiają do `ExceptionMiddleware`.

---

## 2. Walidacje (faza wejściowa)

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Użytkownik ma aktywną firmę | `DocumentService.cs › DocumentService.AddDocument` | `UserHasNoAssociatedFirmException` → `400` (WAL-01) |
| 2 | Firma ma aktywne konto bankowe | `DocumentService.cs › DocumentService.AddDocument` | `NoBankAccountAddedException` → `400` (WAL-02) |
| 3 | Istniejące produkty (Id>0) istnieją w DB po Name+UserFirmId | `DocumentService.cs › DocumentService.UpdateDocumentProducts` | `Exception("Product not found.")` → `500` ⚠️ (WAL-03) |

```csharp
// WAL-01
var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
if (!userFirmId.HasValue)
{
    throw new UserHasNoAssociatedFirmException();
}

// WAL-02 (wbudowany w inicjalizator Document)
BankAccount = await _unitOfWork.BankAccounts.Query()
    .Where(ba => ba.UserFirmId == userFirmId && ba.IsActive)
    .FirstOrDefaultAsync() ?? throw new NoBankAccountAddedException()
```

```csharp
// WAL-03 — w UpdateDocumentProducts
if (documentProductDto.Id > 0)
{
    product = await _unitOfWork.Products.Query()
        .FirstOrDefaultAsync(product => product.Name == documentProductDto.Name && product.UserFirmId == userFirmId);
    if (product == null)
    {
        throw new Exception("Product not found.");
    }
}
```

---

## 3. Logika biznesowa

Kotwica: `DocumentService.cs › DocumentService.AddDocument`

**Krok 1: Budowa encji `Document` bez AutoMapper**

```csharp
var document = new Document
{
    Id = documentRequestDto.Id,
    DocumentNumber = documentRequestDto.DocumentSeries?.SeriesName +
                     documentRequestDto.DocumentSeries?.CurrentNumber.ToString("D4"),
    IssueDate = documentRequestDto.IssueDate,
    DueDate = documentRequestDto.DueDate,
    DocumentTypeId = documentRequestDto.DocumentSeries?.DocumentType?.Id,
    DocumentStatusId = (int)DocumentStatusEnum.Unpaid,
    BankAccount = await _unitOfWork.BankAccounts.Query()
        .Where(ba => ba.UserFirmId == userFirmId && ba.IsActive)
        .FirstOrDefaultAsync() ?? throw new NoBankAccountAddedException(),
    ClientId = documentRequestDto.Client.Id,
    UserFirmId = userFirmId
};
```

> `DocumentNumber` = `SeriesName + CurrentNumber.ToString("D4")` — numer generowany z **aktualnego** `CurrentNumber` (przed inkrementacją). `CurrentNumber.ToString("D4")` → zero-padding do 4 cyfr, np. `1` → `"0001"`, wynik: `"20260001"`.

---

**Krok 2: `UpdateDocumentProducts` — zastępowanie i tworzenie pozycji faktury**

Kotwica: `DocumentService.cs › DocumentService.UpdateDocumentProducts`

```csharp
private async Task UpdateDocumentProducts(int documentId, List<DocumentProductRequestDto> documentProductsDto, int userFirmId)
{
    decimal totalInvoicePrice = 0;
    decimal totalInvoicePriceWithTva = 0;

    var existingDocumentProducts = _unitOfWork.DocumentProducts.GetAllDocumentProductsForDocument(documentId);
    await _unitOfWork.DocumentProducts.RemoveRangeAsync(existingDocumentProducts);

    foreach (var documentProductDto in documentProductsDto)
    {
        Product product;

        if (documentProductDto.Id > 0)
        {
            product = await _unitOfWork.Products.Query()
                .FirstOrDefaultAsync(product => product.Name == documentProductDto.Name && product.UserFirmId == userFirmId);
            if (product == null) throw new Exception("Product not found.");
        }
        else
        {
            product = _mapper.Map<Product>(documentProductDto); // DocumentProductProfile
            product.UserFirmId = userFirmId;
            await _unitOfWork.Products.AddAsync(product);
        }

        var documentProduct = new DocumentProduct
        {
            Quantity = documentProductDto.Quantity,
            Product = product,
            DocumentId = documentId,
            UnitPrice = documentProductDto.UnitPrice,
            TotalPrice = documentProductDto.TotalPrice,
        };

        totalInvoicePrice += documentProductDto.UnitPrice * documentProductDto.Quantity;
        totalInvoicePriceWithTva += documentProductDto.TotalPrice;

        await _unitOfWork.DocumentProducts.AddAsync(documentProduct);
    }

    var document = await _unitOfWork.Documents.GetByIdAsync(documentId);
    if (document != null)
    {
        document.UnitPrice = totalInvoicePrice;
        document.TotalPrice = totalInvoicePriceWithTva;
        await _unitOfWork.Documents.UpdateAsync(document);
    }
}
```

---

**Krok 3: `IncreaseDocumentSeriesNumber` — inkrementacja serii**

Kotwica: `DocumentService.cs › DocumentService.IncreaseDocumentSeriesNumber`

```csharp
private async Task IncreaseDocumentSeriesNumber(int documentSeriesId)
{
    var docSeries = await _unitOfWork.DocumentSeries.GetByIdAsync(documentSeriesId);
    docSeries!.CurrentNumber++;
    await _unitOfWork.DocumentSeries.UpdateAsync(docSeries);
}
```

> Null forgiving `!` — brak null check. Jeśli seria o danym `Id` nie istnieje, `docSeries` = null → `NullReferenceException` przy `docSeries.CurrentNumber++`.

---

### Tabela: pole encji `Document` → źródło (AddDocument)

| Pole encji `Document` | Źródło |
|---|---|
| `Id` | generowany przez DB (IDENTITY) po pierwszym `CompleteAsync()` |
| `DocumentNumber` | `documentRequestDto.DocumentSeries.SeriesName + documentRequestDto.DocumentSeries.CurrentNumber.ToString("D4")` |
| `IssueDate` | `documentRequestDto.IssueDate` |
| `DueDate` | `documentRequestDto.DueDate` |
| `DocumentTypeId` | `documentRequestDto.DocumentSeries.DocumentType.Id` |
| `DocumentStatusId` | `1` (`(int)DocumentStatusEnum.Unpaid` — hardcoded) |
| `BankAccountId` | automatycznie przez EF Core z navigation `BankAccount = <obiekt z DB>` |
| `ClientId` | `documentRequestDto.Client.Id` |
| `UserFirmId` | `userFirmId.Value` (wynik `GetUserFirmIdAsync`) |
| `UnitPrice` | `sum(dto.UnitPrice * dto.Quantity)` — ustawiany w `UpdateDocumentProducts` |
| `TotalPrice` | `sum(dto.TotalPrice)` — ustawiany w `UpdateDocumentProducts` |

---

### Tabela: pole encji `DocumentProduct` → źródło

| Pole encji `DocumentProduct` | Źródło |
|---|---|
| `Id` | generowany przez DB (IDENTITY) po drugim `CompleteAsync()` |
| `Quantity` | `documentProductDto.Quantity` |
| `UnitPrice` | `documentProductDto.UnitPrice` |
| `TotalPrice` | `documentProductDto.TotalPrice` |
| `DocumentId` | `documentId` (explicit — Id dokumentu po pierwszym CompleteAsync) |
| `ProductId` | automatycznie przez EF Core z navigation `Product = <obiekt>` |

---

### Tabela: pole encji `Product` → źródło (gdy Id == 0 — nowy produkt)

| Pole encji `Product` | Źródło |
|---|---|
| `Id` | generowany przez DB (IDENTITY) po drugim `CompleteAsync()` |
| `Name` | `documentProductDto.Name` |
| `Price` | `documentProductDto.UnitPrice` (AutoMapper: `MapFrom(src => src.UnitPrice)`) |
| `ContainsTva` | `documentProductDto.ContainsTva` |
| `UnitOfMeasurement` | `documentProductDto.UnitOfMeasurement` |
| `TvaValue` | `documentProductDto.TvaValue` |
| `UserFirmId` | `userFirmId` (ustawiany ręcznie po mapowaniu) |

---

## 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | `CompleteAsync()` |
|---|---|---|---|
| 1 | `AddAsync(document)` | `GenericRepository.AddAsync` | nie |
| 2 | **Pierwszy `CompleteAsync()`** | `UnitOfWork.CompleteAsync()` | **tak — nadaje `document.Id`** |
| 3 | `RemoveRangeAsync(existingDocumentProducts)` (dla nowego doc = pusta lista) | `DocumentProductRepository` / `GenericRepository` | nie |
| 4 | `AddAsync(product)` × N (nowe produkty, Id==0) | `GenericRepository.AddAsync` | nie |
| 5 | `AddAsync(documentProduct)` × N | `GenericRepository.AddAsync` | nie |
| 6 | `UpdateAsync(document)` (UnitPrice, TotalPrice) | `GenericRepository.UpdateAsync` | nie |
| 7 | `UpdateAsync(docSeries)` (CurrentNumber++) | `GenericRepository.UpdateAsync` | nie |
| 8 | **Drugi `CompleteAsync()`** | `UnitOfWork.CompleteAsync()` | **tak — zapisuje kroki 3–7** |

> [UWAGA: Dwa `CompleteAsync()` bez jawnej transakcji (`IDbContextTransaction`). Jeśli krok po pierwszym `CompleteAsync()` zawiedzie (np. WAL-03 w `UpdateDocumentProducts` lub błąd w `IncreaseDocumentSeriesNumber`), rekord `Document` już istnieje w DB bez pozycji i bez zaktualizowanych sum. Brak rollbacku. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 5. Odpowiedź

HTTP `200 OK`. Ciało: **oryginalny obiekt żądania** `documentRequestDto` (ten sam, który przyszedł w POST). Serwis nie remapuje zapisanej encji z DB — zwraca `return documentRequestDto` bez zmian. Pole `DocumentRequestDto.Id` = `0` (wartość z żądania), a nie wygenerowany `document.Id`. Kontroler: `return Ok(documentRequestDto)`.

> [UWAGA: Odpowiedź zawiera oryginalny DTO z `Id = 0` (lub wartość z żądania), nie `document.Id` nadany przez DB. Klient nie zna `Id` nowo wystawionego dokumentu. Aby pobrać Id, należy wywołać `GET /api/Document/GetDocumentTableRecords/{documentTypeId}`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 6. Uwagi techniczne

- [UWAGA: Dwa `CompleteAsync()` bez jawnej transakcji → partial commit risk. Kotwica: `DocumentService.cs › DocumentService.AddDocument`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Produkt o `Id > 0` wyszukiwany po `Name + UserFirmId`, **nie** po `Id`. Jeśli nazwa produktu w DTO różni się od nazwy w DB (np. po edycji produktu), wyjątek `Exception("Product not found.")` → `500`. Kotwica: `DocumentService.cs › DocumentService.UpdateDocumentProducts`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `IncreaseDocumentSeriesNumber` używa null forgiving `docSeries!.CurrentNumber++` — brak null check. Jeśli seria o `documentRequestDto.DocumentSeries.Id` nie istnieje → `NullReferenceException` → 500. Kotwica: `DocumentService.cs › DocumentService.IncreaseDocumentSeriesNumber`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `Document.Id` nie jest zwracany w odpowiedzi — `return Ok(documentRequestDto)` zawiera oryginalny DTO z `Id = 0`. Klient nie zna Id nowego dokumentu. Kotwica: `DocumentController.cs › DocumentController.AddDocument`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `DocumentRequestDto.DocumentType` i `DocumentRequestDto.DocumentStatus` to encje domenowe osadzone w DTO (nie dedykowane DTO). W `AddDocument` są ignorowane (DocumentTypeId pobierany z `DocumentSeries.DocumentType.Id`, DocumentStatusId hardcoded). Kotwica: `DocumentRequestDto.cs`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `DocumentNumber` budowany z `DocumentSeries.CurrentNumber` (przed inkrementacją). Logika poprawna — ale wartość `CurrentNumber` pochodzi z DTO, nie z DB, więc klient musi przesłać aktualną wartość `CurrentNumber` z serii. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
