# ManageDocumentPdf — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

### Endpoint A — GenerateDocumentPdf (API-28)

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01A` | Użytkownik ma aktywną firmę | `DocumentService.cs › DocumentService.GeneratePdfDocument` | `GetUserFirmAsync` zwraca `null` | `UserHasNoAssociatedFirmException` | `400 Bad Request` | `"User has no associated firm."` |

> WAL-01A — wyjątek złapany przez **kontrolerowy** `try/catch`, NIE przez ExceptionMiddleware.

### Endpoint B — GetInvoicePdfStream (API-29)

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01B` | Użytkownik ma aktywną firmę | `DocumentService.cs › DocumentService.GetInvoicePdfStream` | `GetUserFirmAsync` zwraca `null` | `UserHasNoAssociatedFirmException` | `400 Bad Request` | `"User has no associated firm."` |
| `WAL-02B` | PDF zostało pomyślnie wygenerowane | `DocumentController.cs › DocumentController.GetInvoicePdfStream` | `documentStreamDto.PdfContent == null` | brak wyjątku — sprawdzenie w kontrolerze | `400 Bad Request` | `"Failed to generate the PDF document."` |

> WAL-01B — wyjątek przechodzi przez ExceptionMiddleware (brak try/catch w kontrolerze dla API-29).
> WAL-02B — sprawdzenie bezpośrednio w kontrolerze po zwróceniu `DocumentStreamDto` przez serwis.

---

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Endpoint | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|---|
| `UserHasNoAssociatedFirmException` | API-28 | tak (kontroler) | `400 Bad Request` | `DocumentController.cs › GenerateDocument` (try/catch) |
| `UserHasNoAssociatedFirmException` | API-29 | tak (middleware) | `400 Bad Request` | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` |
| `NullReferenceException` (DocumentSeries!) | API-29 | nie | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all) |
| Wyjątki EF Core / infrastrukturalne | oba | nie | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all) |

> Pełen rejestr wyjątek→HTTP: `../../KATALOG_WYJATKOW.md`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze/akcji | `[Authorize(Roles = "User")]` na klasie `DocumentController` |
| Wymagana rola | `User` |
| Źródło tożsamości | `IUserService.GetCurrentUserId()` → `userId` |
| Token | JWT (`JwtBearerDefaults.AuthenticationScheme`) |

---

## 4. Uwagi bezpieczeństwa

- [UWAGA: `GenerateDocumentPdf` (API-28) ma własny `try { ... } catch(Exception ex) { return BadRequest(ex.Message); }`. Łapie KAŻDY wyjątek (nie tylko domenowy) i zwraca jego `Message` jako `BadRequest`. Może ujawnić wewnętrzne detale implementacji (np. ścieżki plików). Kotwica: `DocumentController.cs › DocumentController.GenerateDocument`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: `PdfGenerationService.GenerateInvoicePdf` ma wewnętrzny try/catch — błąd zapisu PDF na dysk jest połykany. Serwis zwraca `null`; `DocumentService.GeneratePdfDocument` ignoruje tę wartość i zwraca `documentRequestDto`. Kontroler zwraca `200 OK` pomimo nieudanego generowania. Kotwica: `PdfGenerationService.cs › PdfGenerationService.GenerateInvoicePdf`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: PDF zapisywany na dysku serwera pod ścieżką `<BaseDir>/Documents/Invoice_<N>.pdf`. Brak weryfikacji ścieżki, brak rotacji / czyszczenia starych plików. Kotwica: `PdfGenerationService.cs › PdfGenerationService.GenerateInvoicePdf`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: API-29 pobiera konto bankowe z pierwszego dokumentu firmy (`FirstOrDefaultAsync` bez `OrderBy`) — nie jest to konto bankowe dokumentu z requestu. Kotwica: `DocumentService.cs › DocumentService.GetInvoicePdfStream`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: Null-forgiving `documentRequestDto.DocumentSeries!.CurrentNumber.ToString()` — gdy `DocumentNumber == null` I `DocumentSeries == null` → `NullReferenceException → 500`. Kotwica: `DocumentService.cs › DocumentService.GetInvoicePdfStream`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
