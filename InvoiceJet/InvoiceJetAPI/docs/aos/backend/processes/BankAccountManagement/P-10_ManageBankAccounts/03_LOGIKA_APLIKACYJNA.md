# ManageBankAccounts — Logika aplikacyjna

Proces `P-10` obsługuje cztery endpointy CRUD dla zasobu `BankAccount`. Każdy ma osobną sekcję.

---

## Endpoint A — `GET /api/BankAccount/GetUserFirmBankAccounts`

### 0. Algorytm w skrócie

1. Kontroler odbiera GET bez parametrów, wywołuje `_bankAccountService.GetUserFirmBankAccounts()`.
2. Serwis pobiera `userId` z JWT, wywołuje `BankAccountRepository.GetUserFirmBankAccountsAsync(userId)`.
3. Repozytorium zwraca konta należące do aktywnej firmy użytkownika.
4. Jeśli lista pusta → zwrot pustej kolekcji (bez wyjątku).
5. AutoMapper mapuje `List<BankAccount>` → `List<BankAccountDto>`.
6. Kontroler zwraca `200 OK` z kolekcją DTO.

### 1. Wejście do procesu

Kotwica: `BankAccountController.cs › BankAccountController.GetUserFirmBankAccounts`

```csharp
[HttpGet("GetUserFirmBankAccounts")]
public async Task<ActionResult<BankAccountDto>> GetUserFirmBankAccounts()
{
    var bankAccountDto = await _bankAccountService.GetUserFirmBankAccounts();
    return Ok(bankAccountDto);
}
```

Brak parametrów — `userId` pobierany z tokenu JWT w serwisie przez `IUserService.GetCurrentUserId()`.

### 2. Walidacje (faza wejściowa)

> Wymiar nie występuje w tym endpoincie. Endpoint jest read-only. Brak walidacji wejściowych — jeśli użytkownik nie ma firmy lub kont, zwracana jest pusta kolekcja.

### 3. Logika biznesowa

Kotwica: `BankAccountService.cs › BankAccountService.GetUserFirmBankAccounts`

```csharp
public async Task<ICollection<BankAccountDto>> GetUserFirmBankAccounts()
{
    var bankAccounts = await _unitOfWork.BankAccounts.GetUserFirmBankAccountsAsync(_userService.GetCurrentUserId());
    if (bankAccounts.Count == 0)
    {
        return new List<BankAccountDto>();
    }

    var bankAccountDtos = _mapper.Map<List<BankAccountDto>>(bankAccounts);
    return bankAccountDtos;
}
```

**Krok 1:** `_userService.GetCurrentUserId()` — pobranie `userId` z JWT claim `HttpContext`.

**Krok 2:** `BankAccountRepository.GetUserFirmBankAccountsAsync(userId)` — filtruje konta aktywnej firmy użytkownika. Kotwica: `BankAccountRepository.cs › BankAccountRepository.GetUserFirmBankAccountsAsync`:

```csharp
return await _dbSet
    .Where(ba => ba.UserFirm.UserId == userId
              && ba.UserFirm.User.ActiveUserFirmId == ba.UserFirmId)
    .ToListAsync();
```

**Krok 3:** Jeśli `Count == 0` → zwrot `new List<BankAccountDto>()` (pusta kolekcja, nie `null`).

**Krok 4:** `AutoMapper.Map<List<BankAccountDto>>(bankAccounts)`.

### 4. Zapisy do bazy i transakcje

> Wymiar nie dotyczy. Endpoint jest read-only — brak zapisów, brak `CompleteAsync()`.

### 5. Odpowiedź

HTTP `200 OK`. Ciało: `ICollection<BankAccountDto>` (typ zwracany `List<BankAccountDto>`) — tablica DTO lub `[]` gdy brak kont.

---

## Endpoint B — `POST /api/BankAccount/AddUserFirmBankAccount`

### 0. Algorytm w skrócie

1. Kontroler odbiera `BankAccountDto` z body `[FromBody]`, wywołuje `_bankAccountService.AddUserFirmBankAccount(bankAccountDto)`.
2. Serwis mapuje DTO → `BankAccount` przez AutoMapper.
3. Serwis pobiera `userFirmId` → null → `UserHasNoAssociatedFirmException` (WAL-01 → 400).
4. Serwis ustawia `bankAccount.UserFirmId = userFirmId.Value`.
5. Jeśli `bankAccount.IsActive == true` → `DeactivateOtherBankAccounts(userFirmId)` — dezaktywuje wszystkie inne konta firmy (`IsActive = false`, `UpdateAsync` per konto, bez `CompleteAsync`).
6. `BankAccounts.AddAsync(bankAccount)` + `CompleteAsync()` — jeden atomowy commit (dezaktywacje + dodanie).
7. AutoMapper mapuje `BankAccount` → `BankAccountDto` (z nadanym `Id`).
8. Kontroler zwraca `200 OK` z `BankAccountDto`.

