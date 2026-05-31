# Szablon dokumentu PDF — budowa i źródła danych

| Atrybut | Wartość |
|---|---|
| Dotyczy | Faktura / Proforma / Storno |
| Biblioteka | QuestPDF 2024.3.10 Community |
| Klasy szablonów | `Invoice.cs`, `ProformaInvoice.cs`, `StornoInvoice.cs` |
| Komponent adresu | `AddressComponent.cs` |
| Fabryka | `InvoiceDocumentFactory`, `ProformaDocumentFactory`, `StornoDocumentFactory` |
| Endpoint (poprawny) | [`POST /api/Document/GetInvoicePdfStream`](../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) |
| Endpoint (błędny) | [`POST /api/Document/GenerateDocumentPdf`](../../04_api_i_integracje/01_api_frontend/document/POST_Document_GeneratePdf.md) |
| Algorytm PDF | [ALG-07 PDF Generation](../../03_algorytmy/ALG-07_PdfGeneration.md) |
| Algorytm liczenia sum | [ALG-05 Document Total Calculation](../../03_algorytmy/ALG-05_DocumentTotalCalculation.md) |
| Algorytm numerowania | [ALG-02 Document Number Generation](../../03_algorytmy/ALG-02_DocumentNumberGeneration.md) |
| Ostatnia walidacja | 2026-05-31 (na podstawie kodu źródłowego) |

---

## 1. Dwa endpointy — dwa różne zachowania

> ⚠️ **KRYTYCZNA ANOMALIA:** Istnieją dwa endpointy PDF i jedno z nich jest błędne.

| Endpoint | Zachowanie | Wada |
|---|---|---|
| `POST GetInvoicePdfStream` ✅ | Używa fabryki → poprawny typ dokumentu | Poprawny — używaj tego |
| `POST GenerateDocumentPdf` ❌ | Hardcodes `new InvoiceDocument()` | Zawsze generuje jako zwykła faktura, niezależnie od `DocumentTypeId`; PDF zapisuje na dysk serwera, klient nie dostaje pliku |

Frontend używa **obu**: `Preview PDF` → GetInvoicePdfStream, `Generate PDF` → GenerateDocumentPdf.

---

## 2. Przepływ danych do PDF (endpoint GetInvoicePdfStream)

```
Frontend (BaseInvoiceComponent)
  └── DocumentRequestDto (formularz)
        ↓ POST /api/Document/GetInvoicePdfStream
Backend (DocumentService.GetInvoicePdfStream)
  ├── 1. Pobierz aktywną UserFirm dla zalogowanego usera
  │       → UserHasNoAssociatedFirmException jeśli brak
  ├── 2. Wzbogać DTO: DocumentRequestDto.Seller = UserFirm.Firm (mapowanie AutoMapper)
  ├── 3. Wzbogać DTO: DocumentRequestDto.BankAccount = pierwsze BankAccount
  │       WHERE BankAccount.UserFirmId == activeUserFirmId
  ├── 4. InvoiceDocumentFactoryProvider.Create(DocumentTypeId, enrichedDto)
  │       → 1 = InvoiceDocument
  │       → 2 = ProformaInvoice
  │       → 3 = StornoInvoice
  └── 5. QuestPDF: document.GeneratePdf(stream)
        → FileStreamResult("application/pdf", "Invoice_{DocumentNumber}.pdf")
```

**Kluczowe:** Seller i BankAccount są **zawsze pobierane z bazy w momencie generowania** (nie z frontendu) — gwarantuje aktualne dane firmy na PDF.

---

## 3. Źródła danych każdego pola w szablonie

### 3.1 Numer dokumentu (`FullDocumentNumber`)

```
IF DocumentSeries != null:
    FullDocumentNumber = SeriesName + CurrentNumber.ToString("D4")
    przykład: "FV" + 5 → "FV0005"
ELSE:
    FullDocumentNumber = Model.DocumentNumber  (z tabeli Document.DocumentNumber)
```

| Pole | Źródło DB | Tabela | Kolumna |
|---|---|---|---|
| `SeriesName` | z requestu (frontend) | `DocumentSeries` | `SeriesName` |
| `CurrentNumber` | z requestu (frontend) ⚠️ | `DocumentSeries` | `CurrentNumber` |
| `DocumentNumber` (fallback) | z requestu (wygenerowany przy AddDocument) | `Document` | `DocumentNumber` |

