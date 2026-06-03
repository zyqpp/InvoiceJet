# DeleteDocuments — Dane, modele i mapowania

## 1. DTO

### Wejście — `int[]`

Ciało żądania to tablica identyfikatorów dokumentów do usunięcia. Brak dedykowanego DTO.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| (array) | `int[]` | tak (framework) | Tablica Id dokumentów do usunięcia; `[FromBody]` |

> Brak atrybutów walidacyjnych. Pusta tablica `[]` → serwis wykonuje `Query().Where(d => [].Contains(d.Id)).ToListAsync()` → pusta lista → `RemoveRangeAsync` na pustej kolekcji → `CompleteAsync()` bez efektu → `200 OK`.

### Wyjście — obiekt anonimowy

```json
{ "message": "Documents deleted successfully." }
```

Kotwica: `DocumentController.cs › DocumentController.DeleteDocuments`

```csharp
return Ok(new { Message = "Documents deleted successfully." });
```

---

## 2. Encje i kolumny

### Encja `Document` → tabela `Document`

Kotwica: `Document.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("Document")`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `Id` | `int IDENTITY` | nie | PK | — |
| `DocumentNumber` | `nvarchar(max)` | nie | — | — |
| `IssueDate` | `datetime2` | nie | — | — |
| `DueDate` | `datetime2` | tak | — | — |
| `TotalPrice` | `decimal(18,2)` | nie | — | — |
| `UnitPrice` | `decimal(18,2)` | nie | — | — |
| `BankAccountId` | `int` | nie | FK→BankAccount | tak |
| `ClientId` | `int` | tak | FK→Firm | tak |
| `DocumentTypeId` | `int` | tak | FK→DocumentType | tak |
| `DocumentStatusId` | `int` | tak | FK→DocumentStatus | tak |
| `UserFirmId` | `int` | tak | FK→UserFirm | tak |

> Pełne definicje: `../P-12_AddDocument/04_DANE_MODELE_MAPOWANIA.md#Document`.

### Encja `DocumentProduct` → tabela `DocumentProduct`

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `Id` | `int IDENTITY` | nie | PK | — |
| `Quantity` | `decimal(18,2)` | nie | — | — |
| `UnitPrice` | `decimal(18,2)` | nie | — | — |
| `TotalPrice` | `decimal(18,2)` | nie | — | — |
| `DocumentId` | `int` | tak | FK→Document | tak |
| `ProductId` | `int` | tak | FK→Product | tak |

---

## 3. Relacje i kaskady

| Z encji | Pole FK | Do encji | Kierunek | Kaskada |
|---|---|---|---|---|
| `DocumentProduct` | `DocumentId` | `Document` | N..1 | brak jawnej kaskady (ręczne usunięcie w serwisie) |
| `Document` | `BankAccountId` | `BankAccount` | N..1 | OnDelete: Cascade (snapshot) |
| `Document` | `UserFirmId` | `UserFirm` | N..1 | OnDelete: Restrict / SetNull |

> `DocumentProduct` jest usuwany ręcznie przez serwis (`RemoveRangeAsync`) przed usunięciem `Document` — brak kaskady DB dla tej relacji.

---

## 4. Mapowania AutoMapper

Brak — proces nie używa AutoMapper.

---

## 5. Zapytania (LINQ/SQL)

Kotwica: `DocumentService.cs › DocumentService.DeleteDocuments`

```csharp
// 1. Pobierz dokumenty z pozycjami
var documents = await _unitOfWork.Documents.Query()
    .Include(dp => dp.DocumentProducts)
    .Where(d => documentIds.Contains(d.Id))
    .ToListAsync();

// 2. Usuń pozycje dokumentów
await _unitOfWork.DocumentProducts.RemoveRangeAsync(documents.SelectMany(d => d.DocumentProducts!));

// 3. Usuń dokumenty
await _unitOfWork.Documents.RemoveRangeAsync(documents);

// 4. Zapisz zmiany
await _unitOfWork.CompleteAsync();
```

> Operator null-forgiving `!` w `d.DocumentProducts!` — jeżeli Include nie zwróciło kolekcji, `SelectMany` rzuci `NullReferenceException`.

---

## 6. Użyte enumy i lookupy

Brak — proces nie czyta ani nie ustawia statusów / typów dokumentów.
