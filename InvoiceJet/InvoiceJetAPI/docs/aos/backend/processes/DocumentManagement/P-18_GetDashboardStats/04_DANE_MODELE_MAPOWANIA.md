# GetDashboardStats — Dane, modele i mapowania

## 1. DTO

### `DashboardStatsDto` (wyjście)

Źródło: `DashboardStatsDto.cs`

| Pole | Typ | Opis |
|---|---|---|
| `TotalDocuments` | `int` | Liczba dokumentów danego roku i typu |
| `TotalClients` | `int` | Liczba firm klienckich użytkownika |
| `TotalProducts` | `int` | Liczba produktów firmy |
| `TotalBankAccounts` | `int` | Liczba kont bankowych firmy |
| `MonthlyTotals` | `List<MonthlyTotalDto>` | Zestawienie miesięczne (tylko miesiące z dokumentami) |

> Gdy brak firmy, serwis zwraca `new DashboardStatsDto()` — pola numeryczne = `0`, `MonthlyTotals = null` (null! initializer).

### `MonthlyTotalDto`

Źródło: `MonthlyTotalDto.cs`

| Pole | Typ | Opis |
|---|---|---|
| `Month` | `int` | Numer miesiąca (1–12) |
| `InvoiceAmount` | `decimal` | Suma `TotalPrice` wszystkich dokumentów w tym miesiącu |
| `IncomeAmount` | `decimal` | Suma `TotalPrice` dokumentów ze statusem `Paid` (DocumentStatusId=2) |

> `MonthlyTotals` zawiera TYLKO miesiące, w których istnieją dokumenty (GroupBy → nie daje 12 wierszy dla każdego roku).

---

## 2. Encje i kolumny

### Encja `Document` (odczyt)

Tabela `Document`. Kolumny używane w zapytaniach:

| Kolumna | Typ SQL | Nullable | Filtr / rola |
|---|---|---|---|
| `UserFirmId` | `int` | tak | filtr `WHERE UserFirmId == userFirmId` |
| `IssueDate` | `datetime2` | nie | filtr rok: `IssueDate.Year == year` |
| `DocumentTypeId` | `int` | tak | Join przez `DocumentType!.Id == documentType` |
| `DocumentStatusId` | `int` | tak | warunek `Paid`: `DocumentStatusId == 2` |
| `TotalPrice` | `decimal(18,2)` | nie | `Sum(TotalPrice)` |

### Encja `Firm` (count klientów)

Tabela `Firm`. Kolumny używane:
- `IsClient` (via `UserFirm`) — filtr klientów

### Encja `Product` (count produktów)

Tabela `Product`. Kolumny używane:
- `UserFirmId` — filtr produktów firmy

### Encja `BankAccount` (count kont bankowych)

Tabela `BankAccount`. Kolumny używane:
- `UserFirmId` — filtr kont firmy

---

## 3. Relacje i kaskady

| Z encji | Pole FK | Do encji | Kierunek | Używana w procesie |
|---|---|---|---|---|
| `Document` | `UserFirmId` | `UserFirm` | N..1 | filtr dokumentów |
| `Document` | `DocumentTypeId` | `DocumentType` | N..1 | filtr po typie (`DocumentType!.Id`) |
| `UserFirm` | `UserId` | `User` | N..1 | `GetTotalClientsAsync(UserId)` |

---

## 4. Mapowania AutoMapper

Brak — `DashboardStatsDto` i `MonthlyTotalDto` budowane bezpośrednio w serwisie (LINQ projection + ręczna inicjalizacja).

---

## 5. Zapytania (LINQ/SQL)

### Query 1: Łączna liczba dokumentów

Kotwica: `DocumentService.cs › DocumentService.GetTotalDocumentsAsync`

```csharp
return await _unitOfWork.Documents.Query()
    .Where(d => d.UserFirmId == userFirmId
                && d.IssueDate.Year == year
                && d.DocumentType!.Id == documentType)
    .CountAsync();
```

### Query 2: Łączna liczba klientów

Kotwica: `FirmRepository.cs › FirmRepository.GetTotalClientsAsync`

```csharp
// Wewnątrz repozytorium — CountAsync z filtrem IsClient=true dla userId
```

### Query 3: Łączna liczba produktów

Kotwica: `ProductRepository.cs › ProductRepository.GetTotalProductsAsync`

### Query 4: Łączna liczba kont bankowych

Kotwica: `BankAccountRepository.cs › BankAccountRepository.GetTotalBankAccountsAsync`

### Query 5: Zestawienie miesięczne

Kotwica: `DocumentService.cs › DocumentService.GetMonthlyTotalsAsync`

```csharp
return await _unitOfWork.Documents.Query()
    .Where(d => d.UserFirmId == userFirmId && d.IssueDate.Year == year && d.DocumentType!.Id == documentType)
    .GroupBy(d => new { month = d.IssueDate.Month })
    .Select(group => new MonthlyTotalDto
    {
        Month = group.Key.month,
        InvoiceAmount = group.Sum(d => d.TotalPrice),
        IncomeAmount = group.Sum(d => d.DocumentStatusId == (int)DocumentStatusEnum.Paid ? d.TotalPrice : 0)
    })
    .OrderBy(x => x.Month)
    .ToListAsync();
```

---

## 6. Użyte enumy i lookupy

| Element | Rodzaj | Wartości |
|---|---|---|
| `DocumentStatusEnum` | enum | `Unpaid=1`, `Paid=2` — używany w warunku `IncomeAmount` |
| `DocumentType` (seed) | tabela | `Id=1→Faktura`, `Id=2→Proforma`, `Id=3→Storno` — parametr `documentType` z trasy |
