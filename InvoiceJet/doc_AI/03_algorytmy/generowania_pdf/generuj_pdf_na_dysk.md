# Generuj PDF na dysk — GenerateInvoicePdf (BUG A-KRIT-04) — algorytm

| Pole | Wartość |
|---|---|
| ID dokumentu | ALG-GenerowaniaPdf-GenerujPdfNaDysk |
| Typ dokumentu | algorytm |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Algorytm generuje plik PDF faktury i zwraca go jako tablicę bajtów (`byte[]`). Jest to **pierwsza z dwóch ścieżek generowania PDF** w systemie InvoiceJet. Zawiera **krytyczny błąd A-KRIT-04**: niezależnie od typu dokumentu (faktura, proforma, storno) zawsze tworzy obiekt `InvoiceDocument`, co skutkuje generowaniem błędnego szablonu PDF dla proform i faktur storno.

## Cel algorytmu

Wygenerowanie pliku PDF dokumentu handlowego (faktura/proforma/storno) i zwrócenie jego zawartości jako `byte[]` do dalszego przekazania klientowi HTTP.

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| ID algorytmu | ALG-GenerowaniaPdf-GenerujPdfNaDysk |
| Kategoria | generowania_pdf |
| Wejście | `documentId: int` — identyfikator dokumentu z bazy danych |
| Wyjście | `byte[]` — zawartość pliku PDF |
| Złożoność (orientacyjna) | O(n) — zależna od liczby pozycji dokumentu |
| Gdzie wywoływany | `DocumentService.GenerateInvoicePdf(int documentId)` |
| Powiązana metoda w kodzie | `DocumentService.GenerateInvoicePdf()` |

## Opis krok po kroku

1. Pobierz dane dokumentu z bazy danych przez `_unitOfWork.Documents.GetByIdWithDetailsAsync(documentId)`.
2. Zmapuj dane dokumentu do obiektu `DocumentData` (DTO dla QuestPDF).
3. **[BŁĄD A-KRIT-04]** Zawsze tworzy obiekt `InvoiceDocument` niezależnie od `DocumentTypeId`:
   ```csharp
   var document = new InvoiceDocument(documentData);
   // ↑ Hardkodowane — niezależnie od DocumentTypeId!
   // Powinno być: InvoiceDocumentFactory.Create(document.DocumentTypeId, documentData)
   ```
4. Wywołaj `document.GeneratePdf()` — QuestPDF renderuje PDF do pamięci.
5. Zwróć `byte[]` z zawartością PDF.

## Skutek błędu A-KRIT-04

| DocumentTypeId | Oczekiwany szablon PDF | Faktyczny szablon PDF |
|---|---|---|
| 1 (Faktura) | InvoiceDocument | InvoiceDocument (poprawnie) |
| 2 (Proforma) | ProformaDocument | **InvoiceDocument (BŁĄD!)** |
| 3 (Storno) | StornoDocument | **InvoiceDocument (BŁĄD!)** |

Użytkownicy generujący PDF przez ten endpoint zawsze otrzymują szablon faktury zwykłej, nawet dla pro-form i faktur storno.

## Architektura QuestPDF (kontekst)

```
IInvoiceDocument (interface)
    ├── InvoiceDocument        ← zawsze używane (błąd)
    ├── ProformaDocument       ← nigdy nie używane przez ten endpoint
    └── StornoDocument         ← nigdy nie używane przez ten endpoint

InvoiceDocumentFactory         ← pomijane przez ten endpoint
    └── Create(documentTypeId) → IInvoiceDocument
```

## Poprawna implementacja (referencyjna)

Zob. [`generuj_pdf_stream.md`](generuj_pdf_stream.md) — implementacja z `InvoiceDocumentFactory`.

```csharp
// Prawidłowe — z fabryką
var invoiceDoc = InvoiceDocumentFactory.Create(document.DocumentTypeId, documentData);
byte[] pdfBytes = invoiceDoc.GeneratePdf();
```

## Przypadki brzegowe

| Przypadek | Dane wejściowe | Oczekiwane zachowanie |
|---|---|---|
| Dokument nie istnieje | `documentId` bez rekordu w DB | `DocumentNotFoundException` → 404 |
| DocumentTypeId = 2 (Proforma) | Proforma | Generowany PDF jako faktura zwykła (błąd A-KRIT-04) |
| DocumentTypeId = 3 (Storno) | Storno | Generowany PDF jako faktura zwykła (błąd A-KRIT-04) |
| Brak pozycji dokumentu | Dokument bez `DocumentProduct` | QuestPDF generuje PDF z pustą tabelą pozycji |

## Powiązania

- Wywoływany z procesu: [`../../02_procesy/dokumenty/generuj_pdf/proces.md`](../../02_procesy/dokumenty/generuj_pdf/proces.md)
- Wywoływany z endpointu: [`../../04_api_i_integracje/01_api_frontend/document/`](../../04_api_i_integracje/01_api_frontend/document/) — endpoint `GenerateInvoicePdf`
- Powiązane algorytmy: [`generuj_pdf_stream.md`](generuj_pdf_stream.md) — poprawna alternatywna ścieżka

## Powiązania z kodem

- Klasa implementująca: `InvoiceJet.Application/Services/DocumentService.cs`
- Metoda: `DocumentService.GenerateInvoicePdf(int documentId)`
- Biblioteka: `QuestPDF 2024.3.10 Community`
- Klasy PDF: `InvoiceJet.Application/Documents/InvoiceDocument.cs`, `ProformaDocument.cs`, `StornoDocument.cs`
- Fabryka (pomijana): `InvoiceJet.Application/Documents/InvoiceDocumentFactory.cs`

## Wątpliwości i braki

- **PDF-01 [KRYTYCZNE]:** Hardkodowane `new InvoiceDocument()` zamiast `InvoiceDocumentFactory.Create(documentTypeId, data)`. Błąd dotyczy każdego żądania PDF dla proform i faktur storno. Wymaga naprawy przed wdrożeniem produkcyjnym.
- **PDF-02:** Dwie różne ścieżki generowania PDF (`GenerateInvoicePdf` i `GetPdfStream`) z różnym zachowaniem — brak spójności API. Czy obie ścieżki są potrzebne? Rozważyć konsolidację do jednej.
- **PDF-03:** Brak cache wygenerowanych PDF — każde żądanie generuje PDF od nowa (obciążenie CPU).
- **PDF-04:** QuestPDF Community Edition — przy przekroczeniu $1M rocznego przychodu firmy wymagana licencja komercyjna.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — wydzielona z ALG-07_PdfGeneration.md (ścieżka GenerateInvoicePdf). |
