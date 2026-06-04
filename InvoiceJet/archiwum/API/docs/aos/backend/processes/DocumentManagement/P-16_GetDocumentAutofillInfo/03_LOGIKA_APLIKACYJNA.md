# GetDocumentAutofillInfo — Logika aplikacyjna

## 0. Algorytm w skrócie

1. Kontroler odbiera `{documentTypeId}` z trasy i wywołuje `_documentService.GetDocumentAutofillInfo(documentTypeId)`.
2. Serwis pobiera `userId` z `IUserService.GetCurrentUserId()`.
3. `UserRepository.GetUserFirmIdAsync(userId)` → `int?`; jeżeli `null` → zwraca `new DocumentAutofillDto()` (pola null).
4. Cztery równoległe (sekwencyjne w kodzie) zapytania: klienci, serie dokumentów, statusy, produkty.
5. AutoMapper mapuje listy na odpowiednie kolekcje DTO.
6. Kontroler zwraca `200 OK` z `DocumentAutofillDto`.

---

## 1. Wejście do procesu

Kotwica: `DocumentController.cs › DocumentController.GetDocumentAutofillInfo`

```csharp
[HttpGet("GetDocumentAutofillInfo/{documentTypeId}")]
public async Task<IActionResult> GetDocumentAutofillInfo(int documentTypeId)
{
    var dto = await _documentService.GetDocumentAutofillInfo(documentTypeId);
    return Ok(dto);
}
```

---

## 2. Walidacje (faza wejściowa)

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Użytkownik ma firmę (`userFirmId.HasValue`) | `DocumentService.cs › DocumentService.GetDocumentAutofillInfo` | `return new DocumentAutofillDto()` (wszystkie listy `null`) |

```csharp
var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(userId);
if (!userFirmId.HasValue) return new DocumentAutofillDto();
```

> Brak wyjątku — zwracany jest pusty obiekt DTO z polami `null!`.

---

## 3. Logika biznesowa

Kotwica: `DocumentService.cs › DocumentService.GetDocumentAutofillInfo`

```csharp
public async Task<DocumentAutofillDto> GetDocumentAutofillInfo(int documentTypeId)
{
    var userId = _userService.GetCurrentUserId();
    var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(userId);
    if (!userFirmId.HasValue) return new DocumentAutofillDto();

    var clients = await _unitOfWork.Firms.Query()
        .Where(f => f.UserFirms!.Any(uf => uf.UserId == userId && uf.IsClient))
        .ToListAsync();
    var documentSeries = await _unitOfWork.DocumentSeries.Query()
        .Where(ds => ds.UserFirmId == userFirmId && ds.DocumentTypeId == documentTypeId)
        .Include(ds => ds.DocumentType)
        .ToListAsync();
    var documentStatuses = await _unitOfWork.DocumentStatuses.Query().ToListAsync();
    var products = await _unitOfWork.Products.Query()
        .Where(p => p.UserFirmId == userFirmId)
        .ToListAsync();

    var dto = new DocumentAutofillDto
    {
        Clients = _mapper.Map<List<FirmDto>>(clients),
        DocumentSeries = _mapper.Map<List<DocumentSeriesDto>>(documentSeries),
        DocumentStatuses = _mapper.Map<List<DocumentStatusDto>>(documentStatuses),
        Products = _mapper.Map<List<ProductDto>>(products)
    };

    return dto;
}
```

**Zapytanie 1 — Klienci:**
- Filtr: `f.UserFirms!.Any(uf => uf.UserId == userId && uf.IsClient)` — firmy powiązane z użytkownikiem przez tabelę `UserFirm` z `IsClient=true`.
- Null-forgiving `!` na `f.UserFirms!`.

**Zapytanie 2 — Serie dokumentów:**
- Filtr: `ds.UserFirmId == userFirmId && ds.DocumentTypeId == documentTypeId` — filtruje po firmie i typie dokumentu.
- Include: `ds.DocumentType` — zagnieżdżony typ dokumentu w odpowiedzi.

**Zapytanie 3 — Statusy:**
- Brak filtra — zwracane są WSZYSTKIE statusy z tabeli `DocumentStatus` (seed: Unpaid, Paid).

**Zapytanie 4 — Produkty:**
- Filtr: `p.UserFirmId == userFirmId` — produkty własne firmy.

---

## 4. Zapisy do bazy i transakcje

Brak — endpoint read-only.

---

## 5. Odpowiedź

HTTP `200 OK`. Ciało: `DocumentAutofillDto` z czterema listami. Gdy brak firmy — wszystkie cztery listy mają wartość `null` (nie `[]`).

---

## 6. Uwagi techniczne

- [UWAGA: Gdy `GetUserFirmIdAsync` zwraca `null`, serwis zwraca `new DocumentAutofillDto()` — obiekt z polami `Clients=null`, `DocumentSeries=null`, `DocumentStatuses=null`, `Products=null`. Frontend może otrzymać JSON z `null` zamiast pustych tablic. Kotwica: `DocumentService.cs › DocumentService.GetDocumentAutofillInfo`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: `DocumentStatuses` pobierane bez filtra firmy — wszystkie statusy są globalne (seed). Potencjalnie niespójne z podejściem do innych kolekcji. — UWAGA informacyjna]

- [UWAGA: Null-forgiving `f.UserFirms!` w filtrze klientów — jeżeli `UserFirms` nie jest załadowane (brak Include), LINQ to SQL przetłumaczy jako podzapytanie; null safety jest tutaj na poziomie nullability C# (nie EF). — UWAGA informacyjna]
