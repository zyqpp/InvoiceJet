# Generowanie dokumentu PDF — Logika aplikacyjna

## Przepływ wykonania

1. Kontroler wywołuje `DocumentService.GeneratePdfDocument(documentRequestDTO)`.
2. Serwis pobiera aktywną firmę użytkownika.
3. Gdy aktywna firma nie istnieje, serwis rzuca `UserHasNoAssociatedFirmException`.
4. Serwis mapuje `activeUserFirm.Firm` do `documentRequestDto.Seller`.
5. Serwis wywołuje `_pdfGenerationService.GenerateInvoicePdf(documentRequestDto)`.
6. Serwis zwraca DTO.
7. Kontroler zwraca `200 OK`.

---

## Uwagi

- `PdfGenerationService.GenerateInvoicePdf(...)` zwraca ścieżkę pliku lub `null`, ale wynik nie jest walidowany w `DocumentService`. [UWAGA: kontroler może zwrócić `200 OK` nawet gdy generowanie PDF zwróciło `null` bez wyjątku — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- `PdfGenerationService` zapisuje plik w katalogu `Documents` pod `AppDomain.CurrentDomain.BaseDirectory`.