> ⚠️ `CurrentNumber` pochodzi z frontendu — możliwy race condition ([ALG-02](../../03_algorytmy/ALG-02_DocumentNumberGeneration.md)).

---

### 3.2 Sekcja HEADER

| Pole na PDF | Wartość | Źródło | Transformacja |
|---|---|---|---|
| Tytuł | `Invoice #<FullDocumentNumber>` | patrz §3.1 | Konkatenacja SeriesName + D4 number |
| Issue date | `Model.IssueDate` | `Document.IssueDate` | Format `d` (locale date) |
| Due date | `Model.DueDate` | `Document.DueDate` | Format `d`; nie wyświetla się jeśli null |
| Badge (Faktura) | "Paid" zielony / "Unpaid" czerwony | `DocumentStatus.Status` | Porównanie string "Paid" |
| Badge (Proforma) | "Proforma" żółty | stały tekst | brak |
| Badge (Storno) | "Storno" żółty | stały tekst | brak |

**Kolor badge:**
- Faktura opłacona: `Colors.Green.Medium` + "Paid"
- Faktura nieopłacona: `Colors.Red.Medium` + "Unpaid"
- Proforma: `Colors.Yellow.Darken3` + "Proforma"
- Storno: `Colors.Yellow.Medium` + "Storno"

---

### 3.3 Sekcja FROM (sprzedawca) — `AddressComponent("From", Seller, BankAccount)`

> Dane pobierane z bazy przez backend, NIE z frontendu.

