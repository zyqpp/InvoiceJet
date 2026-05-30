# Pobranie strumienia PDF faktury — Logika aplikacyjna

## Przepływ wykonania

1. Serwis pobiera aktywną firmę użytkownika.
2. Gdy brak aktywnej firmy, rzuca `UserHasNoAssociatedFirmException`.
3. Serwis pobiera pierwsze konto bankowe z dokumentów aktywnej firmy:
   - `Documents.Query().Where(d => d.UserFirmId == activeUserFirm.UserFirmId).Select(d => d.BankAccount).FirstOrDefaultAsync()`.
4. Serwis uzupełnia:
   - `documentRequestDto.Seller`,
   - `documentRequestDto.BankAccount`.
5. Serwis wywołuje `_pdfGenerationService.GetInvoicePdfStream(documentRequestDto)`.
6. Serwis tworzy `DocumentStreamDto` z:
   - `DocumentNumber = documentRequestDto.DocumentNumber ?? documentRequestDto.DocumentSeries!.CurrentNumber.ToString()`,
   - `PdfContent = pdfContent`.
7. Kontroler:
   - zwraca `400 BadRequest("Failed to generate the PDF document.")`, gdy `PdfContent == null`,
   - zwraca `File(pdfContent, "application/pdf", $"Invoice_{documentNumber}.pdf")` dla sukcesu.

---

## Uwagi

- Operacja używa konta bankowego pobranego z istniejących dokumentów firmy, nie z aktywnego konta bankowego firmy. [UWAGA: źródło konta bankowego dla PDF wymaga potwierdzenia biznesowego — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Dla `DocumentNumber == null` i `DocumentSeries == null` może wystąpić błąd `NullReferenceException`. [WYMAGA WERYFIKACJI]
