# Edycja dokumentu — Logika aplikacyjna

## Przepływ wykonania

1. Serwis pobiera aktywną firmę użytkownika przez `Users.GetUserFirmIdAsync(...)`.
2. Gdy aktywna firma nie istnieje, rzuca `UserHasNoAssociatedFirmException`.
3. Serwis pobiera dokument po `documentRequestDto.Id`.
4. Gdy dokument nie istnieje, rzuca `Exception("Document not found.")`.
5. Serwis aktualizuje pola:
   - `IssueDate`,
   - `DueDate`,
   - `DocumentTypeId` z `DocumentType?.Id`,
   - `DocumentStatusId` z `DocumentStatus?.Id`,
   - `ClientId`,
   - `UserFirmId`.
6. Serwis zapisuje aktualizację encji dokumentu.
7. Serwis wywołuje `UpdateDocumentProducts(document.Id, documentRequestDto.Products, userFirmId.Value)`.
8. Serwis wykonuje `_unitOfWork.CompleteAsync()`.

---

## Uwagi

- Logika `UpdateDocumentProducts` jest współdzielona z procesem dodawania dokumentu.
- Dla pozycji z `id > 0` wyszukiwanie produktu odbywa się po `Name` i `UserFirmId`.