| Pole na PDF | Źródło (C#) | Tabela | Kolumna | Warunkowe |
|---|---|---|---|---|
| Nazwa firmy | `Seller.Name` | `Firm` | `Name` | zawsze |
| Adres | `Seller.Address` | `Firm` | `Address` | zawsze |
| Miasto, okręg | `Seller.City`, `Seller.County` | `Firm` | `City`, `County` | zawsze (format: "City, County") |
| CUI | `Seller.Cui` | `Firm` | `Cui` | tylko jeśli `!IsNullOrEmpty` |
| Reg. Com | `Seller.RegCom` | `Firm` | `RegCom` | tylko jeśli `!IsNullOrEmpty` |
| Nazwa banku | `BankAccount.BankName` | `BankAccount` | `BankName` | tylko jeśli BankAccount != null i `!IsNullOrEmpty` |
| IBAN | `BankAccount.Iban` | `BankAccount` | `Iban` | tylko jeśli BankAccount != null i `!IsNullOrEmpty` |

**Pobieranie BankAccount:** backend wyszukuje `BankAccount WHERE UserFirmId = activeUserFirmId` — **pierwsze** pasujące konto.

---

### 3.4 Sekcja FOR (nabywca) — `AddressComponent("For", Client)`

> Dane z frontendu (z DocumentRequestDto.Client).

| Pole na PDF | Źródło (C#) | Tabela | Kolumna | Warunkowe |
|---|---|---|---|---|
| Nazwa firmy | `Client.Name` | `Firm` (Client) | `Name` | zawsze |
| Adres | `Client.Address` | `Firm` | `Address` | zawsze |
| Miasto, okręg | `Client.City`, `Client.County` | `Firm` | `City`, `County` | zawsze |
| CUI | `Client.Cui` | `Firm` | `Cui` | tylko jeśli `!IsNullOrEmpty` |
| Reg. Com | `Client.RegCom` | `Firm` | `RegCom` | tylko jeśli `!IsNullOrEmpty` |
| BankAccount | — | — | — | **BRAK** — blok For nie zawiera konta bankowego |

---

### 3.5 Tabela produktów — nagłówek i wiersze

**Kolumny tabeli:**

| Kolumna PDF | Opis | Źródło danych | Obliczone? |
|---|---|---|---|
| `#` | Numer porządkowy | licznik pętli (1, 2, 3…) | TAK — licznik pętli |
| `Product` | Nazwa produktu | `DocumentProduct.Product.Name` → `item.Name` | NIE — wprost z DB |
| `Qt.` | Ilość | `DocumentProduct.Quantity` → `item.Quantity` | NIE (Storno: `-item.Quantity`) |
| `Unit price` | Cena jednostkowa netto | `DocumentProduct.UnitPrice` → `item.UnitPrice` | NIE (Storno: `-item.UnitPrice`) |
| `Value` | Wartość netto wiersza | `item.UnitPrice × item.Quantity` | **TAK** — obliczane w szablonie |
| `Total TVA` | Kwota VAT wiersza | `item.TotalPrice - item.UnitPrice × item.Quantity` | **TAK** — obliczane w szablonie |

**Uwaga storno:** `Qt.`, `Unit price`, `Value`, `Total TVA` wyświetlane są ze znakiem minus (`-item.Quantity` itd.).

---

### 3.6 Podsumowanie tabeli (footer)

| Wiersz | Kolumna | Formuła | Obliczone |
|---|---|---|---|
| Row 1 | "Subtotal:" | `Σ(UnitPrice × Quantity)` dla wszystkich pozycji | **TAK** w szablonie |
| Row 1 | TVA kolumna | `Σ(TotalPrice - UnitPrice × Quantity)` | **TAK** w szablonie |
| Row 2 | "Total pay:" | `Subtotal + TotalTVA` + " lei" | **TAK** w szablonie (16px bold) |

**Storno:** wszystkie wartości są negowane (`-subtotal`, `-totalTVA`, `-grandTotal`).

> ⚠️ `TotalPrice` w tabeli `Document` (suma brutto całości) **NIE** jest używane w szablonie do wyświetlenia — grandTotal jest wyliczany od nowa z pozycji.

---

### 3.7 Stopka strony (page footer)

| Pole | Wartość |
|---|---|
| Numer strony | `CurrentPageNumber / TotalPages` (wyrównanie do środka) |

---

## 4. Zapytania DB zaangażowane w generowanie PDF

### Zapytanie 1: Aktywna firma użytkownika (Seller)

```sql
SELECT f.*, uf.*
FROM UserFirm uf
JOIN Firm f ON uf.FirmId = f.Id
WHERE uf.UserId = @userId
  AND uf.IsActive = 1  -- lub analogiczna logika aktywności
```

Tabele: [`dbo.UserFirm`](../../05_model_danych/01_db/dbo/dbo.UserFirm.md), [`dbo.Firm`](../../05_model_danych/01_db/dbo/dbo.Firm.md)

### Zapytanie 2: Konto bankowe (BankAccount)

```sql
SELECT TOP 1 *
FROM BankAccount
WHERE UserFirmId = @activeUserFirmId
```

Tabela: [`dbo.BankAccount`](../../05_model_danych/01_db/dbo/dbo.BankAccount.md)

### Dane klienta i produktów

Pobierane **z DocumentRequestDto** przekazanego z frontendu — nie ma dodatkowego zapytania do DB dla klienta i pozycji.

---

## 5. Co jest obliczane w szablonie (nie pochodzi z DB)

| Wartość | Formuła | Gdzie |
|---|---|---|
| `Value` (wartość netto wiersza) | `UnitPrice × Quantity` | szablon, każdy wiersz |
| `Total TVA` (VAT wiersza) | `TotalPrice - UnitPrice × Quantity` | szablon, każdy wiersz |
| `Subtotal` | `Σ(UnitPrice × Quantity)` | szablon, footer |
| `TotalTVA` (suma VAT) | `Σ(TotalPrice - UnitPrice × Quantity)` | szablon, footer |
| `GrandTotal` | `Subtotal + TotalTVA` | szablon, footer |
| `FullDocumentNumber` | `SeriesName + CurrentNumber.D4` | właściwość klasy szablonu |
| Numer wiersza `#` | licznik pętli | szablon |
| Negacja dla Storno | `-wartość` | szablon Storno |

**Co NIE jest obliczane — pochodzi wprost z DB:**
- Nazwa produktu (`DocumentProduct.Product.Name`)
- Cena jednostkowa netto (`DocumentProduct.UnitPrice`) — snapshot z momentu wystawienia
- Ilość (`DocumentProduct.Quantity`)
- Stawka VAT (`DocumentProduct.VatRate`) — **nie używana** w szablonie, VAT wyliczany z różnicy TotalPrice-UnitPrice×Qty
- Daty wystawienia i płatności
- Status płatności
- Dane adresowe

---

## 6. Snapshot cen — ważna właściwość

`DocumentProduct.UnitPrice` i `DocumentProduct.TotalPrice` to **wartości z momentu wystawienia dokumentu** (snapshot). Zmiana ceny produktu w katalogu (`Product.Price`) **nie wpływa** na wydrukowane PDF już wystawionych dokumentów.

Tabela: [`dbo.DocumentProduct`](../../05_model_danych/01_db/dbo/dbo.DocumentProduct.md)

---

## 7. Różnice między typami dokumentów

| Element | Faktura | Proforma | Storno |
|---|---|---|---|
| Tytuł nagłówka | `Invoice #<nr>` | `Invoice #<nr>` | `Invoice #<nr>` |
| Badge kolor | Zielony (Paid) / Czerwony (Unpaid) | Żółty ciemny | Żółty średni |
| Badge tekst | "Paid" / "Unpaid" | "Proforma" | "Storno" |
| Wartości pozycji | dodatnie | dodatnie | **ujemne** (negowane) |
| Footer sumy | dodatnie | dodatnie | **ujemne** (negowane) |
| Klasa C# | `InvoiceDocument` | `ProformaInvoice` | `StornoInvoice` |

> ⚠️ Tytuł `Invoice #` pojawia się na **wszystkich typach** — w tym na proformach i stornach.

---

## 8. Nazwa pliku PDF

```
Invoice_{DocumentNumber}.pdf
```

Gdzie `DocumentNumber` = wartość z `DocumentStreamDto.DocumentNumber` (przechowywana w [`Document.DocumentNumber`](../../05_model_danych/01_db/dbo/dbo.Document.md)).

---

## 9. Anomalie

| ID | Opis | Dotyczy |
|---|---|---|
| PDF-01 | `GenerateDocumentPdf` hardcodes `new InvoiceDocument()` — proformy i storna generują PDF jako zwykła faktura | endpoint GenerateDocumentPdf |
| PDF-02 | Dwa endpointy z różnym zachowaniem — frontend używa obu | architektura |
| PDF-03 | `CurrentNumber` pobierany z frontendu (nie z DB) — możliwy race condition na numer | FullDocumentNumber |
| PDF-04 | Tytuł PDF zawsze `Invoice #...` niezależnie od typu — proforma i storno mają ten sam tytuł co faktura | szablon |
| PDF-05 | Brak pola `TotalNetAmount` i `TotalVatAmount` w `dbo.Document` — tylko TotalPrice (brutto); rozbicie w PDF wyliczane z pozycji | model danych |
| PDF-06 | BankAccount na PDF = pierwsze konto WHERE UserFirmId — brak możliwości wyboru konta na poziomie dokumentu przez usera | logika doboru konta |

---

## 10. Powiązane

| Typ | Dokument |
|---|---|
| API — podgląd | [POST /Document/GetInvoicePdfStream](../../04_api_i_integracje/01_api_frontend/document/POST_Document_GetPdfStream.md) |
| API — generowanie | [POST /Document/GenerateDocumentPdf](../../04_api_i_integracje/01_api_frontend/document/POST_Document_GeneratePdf.md) |
| Algorytm | [ALG-07 PDF Generation](../../03_algorytmy/ALG-07_PdfGeneration.md) |
| Algorytm | [ALG-05 Document Total Calculation](../../03_algorytmy/ALG-05_DocumentTotalCalculation.md) |
| Algorytm | [ALG-02 Document Number Generation](../../03_algorytmy/ALG-02_DocumentNumberGeneration.md) |
| Model | [dbo.Document](../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Model | [dbo.DocumentProduct](../../05_model_danych/01_db/dbo/dbo.DocumentProduct.md) |
| Model | [dbo.Firm](../../05_model_danych/01_db/dbo/dbo.Firm.md) |
| Model | [dbo.BankAccount](../../05_model_danych/01_db/dbo/dbo.BankAccount.md) |
| DTO | [DocumentRequestDto](../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Ekran (frontend) | [Formularz faktury](../../01_ekrany/faktury/dodaj_edytuj_fakture/ekran.md) |
| Ekran (frontend) | [PDF Viewer (modal)](../../01_ekrany/00_wspolne/modale_wspolne/pdf_viewer/modal.md) |
| Dokumentacja użytkownika | [doc_user: Jak wygląda dokument PDF](../../../doc_user/01_ekrany/13_dokument_pdf.md) |
