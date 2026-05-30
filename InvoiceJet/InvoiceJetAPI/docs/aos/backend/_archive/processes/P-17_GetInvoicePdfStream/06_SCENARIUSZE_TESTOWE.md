# Pobranie strumienia PDF faktury — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Pobranie PDF | Aktywna firma istnieje, generator zwraca bytes. | `200 OK`, odpowiedź ma `Content-Type: application/pdf` i nazwę pliku `Invoice_<nr>.pdf`. |

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Brak aktywnej firmy | `GetUserFirmAsync` zwraca `null`. | `400 Bad Request`, komunikat wyjątku. |
| TC-N02 | Brak strumienia PDF | `PdfGenerationService.GetInvoicePdfStream()` zwraca `null`. | `400 Bad Request`, komunikat `Failed to generate the PDF document.` |
