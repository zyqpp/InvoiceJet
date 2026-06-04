# EditDocument — Logika aplikacyjna

## 0. Algorytm w skrócie

1. Kontroler odbiera `PUT` z `DocumentRequestDto` w body, wywołuje `_documentService.EditDocument(documentRequestDto)`.
2. Serwis sprawdza aktywną firmę → brak → `UserHasNoAssociatedFirmException` → `400` (WAL-01).
3. `Documents.GetByIdAsync(documentRequestDto.Id)` → null → `Exception("Document not found.")` → `500` ⚠️ (WAL-02).
4. Ręczna aktualizacja pól tracked encji: `IssueDate`, `DueDate`, `DocumentTypeId`, `DocumentStatusId`, `ClientId`, `UserFirmId`.
5. `Documents.UpdateAsync(document)` — oznaczenie do zapisu (bez `CompleteAsync`).
6. `UpdateDocumentProducts(document.Id, documentRequestDto.Products, userFirmId)`:
   - Usuwa istniejące `DocumentProduct` dla dokumentu
   - Dla każdego produktu: jeśli `Id > 0` → szuka po `Name+UserFirmId` → brak → `Exception("Product not found.")` → `500` ⚠️ (WAL-03)
   - Jeśli `Id == 0` → tworzy nowy `Product`
   - Tworzy `DocumentProduct`; aktualizuje `Document.UnitPrice` i `Document.TotalPrice`
7. **Jeden** `CompleteAsync()` → zapisuje dokument, pozycje, sumy.
8. Kontroler zwraca `Ok(documentRequestDto)` — oryginalny DTO.

---

## 1. Wejście do procesu

Kotwica: `DocumentController.cs › DocumentController.EditDocument`

```csharp
[HttpPut("EditDocument")]
public async Task<ActionResult<DocumentRequestDto>> EditDocument(DocumentRequestDto documentRequestDto)
{
    await _documentService.EditDocument(documentRequestDto);
    return Ok(documentRequestDto);
}
```

Brak `try/catch` — wyjątki do `ExceptionMiddleware`.

---

## 2. Walidacje (faza wejściowa)

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Użytkownik ma aktywną firmę | `DocumentService.cs › DocumentService.EditDocument` | `UserHasNoAssociatedFirmException` → `400` (WAL-01) |
| 2 | Dokument o podanym `Id` istnieje w DB | `DocumentService.cs › DocumentService.EditDocument` | `Exception("Document not found.")` → `500` ⚠️ (WAL-02) |
| 3 | Istniejące produkty (`Id > 0`) znalezione po `Name+UserFirmId` | `DocumentService.cs › DocumentService.UpdateDocumentProducts` | `Exception("Product not found.")` → `500` ⚠️ (WAL-03) |

```csharp
// WAL-01
var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
if (!userFirmId.HasValue)
{
    throw new UserHasNoAssociatedFirmException();
}

// WAL-02
var document = await _unitOfWork.Documents.GetByIdAsync(documentRequestDto.Id);
if (document == null)
{
    throw new Exception("Document not found.");
}
```

---

## 3. Logika biznesowa

Kotwica: `DocumentService.cs › DocumentService.EditDocument`

**Krok 1: Ręczna aktualizacja pól tracked encji**

```csharp
document.IssueDate = documentRequestDto.IssueDate;
document.DueDate = documentRequestDto.DueDate;
document.DocumentTypeId = documentRequestDto.DocumentType?.Id;
document.DocumentStatusId = documentRequestDto.DocumentStatus?.Id;
document.ClientId = documentRequestDto.Client.Id;
document.UserFirmId = userFirmId;

await _unitOfWork.Documents.UpdateAsync(document);
```

> Uwaga: `document.UserFirmId = userFirmId` — ustawia `UserFirmId` na aktualną firmę. Nie sprawdza, czy dokument należał wcześniej do tej firmy.

**Krok 2: `UpdateDocumentProducts`** — identyczna jak w P-12. Pełna dokumentacja: `../P-12_AddDocument/03_LOGIKA_APLIKACYJNA.md#UpdateDocumentProducts`.

---

### Tabela: pole encji `Document` → źródło (EditDocument)

| Pole encji `Document` | Źródło |
|---|---|
| `Id` | bez zmian |
| `DocumentNumber` | bez zmian (numer nie jest aktualizowany!) |
| `BankAccountId` | bez zmian |
| `IssueDate` | `documentRequestDto.IssueDate` |
| `DueDate` | `documentRequestDto.DueDate` |
| `DocumentTypeId` | `documentRequestDto.DocumentType?.Id` |
| `DocumentStatusId` | `documentRequestDto.DocumentStatus?.Id` |
| `ClientId` | `documentRequestDto.Client.Id` |
| `UserFirmId` | `userFirmId.Value` |
| `UnitPrice` | `sum(dto.UnitPrice * dto.Quantity)` — przez `UpdateDocumentProducts` |
| `TotalPrice` | `sum(dto.TotalPrice)` — przez `UpdateDocumentProducts` |

---

## 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | `CompleteAsync()` |
|---|---|---|---|
| 1 | `UpdateAsync(document)` | `GenericRepository.UpdateAsync` | nie |
| 2 | `RemoveRangeAsync(existingDocumentProducts)` | `DocumentProductRepository` | nie |
| 3 | `AddAsync(product)` × N (nowe produkty Id=0) | `GenericRepository.AddAsync` | nie |
| 4 | `AddAsync(documentProduct)` × N | `GenericRepository.AddAsync` | nie |
| 5 | `UpdateAsync(document)` (sumy) | `GenericRepository.UpdateAsync` | nie |
| 6 | **`CompleteAsync()`** | `UnitOfWork.CompleteAsync()` | **tak — jeden commit** |

> Różnica względem P-12 (AddDocument): **jeden** `CompleteAsync()`, nie dwa. Atomowy zapis wszystkich zmian.

---

## 5. Odpowiedź

HTTP `200 OK`. Ciało: oryginalny `documentRequestDto` (bez Id z DB, wartości z żądania).

---

## 6. Uwagi techniczne

- [UWAGA: `GetByIdAsync(documentRequestDto.Id)` pobiera dokument bez sprawdzenia, czy należy do aktywnej firmy bieżącego użytkownika. Możliwa edycja dokumentu innego użytkownika znając jego `Id`. Kotwica: `DocumentService.cs › DocumentService.EditDocument`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: WAL-02 zwraca `500` zamiast `404`/`400`. Brak dedykowanego `DocumentNotFoundException`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: WAL-03 zwraca `500` (wspólne z P-12). — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `DocumentNumber` nie jest aktualizowany przy edycji — zostaje z momentu wystawienia. — UWAGA informacyjna, zachowanie celowe]
- [UWAGA: Produkty z `Id > 0` szukane po `Name+UserFirmId`, nie po `Id`. Kotwica: `DocumentService.cs › DocumentService.UpdateDocumentProducts`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
