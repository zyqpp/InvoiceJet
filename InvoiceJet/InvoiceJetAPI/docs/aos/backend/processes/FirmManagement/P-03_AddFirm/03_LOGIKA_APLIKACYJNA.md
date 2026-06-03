# AddFirm — Logika aplikacyjna

## 0. Algorytm w skrócie

1. Kontroler odbiera `FirmDto` z body i `isClient` z URL, wywołuje `FirmService.AddFirm(firmDto, isClient)`.
2. Serwis mapuje `FirmDto → Firm` przez AutoMapper.
3. Dodaje `Firm` do EF Core tracking, zapisuje do DB (`CompleteAsync #1`) — `Firm.Id` zostaje nadany.
4. Wywołuje prywatną metodę `ManageUserFirmRelation(firm.Id, isClient)`.
5. Sprawdza w DB, czy relacja `UserFirm` dla `(userId, firmId)` już istnieje.
6. **Gałąź A — nowa relacja** (standardowa dla AddFirm): tworzy `UserFirm`, sprawdza czy to pierwsza firma użytkownika.
   - **Gałąź A1 — pierwsza firma**: ustawia `User.ActiveUserFirm`, wywołuje `AddInitialDocumentSeries` (tworzy 3 serie i zapisuje — `CompleteAsync #2`); zewnętrzny `CompleteAsync #3` jest pusty.
   - **Gałąź A2 — kolejna firma**: zapisuje `UserFirm` (`CompleteAsync #3`).
7. Ustawia `firmDto.Id = firm.Id`, zwraca `firmDto`.
8. Kontroler zwraca `200 OK` z wypełnionym `FirmDto`.

---

## 1. Wejście do procesu

Kotwica: `AuthController.cs` — nie, `FirmController.cs › FirmController.AddFirm`

```csharp
// FirmController.cs › FirmController.AddFirm
[HttpPost("AddFirm/{isClient}")]
public async Task<ActionResult> AddFirm([FromBody] FirmDto firmDto, bool isClient)
{
    var updatedOrNewFirm = await _firmService.AddFirm(firmDto, isClient);
    return Ok(updatedOrNewFirm);
}
```

- `firmDto`: z body JSON (`[FromBody]`).
- `isClient`: z segmentu URL (`{isClient}` w route template) — typ `bool`, ASP.NET Core parsuje `true`/`false`.
- Autoryzacja: `[Authorize(Roles = "User")]` na poziomie klasy `FirmController`.

---

## 2. Walidacje (faza wejściowa)

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Token JWT obecny i ważny z rolą `"User"` | ASP.NET Core middleware (`[Authorize(Roles = "User")]`) | `401 Unauthorized` / `403 Forbidden` — poza `ExceptionMiddleware` |

