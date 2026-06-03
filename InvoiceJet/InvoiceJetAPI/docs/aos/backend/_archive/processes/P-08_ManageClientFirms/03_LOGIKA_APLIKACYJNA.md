# Zarządzanie firmami-klientami — Logika aplikacyjna

## Pobranie listy klientów

1. `FirmController.GetUserClientFirms()` wywołuje `FirmService.GetUserClientFirms()`.
2. Serwis pobiera relacje przez `UserFirms.GetUserFirmClients(currentUserId)`.
3. Dla pustej listy zwraca pustą `List<FirmDto>`.
4. Dla niepustej listy mapuje `Firm` do `FirmDto`.

## Usuwanie firm-klientów

1. `FirmController.DeleteFirms(...)` wywołuje `FirmService.DeleteFirms(firmIds)`.
2. Serwis iteruje po `firmIds`.
3. Dla każdego `firmId` pobiera encję `Firm`.
4. Serwis sprawdza powiązanie z dokumentami:
   - `_unitOfWork.Documents.Query().AnyAsync(d => d.ClientId == firmId)`.
5. Gdy istnieje powiązanie, serwis rzuca `FirmAssociatedWithDocumentException`.
6. Gdy brak powiązania, serwis usuwa firmę.
7. Po pętli serwis wykonuje `_unitOfWork.CompleteAsync()`.

---

## Uwagi

- Gdy firma nie istnieje, kod rzuca `Exception("Product not found.")`. [UWAGA: treść wyjątku nie odpowiada domenie firmy — WYMAGA WERYFIKACJI Z ZESPOŁEM]
