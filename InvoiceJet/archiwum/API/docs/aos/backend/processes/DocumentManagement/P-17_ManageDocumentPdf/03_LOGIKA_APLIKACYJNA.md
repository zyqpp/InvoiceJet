# ManageDocumentPdf — Logika aplikacyjna

Proces P-17 obejmuje dwa endpointy generowania PDF.

---

## Endpoint A — `POST /api/Document/GenerateDocumentPdf`

### 0. Algorytm w skrócie

1. Kontroler odbiera `DocumentRequestDto` z body, owija wywołanie serwisu w blok `try/catch`.
2. Serwis pobiera aktywną firmę (`GetUserFirmAsync`) → null → `UserHasNoAssociatedFirmException`.
3. Serwis nadpisuje `documentRequestDto.Seller` mapując `activeUserFirm.Firm` → `FirmDto`.
4. `PdfGenerationService.GenerateInvoicePdf(documentRequestDto)` — zapisuje PDF na dysk; wewnętrzny try/catch w serwisie PDF (błędy połykane, zwraca `null`).
5. Kontroler zwraca `200 OK` (puste body).
6. Wyjątek z kroku 2 złapany przez kontrolerowy try/catch → `400 BadRequest(ex.Message)` — z pominięciem ExceptionMiddleware.

### 1. Wejście do procesu

Kotwica: `DocumentController.cs › DocumentController.GenerateDocument`

```csharp
[HttpPost("GenerateDocumentPdf")]
public async Task<ActionResult<DocumentRequestDto>> GenerateDocument(DocumentRequestDto documentRequestDTO)
{
    try
    {
        await _documentService.GeneratePdfDocument(documentRequestDTO);
        return Ok();
    }
    catch (Exception ex)
    {
        return BadRequest(ex.Message);
    }
}
```

### 2. Walidacje

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Użytkownik ma aktywną firmę | `DocumentService.cs › DocumentService.GeneratePdfDocument` | `throw new UserHasNoAssociatedFirmException()` → złapane przez kontroler → `400 BadRequest` |

```csharp
var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(_userService.GetCurrentUserId());
if (activeUserFirm is null)
    throw new UserHasNoAssociatedFirmException();
```

### 3. Logika biznesowa

Kotwica: `DocumentService.cs › DocumentService.GeneratePdfDocument`

```csharp
public async Task<DocumentRequestDto> GeneratePdfDocument(DocumentRequestDto documentRequestDto)
{
    var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(_userService.GetCurrentUserId());
    if (activeUserFirm is null)
        throw new UserHasNoAssociatedFirmException();

    documentRequestDto.Seller = _mapper.Map<FirmDto>(activeUserFirm.Firm);

    _pdfGenerationService.GenerateInvoicePdf(documentRequestDto);

    return documentRequestDto;
}
```

1. `GetUserFirmAsync` — pobiera `UserFirm` z Include `Firm`.
2. Nadpisuje `documentRequestDto.Seller` → `FirmDto` z `activeUserFirm.Firm`.
3. `GenerateInvoicePdf(documentRequestDto)` — zapisuje PDF na dysku pod ścieżką `<BaseDir>/Documents/Invoice_<CurrentNumber>.pdf`. Wewnątrz `PdfGenerationService` jest try/catch: błędy logowane/ignorowane, zwraca `null` przy niepowodzeniu.
4. Serwis zwraca `documentRequestDto` (choć kontroler ignoruje tę wartość i zwraca `Ok()`).

### 4. Zapisy do bazy i transakcje

Brak — endpoint nie modyfikuje bazy danych. Zapis trafia na dysk (plik PDF).

### 5. Odpowiedź

HTTP `200 OK`. Puste body (`return Ok()`).

---

## Endpoint B — `POST /api/Document/GetInvoicePdfStream`

### 0. Algorytm w skrócie

1. Kontroler odbiera `DocumentRequestDto`, wywołuje serwis bez try/catch.
2. Serwis pobiera firmę (`GetUserFirmAsync`) → null → `UserHasNoAssociatedFirmException` → ExceptionMiddleware → `400`.
3. Serwis pobiera konto bankowe z pierwszego dokumentu firmy (Query + FirstOrDefaultAsync).
4. Serwis nadpisuje `Seller` i `BankAccount` w DTO.
5. `PdfGenerationService.GetInvoicePdfStream(documentRequestDto)` → `byte[]` lub `null`.
6. Zwraca `DocumentStreamDto { DocumentNumber, PdfContent }`.
7. Kontroler: jeżeli `PdfContent == null` → `BadRequest("Failed to generate...")`.
8. Sukces: `File(pdfContent, "application/pdf", "Invoice_N.pdf")`.

