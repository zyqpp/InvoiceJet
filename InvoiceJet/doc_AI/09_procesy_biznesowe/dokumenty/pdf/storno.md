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

> **Potwierdzone w kodzie:** negacja jest tylko **wizualna w szablonie** (`-item.Quantity` w tekście).
> Dane w bazie (`DocumentProduct.Quantity`, `DocumentProduct.UnitPrice`) są **przechowywane jako wartości dodatnie**.
>
> Wynika to z architektury `TransformToStorno`: operacja zmienia **wyłącznie** `DocumentTypeId = 3` — nie tworzy nowego dokumentu, nie neguje żadnych wartości w DB.
> → [ALG-08 TransformToStorno](../../../03_algorytmy/ALG-08_TransformToStorno.md) — sekcja „Czym jest storno w InvoiceJet"

---

## Jak powstaje storno — kontekst (zweryfikowany)

Storno tworzone jest przez endpoint [`PUT /Document/TransformToStorno`](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_TransformToStorno.md).

> ⚠️ **Korekta wcześniejszej dokumentacji:** storno **NIE kopiuje pozycji** do nowego dokumentu. Operacja modyfikuje **istniejący** dokument (fakturę), zmieniając tylko jego `DocumentTypeId` z `1` na `3`. Nie powstaje żaden nowy rekord — oryginalny dokument zmienia klasyfikację.

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
| STORNO-06 | **ARCHITEKTONICZNIE:** storno to MUTACJA oryginału, nie nowy dokument — brak referencji storno→oryginał, brak możliwości wyświetlenia obu jednocześnie, numer dokumentu niezmieniony |
| STORNO-07 | Wartości w DB zawsze dodatnie — przy analizie bazy danych saldo storn wygląda na sumę dodatnią. Ujemne wartości na PDF to wyłącznie efekt wizualny szablonu |
| STORNO-03 | Numer dokumentu po transform pozostaje bez zmian (np. `FV0001` zamiast `STORNO0001`) |
| STORNO-04 | `DocumentStatusId` nie jest resetowany — storno może mieć status „Paid" |

---

## Powiązane

- [Wspólna struktura](wspolna_struktura.md)
- [Faktura](faktura.md)
- [Proforma](proforma.md)
- [Algorytm: Transform to Storno](../../../03_algorytmy/ALG-08_TransformToStorno.md)
- [Endpoint: TransformToStorno](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_TransformToStorno.md)
- [Ekran: Lista storn](../../../01_ekrany/faktury_storno/lista_faktur_storno/ekran.md)
- [Ekran: Formularz storno](../../../01_ekrany/faktury_storno/dodaj_edytuj_fakture_storno/ekran.md)
