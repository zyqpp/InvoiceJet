# Wspólna struktura szablonu PDF

Wszystkie trzy typy (`Invoice`, `ProformaInvoice`, `StornoInvoice`) dziedziczą tę samą strukturę.
Różnice między typami opisane są w osobnych plikach: [faktura.md](faktura.md) · [proforma.md](proforma.md) · [storno.md](storno.md).

---

## 1. Przepływ danych (wspólny dla wszystkich typów)

```
Frontend → DocumentRequestDto
              ↓
Backend: DocumentService.GetInvoicePdfStream()
  1. Pobierz UserFirm aktywną dla zalogowanego usera
       → Firm → dto.Seller (wzbogacenie po stronie backendu)
  2. Pobierz BankAccount WHERE UserFirmId = activeUserFirmId (TOP 1)
       → dto.BankAccount (wzbogacenie po stronie backendu)
  3. InvoiceDocumentFactoryProvider.Create(DocumentTypeId, dto)
       → odpowiednia klasa szablonu
  4. QuestPDF: document.GeneratePdf(stream)
  5. FileStreamResult("application/pdf", "Invoice_{DocumentNumber}.pdf")
```

**Kluczowe:** `Seller` i `BankAccount` są **zawsze pobierane z bazy w momencie generowania**. Frontend nie wysyła danych sprzedawcy.

---

## 2. FullDocumentNumber (wspólna logika)

```csharp
// identyczna we wszystkich 3 klasach
if (Model.DocumentSeries != null)
    return SeriesName + CurrentNumber.ToString("D4");
else
    return Model.DocumentNumber;
```

| Wejście | Źródło | Tabela/Kolumna |
|---|---|---|
| `SeriesName` | `DocumentRequestDto.DocumentSeries.SeriesName` | `DocumentSeries.SeriesName` |
| `CurrentNumber` | `DocumentRequestDto.DocumentSeries.CurrentNumber` ⚠️ z frontendu | `DocumentSeries.CurrentNumber` |
| `DocumentNumber` (fallback) | `DocumentRequestDto.DocumentNumber` | `Document.DocumentNumber` |

---

## 3. Układ strony QuestPDF (wspólny)

```csharp
container.Page(page => {
    page.Margin(50);           // margines 50pt ze wszystkich stron
    page.Header().Element(ComposeHeader);
    page.Content().Element(ComposeContent);
    page.Footer().AlignCenter().Text(CurrentPageNumber / TotalPages);
});
```

---

## 4. HEADER — elementy wspólne

Dwie kolumny:
- **Lewa (RelativeItem):** tytuł + daty — patrz typ-specyficzny dla badge
- **Prawa (ConstantItem 100px):** badge statusu — **różny per typ**

### Elementy lewej kolumny (takie same we wszystkich):

| Element | Wartość | Źródło | Transformacja |
|---|---|---|---|
| Tytuł | `Invoice #<FullDocumentNumber>` | patrz §2 | FontSize 20, SemiBold, Blue.Medium |
| Issue date | `Issue date: {Model.IssueDate:d}` | `Document.IssueDate` | Format `d` (short date locale) |
| Due date | `Due date: {Model.DueDate:d}` | `Document.DueDate` | Tylko jeśli `DueDate.HasValue`; format `d` |

---

## 5. CONTENT — AddressComponent (wspólny)

Używany identycznie we wszystkich typach:

```csharp
row.RelativeItem().Component(new AddressComponent("From", Model.Seller, Model.BankAccount));
row.ConstantItem(50);   // odstęp
row.RelativeItem().Component(new AddressComponent("For", Model.Client));
```

### AddressComponent — pola i warunki wyświetlania

| Pole na PDF | Źródło C# | Tabela DB | Kolumna | Warunek |
|---|---|---|---|---|
| Tytuł sekcji | parametr `Title` | — | — | zawsze |
| Nazwa firmy | `Address.Name` | `Firm` | `Name` | zawsze |
| Adres | `Address.Address` | `Firm` | `Address` | zawsze |
| Miasto, okręg | `Address.City, Address.County` | `Firm` | `City`, `County` | zawsze |
| CUI | `Address.Cui` | `Firm` | `Cui` | `!IsNullOrEmpty(Cui)` |
| Reg. Com | `Address.RegCom` | `Firm` | `RegCom` | `!IsNullOrEmpty(RegCom)` |
| Bank (tylko From) | `BankAccount.BankName` | `BankAccount` | `BankName` | `BankAccount != null && !IsNullOrEmpty` |
| IBAN (tylko From) | `BankAccount.Iban` | `BankAccount` | `Iban` | `BankAccount != null && !IsNullOrEmpty` |

