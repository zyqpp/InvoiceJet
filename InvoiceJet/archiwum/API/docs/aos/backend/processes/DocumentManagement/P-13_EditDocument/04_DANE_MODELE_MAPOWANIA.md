# EditDocument — Dane, modele i mapowania

## 1. DTO

### `DocumentRequestDto` (wejście i wyjście)

Taki sam typ jak w P-12 AddDocument. Pola istotne dla EditDocument:

| Pole | Typ | Wymagane | Opis / źródło wartości |
|---|---|---|---|
| `Id` | `int` | tak | Id edytowanego dokumentu; musi istnieć w DB |
| `IssueDate` | `DateTime` | tak | Nowa data wystawienia |
| `DueDate` | `DateTime?` | nie | Nowa data płatności |
| `Client.Id` | `int` | tak | Id klienta (`Document.ClientId`) |
| `DocumentType.Id` | `int` | tak | Id typu dokumentu → `Document.DocumentTypeId` |
| `DocumentStatus.Id` | `int` | tak | Id statusu → `Document.DocumentStatusId` |
| `Products` | `List<DocumentProductRequestDto>` | tak | Lista pozycji — zastępuje istniejące |

> [UWAGA: `DocumentRequestDto.DocumentType` i `DocumentRequestDto.DocumentStatus` to typy encji domenowych, nie DTO. Kotwica: `DocumentRequestDto.cs`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

> Atrybuty walidacyjne DTO: brak.

Pełna tabela pól DTO: `../P-12_AddDocument/04_DANE_MODELE_MAPOWANIA.md#DocumentRequestDto`.

---

## 2. Encje i kolumny

### Encja `Document` → tabela `Document` (pola modyfikowane)

Kotwica: `DocumentService.cs › DocumentService.EditDocument`, snapshot: `InvoiceJetDbContextModelSnapshot.cs`.

| Pole encji | Zmiana |
|---|---|
| `IssueDate` | `documentRequestDto.IssueDate` |
| `DueDate` | `documentRequestDto.DueDate` |
| `DocumentTypeId` | `documentRequestDto.DocumentType?.Id` |
| `DocumentStatusId` | `documentRequestDto.DocumentStatus?.Id` |
| `ClientId` | `documentRequestDto.Client.Id` |
| `UserFirmId` | `userFirmId.Value` |
| `UnitPrice` | `sum(UnitPrice * Quantity)` — przez `UpdateDocumentProducts` |
| `TotalPrice` | `sum(TotalPrice)` — przez `UpdateDocumentProducts` |

Pola **niezmieniane**: `Id`, `DocumentNumber`, `BankAccountId`.

Pełna tabela kolumn tabeli `Document`: `../P-12_AddDocument/04_DANE_MODELE_MAPOWANIA.md#Document`.

---

### Encja `DocumentProduct` → tabela `DocumentProduct`

Istniejące rekordy usuwane, nowe tworzone per pozycja. Pełna tabela: `../P-12_AddDocument/04_DANE_MODELE_MAPOWANIA.md#DocumentProduct`.

---

## 3. Relacje i kaskady

Identyczne jak w P-12. Pełna tabela: `../P-12_AddDocument/04_DANE_MODELE_MAPOWANIA.md#relacje`.

---

## 4. Mapowania AutoMapper

| Źródło | Cel | Profil | Uwagi |
|---|---|---|---|
| `DocumentProductRequestDto` | `Product` | `DocumentProductProfile` | Używane dla nowych produktów (`Id=0`) w `UpdateDocumentProducts` |

`EditDocument` nie używa AutoMapper do mapowania `Document` — aktualizuje pola encji tracked przez EF Core ręcznie.

---

## 5. Zapytania (LINQ/SQL)

### Query 1: Sprawdzenie aktywnej firmy

```csharp
var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
```

### Query 2: Pobranie dokumentu do edycji

Kotwica: `DocumentService.cs › DocumentService.EditDocument`
```csharp
var document = await _unitOfWork.Documents.GetByIdAsync(documentRequestDto.Id);
if (document == null)
{
    throw new Exception("Document not found.");
}
```

Semantyka: generyczny `GetByIdAsync` — pobiera dokument bez Include. Brak sprawdzenia własności (`UserFirmId`) — możliwe edytowanie dokumentów innego użytkownika.

### Query 3–5: UpdateDocumentProducts

Identyczne jak w P-12. Pełna dokumentacja: `../P-12_AddDocument/04_DANE_MODELE_MAPOWANIA.md#Query3`.

---

## 6. Użyte enumy i lookupy

| Element | Rodzaj | Plik | Wartości |
|---|---|---|---|
| `DocumentStatusEnum` | enum | `InvoiceJet.Domain/Enums/DocumentStatus.cs` | `Unpaid = 1`, `Paid = 2` |
| `DocumentTypeEnum` | enum | `InvoiceJet.Domain/Enums/DocumentType.cs` | `Invoice = 1`, `ProformaInvoice = 2`, `StornoInvoice = 3` |
