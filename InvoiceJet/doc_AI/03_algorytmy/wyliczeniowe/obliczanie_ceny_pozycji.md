# Obliczanie ceny brutto pozycji (per-line price) — algorytm

| Pole | Wartość |
|---|---|
| ID | ALG-Wyliczeniowe-ObliczanieCenyPozycji |
| Kategoria | wyliczeniowe |
| Gdzie wywoływany | **Wyłącznie frontend** — `BaseInvoiceComponent` (Angular) |
| Powiązane | [obliczanie_wartosci_dokumentu.md](obliczanie_wartosci_dokumentu.md) · [aktualizacja_produktow_dokumentu.md](aktualizacja_produktow_dokumentu.md) |
| Ostatnia walidacja | 2026-05-31 (kod źródłowy `Invoice.cs`, `UpdateDocumentProducts`) |

---

## Ważne ustalenie: backend UFA frontendowi

> Backend **nie przelicza** ceny brutto pozycji — przyjmuje wartość `TotalPrice` z DTO (wysłaną przez frontend) i zapisuje ją wprost do `DocumentProduct.TotalPrice`.
>
> Obliczenie ceny brutto wiersza to **wyłącznie odpowiedzialność frontendu.**

```
FRONTEND                               BACKEND
────────────────────────────────────   ────────────────────────────────
Użytkownik wpisuje UnitPrice,          Odbiera DocumentProductRequestDto
Quantity, VatRate                      z polami:
        ↓                                - UnitPrice  (netto)
TotalPrice = UnitPrice × Qty           - Quantity
             × (1 + VAT/100)           - TotalPrice   ← nie weryfikuje!
        ↓                                        ↓
Wysyła w DTO → → → → → → → → → →     DocumentProduct.TotalPrice = dto.TotalPrice
```

---

## Wzór (frontend)

### Cena brutto jednej pozycji

```
TotalPrice = UnitPrice × Quantity × (1 + VatRate / 100)
```

### Przykłady

| UnitPrice | Quantity | VatRate | TotalPrice |
|---|---|---|---|
| 100.00 | 2 | 19 | 100 × 2 × 1.19 = **238.00** |
| 50.00 | 1 | 5 | 50 × 1 × 1.05 = **52.50** |
| 200.00 | 3 | 0 | 200 × 3 × 1.00 = **600.00** |
| 150.00 | 10 | 23 | 150 × 10 × 1.23 = **1845.00** |

---

## Implementacja frontend (BaseInvoiceComponent.ts)

```typescript
// Reakcja na zmianę wartości formularza (ReactiveForm valueChanges)
calculateTotals() {
    // Suma netto (UnitPrice × Quantity dla każdej pozycji)
    this.totalNetAmount = this.products.controls.reduce((sum, ctrl) =>
        sum + (ctrl.value.unitPrice * ctrl.value.quantity), 0);

    // Suma VAT
    this.totalVatAmount = this.products.controls.reduce((sum, ctrl) =>
        sum + (ctrl.value.unitPrice * ctrl.value.quantity * ctrl.value.vatRate / 100), 0);

    // Suma brutto = netto + VAT
    this.totalGrossAmount = this.totalNetAmount + this.totalVatAmount;
}
```

Każda pozycja `ctrl.value` zawiera:
- `unitPrice` — cena jednostkowa netto
- `quantity` — ilość
- `vatRate` — stawka VAT (%)

Obliczona `TotalPrice` per wiersz = `unitPrice × quantity × (1 + vatRate/100)` trafia do DTO jako `DocumentProductRequestDto.TotalPrice`.

---

## Implementacja backend (brak obliczenia — zapis z DTO)

```csharp
// DocumentService.UpdateDocumentProducts — FRAGMENT
var documentProduct = new DocumentProduct
{
    Quantity  = documentProductDto.Quantity,
    UnitPrice = documentProductDto.UnitPrice,
    TotalPrice = documentProductDto.TotalPrice,  // ← PRZYJMUJE od frontendu bez przeliczania
    Product    = product,
    DocumentId = documentId,
};
```

Backend agreguje sumy na poziomie dokumentu:
```csharp
totalInvoicePrice    += documentProductDto.UnitPrice * documentProductDto.Quantity; // netto (backend liczy)
totalInvoicePriceWithTva += documentProductDto.TotalPrice; // brutto (backend sumuje z DTO)
```

---

## Model danych

| Tabela | Kolumna | Typ | Rola |
|---|---|---|---|
| `DocumentProduct` | `UnitPrice` | `decimal(18,2)` | Cena jednostkowa netto — snapshot z chwili wystawienia |
| `DocumentProduct` | `Quantity` | `decimal(18,2)` | Ilość |
| `DocumentProduct` | `TotalPrice` | `decimal(18,2)` | Cena brutto pozycji — **snapshot z chwili wystawienia, obliczony przez frontend** |
| `Document` | `UnitPrice` | `decimal(18,2)` | Suma netto wszystkich pozycji — obliczona przez backend |
| `Document` | `TotalPrice` | `decimal(18,2)` | Suma brutto — backend sumuje `DocumentProduct.TotalPrice` z DTO |

---

## Jak obliczone wartości trafiają na PDF

Szablon `StornoInvoice.cs` / `InvoiceDocument.cs` używa:
```csharp
var value        = item.UnitPrice * item.Quantity;             // netto wiersza (w szablonie)
var totalTVAItem = item.TotalPrice - item.UnitPrice * item.Quantity;  // VAT wiersza (w szablonie)
```

Różnica: `item.TotalPrice` (z DB) minus `UnitPrice × Quantity` (z szablonu) = kwota VAT wiersza.
→ Zobacz [szablon PDF: wspólna struktura](../../09_procesy_biznesowe/dokumenty/pdf/wspolna_struktura.md)

---

## Anomalie

| ID | Opis |
|---|---|
| CALC-03 | Backend nie weryfikuje `TotalPrice` z DTO — zmanipulowana wartość od frontendu zostanie zapisana do DB bez walidacji |
| CALC-04 | `VatRate` ze strony DTO nie jest przechowywany w `DocumentProduct` — tylko `UnitPrice` i `TotalPrice` (snapshot). Odtworzenie stawki VAT z istniejącego dokumentu jest niemożliwe bez przeliczenia wstecznego |
| CALC-02 | Precyzja `decimal(18,2)` — przy wielu pozycjach z różnymi stawkami VAT możliwe błędy zaokrąglenia na poziomie groszy |

---

## Powiązane

| Typ | Dokument |
|---|---|
| Algorytm | [obliczanie_wartosci_dokumentu.md](obliczanie_wartosci_dokumentu.md) — sumy całego dokumentu |
| Algorytm | [aktualizacja_produktow_dokumentu.md](aktualizacja_produktow_dokumentu.md) — zapis do DB |
| Szablon PDF | [pdf/wspolna_struktura.md](../../09_procesy_biznesowe/dokumenty/pdf/wspolna_struktura.md) — jak wartości są wyświetlane |
| Model | [dbo.DocumentProduct](../../05_model_danych/01_db/dbo/dbo.DocumentProduct.md) |
| Model | [dbo.Document](../../05_model_danych/01_db/dbo/dbo.Document.md) |
| DTO | [DocumentProductRequestDto](../../05_model_danych/02_dto/DTO-08_DocumentProductRequestDto.md) |
