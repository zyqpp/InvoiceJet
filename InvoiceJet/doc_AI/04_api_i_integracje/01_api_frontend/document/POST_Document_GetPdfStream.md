# POST /api/Document/GetInvoicePdfStream — Pobieranie PDF (strumień)

| Atrybut | Wartość |
|---|---|
| ID | API-29 |
| Metoda | POST |
| URL | `/api/Document/GetInvoicePdfStream` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentController.GetInvoicePdfStream` |
| Serwis | `IDocumentService.GetInvoicePdfStream` → `IPdfGenerationService.GetInvoicePdfStream` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Body (JSON) — `DocumentRequestDto`

Takie same pola jak w `POST_Document_Add.md`.

## Response

### 200 OK — plik PDF

```
Content-Type: application/pdf
Content-Disposition: attachment; filename="Invoice_{documentNumber}.pdf"
[binary PDF content]
```

Kontroler zwraca:
```csharp
return File(documentStreamDto.PdfContent, "application/pdf",
    $"Invoice_{documentStreamDto.DocumentNumber}.pdf");
```

### Błędy

| Status HTTP | Warunek |
|---|---|
| 400 Bad Request | `"Failed to generate the PDF document."` — gdy `PdfContent == null` |
| 400 Bad Request | `UserHasNoAssociatedFirmException` |

## Algorytm (serwis)

1. Pobierz aktywną `UserFirm` (właściciel) → `UserHasNoAssociatedFirmException` jeśli brak
2. Pobierz konto bankowe dokumentu (WHERE `UserFirmId == activeUserFirmId`) — pierwsze pasujące
3. Uzupełnij `documentRequestDto.Seller` = mapowanie `UserFirm.Firm → FirmDto`
4. Uzupełnij `documentRequestDto.BankAccount` = mapowanie `BankAccount → BankAccountDto`
5. `_pdfGenerationService.GetInvoicePdfStream(documentRequestDto)` → `byte[]`
6. Zwróć `DocumentStreamDto { DocumentNumber, PdfContent }`

**Factory pattern:** `GetInvoicePdfStream` używa factory (w przeciwieństwie do `GenerateInvoicePdf` który hardcodes `InvoiceDocument`).

## Zachowanie po stronie frontendu

`BaseInvoiceComponent.getInvoicePdfStream()`:
- Wywołuje endpoint z `responseType: 'blob'`
- Tworzy URL przez `URL.createObjectURL(blob)`
- Otwiera `PdfViewerComponent` (dialog `100vw × 90vh`) z `safeUrl`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
