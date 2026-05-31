# Algorytm: Generowanie PDF (QuestPDF)

| Atrybut | Wartość |
|---|---|
| ID | ALG-07 |
| Nazwa | PDF Generation (QuestPDF) |
| Kategoria | Generowanie dokumentów |
| Pliki | `DocumentService.cs`, `InvoiceDocument.cs`, `ProformaDocument.cs`, `StornoDocument.cs`, `InvoiceDocumentFactory.cs` |
| Biblioteka | `QuestPDF 2024.3.10 Community` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Generowanie pliku PDF faktury/proformy/storno na podstawie danych dokumentu z bazy danych. Dwa różne endpointy — jeden z błędem, drugi poprawny.

## Architektura

```
IInvoiceDocument (interface)
    ├── InvoiceDocument        (faktura zwykła)
    ├── ProformaDocument       (proforma)
    └── StornoDocument         (storno)

InvoiceDocumentFactory
    └── Create(documentTypeId) → IInvoiceDocument
```

## Endpoint 1: GenerateInvoicePdf — BŁĘDNY

```csharp
// DocumentService › GenerateInvoicePdf
// KRYTYCZNA ANOMALIA: hardkodowane new InvoiceDocument()
var document = new InvoiceDocument(documentData);
// ↑ Zawsze faktura zwykła, niezależnie od DocumentTypeId!
byte[] pdfBytes = document.GeneratePdf();
```

## Endpoint 2: GetPdfStream — POPRAWNY (z fabryką)

```csharp
// DocumentService › GetPdfStream
var document = await _unitOfWork.Documents.GetByIdWithDetailsAsync(documentId);
var invoiceDoc = InvoiceDocumentFactory.Create(document.DocumentTypeId, documentData);
// ↑ Poprawna fabryka: 1=Factura, 2=Proforma, 3=Storno

var stream = new MemoryStream();
invoiceDoc.GeneratePdf(stream);
stream.Position = 0;
return new FileStreamResult(stream, "application/pdf");
```

## InvoiceDocumentFactory (schemat)

```csharp
public static IInvoiceDocument Create(int documentTypeId, DocumentData data)
{
    return documentTypeId switch {
        1 => new InvoiceDocument(data),
        2 => new ProformaDocument(data),
        3 => new StornoDocument(data),
        _ => throw new InvalidDocumentTypeException()
    };
}
```

## QuestPDF — struktura dokumentu

```csharp
public class InvoiceDocument : IDocument
{
    public void Compose(IDocumentContainer container)
    {
        container.Page(page => {
            page.Header().Element(ComposeHeader);
            page.Content().Element(ComposeContent);
            page.Footer().Element(ComposeFooter);
        });
    }
}
```

## Anomalie

| # | Anomalia |
|---|---|
| PDF-01 | **KRYTYCZNE:** `GenerateInvoicePdf` hardkoduje `new InvoiceDocument()` — proformy i storna generują PDF jako zwykła faktura |
| PDF-02 | Dwie różne ścieżki generowania PDF z różnym zachowaniem — brak spójności |
| PDF-03 | Brak cache wygenerowanych PDF — każde żądanie generuje od nowa |
| PDF-04 | QuestPDF Community — przy przekroczeniu $1M przychodu wymagana licencja komercyjna |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
