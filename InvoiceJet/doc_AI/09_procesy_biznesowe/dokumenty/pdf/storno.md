# Szablon PDF — Storno / Faktura korygująca (DocumentTypeId = 3)

| Atrybut | Wartość |
|---|---|
| Klasa C# | `StornoInvoice` |
| Plik | `InvoiceJet.Infrastructure/Services/IQuestPDFDocument/StornoInvoice.cs` |
| Fabryka | `StornoDocumentFactory` |
| DocumentTypeId | `3` |
| Endpoint (poprawny) | [POST /Document/GetInvoicePdfStream](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) |

Struktura wspólna z fakturą i proformą: [wspolna_struktura.md](wspolna_struktura.md)

---

## Co jest unikalne dla storna

### Badge statusu (prawa część nagłówka)

Badge **stały**, nie zależy od `DocumentStatus`:

```csharp
e.Background(Colors.Yellow.Medium)
    .AlignCenter()
    .AlignMiddle()
    .Padding(5)
    .Text("Storno")
    .FontSize(14)
    .Bold();
```

| Tło | Tekst | Zależy od danych? |
|---|---|---|
| 🟡 `Colors.Yellow.Medium` | „Storno" | ❌ NIE — stały tekst |

---

### ⚠️ Negowanie wartości — kluczowa różnica

Storno jest jedynym typem, który neguje wszystkie wartości liczbowe. Jest to zaimplementowane bezpośrednio w szablonie przez negację (`-`):

#### Tabela pozycji — wiersz danych

```csharp
// StornoInvoice.cs — vs Invoice.cs (bez minusa)
table.Cell().AlignRight().Text($"{-item.Quantity}");    // MINUS
table.Cell().AlignRight().Text($"{-item.UnitPrice}");   // MINUS
table.Cell().AlignRight().Text($"{-value:F2}");         // MINUS
table.Cell().AlignRight().Text($"{-totalTVAItem:F2}"); // MINUS
```

#### Footer tabeli — sumy

```csharp
// StornoInvoice.cs
footer.Cell().Text($"{-subtotal:F2}");      // MINUS
footer.Cell().Text($"{-totalTVA:F2}");      // MINUS
footer.Cell().Text($"{-grandTotal:F2} lei"); // MINUS
```

#### Zestawienie: co jest negowane

| Kolumna / Pole | Formuła stornem | Formuła bez storna |
|---|---|---|
| Qt. | `-item.Quantity` | `+item.Quantity` |
| Unit price | `-item.UnitPrice` | `+item.UnitPrice` |
| Value | `-(UnitPrice × Quantity)` | `+(UnitPrice × Quantity)` |
| Total TVA | `-(TotalPrice − UnitPrice×Qty)` | `+(TotalPrice − UnitPrice×Qty)` |
| Subtotal | `-Σ(UnitPrice × Qty)` | `+Σ(UnitPrice × Qty)` |
| Total TVA footer | `-Σ(TotalPrice − UnitPrice×Qty)` | `+Σ(TotalPrice − UnitPrice×Qty)` |
| **Total pay** | `-grandTotal lei` | `+grandTotal lei` |

> **Uwaga:** negacja jest tylko **wizualna w szablonie** (`-item.Quantity` w tekście).
> Dane w bazie (`DocumentProduct.Quantity`, `DocumentProduct.UnitPrice`) są **przechowywane jako wartości dodatnie**. Storno nie zmienia danych w DB — tylko szablon PDF wyświetla je ze znakiem minus.

---

## Jak powstaje storno — kontekst

Storno tworzone jest przez endpoint [`PUT /Document/TransformToStorno`](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_TransformToStorno.md), który **kopiuje pozycje z oryginalnej faktury** do nowego dokumentu typu Storno. Dane w `DocumentProduct` są identyczne z oryginałem — negacja następuje dopiero w szablonie PDF.

---

## Różnice vs faktura i proforma

| Element | Faktura | Proforma | Storno |
|---|---|---|---|
| Badge | Paid🟢/Unpaid🔴 | „Proforma"🟡 | „Storno"🟡 |
| Qt. | `+Qty` | `+Qty` | **`-Qty`** |
| Unit price | `+price` | `+price` | **`-price`** |
| Value | `+value` | `+value` | **`-value`** |
| Total TVA | `+tva` | `+tva` | **`-tva`** |
| Subtotal | `+sub` | `+sub` | **`-sub`** |
| Total pay | `+grand` | `+grand` | **`-grand`** |
| Dane w DB | + dodatnie | + dodatnie | + dodatnie (negacja tylko w PDF!) |

---

## Anomalie specyficzne dla storna

| ID | Opis |
|---|---|
| PDF-04 | Tytuł `Invoice #<nr>` — storno nie ma własnego tytułu odróżniającego od faktury |
| STORNO-01 | Dane pozycji w DB przechowywane jako wartości **dodatnie** — negacja wyłącznie wizualna w szablonie. Deweloper/tester sprawdzający DB może być zdezorientowany. |

---

## Powiązane

- [Wspólna struktura](wspolna_struktura.md)
- [Faktura](faktura.md)
- [Proforma](proforma.md)
- [Algorytm: Transform to Storno](../../../03_algorytmy/ALG-08_TransformToStorno.md)
- [Endpoint: TransformToStorno](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_TransformToStorno.md)
- [Ekran: Lista storn](../../../01_ekrany/faktury_storno/lista_faktur_storno/ekran.md)
- [Ekran: Formularz storno](../../../01_ekrany/faktury_storno/dodaj_edytuj_fakture_storno/ekran.md)
