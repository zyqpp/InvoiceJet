# Generowanie dokumentu PDF — Dane, modele i mapowania

## DTO

| Element | Rola |
|---|---|
| `DocumentRequestDto` | Wejście procesu i nośnik danych dla generatora PDF. |
| `FirmDto` (`Seller`) | Uzupełniane przez serwis na podstawie aktywnej firmy użytkownika. |

---

## Integracja PDF

| Element | Rola |
|---|---|
| `PdfGenerationService.GenerateInvoicePdf` | Tworzy dokument `InvoiceDocument` i generuje plik PDF. |
| `InvoiceDocument` | Implementacja `QuestPDF` dla faktury. |
