# Szablony dokumentów PDF — InvoiceJet

Dokumentacja budowy plików PDF generowanych przez QuestPDF.
Każdy typ dokumentu ma osobną klasę C#, ale współdzielą strukturę.

## Dokumenty w tym folderze

| Plik | Co opisuje |
|---|---|
| [wspolna_struktura.md](wspolna_struktura.md) | Wszystko co jest takie same dla wszystkich 3 typów: AddressComponent, tabela, stopka, przepływ danych, obliczenia |
| [faktura.md](faktura.md) | Specyfika faktury zwykłej (`Invoice.cs`) — badge Paid/Unpaid, klasa C# |
| [proforma.md](proforma.md) | Specyfika proformy (`ProformaInvoice.cs`) — badge „Proforma", różnica vs faktura |
| [storno.md](storno.md) | Specyfika storno (`StornoInvoice.cs`) — **negowanie wartości**, badge „Storno" |

## Skąd 3 typy?

```
InvoiceDocumentFactoryProvider
  └── Create(documentTypeId):
        1 → InvoiceDocumentFactory    → new InvoiceDocument(dto)
        2 → ProformaDocumentFactory   → new ProformaInvoice(dto)
        3 → StornoDocumentFactory     → new StornoInvoice(dto)
```

Klasy fabryki: `InvoiceDocumentFactory.cs`, `ProformaDocumentFactory.cs`, `StornoDocumentFactory.cs`.

## Macierz różnic

| Element | Faktura | Proforma | Storno |
|---|---|---|---|
| Klasa szablonu | `InvoiceDocument` | `ProformaInvoice` | `StornoInvoice` |
| Badge tekst | "Paid" / "Unpaid" | "Proforma" | "Storno" |
| Badge kolor | Zielony / Czerwony | Żółty ciemny | Żółty średni |
| Badge źródło | `DocumentStatus.Status` | stały tekst | stały tekst |
| Qt. w tabeli | `+item.Quantity` | `+item.Quantity` | **`-item.Quantity`** |
| Unit price w tabeli | `+item.UnitPrice` | `+item.UnitPrice` | **`-item.UnitPrice`** |
| Value w tabeli | `+(UnitPrice×Qty)` | `+(UnitPrice×Qty)` | **`-(UnitPrice×Qty)`** |
| Total TVA w tabeli | `+(TotalPrice-UnitP×Qty)` | `+(TotalPrice-UnitP×Qty)` | **`-(TotalPrice-UnitP×Qty)`** |
| Subtotal footer | `+subtotal` | `+subtotal` | **`-subtotal`** |
| Total TVA footer | `+totalTVA` | `+totalTVA` | **`-totalTVA`** |
| GrandTotal footer | `+grandTotal` | `+grandTotal` | **`-grandTotal`** |
| Tytuł nagłówka | `Invoice #<nr>` ⚠️ | `Invoice #<nr>` ⚠️ | `Invoice #<nr>` ⚠️ |

⚠️ Tytuł `Invoice #` pojawia się na wszystkich typach — w tym na proformach i stornach.
To anomalia — patrz [wspolna_struktura.md §anomalie](wspolna_struktura.md#anomalie).

## Powiązane

- [Algorytm ALG-07 PDF Generation](../../../03_algorytmy/ALG-07_PdfGeneration.md)
- [Endpoint GetInvoicePdfStream](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md)
- [Endpoint GenerateDocumentPdf](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GeneratePdf.md)
- [Pełny opis (legacy, nierozdzielony)](../szablon_dokumentu_pdf.md)
- [Dokumentacja użytkownika](../../../../doc_user/01_ekrany/13_dokument_pdf.md)
