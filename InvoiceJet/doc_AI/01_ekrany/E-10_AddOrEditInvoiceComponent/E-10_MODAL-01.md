# MODAL-E10-01 — PdfViewerComponent

| Pole | Wartość |
|---|---|
| ID | MODAL-E10-01 |
| Ekran nadrzędny | [E-10 Formularz faktury](E-10_ekran.md) |
| Wersja | 1.0 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| Otwierany przez | [OP-E10-04 Preview PDF](E-10_OP-04.md) |
| Komponent | `PdfViewerComponent` |
| Parametr wejściowy | `{ pdfUrl: string }` — blob URL (`URL.createObjectURL(blob)`) |
| Wymiary | `width: 100vw`, `height: 90vh` |
| Zamykanie | `disableClose: true` — zamykany tylko przyciskiem wewnątrz |

## Powiązania z kodem

`PdfViewerComponent` w [`pdf-viewer.component.ts`](../../../../InvoiceJetUI/src/app/components/pdf-viewer/pdf-viewer.component.ts)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Wydzielony z E-10_ekran.md. |
