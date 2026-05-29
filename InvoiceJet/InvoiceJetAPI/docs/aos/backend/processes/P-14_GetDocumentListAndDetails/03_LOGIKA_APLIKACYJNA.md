# Lista i szczegóły dokumentów — Logika aplikacyjna

## Lista dokumentów

1. Serwis pobiera aktywną relację firmy użytkownika przez `Users.GetUserFirmAsync(currentUserId)`.
2. Gdy relacja nie istnieje, serwis zwraca pustą listę.
3. Gdy relacja istnieje, serwis pobiera dokumenty:
   - `Documents.GetAllDocumentsByType(activeUserFirm.UserFirmId, documentTypeId)`.
4. Serwis mapuje encje do `List<DocumentTableRecordDto>`.

## Szczegóły dokumentu

1. Serwis pobiera encję dokumentu z relacjami przez `Documents.GetDocumentWithAllInfo(documentId)`.
2. Serwis mapuje wynik do `DocumentRequestDto`.
3. Kontroler zwraca `200 OK`.

---

## Uwagi

- Metoda `GetDocumentById` nie sprawdza jawnie przypadku `document == null` przed mapowaniem. [UWAGA: odpowiedź dla brakującego `documentId` wymaga potwierdzenia testem integracyjnym — WYMAGA WERYFIKACJI Z ZESPOŁEM]
