# ManageDocumentPdf — Dane, modele i mapowania

## 1. DTO

### `DocumentRequestDto` (wejście — oba endpointy)

Taki sam typ jak w P-12/P-13/P-14. Pełna definicja: `../P-12_AddDocument/04_DANE_MODELE_MAPOWANIA.md`.

Pola szczególnie istotne dla procesu P-17:

| Pole | Typ | Opis |
|---|---|---|
| `DocumentNumber` | `string?` | Numer dokumentu — używany jako nazwa pliku PDF |
| `DocumentSeries` | `DocumentSeriesDto?` | Seria (fallback dla numeru gdy `DocumentNumber` null) |
| `Seller` | `FirmDto?` | Nadpisywane przez serwis z `activeUserFirm.Firm` |
| `BankAccount` | `BankAccountDto?` | Nadpisywane przez serwis (`GetInvoicePdfStream` only) |
| `DocumentType` | `DocumentType?` | Używany przez `PdfGenerationService` do wyboru fabryki |
| `Products` | `List<DocumentProductRequestDto>` | Pozycje dokumentu |

---

### `DocumentStreamDto` (wyjście — API-29)

Źródło: `DocumentStreamDto.cs`

| Pole | Typ | Opis |
|---|---|---|
| `DocumentNumber` | `string?` | Numer dokumentu (z DTO lub z `DocumentSeries.CurrentNumber`) |
| `PdfContent` | `byte[]?` | Bajty pliku PDF; `null` gdy generowanie nieudane |

---

## 2. Encje i kolumny

### Encja `UserFirm` (odczyt)

Używana w `GetUserFirmAsync` — pobiera dane sprzedawcy (`Firm`) dla obu endpointów.

| Kolumna | Typ SQL | Nullable | Klucz |
|---|---|---|---|
| `UserId` | `nvarchar(450)` | nie | PK+FK→AspNetUsers |
| `UserFirmId` | `int` | nie | FK→Firm |
| `IsClient` | `bit` | nie | — |

### Encja `BankAccount` (odczyt — API-29 only)

| Kolumna | Typ SQL | Nullable | Klucz |
|---|---|---|---|
| `Id` | `int IDENTITY` | nie | PK |
| `AccountNumber` | `nvarchar(max)` | nie | — |
| `BankName` | `nvarchar(max)` | nie | — |
| `IsActive` | `bit` | nie | — |
| `UserFirmId` | `int` | nie | FK→Firm |

---

## 3. Relacje i kaskady

| Z encji | Pole FK | Do encji | Kierunek | Używana w procesie |
|---|---|---|---|---|
| `Document` | `BankAccountId` | `BankAccount` | N..1 | API-29: `Select(d.BankAccount)` |
| `Document` | `UserFirmId` | `UserFirm` | N..1 | API-29: filtr `d.UserFirmId == firmId` |
| `UserFirm` | `UserFirmId` | `Firm` | N..1 | oba: `GetUserFirmAsync` → `Firm` |

---

## 4. Mapowania AutoMapper

| Źródło | Cel | Profil | Uwagi |
|---|---|---|---|
| `Firm` (UserFirm.Firm) | `FirmDto` | `FirmProfile` | `documentRequestDto.Seller` nadpisywane przez serwis |
| `BankAccount` | `BankAccountDto` | `BankAccountProfile` | `documentRequestDto.BankAccount` nadpisywane przez serwis (API-29 only) |

---

## 5. Zapytania (LINQ/SQL)

### API-28 — GenerateDocumentPdf

Kotwica: `DocumentService.cs › DocumentService.GeneratePdfDocument`

```csharp
// Brak zapytania DB poza GetUserFirmAsync
var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(_userService.GetCurrentUserId());
if (activeUserFirm is null) throw new UserHasNoAssociatedFirmException();
```

### API-29 — GetInvoicePdfStream

Kotwica: `DocumentService.cs › DocumentService.GetInvoicePdfStream`

```csharp
// Pobierz konto bankowe z pierwszego dokumentu firmy
var documentBankAccount = await _unitOfWork.Documents.Query()
    .Where(d => d.UserFirmId == activeUserFirm.UserFirmId)
    .Select(d => d.BankAccount)
    .FirstOrDefaultAsync();
```

> [UWAGA: Zapytanie pobiera konto bankowe z PIERWSZEGO dokumentu firmy (brak kryterium wyboru, bez OrderBy). Nie jest to konto bankowe dokumentu przekazanego w `documentRequestDto`. Kotwica: `DocumentService.cs › DocumentService.GetInvoicePdfStream`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 6. Użyte enumy i lookupy

| Element | Rodzaj | Opis |
|---|---|---|
| `DocumentType.Id` | lookup w `PdfGenerationService` | Używany do wyboru fabryki (`DocumentFactoryProvider.GetDocumentFactory(documentType.Id)`) |
| `DocumentTypeEnum` | enum | `Invoice=1`, `ProformaInvoice=2`, `StornoInvoice=3` |
