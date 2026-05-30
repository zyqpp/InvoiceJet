# GetDocumentAutofillInfo — Dane, modele i mapowania

## 1. DTO

### `DocumentAutofillDto` (wyjście)

Źródło: `DocumentAutofillDto.cs`

| Pole | Typ | Nullable | Opis |
|---|---|---|---|
| `Clients` | `List<FirmDto>` | `null!` | Firmy klienckie powiązane z użytkownikiem (`IsClient=true`) |
| `DocumentSeries` | `List<DocumentSeriesDto>` | `null!` | Serie dokumentów danego typu (`DocumentTypeId`) dla firmy użytkownika |
| `DocumentStatuses` | `List<DocumentStatusDto>` | `null!` | Wszystkie statusy dokumentów z tabeli `DocumentStatus` (globalne) |
| `Products` | `List<ProductDto>` | `null!` | Produkty firmy użytkownika |

> [UWAGA: Wszystkie pola DTO deklarowane są z `null!` initializer. Gdy użytkownik nie ma firmy (`GetUserFirmIdAsync` zwraca `null`), serwis zwraca `new DocumentAutofillDto()` — obiekt z czterema polami `null`. Frontend może dostać `{ clients: null, documentSeries: null, documentStatuses: null, products: null }` zamiast pustych list. Kotwica: `DocumentService.cs › DocumentService.GetDocumentAutofillInfo`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

### `FirmDto` (Clients)

| Pole | Typ | Opis |
|---|---|---|
| `Id` | `int` | Id firmy |
| `Name` | `string` | Nazwa firmy |
| `Cui` | `string` | NIP/CUI |
| `RegCom` | `string` | Nr KRS |
| `Address` | `string` | Adres |
| `County` | `string` | Województwo/Judet |
| `City` | `string` | Miasto |

### `DocumentSeriesDto` (DocumentSeries)

| Pole | Typ | Opis |
|---|---|---|
| `Id` | `int` | Id serii |
| `Name` | `string` | Nazwa serii |
| `CurrentNumber` | `int` | Aktualny numer |
| `DocumentType` | `DocumentType?` | Encja domenowa typu dokumentu (Include) |

> [UWAGA: `DocumentSeriesDto.DocumentType` może być encją domenową, nie DTO — weryfikacja na podstawie `DocumentSeriesDto.cs`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### `DocumentStatusDto` (DocumentStatuses)

| Pole | Typ | Opis |
|---|---|---|
| `Id` | `int` | Id statusu |
| `Status` | `string` | Nazwa statusu |

### `ProductDto` (Products)

| Pole | Typ | Opis |
|---|---|---|
| `Id` | `int` | Id produktu |
| `Name` | `string` | Nazwa |
| `Price` | `decimal` | Cena jednostkowa |
| `TvaValue` | `int` | Stawka VAT |

---

## 2. Encje i kolumny

### Encja `Firm` (clients query)

Tabela `Firm`. Kolumny używane:
- `Id`, `Name`, `Cui`, `RegCom`, `Address`, `County`, `City`
- Join przez `UserFirm` (pośrednia tabela): `UserId`, `IsClient` (filtr: `IsClient=true`, `UserId==userId`)

### Encja `DocumentSeries`

Tabela `DocumentSeries`. Kolumny używane:
- `Id`, `Name`, `CurrentNumber`, `UserFirmId` (filtr), `DocumentTypeId` (filtr), `DocumentType` (Include)

### Encja `DocumentStatus`

Tabela `DocumentStatus`. Wszystkie rekordy (seed: `Unpaid=1`, `Paid=2`).

### Encja `Product`

Tabela `Product`. Kolumny używane:
- `Id`, `Name`, `Price`, `TvaValue`, `UserFirmId` (filtr)

---

## 3. Relacje i kaskady

| Z encji | Pole FK | Do encji | Kierunek | Używana w procesie |
|---|---|---|---|---|
| `UserFirm` | `UserId` | `User` | N..1 | filtr klientów (`uf.UserId == userId`) |
| `UserFirm` | `IsClient` | — | (bool) | filtr klientów |
| `DocumentSeries` | `UserFirmId` | `UserFirm` | N..1 | filtr serii |
| `DocumentSeries` | `DocumentTypeId` | `DocumentType` | N..1 | filtr + Include |
| `Product` | `UserFirmId` | `UserFirm` | N..1 | filtr produktów |

---

## 4. Mapowania AutoMapper

| Źródło | Cel | Profil | Uwagi |
|---|---|---|---|
| `List<Firm>` | `List<FirmDto>` | `FirmProfile` | klienci |
| `List<DocumentSeries>` | `List<DocumentSeriesDto>` | `DocumentSeriesProfile` (lub analogiczny) | ze zagnieżdżonym `DocumentType` |
| `List<DocumentStatus>` | `List<DocumentStatusDto>` | `DocumentStatusProfile` | globalne statusy |
| `List<Product>` | `List<ProductDto>` | `ProductProfile` | produkty firmy |

---

## 5. Zapytania (LINQ/SQL)

Kotwica: `DocumentService.cs › DocumentService.GetDocumentAutofillInfo`

```csharp
// Klienci — firmy powiązane z userId przez UserFirm.IsClient=true
var clients = await _unitOfWork.Firms.Query()
    .Where(f => f.UserFirms!.Any(uf => uf.UserId == userId && uf.IsClient))
    .ToListAsync();

// Serie dokumentów dla firmy i danego typu
var documentSeries = await _unitOfWork.DocumentSeries.Query()
    .Where(ds => ds.UserFirmId == userFirmId && ds.DocumentTypeId == documentTypeId)
    .Include(ds => ds.DocumentType)
    .ToListAsync();

// Statusy — WSZYSTKIE (bez filtra firmy)
var documentStatuses = await _unitOfWork.DocumentStatuses.Query().ToListAsync();

// Produkty firmy
var products = await _unitOfWork.Products.Query()
    .Where(p => p.UserFirmId == userFirmId)
    .ToListAsync();
```

---

## 6. Użyte enumy i lookupy

| Element | Rodzaj | Wartości |
|---|---|---|
| `DocumentStatus` (seed) | tabela słownikowa | `Id=1→"Unpaid"`, `Id=2→"Paid"` |
| `DocumentType` (seed) | tabela słownikowa | `Id=1→"Factura"`, `Id=2→"Factura Proforma"`, `Id=3→"Factura Storno"` |
