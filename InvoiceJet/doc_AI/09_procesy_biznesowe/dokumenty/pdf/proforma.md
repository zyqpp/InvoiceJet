# Szablon PDF — Proforma (DocumentTypeId = 2)

| Atrybut | Wartość |
|---|---|
| Klasa C# | `ProformaInvoice` |
| Plik | `InvoiceJet.Infrastructure/Services/IQuestPDFDocument/ProformaInvoice.cs` |
| Fabryka | `ProformaDocumentFactory` |
| DocumentTypeId | `2` |
| Endpoint (poprawny) | [POST /Document/GetInvoicePdfStream](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) |

Struktura wspólna z fakturą i stornem: [wspolna_struktura.md](wspolna_struktura.md)

---

## Co jest unikalne dla proformy

### Badge statusu (prawa część nagłówka)

Badge **nie zależy od `DocumentStatus`** — jest zawsze stały:

```csharp
e.Background(Colors.Yellow.Darken3)
    .AlignCenter()
    .AlignMiddle()
    .Padding(5)
    .Text("Proforma")
    .FontSize(14)
    .Bold();
```

| Tło | Tekst | Zależy od danych? |
|---|---|---|
| 🟡 `Colors.Yellow.Darken3` | „Proforma" | ❌ NIE — stały tekst |

> W przeciwieństwie do faktury, status Paid/Unpaid **nie jest wyświetlany** na proformie — niezależnie od wartości `DocumentStatus`.

### Tabela pozycji — wartości

Identyczna z fakturą — wszystkie wartości **dodatnie** (bez negowania).

### Footer sumy — wartości

Identyczny z fakturą — wszystkie wartości **dodatnie**.

---

## Różnice vs faktura

| Element | Faktura | Proforma |
|---|---|---|
| Badge | Paid🟢 / Unpaid🔴 (z danych) | „Proforma" 🟡 (stały) |
| Tytuł nagłówka | `Invoice #<nr>` ⚠️ | `Invoice #<nr>` ⚠️ |
| Wartości tabeli | +dodatnie | +dodatnie |
| Klasa C# | `InvoiceDocument` | `ProformaInvoice` |

---

## Anomalie specyficzne dla proformy

| ID | Opis |
|---|---|
| PDF-04 | Tytuł `Invoice #<nr>` — proforma nie ma własnego tytułu, co może wprowadzać odbiorcę w błąd |
| PDF-01 | `GenerateDocumentPdf` generuje proformę jako `InvoiceDocument` (zwykła faktura) — badge i zachowanie faktury zamiast proformy |

---

## Powiązane

- [Wspólna struktura](wspolna_struktura.md)
- [Faktura](faktura.md)
- [Storno](storno.md)
- [Ekran: Lista proform](../../../01_ekrany/faktury_proforma/lista_faktur_proforma/ekran.md)
- [Ekran: Formularz proformy](../../../01_ekrany/faktury_proforma/dodaj_edytuj_fakture_proforma/ekran.md)
