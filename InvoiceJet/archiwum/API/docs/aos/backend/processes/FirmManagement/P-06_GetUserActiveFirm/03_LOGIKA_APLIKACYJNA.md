# GetUserActiveFirm — Logika aplikacyjna

## 1. Punkt wejścia — kontroler

Plik: `InvoiceJet.Presentation/Controllers/FirmController.cs › FirmController.GetUserActiveFirm`

```csharp
[HttpGet("GetUserActiveFirm")]
public async Task<ActionResult> GetUserActiveFirm()
{
    var firm = await _firmService.GetUserActiveFirm();
    return Ok(firm);
}
```

Kontroler bezstanowy: brak parametrów, brak walidacji, brak `try/catch`. Tożsamość użytkownika nie jest przekazywana jawnie — serwis sam ją odczytuje z JWT.

## 2. Algorytm główny — `FirmService.GetUserActiveFirm`

Plik: `InvoiceJet.Application/Services/Impl/FirmService.cs › FirmService.GetUserActiveFirm` (linie 92–96)

```csharp
public async Task<FirmDto> GetUserActiveFirm()
{
    var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(_userService.GetCurrentUserId());
    return activeUserFirm == null ? new FirmDto() : _mapper.Map<FirmDto>(activeUserFirm.Firm);
}
```

### Kroki algorytmu

| Krok | Opis | Kotwica |
|---|---|---|
| 1 | Odczyt tożsamości użytkownika z JWT | `_userService.GetCurrentUserId()` |
| 2 | Pobranie aktywnej relacji `UserFirm` (z firmą) | `_unitOfWork.Users.GetUserFirmAsync(userId)` |
| 3 | Rozgałęzienie: brak firmy → pusty DTO | `activeUserFirm == null ? new FirmDto()` |
| 4 | Mapowanie firmy na DTO | `_mapper.Map<FirmDto>(activeUserFirm.Firm)` |
| 5 | Zwrot DTO (kontroler opakowuje w `200 OK`) | `return ...` |

### Szczegół kroku 1 — tożsamość użytkownika

Plik: `InvoiceJet.Application/Services/Impl/UserService.cs › UserService.GetCurrentUserId`

```csharp
public Guid GetCurrentUserId()
{
    var httpContext = _httpContextAccessor.HttpContext;
    if (httpContext.User.Identity is not { IsAuthenticated: true })
        return Guid.Empty;

    var userIdString = httpContext.User.FindFirst("userId")?.Value;
    return Guid.TryParse(userIdString, out var userId) ? userId : Guid.Empty;
}
```

Odczytuje claim `"userId"` z `HttpContext.User`. Zwraca `Guid.Empty`, gdy użytkownik niezautoryzowany lub claim nieparsowalny. Endpoint chroniony `[Authorize]`, więc w praktyce zawsze zwraca poprawny Guid.

### Szczegół kroku 2 — zapytanie repozytorium

Plik: `InvoiceJet.Infrastructure/Persistence/Repositories/UserRepository.cs › UserRepository.GetUserFirmAsync`

```csharp
var userFirm = await _dbSet
    .Where(u => u.Id == userId)
        .Include(uf => uf.ActiveUserFirm)
            .ThenInclude(uf => uf.Firm)
        .Include(uf => uf.ActiveUserFirm)
            .ThenInclude(u => u.User)
    .Select(uf => uf.ActiveUserFirm)
    .SingleOrDefaultAsync();
```

Zwraca aktywną relację `UserFirm` z eager-loaded `Firm`, lub `null` (gdy brak użytkownika lub brak aktywnej firmy). `SingleOrDefaultAsync` jest bezpieczne — filtr po PK gwarantuje max 1 wiersz.

### Szczegół kroku 3 — gałąź braku firmy

```csharp
return activeUserFirm == null ? new FirmDto() : ...;
```

Gdy `activeUserFirm == null` (brak aktywnej firmy lub brak użytkownika) — zwracany jest **świeży, pusty `FirmDto`** z wartościami domyślnymi (`Id=0`, stringi `""`, `RegCom=null`). Brak wyjątku.

### Szczegół kroku 4 — mapowanie

```csharp
_mapper.Map<FirmDto>(activeUserFirm.Firm);
```

Mapuje encję `Firm` (eager-loaded przez `ThenInclude`) na `FirmDto`. Profil: `FirmProfile` — `CreateMap<Firm, FirmDto>().ReverseMap()`.

## 3. Walidacje wejścia (WAL)

| ID | Walidacja | Gdzie sprawdzana | Wynik naruszenia |
|---|---|---|---|
| `WAL-01` | Ważny JWT z rolą `"User"` | `[Authorize(Roles = "User")]` na `FirmController` | `401` / `403` |

Poza autoryzacją proces nie ma żadnych walidacji domenowych — nie ma danych wejściowych do walidowania.

## 4. Obsługa przypadków brzegowych

| Scenariusz | Zachowanie kodu | Wynik |
|---|---|---|
| Użytkownik ma aktywną firmę | `activeUserFirm != null` → mapowanie | `200 OK` z `FirmDto` |
| Użytkownik bez aktywnej firmy (`ActiveUserFirmId == null`) | `Select` projektuje `null` → `activeUserFirm == null` | `200 OK` z pustym `FirmDto` |
| Użytkownik nie istnieje w DB (np. usunięty po wystawieniu JWT) | brak wierszy → `null` | `200 OK` z pustym `FirmDto` |
| `GetCurrentUserId()` zwraca `Guid.Empty` (teoretycznie) | `WHERE Id == Guid.Empty` → brak dopasowania → `null` | `200 OK` z pustym `FirmDto` |

> [UWAGA: Wszystkie ścieżki „brak danych" zwracają identyczny pusty `FirmDto` z `200 OK`. Brak rozróżnienia między „użytkownik bez firmy" a „użytkownik nie istnieje" — WYMAGA WERYFIKACJI Z ZESPOŁEM]

## 5. Brak wyjątków i brak zapisu

Proces nie rzuca żadnego wyjątku domenowego i nie wykonuje `CompleteAsync()`. Jest w pełni odczytowy i bezpieczny względem stanu bazy.
