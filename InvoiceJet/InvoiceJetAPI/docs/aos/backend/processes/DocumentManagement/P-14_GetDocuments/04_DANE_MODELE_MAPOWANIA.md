# GetDocuments — Dane, modele i mapowania

## 1. DTO

### `DocumentTableRecordDto` (wyjście GetDocumentTableRecords)

Źródło: `DocumentTableRecordDto.cs`

| Pole | Typ | Opis |
|---|---|---|
| `Id` | `int` | Id dokumentu |
| `DocumentNumber` | `string` | Numer dokumentu |
| `ClientName` | `string` | Nazwa klienta (z `Document.Client.Name`) |
| `IssueDate` | `DateTime` | Data wystawienia |
| `DueDate` | `DateTime?` | Data płatności (nullable) |
| `TotalValue` | `decimal` | Wartość brutto (`Document.TotalPrice`) |
| `DocumentStatus` | `DocumentStatus?` | Encja domenowa statusu (Id, Status) |

> [UWAGA: `DocumentTableRecordDto.DocumentStatus` to typ encji domenowej `InvoiceJet.Domain.Models.DocumentStatus`, nie DTO. Naruszenie separacji warstw. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

### `DocumentRequestDto` (wyjście GetDocumentById)

Taki sam typ jak w P-12/P-13. Po mapowaniu przez AutoMapper zawiera wszystkie pola + zagnieżdżone pozycje (`DocumentProducts → Products`).

Pola wypełniane przez `GetDocumentWithAllInfo`:
- `Products` ← `DocumentProducts` (Include → `Product`)
- `DocumentStatus` ← Include `DocumentStatus`
- `Client` ← Include `Client`
- `Seller` ← brak (AutoMapper mapuje `Seller` z `Document.UserFirm`, ale `UserFirm` nie jest Include w `GetDocumentWithAllInfo`)

---

## 2. Encje i kolumny

### Encja `Document` (odczyt)

Tabela `Document` — pełna tabela kolumn: `../P-12_AddDocument/04_DANE_MODELE_MAPOWANIA.md#Document`.

Kolumny używane w `GetDocumentTableRecords`:
- `DocumentNumber`, `IssueDate`, `DueDate`, `TotalPrice`, `ClientId` (Include Client.Name), `DocumentStatusId` (Include DocumentStatus)

Kolumny używane w `GetDocumentById`:
- wszystkie + Include `DocumentProducts→Product`, `DocumentStatus`, `Client`

---

## 3. Relacje i kaskady

Relacje używane (Include):

| Metoda | Include |
|---|---|
| `GetAllDocumentsByType` | `Include(Client)`, `Include(DocumentStatus)` |
| `GetDocumentWithAllInfo` | `Include(DocumentStatus)`, `Include(DocumentProducts).ThenInclude(Product)`, `Include(Client)` |

---

## 4. Mapowania AutoMapper

| Źródło | Cel | Profil | Uwagi |
|---|---|---|---|
| `Document` | `DocumentTableRecordDto` | `DocumentProfile` | `ClientName` ← `src.Client.Name`; `TotalValue` ← `src.TotalPrice` |
| `Document` | `DocumentRequestDto` | `DocumentProfile` | `Seller` ← `src.UserFirm` (może być null — UserFirm nie jest Include); `Products` ← inline map z `DocumentProducts` |

---

## 5. Zapytania (LINQ/SQL)

### Query 1: Lista dokumentów po typie

Kotwica: `DocumentRepository.cs › DocumentRepository.GetAllDocumentsByType`
```csharp
return await _dbSet
    .Where(document => document.UserFirmId == activeUserFirmId && document.DocumentTypeId == documentTypeId)
    .Include(document => document.Client)
    .Include(document => document.DocumentStatus)
    .ToListAsync();
```

### Query 2: Dokument ze wszystkimi danymi

Kotwica: `DocumentRepository.cs › DocumentRepository.GetDocumentWithAllInfo`
```csharp
return _dbSet
    .Where(d => d.Id == documentId)
    .Include(d => d.DocumentStatus)
    .Include(d => d.DocumentProducts)!
    .ThenInclude(dp => dp.Product)
    .Include(d => d.Client)
    .FirstOrDefaultAsync();
```

---

## 6. Użyte enumy i lookupy

| Element | Rodzaj | Wartości |
|---|---|---|
| `DocumentStatus` (seed) | tabela | `Id=1→"Unpaid"`, `Id=2→"Paid"` |
| `DocumentType` (seed) | tabela | `Id=1→"Factura"`, `Id=2→"Factura Proforma"`, `Id=3→"Factura Storno"` |
