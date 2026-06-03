# UpdateDocumentProducts — algorytm zapisu pozycji

| Pole | Wartość |
|---|---|
| ID | ALG-Wyliczeniowe-AktualizacjaProduktowDokumentu |
| Kategoria | wyliczeniowe |
| Metoda | `DocumentService.UpdateDocumentProducts()` |
| Wywoływana z | `AddDocument()` i `EditDocument()` |
| Ostatnia walidacja | 2026-05-31 (kod źródłowy `DocumentService.cs`) |

---

## Co robi

Zapisuje/nadpisuje pozycje dokumentu w bazie oraz aktualizuje sumy (`UnitPrice`, `TotalPrice`) na rekordzie `Document`.

**Ważne:** używana zarówno przy **dodawaniu** jak i **edycji** — za każdym razem **usuwa wszystkie stare pozycje i dodaje nowe** (brak soft-update, zawsze pełna podmiana).

---

## Kod źródłowy (zweryfikowany)

```csharp
private async Task UpdateDocumentProducts(
    int documentId,
    List<DocumentProductRequestDto> documentProductsDto,
    int userFirmId)
{
    decimal totalInvoicePrice = 0;        // suma netto
    decimal totalInvoicePriceWithTva = 0; // suma brutto

    // 1. USUŃ wszystkie istniejące pozycje dla dokumentu
    var existing = _unitOfWork.DocumentProducts
        .GetAllDocumentProductsForDocument(documentId);
    await _unitOfWork.DocumentProducts.RemoveRangeAsync(existing);

    // 2. DODAJ nowe pozycje z DTO
    foreach (var dto in documentProductsDto)
    {
        Product product;

        if (dto.Id > 0)
        {
            // Produkt z katalogu — pobierz po nazwie i UserFirmId
            product = await _unitOfWork.Products.Query()
                .FirstOrDefaultAsync(p => p.Name == dto.Name && p.UserFirmId == userFirmId);
            if (product == null) throw new Exception("Product not found.");
        }
        else
        {
            // Nowy produkt wpisany ręcznie — utwórz rekord w Product
            product = _mapper.Map<Product>(dto);
            product.UserFirmId = userFirmId;
            await _unitOfWork.Products.AddAsync(product);
        }

        var documentProduct = new DocumentProduct
        {
            Quantity   = dto.Quantity,
            UnitPrice  = dto.UnitPrice,
            TotalPrice = dto.TotalPrice,   // ← PRZYJĘTE Z DTO (obliczone przez frontend)
            Product    = product,
            DocumentId = documentId,
        };

        // Akumuluj sumy
        totalInvoicePrice        += dto.UnitPrice * dto.Quantity;  // netto (backend oblicza)
        totalInvoicePriceWithTva += dto.TotalPrice;                // brutto (z DTO)

        await _unitOfWork.DocumentProducts.AddAsync(documentProduct);
    }

    // 3. ZAKTUALIZUJ sumy na dokumencie
    var document = await _unitOfWork.Documents.GetByIdAsync(documentId);
    if (document != null)
    {
        document.UnitPrice  = totalInvoicePrice;        // netto całość
        document.TotalPrice = totalInvoicePriceWithTva; // brutto całość
        await _unitOfWork.Documents.UpdateAsync(document);
    }
}
```

---

## Sekwencja kroków

```
1. Pobierz istniejące DocumentProduct WHERE DocumentId = documentId
2. RemoveRange — usuń WSZYSTKIE (nawet jeśli edycja zmieniła tylko 1 pozycję)
3. Dla każdego dto w documentProductsDto:
   a. Jeśli dto.Id > 0 → pobierz Product z katalogu (WHERE Name=dto.Name AND UserFirmId=userFirmId)
   b. Jeśli dto.Id ≤ 0 → utwórz nowy Product i dodaj do katalogu
   c. Utwórz DocumentProduct z UnitPrice, Quantity, TotalPrice (snapshot z DTO)
   d. Dodaj sumę netto do akumulatora (UnitPrice × Quantity)
   e. Dodaj sumę brutto do akumulatora (TotalPrice z DTO)
4. Zaktualizuj Document.UnitPrice = Σ netto
5. Zaktualizuj Document.TotalPrice = Σ brutto (z DTO)
```

---

## Kluczowe rozróżnienie: netto vs brutto

| Kolumna | Kto oblicza | Wzór |
|---|---|---|
| `Document.UnitPrice` (netto) | **Backend** | `Σ (dto.UnitPrice × dto.Quantity)` |
| `Document.TotalPrice` (brutto) | **Frontend** (backend sumuje) | `Σ dto.TotalPrice` (wartości z DTO) |
| `DocumentProduct.TotalPrice` | **Frontend** | `UnitPrice × Quantity × (1 + VAT/100)` |

→ Szczegóły obliczenia ceny per wiersz: [obliczanie_ceny_pozycji.md](obliczanie_ceny_pozycji.md)

---

## Skutki uboczne — co warto wiedzieć

### Produkty wpisane ręcznie są dodawane do katalogu
Gdy `dto.Id ≤ 0` (użytkownik wpisał nazwę ręcznie, nie wybrał z katalogu), tworzy się **nowy rekord `Product`** w tabeli `Product`. Czyli każde ręczne wpisanie nazwy produktu na fakturze rozrasta katalog produktów.

### Pełna podmiana przy edycji
Każda edycja dokumentu usuwa WSZYSTKIE `DocumentProduct` i dodaje je od nowa. Brak soft-update oznacza:
- Stracone `Id` pozycji (mogą być używane w innych miejscach)
- Nadmiarowe operacje DB (delete+insert zamiast update)

### Brak zapisu VatRate w DocumentProduct
`DocumentProduct` nie ma kolumny `VatRate` — stawka VAT nie jest persystowana. Można ją odtworzyć tylko przez obliczenie wsteczne: `(TotalPrice / (UnitPrice × Quantity) - 1) × 100`.

---

## Anomalie

| ID | Opis |
|---|---|
| UPD-01 | Pełna podmiana przy edycji — `RemoveRange` + re-insert zamiast merge. Przy 100 pozycjach to 100 DELETE + 100 INSERT przy każdej edycji, nawet gdy zmieniono 1 pozycję |
| UPD-02 | Ręcznie wpisany produkt (`dto.Id ≤ 0`) tworzy rekord w `Product` — możliwy niekontrolowany rozrost katalogu produktów |
| UPD-03 | Backend akceptuje `TotalPrice` z DTO bez weryfikacji — możliwa manipulacja ceną brutto przez klienta |
| CALC-04 | `VatRate` nie jest przechowywany w `DocumentProduct` — nie można odtworzyć stawki VAT po fakcie |

---

## Powiązane

| Typ | Dokument |
|---|---|
| Algorytm | [obliczanie_ceny_pozycji.md](obliczanie_ceny_pozycji.md) — jak frontend oblicza TotalPrice |
| Algorytm | [obliczanie_wartosci_dokumentu.md](obliczanie_wartosci_dokumentu.md) — sumy dokumentu |
| Model | [dbo.DocumentProduct](../../05_model_danych/01_db/dbo/dbo.DocumentProduct.md) |
| Model | [dbo.Document](../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Proces | [dodaj_dokument](../../02_procesy/dokumenty/dodaj_dokument/proces.md) |
| Proces | [edytuj_dokument](../../02_procesy/dokumenty/edytuj_dokument/proces.md) |