### 1. Wejście do procesu

Kotwica: `DocumentController.cs › DocumentController.GetInvoicePdfStream`

```csharp
[HttpPost("GetInvoicePdfStream")]
public async Task<IActionResult> GetInvoicePdfStream(DocumentRequestDto documentRequestDto)
{
    var documentStreamDto = await _documentService.GetInvoicePdfStream(documentRequestDto);
    if (documentStreamDto.PdfContent == null)
    {
        return BadRequest("Failed to generate the PDF document.");
    }
    return File(documentStreamDto.PdfContent, "application/pdf",
        $"Invoice_{documentStreamDto.DocumentNumber}.pdf");
}
```

### 2. Walidacje

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Użytkownik ma aktywną firmę | `DocumentService.cs › DocumentService.GetInvoicePdfStream` | `throw new UserHasNoAssociatedFirmException()` → ExceptionMiddleware → `400` |
| 2 | Generowanie PDF się powiodło | `DocumentController.cs › DocumentController.GetInvoicePdfStream` | `PdfContent == null` → `BadRequest("Failed to generate the PDF document.")` |

### 3. Logika biznesowa

Kotwica: `DocumentService.cs › DocumentService.GetInvoicePdfStream`

```csharp
public async Task<DocumentStreamDto> GetInvoicePdfStream(DocumentRequestDto documentRequestDto)
{
    var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(_userService.GetCurrentUserId());
    if (activeUserFirm is null)
        throw new UserHasNoAssociatedFirmException();

    var documentBankAccount = await _unitOfWork.Documents.Query()
        .Where(d => d.UserFirmId == activeUserFirm.UserFirmId)
        .Select(d => d.BankAccount)
        .FirstOrDefaultAsync();

    documentRequestDto.Seller = _mapper.Map<FirmDto>(activeUserFirm.Firm);
    documentRequestDto.BankAccount = _mapper.Map<BankAccountDto>(documentBankAccount);

    var pdfContent = _pdfGenerationService.GetInvoicePdfStream(documentRequestDto);

    return new DocumentStreamDto
    {
        DocumentNumber = documentRequestDto.DocumentNumber ??
                         documentRequestDto.DocumentSeries!.CurrentNumber.ToString(),
        PdfContent = pdfContent
    };
}
```

1. Pobiera firmę użytkownika.
2. Pobiera konto bankowe z pierwszego dokumentu firmy (brak specyficznego kryterium).
3. Nadpisuje `Seller` i `BankAccount` w DTO.
4. `GetInvoicePdfStream` — generuje PDF do `MemoryStream`, zwraca `byte[]`; wewnątrz try/catch, przy błędzie zwraca `null`.
5. `DocumentNumber` — z `documentRequestDto.DocumentNumber` lub `DocumentSeries!.CurrentNumber.ToString()` (null-forgiving `!`).

### 4. Zapisy do bazy i transakcje

Brak — endpoint read-only (PDF generowany w pamięci).

### 5. Odpowiedź

HTTP `200 OK`. Ciało: plik binarny `application/pdf`. Nazwa pliku: `Invoice_<DocumentNumber>.pdf`.

---

## 6. Uwagi techniczne (oba endpointy)

- [UWAGA: `GenerateDocument` (API-28) ma własny `try { ... } catch(Exception ex) { return BadRequest(ex.Message); }` w kontrolerze. Każdy wyjątek (w tym `UserHasNoAssociatedFirmException`) jest złapany przez kontroler zamiast ExceptionMiddleware. Kotwica: `DocumentController.cs › DocumentController.GenerateDocument`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: `PdfGenerationService.GenerateInvoicePdf` ma wewnętrzny try/catch — błąd generowania PDF (np. brak uprawnienia do katalogu) jest połykany; serwis zwraca `null` zamiast rzucać wyjątek. `DocumentService.GeneratePdfDocument` ignoruje tę wartość null i zwraca `200 OK` pomimo nieudanego generowania. Kotwica: `PdfGenerationService.cs › PdfGenerationService.GenerateInvoicePdf`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: `GetInvoicePdfStream` pobiera konto bankowe z pierwszego dokumentu firmy (`FirstOrDefaultAsync` bez OrderBy) — nie jest to konto bankowe dokumentu przekazanego w request. Kotwica: `DocumentService.cs › DocumentService.GetInvoicePdfStream`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: Null-forgiving `documentRequestDto.DocumentSeries!.CurrentNumber.ToString()` — gdy `DocumentNumber == null` I `DocumentSeries == null`, rzuci `NullReferenceException`. Kotwica: `DocumentService.cs › DocumentService.GetInvoicePdfStream`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