> Brak walidacji domenowych (WAL-XX) na polach `FirmDto`. Pola nie są sprawdzane pod kątem wartości `null`, pustości ani formatu przed zapisem do bazy. [UWAGA: brak walidacji wejściowej DTO — NULL pola mogą spowodować DB constraint violation → `500` — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 3. Logika biznesowa

### 3.1 Mapowanie i zapis `Firm`

Kotwica: `FirmService.cs › FirmService.AddFirm`

```csharp
// FirmService.cs › FirmService.AddFirm
var firm = _mapper.Map<Firm>(firmDto);   // FirmDto → Firm (wszystkie pola 1:1)
await _unitOfWork.Firms.AddAsync(firm);
await _unitOfWork.CompleteAsync();        // CompleteAsync #1: Firm zapisany do DB, firm.Id nadany
```

Po `CompleteAsync #1` encja `Firm` ma nadany przez SQL Server `Id` (IDENTITY).

### Tabela: pole encji `Firm` → źródło

| Pole encji `Firm` | Źródło |
|---|---|
| `Id` | auto-generowany przez SQL Server IDENTITY |
| `Name` | `firmDto.Name` |
| `Cui` | `firmDto.Cui` |
| `RegCom` | `firmDto.RegCom` (może być `null` — mismatch z NOT NULL w DB) |
| `Address` | `firmDto.Address` |
| `County` | `firmDto.County` |
| `City` | `firmDto.City` |

---

### 3.2 Zarządzanie relacją `UserFirm` — metoda prywatna `ManageUserFirmRelation`

Kotwica: `FirmService.cs › FirmService.ManageUserFirmRelation`

```csharp
// FirmService.cs › FirmService.ManageUserFirmRelation
private async Task ManageUserFirmRelation(int firmId, bool isClient)
{
    var userId = _userService.GetCurrentUserId();   // claim "userId" z JWT
    var existingUserFirm = await _unitOfWork.UserFirms.GetUserFirmById(userId, firmId);
    // ...
}
```

`GetCurrentUserId()` odczytuje claim `"userId"` (Guid) z `HttpContext.User`. Źródło: `UserService.cs › UserService.GetCurrentUserId`.

**Sprawdzenie istniejącej relacji:**
```csharp
// UserFirmRepository.cs › UserFirmRepository.GetUserFirmById
// (parametr nazywa się "userFirmId" ale query filtruje po FirmId — naming misleading)
_dbSet.Where(uf => uf.UserId == userId && uf.FirmId == userFirmId).FirstOrDefaultAsync()
```

---

### 3.3 Gałąź A — nowa relacja `UserFirm` (typowa dla `AddFirm`)

W `AddFirm` `firm.Id` jest zawsze nowo nadanym Id (nigdy wcześniej nie istniał w `UserFirm`), więc `existingUserFirm == null` zawsze przy wywołaniu z `AddFirm`.

```csharp
// FirmService.cs › FirmService.ManageUserFirmRelation
var newUserFirm = new UserFirm
{
    UserId   = userId,
    FirmId   = firmId,
    IsClient = isClient
};
await _unitOfWork.UserFirms.AddAsync(newUserFirm);
```

### Tabela: pole encji `UserFirm` → źródło

| Pole encji `UserFirm` | Źródło |
|---|---|
| `UserFirmId` | auto-generowany przez SQL Server IDENTITY |
| `UserId` | `_userService.GetCurrentUserId()` — claim z JWT |
| `FirmId` | `firm.Id` (auto-generated po `CompleteAsync #1`) |
| `IsClient` | parametr `isClient` z URL route |

---

### 3.4 Gałąź A1 — pierwsza firma użytkownika (ustawienie aktywnej + inicjalne serie)

```csharp
// FirmService.cs › FirmService.ManageUserFirmRelation
var user = await _unitOfWork.Users.GetUserByIdAsync(_userService.GetCurrentUserId());
// UserRepository: Include(uf => uf.ActiveUserFirm)

if (user!.ActiveUserFirm == null)
{
    user.ActiveUserFirm = newUserFirm;                                   // User tracked: ActiveUserFirmId = newUserFirm.UserFirmId
    await _documentSeriesService.AddInitialDocumentSeries(newUserFirm);  // wewnątrz: CompleteAsync #2
}
```

`AddInitialDocumentSeries` tworzy 3 serie dokumentów:

```csharp
// DocumentSeriesService.cs › DocumentSeriesService.AddInitialDocumentSeries
var documentSeries = new List<DocumentSeries>
{
    new() { SeriesName = DateTime.Now.Year.ToString(), FirstNumber = 1, CurrentNumber = 1,
            IsDefault = true, DocumentType = <lookup "Factura">, UserFirm = userFirm },
    new() { SeriesName = DateTime.Now.Year.ToString(), FirstNumber = 1, CurrentNumber = 1,
            IsDefault = true, DocumentType = <lookup "Factura Storno">, UserFirm = userFirm },
    new() { SeriesName = DateTime.Now.Year.ToString(), FirstNumber = 1, CurrentNumber = 1,
            IsDefault = true, DocumentType = <lookup "Factura Proforma">, UserFirm = userFirm },
};
await _unitOfWork.DocumentSeries.AddRangeAsync(documentSeries);
await _unitOfWork.CompleteAsync();  // CompleteAsync #2: zapisuje newUserFirm + User.ActiveUserFirmId + 3 DocumentSeries
```

### Tabela: pole encji `DocumentSeries` → źródło (dla każdej z 3 tworzonych)

| Pole encji `DocumentSeries` | Źródło |
|---|---|
| `Id` | auto-generowany przez SQL Server IDENTITY |
| `SeriesName` | `DateTime.Now.Year.ToString()` — rok bieżący w momencie wywołania |
| `FirstNumber` | `1` (stała) |
| `CurrentNumber` | `1` (stała) |
| `IsDefault` | `true` (stała) |
| `DocumentTypeId` | Id z `DocumentType` pobranego przez LINQ: `"Factura"` / `"Factura Storno"` / `"Factura Proforma"` |
| `UserFirmId` | `newUserFirm.UserFirmId` (wypełniony po `CompleteAsync #2`) |

---

### 3.5 Gałąź A2 — kolejna firma (nie-pierwsza)

Jeżeli `user.ActiveUserFirm != null`: `AddInitialDocumentSeries` nie jest wywoływana. `CompleteAsync #3` (zewnętrzny w `ManageUserFirmRelation`) zapisuje jedynie `newUserFirm`.

---

### 3.6 Korekta Id w zwracanym DTO

```csharp
// FirmService.cs › FirmService.AddFirm
firmDto.Id = firm.Id;   // uzupełnienie Id generowanego przez DB
return firmDto;
```

---

## 4. Zapisy do bazy i transakcje

| # | Moment | Operacja | Klasa/metoda | `CompleteAsync()` |
|---|---|---|---|---|
| 1 | Po mapowaniu | `AddAsync(firm)` | `GenericRepository.AddAsync` | tak — `FirmService.AddFirm` |
| 2 | Jeśli nowa UserFirm | `AddAsync(newUserFirm)` | `GenericRepository.AddAsync` | nie — zapis dopiero w #2 lub #3 |
| 2 | Jeśli 1. firma: aktualizacja User | `user.ActiveUserFirm = newUserFirm` | EF Core change tracking | nie — jw. |
| 2 | Jeśli 1. firma: 3 serie | `AddRangeAsync(documentSeries)` | `GenericRepository.AddRangeAsync` | tak — `DocumentSeriesService.AddInitialDocumentSeries` (zapisuje UserFirm + User + 3 DocumentSeries) |
| 3 | Zawsze (koniec `ManageUserFirmRelation`) | brak nowych zmian (po A1) lub `newUserFirm` (A2) | `UnitOfWork.CompleteAsync` | tak — `ManageUserFirmRelation` |

> [UWAGA: Proces wykonuje 3 wywołania `CompleteAsync()` bez obejmującej transakcji (`BeginTransactionAsync`). Awaria między `CompleteAsync #1` a `#2` pozostawi w DB zapisan `Firm` bez powiązanego `UserFirm`. Awaria między `#2` a `#3` (gdy 3 serie są zapisane) jest de facto bezpieczna bo `#3` i tak nie ma nic do zapisania w gałęzi A1 — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 5. Odpowiedź

```csharp
// FirmController.cs › FirmController.AddFirm
return Ok(updatedOrNewFirm);  // updatedOrNewFirm == firmDto z Id uzupełnionym
```

`200 OK`, `Content-Type: application/json`, body: `FirmDto` z nadanym `Id`. Zwracany DTO to **ten sam obiekt co żądanie**, zmodyfikowany przez `firmDto.Id = firm.Id` — pozostałe pola nie są przeładowywane z DB.

---

## 6. Uwagi techniczne

- [UWAGA: `isClient = true` przy braku aktywnej firmy użytkownika → firma klienta staje się aktywną firmą użytkownika i generowane są inicjalne serie dokumentów. Może być niezamierzone — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: brak unikalnego indeksu na `Firm.Cui` — ta sama firma (ten sam CUI) może być dodana wielokrotnie, tworząc duplikaty w tabeli `Firm` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `UserFirmRepository.GetUserFirmById` ma parametr `userFirmId` lecz query filtruje po `uf.FirmId == userFirmId`. Nazwa parametru jest myląca — faktycznie jest to `FirmId` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `user!.ActiveUserFirm == null` — null-forgiving operator. Jeżeli `GetUserByIdAsync` zwróci `null` (użytkownik usunięty z DB po wystawieniu JWT) — `NullReferenceException` → `500 Internal Server Error` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- `FirmService` jest zarejestrowany jako `Scoped`. Współdzieli `DbContext` z `DocumentSeriesService` w ramach tego samego żądania — dlatego `CompleteAsync #2` (wywołany wewnątrz `DocumentSeriesService`) zapisuje obiekty trackowane przez `FirmService` (m.in. `newUserFirm`, `user.ActiveUserFirm`).
- `_apiUrl` (`AnafApiUrl`) wczytywany w konstruktorze `FirmService` — `ArgumentNullException` przy starcie jeśli nie skonfigurowany, nie podczas wywołania `AddFirm`.
