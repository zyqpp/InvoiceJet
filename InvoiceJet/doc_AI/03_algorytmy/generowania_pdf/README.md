# generowania_pdf — Algorytmy generowania PDF

Algorytmy odpowiedzialne za generowanie plików PDF faktur, faktur pro-forma i faktur storno przy użyciu biblioteki QuestPDF.

## Drzewo zawartości

```
generowania_pdf/
├── README.md
├── generuj_pdf_na_dysk.md       ← GenerateInvoicePdf — BUG: hardcoded InvoiceDocument (A-KRIT-04)
└── generuj_pdf_stream.md        ← GetPdfStream — poprawna ścieżka z InvoiceDocumentFactory
```

## Kluczowe dokumenty

- [`generuj_pdf_na_dysk.md`](generuj_pdf_na_dysk.md) — **zawiera krytyczny błąd A-KRIT-04**: hardkodowane `new InvoiceDocument()` niezależnie od typu dokumentu.
- [`generuj_pdf_stream.md`](generuj_pdf_stream.md) — poprawna implementacja używająca `InvoiceDocumentFactory.Create()`.

## Powiązane katalogi

- [`../../02_procesy/dokumenty/generuj_pdf/`](../../02_procesy/dokumenty/generuj_pdf/) — proces techniczny generowania PDF
- [`../../04_api_i_integracje/01_api_frontend/document/`](../../04_api_i_integracje/01_api_frontend/document/) — endpointy PDF

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
