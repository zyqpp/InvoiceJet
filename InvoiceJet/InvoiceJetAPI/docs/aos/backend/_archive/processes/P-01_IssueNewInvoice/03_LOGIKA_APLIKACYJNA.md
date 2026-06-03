# Wystawienie nowej faktury — Logika aplikacyjna

## 1. Wejście do procesu

`DocumentController.AddDocument(DocumentRequestDto documentRequestDto)` odbiera żądanie `POST /api/Document/AddDocument`.

Metoda kontrolera wykonuje:

```csharp
await _documentService.AddDocument(documentRequestDto);
return Ok(documentRequestDto);
```

---

## 2. Pobranie aktywnej firmy użytkownika

`DocumentService.AddDocument()` wywołuje:

```csharp
_unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId())
```

Jeżeli wynik nie ma wartości, metoda rzuca `UserHasNoAssociatedFirmException`.

---

## 3. Utworzenie encji `Document`

Serwis tworzy encję `Document` na podstawie `DocumentRequestDto` i danych pobranych z bazy.

| Pole encji `Document` | Źródło |
|---|---|
| `Id` | `documentRequestDto.Id` |
| `DocumentNumber` | `DocumentSeries.SeriesName + CurrentNumber.ToString("D4")` |
| `IssueDate` | `documentRequestDto.IssueDate` |
| `DueDate` | `documentRequestDto.DueDate` |
| `DocumentTypeId` | `documentRequestDto.DocumentSeries.DocumentType.Id` |
| `DocumentStatusId` | `(int)DocumentStatusEnum.Unpaid` |
| `BankAccount` | Aktywne konto bankowe firmy użytkownika |
| `ClientId` | `documentRequestDto.Client.Id` |
| `UserFirmId` | Aktywna relacja `UserFirm` użytkownika |

Jeżeli aktywne konto bankowe nie istnieje, serwis rzuca `NoBankAccountAddedException`.

---

## 4. Pierwszy zapis do bazy

Serwis wykonuje:

```csharp
await _unitOfWork.Documents.AddAsync(document);
await _unitOfWork.CompleteAsync();
```

Pierwsze `CompleteAsync()` zapisuje dokument i nadaje mu identyfikator używany przez pozycje dokumentu.

---

## 5. Aktualizacja pozycji dokumentu

Po utworzeniu dokumentu serwis wywołuje:

```csharp
await UpdateDocumentProducts(document.Id, documentRequestDto.Products, userFirmId.Value);
```

Metoda `UpdateDocumentProducts()` wykonuje:

1. Pobiera istniejące pozycje dokumentu przez `DocumentProducts.GetAllDocumentProductsForDocument(documentId)`.
2. Usuwa pobrane pozycje przez `DocumentProducts.RemoveRangeAsync(...)`.
3. Iteruje po `documentProductsDto`.
4. Dla pozycji z `id > 0` wyszukuje produkt po `Name` i `UserFirmId`.
5. Dla pozycji z `id <= 0` mapuje DTO na `Product`, ustawia `UserFirmId` i dodaje produkt.
6. Tworzy `DocumentProduct`.
7. Sumuje `UnitPrice * Quantity` do `Document.UnitPrice`.
8. Sumuje `TotalPrice` do `Document.TotalPrice`.
9. Aktualizuje encję `Document`.

---

## 6. Zwiększenie numeru serii

Jeżeli `documentRequestDto.DocumentSeries` nie jest `null`, serwis wykonuje:

```csharp
await IncreaseDocumentSeriesNumber(documentRequestDto.DocumentSeries.Id);
```

`IncreaseDocumentSeriesNumber()` pobiera serię dokumentu po identyfikatorze, zwiększa `CurrentNumber` o `1` i aktualizuje encję `DocumentSeries`.

---

## 7. Drugi zapis do bazy

Serwis wykonuje drugie:

```csharp
await _unitOfWork.CompleteAsync();
```

Ten zapis utrwala pozycje dokumentu, sumy dokumentu, nowe produkty i zwiększony numer serii.

---

## 8. Uwagi techniczne

- Wyszukiwanie istniejącego produktu dla pozycji z `id > 0` odbywa się po `Name` i `UserFirmId`, nie po `Id`. [UWAGA: nazwa produktu jest używana jako kryterium wyszukiwania mimo obecności `id` w DTO — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- `UpdateDocumentProducts()` usuwa istniejące pozycje dokumentu przed dodaniem nowych. Dla nowego dokumentu lista istniejących pozycji jest pusta.
- Proces nie otacza dwóch wywołań `CompleteAsync()` jawną transakcją. [UWAGA: zapis dokumentu i zapis pozycji są rozdzielone na dwa zapisy EF Core — WYMAGA WERYFIKACJI Z ZESPOŁEM]