### 1. Wejście do procesu

Kotwica: `BankAccountController.cs › BankAccountController.AddUserFirmBankAccount`

```csharp
[HttpPost("AddUserFirmBankAccount")]
public async Task<ActionResult<BankAccountDto>> AddUserFirmBankAccount([FromBody] BankAccountDto bankAccountDto)
{
    var bankAccount = await _bankAccountService.AddUserFirmBankAccount(bankAccountDto);
    return Ok(bankAccount);
}
```

### 2. Walidacje (faza wejściowa)

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Użytkownik ma aktywną firmę (`userFirmId != null`) | `BankAccountService.cs › BankAccountService.AddUserFirmBankAccount` | `UserHasNoAssociatedFirmException` (WAL-01 → 400) |

```csharp
var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
if (!userFirmId.HasValue)
{
    throw new UserHasNoAssociatedFirmException();
}
```

### 3. Logika biznesowa

Kotwica: `BankAccountService.cs › BankAccountService.AddUserFirmBankAccount`

**Krok 1:** `_mapper.Map<BankAccount>(bankAccountDto)` — mapowanie DTO na nową encję (bez `UserFirmId`, bo pola nie ma w DTO). Wykonywane **przed** walidacją WAL-01.

**Krok 2:** Pobranie i przypisanie `UserFirmId`:
```csharp
bankAccount.UserFirmId = userFirmId.Value;
```

**Krok 3:** Logika aktywacji konta — jeśli `bankAccount.IsActive == true`, serwis dezaktywuje wszystkie inne konta firmy:
```csharp
if (bankAccount.IsActive)
{
    await DeactivateOtherBankAccounts(bankAccount.UserFirmId);
}
```

Kotwica `DeactivateOtherBankAccounts`: `BankAccountService.cs › BankAccountService.DeactivateOtherBankAccounts`

```csharp
public async Task DeactivateOtherBankAccounts(int userFirmId, int? excludeAccountId = null)
{
    var otherAccounts = await _unitOfWork.BankAccounts.Query()
        .Where(ba => ba.UserFirmId == userFirmId && ba.Id != excludeAccountId)
        .ToListAsync();

    foreach (var account in otherAccounts)
    {
        account.IsActive = false;
        await _unitOfWork.BankAccounts.UpdateAsync(account);
    }
}
```

Przy Add: `excludeAccountId = null` → dezaktywuje **wszystkie** inne konta firmy. `UpdateAsync` per konto, ale **bez `CompleteAsync()`** — zapis odłożony do wywołania nadrzędnego.

### Tabela: pole encji `BankAccount` → źródło (AddUserFirmBankAccount)

| Pole encji `BankAccount` | Źródło |
|---|---|
| `Id` | generowany przez DB (IDENTITY) po `CompleteAsync()` |
| `BankName` | `bankAccountDto.BankName` |
| `Iban` | `bankAccountDto.Iban` |
| `Currency` | `bankAccountDto.Currency` (enum `CurrencyEnum`) |
| `IsActive` | `bankAccountDto.IsActive` |
| `UserFirmId` | `userFirmId.Value` — wynik `Users.GetUserFirmIdAsync(userId)` |

### 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | `CompleteAsync()` |
|---|---|---|---|
| 1..N | `UpdateAsync(account)` — dezaktywacja innych kont (w pętli `DeactivateOtherBankAccounts`) | `GenericRepository.UpdateAsync` | nie — tylko oznaczenie |
| N+1 | `AddAsync(bankAccount)` | `GenericRepository.AddAsync` | nie |
| N+2 | `CompleteAsync()` | `UnitOfWork.CompleteAsync()` | tak — atomowy commit: dezaktywacje + dodanie nowego konta |

> Jeden `CompleteAsync()` po wszystkich operacjach — atomowość gwarantuje, że dezaktywacja starych kont i dodanie nowego konta jest jedną transakcją DB. Brak jawnej transakcji `BeginTransactionAsync`, ale EF Core owija `SaveChangesAsync()` automatyczną transakcją SQL Server.

### 5. Odpowiedź

```csharp
return _mapper.Map<BankAccountDto>(bankAccount);
```

HTTP `200 OK`. Ciało: `BankAccountDto` z wypełnionym `Id` (nadanym przez DB). `Currency` jako wartość enum.

### 6. Uwagi techniczne

