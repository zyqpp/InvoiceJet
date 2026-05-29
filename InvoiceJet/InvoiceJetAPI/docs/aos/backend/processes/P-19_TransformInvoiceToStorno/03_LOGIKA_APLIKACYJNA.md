# Transformacja faktury do storna — Logika aplikacyjna

## Przepływ wykonania

1. Serwis pobiera aktywne `userFirmId` użytkownika.
2. Gdy brak aktywnej firmy, rzuca `Exception("User firm not found.")`.
3. Serwis iteruje po `documentIds`.
4. Dla każdego identyfikatora pobiera dokument po:
   - `Id == documentId`,
   - `UserFirmId == activeUserFirmId`.
5. Gdy dokument nie istnieje, rzuca `Exception("Document not found.")`.
6. Serwis ustawia:
   - `document.DocumentTypeId = (int)DocumentTypeEnum.StornoInvoice`.
7. Serwis aktualizuje dokument i wykonuje `CompleteAsync()` w każdej iteracji.
8. Kontroler zwraca `200 OK`.

---

## Uwagi

- `CompleteAsync()` jest wywoływane w każdej iteracji pętli, nie po całej liście dokumentów. [WYMAGA WERYFIKACJI]
