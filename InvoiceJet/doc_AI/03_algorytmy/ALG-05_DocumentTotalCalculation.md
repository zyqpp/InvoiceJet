# Algorytm: Obliczanie sum dokumentu (Document Total Calculation)

| Atrybut | Wartość |
|---|---|
| ID | ALG-05 |
| Nazwa | Document Total Price Calculation |
| Kategoria | Logika biznesowa |
| Pliki | `DocumentService.cs › AddDocument()`, `BaseInvoiceComponent` (Angular) |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Obliczenie łącznej wartości dokumentu (`TotalPrice`) na podstawie pozycji dokumentu. Obliczenia wykonywane zarówno po stronie frontendu (podgląd na żywo) jak i backendu (zapis do DB).

## Model pozycji dokumentu

| Pole | Typ | Opis |
|---|---|---|
| `Quantity` | `decimal` | Ilość |
| `Price` | `decimal` | Cena jednostkowa netto |
| `VatRate` | `decimal` | Stawka VAT w % (np. 19.00) |

## Wzór obliczenia

### Wartość brutto jednej pozycji

```
LineTotal = Price × Quantity × (1 + VatRate / 100)
```

### Suma całego dokumentu

```
TotalPrice = Σ(LineTotal) dla każdej pozycji
```

## Implementacja backend (zweryfikowana w kodzie)

> ⚠️ **Korekta:** poprzednia wersja tego dokumentu miała fragment „szacowany" z błędną formułą.
> Backend **nie przelicza** ceny brutto per pozycja — sumuje `TotalPrice` z DTO (wartość obliczoną przez frontend).

```csharp
// DocumentService › UpdateDocumentProducts (wywoływana z AddDocument i EditDocument)
decimal totalInvoicePrice        = 0;  // suma netto
decimal totalInvoicePriceWithTva = 0;  // suma brutto

foreach (var dto in documentProductsDto)
{
    // ...tworzenie DocumentProduct...
    totalInvoicePrice        += dto.UnitPrice * dto.Quantity;  // netto — backend oblicza
    totalInvoicePriceWithTva += dto.TotalPrice;                // brutto — z DTO (frontend obliczył)
}

document.UnitPrice  = totalInvoicePrice;
document.TotalPrice = totalInvoicePriceWithTva;
```

Szczegóły: [wyliczeniowe/aktualizacja_produktow_dokumentu.md](wyliczeniowe/aktualizacja_produktow_dokumentu.md)

## Implementacja frontend (BaseInvoiceComponent)

```typescript
// Angular — reactive form valueChanges subscription
calculateTotals() {
    this.totalNetAmount = this.products.controls.reduce((sum, ctrl) =>
        sum + (ctrl.value.price * ctrl.value.quantity), 0);

    this.totalVatAmount = this.products.controls.reduce((sum, ctrl) =>
        sum + (ctrl.value.price * ctrl.value.quantity * ctrl.value.vatRate / 100), 0);

    this.totalGrossAmount = this.totalNetAmount + this.totalVatAmount;
}
```

## Wartości w modelu DB

| Tabela | Kolumna | Typ | Opis |
|---|---|---|---|
| `Document` | `TotalPrice` | `decimal(18,2)` | Suma brutto całego dokumentu |
| `DocumentProduct` | `Price` | `decimal(18,2)` | Cena jedn. netto pozycji |
| `DocumentProduct` | `Quantity` | `decimal(18,2)` | Ilość |
| `DocumentProduct` | `VatRate` | `decimal(18,2)` | Stawka VAT (%) |

## Anomalie

| # | Anomalia |
|---|---|
| CALC-01 | Brak przechowywania `TotalNetAmount` i `TotalVatAmount` osobno w tabeli `Document` — tylko `TotalPrice` (brutto); rozbicie na netto/VAT tylko na froncie |
| CALC-02 | Precyzja `decimal(18,2)` — przy wielu pozycjach możliwe błędy zaokrąglenia |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
