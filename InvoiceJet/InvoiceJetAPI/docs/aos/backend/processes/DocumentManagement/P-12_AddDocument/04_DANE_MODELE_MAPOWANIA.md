# AddDocument — Dane, modele i mapowania

## 1. DTO

### `DocumentRequestDto` (wejście i wyjście AddDocument)

Źródło: `DocumentRequestDto.cs`

| Pole | Typ | Wymagane | Opis / źródło wartości |
|---|---|---|---|
| `Id` | `int` | nie (tworzenie) | Przy tworzeniu = 0; po `AddAsync+CompleteAsync` nadawany przez DB |
| `DocumentNumber` | `string?` | nie (wejście) | Wyliczany w serwisie: `SeriesName + CurrentNumber.ToString("D4")`; w żądaniu ignorowany |
| `Seller` | `FirmDto?` | nie (wejście) | Pomijane przy AddDocument; wypełniane przez GeneratePdf process |
| `Client` | `FirmDto` | tak | `Client.Id` → `Document.ClientId`; inicjalizator `null!` |
| `IssueDate` | `DateTime` | tak | Data wystawienia |
| `DueDate` | `DateTime?` | nie | Data płatności (nullable) |
| `BankAccount` | `BankAccountDto?` | nie (wejście) | Ignorowane przy AddDocument; serwis pobiera aktywne konto bankowe z DB |
| `DocumentSeries` | `DocumentSeriesDto?` | tak (pośrednio) | `DocumentSeries.SeriesName + CurrentNumber` → `DocumentNumber`; `DocumentSeries.Id` → `IncreaseDocumentSeriesNumber`; `DocumentSeries.DocumentType.Id` → `Document.DocumentTypeId` |
| `DocumentType` | `DocumentType?` | nie (wejście) | Encja domenowa! Ignorowane przy AddDocument; `DocumentTypeId` pobierane z `DocumentSeries.DocumentType.Id` |
| `DocumentStatus` | `DocumentStatus?` | nie (wejście) | Encja domenowa! Ignorowane przy AddDocument; `DocumentStatusId` = `DocumentStatusEnum.Unpaid = 1` (hardcoded) |
| `Products` | `List<DocumentProductRequestDto>` | tak | Lista produktów; inicjalizator `null!` |

