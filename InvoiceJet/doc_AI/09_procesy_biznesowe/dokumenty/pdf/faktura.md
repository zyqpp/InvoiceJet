# Szablon PDF — Faktura zwykła (DocumentTypeId = 1)

| Atrybut | Wartość |
|---|---|
| Klasa C# | `InvoiceDocument` |
| Plik | `InvoiceJet.Infrastructure/Services/IQuestPDFDocument/Invoice.cs` |
| Fabryka | `InvoiceDocumentFactory` |
| DocumentTypeId | `1` |
| Endpoint (poprawny) | [POST /Document/GetInvoicePdfStream](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) |

Struktura wspólna z proformą i stornem: [wspolna_struktura.md](wspolna_struktura.md)

---

## Co jest unikalne dla faktury

### Badge statusu (prawa część nagłówka)

Badge zmienia się dynamicznie w zależności od wartości `DocumentStatus.Status`:

```csharp
if (Model.DocumentStatus?.Status == "Paid")
{
    e.Background(Colors.Green.Medium).Text("Paid");
}
else
{
    e.Background(Colors.Red.Medium).Text("Unpaid");
}
```

| Wartość `DocumentStatus.Status` | Tło | Tekst | Źródło |
|---|---|---|---|
| `"Paid"` | 🟢 `Colors.Green.Medium` | „Paid" | `DocumentStatus.Status` |
| `"Unpaid"` (lub cokolwiek innego) | 🔴 `Colors.Red.Medium` | „Unpaid" | warunek `else` |
| `null` | 🔴 `Colors.Red.Medium` | „Unpaid" | warunek `else` (null safety) |

**Źródło `DocumentStatus`:**
- Tabela: [`dbo.DocumentStatus`](../../../05_model_danych/01_db/dbo/dbo.DocumentStatus.md)
- Kolumna: `Status` (string)
- Pobierane przez: `DocumentRequestDto.DocumentStatus.Status`

### Tabela pozycji — wartości

Wszystkie wartości **dodatnie** (bez negowania):

```csharp
var value        = item.UnitPrice * item.Quantity;
var totalTVAItem = item.TotalPrice - item.UnitPrice * item.Quantity;

table.Cell().AlignRight().Text($"{item.Quantity}");
table.Cell().AlignRight().Text($"{item.UnitPrice}");
table.Cell().AlignRight().Text($"{value:F2}");
table.Cell().AlignRight().Text($"{totalTVAItem:F2}");
```

### Footer sumy — wartości

Wszystkie wartości **dodatnie**:

```csharp
var subtotal   = Model.Products.Sum(x => x.UnitPrice * x.Quantity);
var totalTVA   = Model.Products.Sum(x => x.TotalPrice - x.UnitPrice * x.Quantity);
var grandTotal = subtotal + totalTVA;

// Wyświetlane bez negowania
footer.Cell().Text($"{subtotal:F2}");
footer.Cell().Text($"{totalTVA:F2}");
footer.Cell().Text($"{grandTotal:F2} lei");  // 16px Bold
```

---

## Anomalie specyficzne dla faktury

| ID | Opis |
|---|---|
| PDF-01 | `GenerateDocumentPdf` (drugi endpoint) hardcodes `new InvoiceDocument()` — proformy i storna generowane jako faktura zwykła |

---

## Powiązane

- [Wspólna struktura](wspolna_struktura.md)
- [Proforma](proforma.md)
- [Storno](storno.md)
- [Ekran: Lista faktur](../../../01_ekrany/faktury/lista_faktur/ekran.md)
- [Ekran: Formularz faktury](../../../01_ekrany/faktury/dodaj_edytuj_fakture/ekran.md)
