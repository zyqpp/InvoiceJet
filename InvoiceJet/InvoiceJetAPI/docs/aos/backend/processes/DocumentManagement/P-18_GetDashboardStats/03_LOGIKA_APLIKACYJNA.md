# GetDashboardStats — Logika aplikacyjna

## 0. Algorytm w skrócie

1. Kontroler odbiera `{year}` i `{documentType}` z trasy, wywołuje `_documentService.GetDashboardStats(year, documentType)`.
2. Serwis pobiera aktywną firmę (`GetUserFirmAsync`) → null → zwraca `new DashboardStatsDto()` (wartości domyślne).
3. Sekwencyjnie wykonuje 5 zapytań: liczba dokumentów, klientów, produktów, kont bankowych, zestawienie miesięczne.
4. Buduje i zwraca `DashboardStatsDto`.
5. Kontroler zwraca `200 OK`.

---

## 1. Wejście do procesu

Kotwica: `DocumentController.cs › DocumentController.GetDashboardStats`

```csharp
[HttpGet("GetDashboardStats/{year}/{documentType}")]
public async Task<IActionResult> GetDashboardStats(int year, int documentType)
{
    var dashboardStats = await _documentService.GetDashboardStats(year, documentType);
    return Ok(dashboardStats);
}
```

---

## 2. Walidacje (faza wejściowa)

Brak jawnych walidacji. Użytkownik bez firmy → cichy fallback do domyślnego DTO.

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| — | Brak WAL; użytkownik bez firmy → `return new DashboardStatsDto()` | `DocumentService.cs › DocumentService.GetDashboardStats` | `200 OK` z zerami i `null` MonthlyTotals |

```csharp
var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(_userService.GetCurrentUserId());
if (activeUserFirm is null)
    return new DashboardStatsDto();
```

---

## 3. Logika biznesowa

Kotwica: `DocumentService.cs › DocumentService.GetDashboardStats`

```csharp
public async Task<DashboardStatsDto> GetDashboardStats(int year, int documentType)
{
    var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(_userService.GetCurrentUserId());
    if (activeUserFirm is null)
        return new DashboardStatsDto();

    var totalDocumentsTask = await GetTotalDocumentsAsync(activeUserFirm.UserFirmId, year, documentType);
    var totalClientsTask = await _unitOfWork.Firms.GetTotalClientsAsync(activeUserFirm.UserId);
    var totalProductsTask = await _unitOfWork.Products.GetTotalProductsAsync(activeUserFirm.UserFirmId);
    var totalBankAccountsTask = await _unitOfWork.BankAccounts.GetTotalBankAccountsAsync(activeUserFirm.UserFirmId);
    var monthlyTotalsTask = await GetMonthlyTotalsAsync(activeUserFirm.UserFirmId, year, documentType);

    return new DashboardStatsDto
    {
        TotalDocuments = totalDocumentsTask,
        TotalClients = totalClientsTask,
        TotalProducts = totalProductsTask,
        TotalBankAccounts = totalBankAccountsTask,
        MonthlyTotals = monthlyTotalsTask
    };
}
```

**Zapytanie 1 — TotalDocuments:**

Kotwica: `DocumentService.cs › DocumentService.GetTotalDocumentsAsync`

```csharp
return await _unitOfWork.Documents.Query()
    .Where(d => d.UserFirmId == userFirmId
                && d.IssueDate.Year == year
                && d.DocumentType!.Id == documentType)
    .CountAsync();
```

Filtruje dokumenty po `UserFirmId`, roku wystawienia i typie dokumentu. Null-forgiving `d.DocumentType!`.

**Zapytanie 2 — TotalClients:**

`FirmRepository.GetTotalClientsAsync(activeUserFirm.UserId)` — liczy firmy klienckie dla `UserId` (nie dla `UserFirmId`).

**Zapytanie 3 — TotalProducts:**

`ProductRepository.GetTotalProductsAsync(activeUserFirm.UserFirmId)` — liczy produkty firmy.

**Zapytanie 4 — TotalBankAccounts:**

`BankAccountRepository.GetTotalBankAccountsAsync(activeUserFirm.UserFirmId)` — liczy konta bankowe firmy.

**Zapytanie 5 — MonthlyTotals:**

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

GroupBy miesiąc → suma całkowita i suma opłaconych. Zawiera tylko miesiące z dokumentami.

### Tabela: pole DTO → źródło

| Pole `DashboardStatsDto` | Źródło |
|---|---|
| `TotalDocuments` | `CountAsync` po `UserFirmId`, roku, typie |
| `TotalClients` | `CountAsync(IsClient=true)` po `UserId` |
| `TotalProducts` | `CountAsync` po `UserFirmId` |
| `TotalBankAccounts` | `CountAsync` po `UserFirmId` |
| `MonthlyTotals` | `GroupBy(Month).Select(Sum(TotalPrice), Sum(Paid))` |

---

## 4. Zapisy do bazy i transakcje

Brak — endpoint read-only.

---

## 5. Odpowiedź

HTTP `200 OK`. Ciało: `DashboardStatsDto`. Gdy brak firmy — pola `int` = `0`, `MonthlyTotals = null`.

---

## 6. Uwagi techniczne

- [UWAGA: Pomimo nazw zmiennych z sufiksem `Task` (np. `totalDocumentsTask`), wszystkie zapytania są wykonywane **sekwencyjnie** (każde `await` blokuje poprzednie). Brak `Task.WhenAll`. Kotwica: `DocumentService.cs › DocumentService.GetDashboardStats`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: `GetTotalClientsAsync(activeUserFirm.UserId)` — liczy klientów po `UserId`, nie `UserFirmId`. Może prowadzić do niespójności jeśli firma ma wielu użytkowników. Kotwica: `DocumentService.cs › DocumentService.GetDashboardStats`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: Null-forgiving `d.DocumentType!.Id` w obu zapytaniach — jeżeli `DocumentType` jest null (dokument bez przypisanego typu), EF może rzucić wyjątek. Kotwica: `DocumentService.cs › DocumentService.GetTotalDocumentsAsync / GetMonthlyTotalsAsync`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: `MonthlyTotals` zawiera tylko miesiące z dokumentami, nie 12 wierszy za rok. Frontend musi uzupełniać brakujące miesiące po stronie klienta. — UWAGA informacyjna]

- [UWAGA: Gdy brak firmy, `MonthlyTotals` ma wartość `null` (nie `[]`). Frontend może crashować przy iteracji. Kotwica: `DashboardStatsDto.cs` — pole `MonthlyTotals` z initializer `null!`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
