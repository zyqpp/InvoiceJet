# Komponent: Podgląd PDF (PDF Viewer)

| Atrybut | Wartość |
|---|---|
| ID | DIALOG-05 |
| Komponent | `PdfViewerComponent` |
| Plik | `src/app/components/pdf-viewer/pdf-viewer.component.ts` |
| Otwierany z | EKRAN-09, EKRAN-11, EKRAN-13 (listy dokumentów) |
| Typ | Komponent routingowy lub dialog |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Komponent wyświetlania podglądu wygenerowanego PDF faktury. Wywołuje API pobierające strumień PDF i renderuje go w przeglądarce.

## Przepływ

1. Użytkownik klika "Podgląd" / "Pobierz PDF" przy dokumencie
2. Wywołanie `POST /api/Document/GetPdfStream` z `{documentId}`
3. Odpowiedź to `application/pdf` (FileStreamResult)
4. Komponent renderuje PDF w `<iframe>` lub `<object>` albo otwiera nową kartę (`window.open`)

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Pobranie strumienia PDF | `POST /api/Document/GetPdfStream` |

## Anomalie

| # | Anomalia |
|---|---|
| PDF-01 | `GenerateInvoicePdf` (endpoint osobny) hardkoduje `new InvoiceDocument()` — zawsze generuje fakturę zwykłą niezależnie od `DocumentTypeId`. `GetPdfStream` natomiast używa fabryki `InvoiceDocumentFactory` i generuje właściwy typ |
| PDF-02 | Brak walidacji po stronie frontendu czy dokument ma już PDF — zawsze wywołuje API |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