- [UWAGA: Mapowanie `_mapper.Map<BankAccount>(bankAccountDto)` wykonywane **przed** sprawdzeniem `userFirmId` (WAL-01). Jeśli `userFirmId == null`, wyjątek zostanie rzucony po mapowaniu — nieistotne funkcjonalnie, ale mapowanie jest niepotrzebne gdy firma nie istnieje. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## Endpoint C — `PUT /api/BankAccount/EditUserFirmBankAccount`

### 0. Algorytm w skrócie

1. Kontroler odbiera `BankAccountDto` z body `[FromBody]` (musi zawierać `Id`), wywołuje `_bankAccountService.EditUserFirmBankAccount(bankAccountDto)`.
2. Serwis pobiera encję z DB po `bankAccountDto.Id` → brak → `Exception("Bank account not found.")` (WAL-02 → **500 ⚠️**).
3. AutoMapper mapuje DTO na tracked encję.
4. Jeśli `bankAccount.IsActive == true` → `DeactivateOtherBankAccounts(userFirmId, bankAccount.Id)` — dezaktywuje inne konta (z wyjątkiem edytowanego).
5. `CompleteAsync()` — jeden atomowy commit.
6. AutoMapper mapuje encję → `BankAccountDto`.
7. Kontroler zwraca `200 OK`.

### 1. Wejście do procesu

Kotwica: `BankAccountController.cs › BankAccountController.EditUserFirmBankAccount`

```csharp
[HttpPut("EditUserFirmBankAccount")]
public async Task<ActionResult<BankAccountDto>> EditUserFirmBankAccount([FromBody] BankAccountDto bankAccountDto)
{
    var bankAccount = await _bankAccountService.EditUserFirmBankAccount(bankAccountDto);
    return Ok(bankAccount);
}
```

### 2. Walidacje (faza wejściowa)

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Konto o danym `Id` istnieje w DB | `BankAccountService.cs › BankAccountService.EditUserFirmBankAccount` | `Exception("Bank account not found.")` (WAL-02 → **500 ⚠️**) |

```csharp
var bankAccount = await _unitOfWork.BankAccounts.GetByIdAsync(bankAccountDto.Id) ?? throw new Exception("Bank account not found.");
```

### 3. Logika biznesowa

Kotwica: `BankAccountService.cs › BankAccountService.EditUserFirmBankAccount`

**Krok 1:** `_mapper.Map(bankAccountDto, bankAccount)` — mapuje pola DTO na istniejącą tracked encję. `UserFirmId` nie jest w DTO → pozostaje bez zmian.

**Krok 2:** Jeśli po mapowaniu `bankAccount.IsActive == true` → `DeactivateOtherBankAccounts(bankAccount.UserFirmId, bankAccount.Id)`:

```csharp
if (bankAccount.IsActive)
{
    await DeactivateOtherBankAccounts(bankAccount.UserFirmId, bankAccount.Id);
}
```

`excludeAccountId = bankAccount.Id` → dezaktywuje wszystkie konta firmy **poza edytowanym** (żeby nie wyzerować aktywności właśnie aktualizowanego konta).

### Tabela: pole encji `BankAccount` → źródło (EditUserFirmBankAccount)

| Pole encji `BankAccount` | Źródło |
|---|---|
| `Id` | bez zmian (tracked przez EF Core) |
| `BankName` | `bankAccountDto.BankName` |
| `Iban` | `bankAccountDto.Iban` |
| `Currency` | `bankAccountDto.Currency` |
| `IsActive` | `bankAccountDto.IsActive` |
| `UserFirmId` | bez zmian (pole nie istnieje w `BankAccountDto`) |

### 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | `CompleteAsync()` |
|---|---|---|---|
| 1..N | `UpdateAsync(account)` — dezaktywacja innych kont (jeśli `IsActive = true`) | `GenericRepository.UpdateAsync` | nie |
| N+1 | `CompleteAsync()` | `UnitOfWork.CompleteAsync()` | tak — atomowy commit |

### 5. Odpowiedź

```csharp
return _mapper.Map<BankAccountDto>(bankAccount);
```

HTTP `200 OK`. Ciało: `BankAccountDto` odzwierciedlający stan encji po zapisie.

### 6. Uwagi techniczne

- [UWAGA: Generyczny `Exception("Bank account not found.")` (WAL-02) trafia do catch-all w `ExceptionMiddleware` → `500 Internal Server Error` zamiast `400`/`404`. Brak dedykowanego `BankAccountNotFoundException`. Kotwica: `BankAccountService.cs › BankAccountService.EditUserFirmBankAccount`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `EditUserFirmBankAccount` nie sprawdza, czy edytowane konto należy do aktywnej firmy bieżącego użytkownika. `GetByIdAsync(bankAccountDto.Id)` zwraca każde konto z DB po `Id` — użytkownik mógłby edytować konto innego użytkownika znając `Id`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## Endpoint D — `PUT /api/BankAccount/DeleteUserFirmBankAccounts`

### 0. Algorytm w skrócie

1. Kontroler odbiera `int[] bankAccountIds` z body `[FromBody]`, wywołuje `_bankAccountService.DeleteUserFirmBankAccounts(bankAccountIds)`.
2. Serwis iteruje po `bankAccountIds`:
   a. Pobiera konto po ID → brak → `Exception("Bank account not found.")` (WAL-03 → **500 ⚠️**).
   b. Sprawdza powiązanie z `Document` → istnieje → `BankAccountAssociatedWithDocumentsException` (WAL-04 → 400).
   c. Oznacza konto do usunięcia: `RemoveAsync(bankAccount)`.
3. Po pętli: `CompleteAsync()` — usuwa wszystkie oznaczone konta.
4. Kontroler zwraca `200 OK` (puste ciało).

### 1. Wejście do procesu

Kotwica: `BankAccountController.cs › BankAccountController.DeleteUserFirmBankAccounts`

```csharp
[HttpPut("DeleteUserFirmBankAccounts")]
public async Task<ActionResult<BankAccountDto>> DeleteUserFirmBankAccounts([FromBody] int[] bankAccountIds)
{
    await _bankAccountService.DeleteUserFirmBankAccounts(bankAccountIds);
    return Ok();
}
```

> Parametr `int[] bankAccountIds` — bindowany z **body** `[FromBody]`, **nie z query string** (w odróżnieniu od `ProductController.DeleteProducts`, który używał query string). Tablica JSON w body.

### 2. Walidacje (faza wejściowa — per iteracja)

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Konto o danym ID istnieje | `BankAccountService.cs › BankAccountService.DeleteUserFirmBankAccounts` | `Exception("Bank account not found.")` (WAL-03 → **500 ⚠️**) |
| 2 | Konto nie jest powiązane z dokumentem | `BankAccountService.cs › BankAccountService.DeleteUserFirmBankAccounts` | `BankAccountAssociatedWithDocumentsException` (WAL-04 → 400) |

**WAL-03:**
```csharp
var bankAccount = await _unitOfWork.BankAccounts.GetByIdAsync(bankAccountId) ?? throw new Exception("Bank account not found.");
```

**WAL-04:**
```csharp
bool isAssociatedWithDocuments = await _unitOfWork.Documents.Query()
    .AnyAsync(d => d.BankAccountId == bankAccountId);

if (isAssociatedWithDocuments)
{
    throw new BankAccountAssociatedWithDocumentsException($"Can't delete. Bank account is associated with documents.");
}
```

### 3. Logika biznesowa

Kotwica: `BankAccountService.cs › BankAccountService.DeleteUserFirmBankAccounts`

```csharp
await _unitOfWork.BankAccounts.RemoveAsync(bankAccount);
```

Każde konto przechodzące walidacje jest oznaczane do usunięcia (`RemoveAsync`). EF Core zbiera zmiany w change tracker — rzeczywisty `DELETE` następuje przy `CompleteAsync()`.

### Tabela: pole encji → źródło

> Wymiar nie dotyczy — encje są usuwane, nie tworzone ani modyfikowane.

### 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | `CompleteAsync()` |
|---|---|---|---|
| 1..N | `RemoveAsync(bankAccount)` (w pętli) | `GenericRepository.RemoveAsync` | nie — tylko oznaczenie |
| N+1 | `CompleteAsync()` | `UnitOfWork.CompleteAsync()` | tak — wszystkie DELETE naraz |

> Brak jawnej transakcji. EF Core automatycznie owija `SaveChangesAsync()` transakcją SQL Server — jeśli którykolwiek `DELETE` się nie powiedzie, cały batch jest wycofywany. Wyjątek rzucony podczas iteracji przed `CompleteAsync()` przerwie pętlę — brak częściowego zapisu.

### 5. Odpowiedź

HTTP `200 OK`. Puste ciało (`return Ok()` bez argumentu).

### 6. Uwagi techniczne

- [UWAGA: `DeleteUserFirmBankAccounts` używa metody HTTP `PUT` do usuwania zasobów — niezgodność z konwencją REST (`DELETE`). Kotwica: `BankAccountController.cs › BankAccountController.DeleteUserFirmBankAccounts` — `[HttpPut("DeleteUserFirmBankAccounts")]`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Generyczny `Exception("Bank account not found.")` (WAL-03) trafia do catch-all → `500`. Brak dedykowanego wyjątku. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `DeleteUserFirmBankAccounts` nie sprawdza, czy usuwane konta należą do aktywnej firmy bieżącego użytkownika. Użytkownik znający `Id` konta mógłby usunąć konto innego użytkownika. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Parametr `bankAccountIds` jest pobierany z body (`[FromBody]`), podczas gdy `ProductController.DeleteProducts` używał query string. Niespójność między endpointami usuwania w różnych kontrolerach. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