> [UWAGA: `DocumentRequestDto.DocumentType` i `DocumentRequestDto.DocumentStatus` to typy encji domenowych (`InvoiceJet.Domain.Models.DocumentType` / `DocumentStatus`), nie dedykowane DTO. Naruszenie separacji warstw. Kotwica: `DocumentRequestDto.cs`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

> Atrybuty walidacyjne DTO: brak atrybutów z `System.ComponentModel.DataAnnotations`. Cała walidacja realizowana w `DocumentService`.

---

### `DocumentProductRequestDto` (zagnieżdżony w `DocumentRequestDto.Products`)

Źródło: `DocumentProductRequestDto.cs`

| Pole | Typ | Wymagane | Opis / źródło wartości |
|---|---|---|---|
| `Id` | `int` | tak | `0` = nowy produkt (tworzy `Product` + `DocumentProduct`); `>0` = istniejący (szuka po `Name+UserFirmId`) |
| `Name` | `string` | tak | Nazwa produktu; inicjalizator `string.Empty` |
| `UnitPrice` | `decimal` | tak | Cena jednostkowa netto |
| `TotalPrice` | `decimal` | tak | Cena łączna z VAT (`UnitPrice * Quantity * (1 + TvaValue/100)`) |
| `ContainsTva` | `bool` | nie | Czy cena już zawiera VAT; domyślnie `false` |
| `UnitOfMeasurement` | `string` | nie | Jednostka miary (np. `"buc"`, `"ora"`); inicjalizator `string.Empty` |
| `TvaValue` | `int` | nie | Stawka VAT %; domyślnie `19` |
| `Quantity` | `int` | tak | Ilość; `(int)dp.Quantity` przy mapowaniu z `DocumentProduct` |

> Atrybuty walidacyjne DTO: brak.

---

## 2. Encje i kolumny

### Encja `Document` → tabela `Document`

Kotwica: `Document.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("InvoiceJet.Domain.Models.Document", b => ...)`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | nie | PK | — |
| `DocumentNumber` | `nvarchar(max)` | nie | — | — |
| `IssueDate` | `datetime2` | nie | — | — |
| `DueDate` | `datetime2` | tak | — | — |
| `UnitPrice` | `decimal(18,2)` | nie | — | — |
| `TotalPrice` | `decimal(18,2)` | nie | — | — |
| `BankAccountId` | `int` | nie | FK→`BankAccount` (IsRequired, OnDelete Cascade) | tak |
| `ClientId` | `int` | tak | FK→`Firm` (nullable) | tak |
| `DocumentStatusId` | `int` | tak | FK→`DocumentStatus` (nullable) | tak |
| `DocumentTypeId` | `int` | tak | FK→`DocumentType` (nullable) | tak |
| `UserFirmId` | `int` | tak | FK→`UserFirm` (nullable, `WithMany("Documents")`) | tak |

Uwagi:
- `BankAccountId` jest `IsRequired()` w encji — NOT NULL — mimo że nullable w snapshot. W praktyce serwis zawsze ustawia `BankAccount` (przez navigation property). ⚠️ Brak jawnego `BankAccountId = ...` — EF Core ustawia przez `document.BankAccount = <obiekt>`.
- `UnitPrice` i `TotalPrice` nie są ustawiane przy pierwszym `CompleteAsync()` — ich wartości wylicza `UpdateDocumentProducts` w drugim kroku i aktualizuje przez `Documents.UpdateAsync(document)`.

> Pełne definicje: `../../SLOWNIK_DANYCH.md#Document`.

---

### Encja `DocumentProduct` → tabela `DocumentProduct`

Kotwica: `DocumentProduct.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("InvoiceJet.Domain.Models.DocumentProduct", b => ...)`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | nie | PK | — |
| `Quantity` | `decimal(18,2)` | nie | — | — |
| `UnitPrice` | `decimal(18,2)` | nie | — | — |
| `TotalPrice` | `decimal(18,2)` | nie | — | — |
| `DocumentId` | `int` | tak | FK→`Document` (`WithMany("DocumentProducts")`, brak kaskady jawnej) | tak |
| `ProductId` | `int` | tak | FK→`Product` (nullable, brak kaskady jawnej) | tak |

> Pełne definicje: `../../SLOWNIK_DANYCH.md#DocumentProduct`.

---

### Encja `Product` → tabela `Product` (lookup / tworzona on-the-fly)

Dotyczy: nowe produkty (`documentProductDto.Id == 0`) tworzone przez `UpdateDocumentProducts`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | nie | PK | — |
| `Name` | `nvarchar(max)` | nie | — | unikalny per `UserFirmId` |
| `Price` | `decimal(18,2)` | nie | — | — |
| `ContainsTva` | `bit` | nie | — | — |
| `UnitOfMeasurement` | `nvarchar(max)` | tak | — | — |
| `TvaValue` | `int` | nie | — | — |
| `UserFirmId` | `int` | tak | FK→`UserFirm` | tak |

> Pełne definicje: `../../SLOWNIK_DANYCH.md#Product`.

---

### Encja `DocumentSeries` → tabela `DocumentSeries` (pola modyfikowane)

Dotyczy: `IncreaseDocumentSeriesNumber` inkrementuje `CurrentNumber`.

| Kolumna modyfikowana | Zmiana |
|---|---|
| `CurrentNumber` | `+= 1` (po `UpdateDocumentProducts`, przed drugim `CompleteAsync`) |

> Pełna tabela kolumn: `../../../DocumentSeriesManagement/P-11_ManageDocumentSeries/04_DANE_MODELE_MAPOWANIA.md#DocumentSeries`.

---

## 3. Relacje i kaskady

| Z encji | Pole FK | Do encji | Kierunek | Kaskada |
|---|---|---|---|---|
| `Document` | `BankAccountId` | `BankAccount` | N..1 | `OnDelete(Cascade)` — IsRequired |
| `Document` | `ClientId` | `Firm` | N..1 | brak jawnej kaskady (nullable FK) |
| `Document` | `DocumentStatusId` | `DocumentStatus` | N..1 | brak jawnej kaskady (nullable FK) |
| `Document` | `DocumentTypeId` | `DocumentType` | N..1 | brak jawnej kaskady (nullable FK) |
| `Document` | `UserFirmId` | `UserFirm` | N..1 | brak jawnej kaskady (nullable FK) |
| `DocumentProduct` | `DocumentId` | `Document` | N..1 | brak jawnej kaskady (nullable FK) |
| `DocumentProduct` | `ProductId` | `Product` | N..1 | brak jawnej kaskady (nullable FK) |

> [UWAGA: `Document.BankAccountId` ma `OnDelete(Cascade)` i jest `IsRequired()` — usunięcie `BankAccount` kaskadowo usuwa wszystkie powiązane dokumenty na poziomie DB. Serwis broni przed usunięciem konta powiązanego z dokumentem (`BankAccountAssociatedWithDocumentsException` w P-10), ale relacja DB nadal umożliwia kaskadowe usunięcie przez bezpośrednie zapytanie do DB. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 4. Mapowania AutoMapper

Źródła: `DocumentProfile.cs`, `DocumentProductProfile.cs`

| Źródło | Cel | Profil | Uwagi |
|---|---|---|---|
| `Document` | `DocumentRequestDto` | `DocumentProfile` | `Seller` ← `src.UserFirm`; `Products` ← inline map z `DocumentProducts` (nieużywane w AddDocument — return `documentRequestDto` bez remapowania) |
| `Document` | `DocumentTableRecordDto` | `DocumentProfile` | `ClientName` ← `src.Client.Name`; `TotalValue` ← `src.TotalPrice` (nieużywane w AddDocument) |
| `DocumentProductRequestDto` | `Product` | `DocumentProductProfile` | `Price` ← `src.UnitPrice`; `UserFirm = Ignore`; `UserFirmId = Ignore`; używane gdy `Id == 0` (nowy produkt) |

> **Kluczowe:** `AddDocument` **nie używa AutoMapper do budowania `Document`** — encja tworzona ręcznie przez inicjalizator obiektowy `new Document { ... }`. AutoMapper używany jest tylko w `UpdateDocumentProducts` (dla nowych produktów: `_mapper.Map<Product>(documentProductDto)`).

---

## 5. Zapytania (LINQ/SQL)

### Query 1: Sprawdzenie aktywnej firmy

Kotwica: `DocumentService.cs › DocumentService.AddDocument`
```csharp
var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
```

### Query 2: Pobranie aktywnego konta bankowego firmy

Kotwica: `DocumentService.cs › DocumentService.AddDocument`
```csharp
BankAccount = await _unitOfWork.BankAccounts.Query()
    .Where(ba => ba.UserFirmId == userFirmId && ba.IsActive)
    .FirstOrDefaultAsync() ?? throw new NoBankAccountAddedException()
```

Semantyka: pobiera pierwsze aktywne konto bankowe firmy. Jeśli brak — rzuca `NoBankAccountAddedException`.

### Query 3: Pobranie istniejącego produktu po Name+UserFirmId (w UpdateDocumentProducts gdy Id > 0)

Kotwica: `DocumentService.cs › DocumentService.UpdateDocumentProducts`
```csharp
product = await _unitOfWork.Products.Query()
    .FirstOrDefaultAsync(product => product.Name == documentProductDto.Name && product.UserFirmId == userFirmId);
if (product == null)
{
    throw new Exception("Product not found.");
}
```

> [UWAGA: Produkt o `Id > 0` szukany jest po `Name + UserFirmId`, **nie** po `Id`. Możliwy błąd gdy produkt zmienił nazwę lub `Name` w DTO nie odpowiada nazwie w DB. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Query 4: Pobranie serii do inkrementacji (IncreaseDocumentSeriesNumber)

Kotwica: `DocumentService.cs › DocumentService.IncreaseDocumentSeriesNumber`
```csharp
var docSeries = await _unitOfWork.DocumentSeries.GetByIdAsync(documentSeriesId);
docSeries!.CurrentNumber++;
await _unitOfWork.DocumentSeries.UpdateAsync(docSeries);
```

Semantyka: `GetByIdAsync` — generyczny `GetByIdAsync` z `GenericRepository`. Null forgiving (`!`) — brak null check; jeśli seria nie istnieje, `NullReferenceException` w runtime.

### Query 5: Aktualizacja sumy dokumentu (w UpdateDocumentProducts)

Kotwica: `DocumentService.cs › DocumentService.UpdateDocumentProducts`
```csharp
var document = await _unitOfWork.Documents.GetByIdAsync(documentId);
if (document != null)
{
    document.UnitPrice = totalInvoicePrice;
    document.TotalPrice = totalInvoicePriceWithTva;
    await _unitOfWork.Documents.UpdateAsync(document);
}
```

---

## 6. Użyte enumy i lookupy

| Element | Rodzaj | Plik | Wartości |
|---|---|---|---|
| `DocumentStatusEnum` | enum | `InvoiceJet.Domain/Enums/DocumentStatus.cs` | `Unpaid = 1`, `Paid = 2` |
| `DocumentTypeEnum` | enum | `InvoiceJet.Domain/Enums/DocumentType.cs` | `Invoice = 1`, `ProformaInvoice = 2`, `StornoInvoice = 3` |
| `DocumentStatus` (seed) | tabela słownikowa | `InvoiceJet.Domain/Models/DocumentStatus.cs` + `DbSeeder.cs` | `Id=1 → "Unpaid"`, `Id=2 → "Paid"` |
| `DocumentType` (seed) | tabela słownikowa | `InvoiceJet.Domain/Models/DocumentType.cs` + `DbSeeder.cs` | `Id=1 → "Factura"`, `Id=2 → "Factura Proforma"`, `Id=3 → "Factura Storno"` |