**From** = Seller (backend pobiera z `UserFirm.Firm` + `BankAccount`)
**For** = Client (z frontendu, bez konta bankowego)

---

## 6. Tabela produktów — nagłówek (wspólny)

```
| # | Product | Qt. | Unit price | Value | Total TVA |
```

Definicja kolumn QuestPDF:
```csharp
columns.ConstantColumn(25);   // #
columns.RelativeColumn(3);    // Product
columns.RelativeColumn();     // Qt.
columns.RelativeColumn();     // Unit price
columns.RelativeColumn();     // Value
columns.RelativeColumn();     // Total TVA
```

---

## 7. Obliczenia w szablonie (wspólna logika, różne znaki dla Storno)

Dla każdego wiersza:
```
value         = item.UnitPrice × item.Quantity
totalTVAItem  = item.TotalPrice − item.UnitPrice × item.Quantity
```

Footer tabeli:
```
subtotal  = Σ(item.UnitPrice × item.Quantity)
totalTVA  = Σ(item.TotalPrice − item.UnitPrice × item.Quantity)
grandTotal = subtotal + totalTVA
```

> Storno neguje wszystkie wartości — patrz [storno.md](storno.md).

### Źródła danych pozycji

| Pole | Tabela DB | Kolumna | Opis |
|---|---|---|---|
| `item.Name` | `Product` (via `DocumentProduct`) | `Name` | Nazwa z momentu wystawienia |
| `item.UnitPrice` | `DocumentProduct` | `UnitPrice` | **Snapshot** — cena z momentu wystawienia |
| `item.Quantity` | `DocumentProduct` | `Quantity` | Ilość (decimal) |
| `item.TotalPrice` | `DocumentProduct` | `TotalPrice` | Cena brutto pozycji — snapshot |

---

## 8. FOOTER strony (wspólny)

```csharp
page.Footer().AlignCenter().Text(text => {
    text.CurrentPageNumber();
    text.Span(" / ");
    text.TotalPages();
});
```

Wyświetla: `1 / 3`, `2 / 3`, itd.

---

## 9. Nazwa pliku PDF

```
Invoice_{DocumentNumber}.pdf
```

`DocumentNumber` = wartość z `DocumentStreamDto.DocumentNumber` (= `Document.DocumentNumber` z DB).

---

## 10. Anomalie wspólne

| ID | Opis |
|---|---|
| PDF-04 | Tytuł zawsze `Invoice #...` — proforma i storno mają ten sam tytuł co faktura |
| PDF-03 | Brak cache — PDF generowany od nowa przy każdym żądaniu |
| PDF-05 | `Document.TotalPrice` (DB) nie jest używane w szablonie — grandTotal wyliczany z pozycji |
| PDF-06 | BankAccount = pierwsze WHERE UserFirmId — brak wyboru konta przez usera |
| ALG02-03 | `CurrentNumber` pochodzi z frontendu — możliwy race condition na numer |

---

## Powiązane

| Typ | Dokument |
|---|---|
| Typy dokumentów | [faktura.md](faktura.md) · [proforma.md](proforma.md) · [storno.md](storno.md) |
| Algorytm | [ALG-07 PDF Generation](../../../03_algorytmy/ALG-07_PdfGeneration.md) |
| Algorytm | [ALG-05 Total Calculation](../../../03_algorytmy/ALG-05_DocumentTotalCalculation.md) |
| Model | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Model | [dbo.DocumentProduct](../../../05_model_danych/01_db/dbo/dbo.DocumentProduct.md) |
| Model | [dbo.Firm](../../../05_model_danych/01_db/dbo/dbo.Firm.md) |
| Model | [dbo.BankAccount](../../../05_model_danych/01_db/dbo/dbo.BankAccount.md) |
| DTO | [DocumentRequestDto DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
