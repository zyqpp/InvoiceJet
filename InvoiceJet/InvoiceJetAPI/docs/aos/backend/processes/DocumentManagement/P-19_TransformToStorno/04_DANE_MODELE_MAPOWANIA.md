# TransformToStorno — Dane, modele i mapowania

## 1. DTO

### Wejście — `int[]`

Ciało żądania to tablica identyfikatorów dokumentów do przekształcenia w storno.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| (array) | `int[]` | tak (framework) | Tablica Id dokumentów; `[FromBody]` |

> Brak atrybutów walidacyjnych. Pusta tablica `[]` → pętla `foreach` nie wykonuje żadnej iteracji → `200 OK` bez zmian.

### Wyjście

Brak body (`return Ok()` — HTTP 200 bez zawartości).

---

## 2. Encje i kolumny

### Encja `Document` → tabela `Document`

Kotwica: `Document.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("Document")`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks | Rola w procesie |
|---|---|---|---|---|---|
| `Id` | `int IDENTITY` | nie | PK | — | filtr w WHERE |
| `DocumentTypeId` | `int` | tak | FK→DocumentType | tak | **aktualizowana** → `3` (StornoInvoice) |
| `UserFirmId` | `int` | tak | FK→UserFirm | tak | filtr ownership |

Kolumny niezmieniane w tym procesie: `DocumentNumber`, `IssueDate`, `DueDate`, `TotalPrice`, `BankAccountId`, `ClientId`, `DocumentStatusId`.

---

## 3. Relacje i kaskady

| Z encji | Pole FK | Do encji | Kierunek | Rola |
|---|---|---|---|---|
| `Document` | `DocumentTypeId` | `DocumentType` | N..1 | aktualizowany do `3` (StornoInvoice) |
| `Document` | `UserFirmId` | `UserFirm` | N..1 | filtr ownership w Query |

---

## 4. Mapowania AutoMapper

Brak — proces nie używa AutoMapper.

---

## 5. Zapytania (LINQ/SQL)

Kotwica: `DocumentService.cs › DocumentService.TransformToStorno`

```csharp
// Dla każdego documentId w pętli:
var document = await _unitOfWork.Documents.Query()
    .Where(d => d.Id == documentId && d.UserFirmId == activeUserFirmId)
    .FirstOrDefaultAsync();

if (document == null)
    throw new Exception("Document not found.");

document.DocumentTypeId = (int)DocumentTypeEnum.StornoInvoice;  // = 3
await _unitOfWork.Documents.UpdateAsync(document);
await _unitOfWork.CompleteAsync();
```

> [UWAGA: `UpdateAsync` + `CompleteAsync` wewnątrz `foreach` — N zapytań UPDATE + N `SaveChangesAsync`. Brak transakcji obejmującej całą operację. Kotwica: `DocumentService.cs › DocumentService.TransformToStorno`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 6. Użyte enumy i lookupy

| Element | Rodzaj | Wartości |
|---|---|---|
| `DocumentTypeEnum` | enum | `Invoice=1`, `ProformaInvoice=2`, `StornoInvoice=3` |
| `DocumentType` (seed) | tabela słownikowa | `Id=3 → "Factura Storno"` — wartość docelowa po transform |
