# GetDocuments — Logika aplikacyjna

Proces `P-14` obejmuje dwa endpointy odczytu.

---

## Endpoint A — `GET /api/Document/GetDocumentTableRecords/{documentTypeId}`

### 0. Algorytm w skrócie

1. Kontroler odbiera `{documentTypeId}` z trasy, wywołuje `_documentService.GetDocumentTableRecords(documentTypeId)`.
2. Serwis pobiera aktywną firmę (`GetUserFirmAsync`) → null → zwraca `new List<DocumentTableRecordDto>()`.
3. `DocumentRepository.GetAllDocumentsByType(userFirmId, documentTypeId)` — filtruje po `UserFirmId` + `DocumentTypeId`, Include `Client` i `DocumentStatus`.
4. AutoMapper: `List<Document>` → `List<DocumentTableRecordDto>`.
5. Kontroler zwraca `200 OK` z listą.

### 1. Wejście do procesu

Kotwica: `DocumentController.cs › DocumentController.GetDocumentTableRecords`

```csharp
[HttpGet("GetDocumentTableRecords/{documentTypeId}")]
public async Task<IActionResult> GetDocumentTableRecords(int documentTypeId)
{
    var documents = await _documentService.GetDocumentTableRecords(documentTypeId);
    return Ok(documents);
}
```

### 2. Walidacje (faza wejściowa)

Brak walidacji wejściowych. Użytkownik bez firmy → `200 OK` z `[]`.

### 3. Logika biznesowa

Kotwica: `DocumentService.cs › DocumentService.GetDocumentTableRecords`

```csharp
public async Task<List<DocumentTableRecordDto>> GetDocumentTableRecords(int documentTypeId)
{
    var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(_userService.GetCurrentUserId());
    if (activeUserFirm is null)
        return new List<DocumentTableRecordDto>();

    var documents = await _unitOfWork.Documents.GetAllDocumentsByType(activeUserFirm.UserFirmId, documentTypeId);
    return _mapper.Map<List<DocumentTableRecordDto>>(documents);
}
```

### 4. Zapisy do bazy i transakcje

Brak — endpoint read-only.

### 5. Odpowiedź

HTTP `200 OK`. Ciało: `List<DocumentTableRecordDto>` — może być `[]`.

---

## Endpoint B — `GET /api/Document/GetDocumentById/{documentId}`

### 0. Algorytm w skrócie

1. Kontroler odbiera `{documentId}` z trasy, wywołuje `_documentService.GetDocumentById(documentId)`.
2. `DocumentRepository.GetDocumentWithAllInfo(documentId)` — Include `DocumentStatus`, `DocumentProducts→Product`, `Client`.
3. AutoMapper: `Document` → `DocumentRequestDto`.
4. Kontroler zwraca `200 OK`.

### 1. Wejście do procesu

Kotwica: `DocumentController.cs › DocumentController.GetDocumentById`

```csharp
[HttpGet("GetDocumentById/{documentId}")]
public async Task<IActionResult> GetDocumentById(int documentId)
{
    var document = await _documentService.GetDocumentById(documentId);
    return Ok(document);
}
```

### 2. Walidacje (faza wejściowej)

Brak walidacji. Nieistniejące `documentId` → `GetDocumentWithAllInfo` zwraca `null` → AutoMapper mapuje `null` → odpowiedź `200 OK` z `null` w body.

> [UWAGA: Brak sprawdzenia, czy dokument istnieje. `GetDocumentById` dla nieistniejącego Id zwraca `200 OK` z `null` zamiast `404`. Kotwica: `DocumentService.cs › DocumentService.GetDocumentById`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

> [UWAGA: Brak sprawdzenia własności — `GetDocumentWithAllInfo(documentId)` pobiera KAŻDY dokument po `Id` bez weryfikacji `UserFirmId`. Możliwe odczytanie dokumentów innego użytkownika. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### 3. Logika biznesowa

Kotwica: `DocumentService.cs › DocumentService.GetDocumentById`

```csharp
public async Task<DocumentRequestDto> GetDocumentById(int documentId)
{
    var document = await _unitOfWork.Documents.GetDocumentWithAllInfo(documentId);
    return _mapper.Map<DocumentRequestDto>(document);
}
```

### 4. Zapisy do bazy i transakcje

Brak — endpoint read-only.

### 5. Odpowiedź

HTTP `200 OK`. Ciało: `DocumentRequestDto` z zagnieżdżonymi `Products` (z danych `DocumentProduct→Product`), `DocumentStatus`, `Client`. Pole `Seller` będzie `null` (brak Include `UserFirm` w `GetDocumentWithAllInfo`).

---

## 6. Uwagi techniczne (oba endpointy)

- [UWAGA: `GetDocumentById` zwraca `200 OK null` dla nieistniejącego Id. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `GetDocumentById` bez ownership check. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `DocumentTableRecordDto.DocumentStatus` to encja domenowa, nie DTO. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `GetDocumentById` nie Include `UserFirm` → `Seller` = null w odpowiedzi. — UWAGA informacyjna]
