# GetUserClientFirms — Logika aplikacyjna

## 1. Punkt wejścia — kontroler

Plik: `InvoiceJet.Presentation/Controllers/FirmController.cs › FirmController.GetUserClientFirms`

```csharp
[HttpGet("GetUserClientFirms")]
public async Task<ActionResult> GetUserClientFirms()
{
    var clientFirms = await _firmService.GetUserClientFirms();
    return Ok(clientFirms);
}
```

Kontroler bezstanowy: brak parametrów, brak walidacji, brak `try/catch`. Tożsamość użytkownika nie jest przekazywana jawnie — serwis sam ją odczytuje z JWT.

## 2. Algorytm główny — `FirmService.GetUserClientFirms`

Plik: `InvoiceJet.Application/Services/Impl/FirmService.cs › FirmService.GetUserClientFirms` (linie 98–108)

```csharp
public async Task<List<FirmDto>> GetUserClientFirms()
{
    var clients = await _unitOfWork.UserFirms.GetUserFirmClients(_userService.GetCurrentUserId());
    if (clients.Count == 0)
    {
        return new List<FirmDto>();
    }

    var firms = clients.Select(u => u.Firm).ToList();
    return _mapper.Map<List<FirmDto>>(firms);
}
```

### Kroki algorytmu

| Krok | Opis | Kotwica |
|---|---|---|
| 1 | Odczyt tożsamości użytkownika z JWT | `_userService.GetCurrentUserId()` |
| 2 | Pobranie relacji `UserFirm` z `IsClient=true` (z firmami) | `_unitOfWork.UserFirms.GetUserFirmClients(userId)` |
| 3 | Wczesny zwrot pustej listy gdy brak klientów | `if (clients.Count == 0) return new List<FirmDto>()` |
| 4 | Projekcja `UserFirm` → `Firm` (w pamięci) | `clients.Select(u => u.Firm).ToList()` |
| 5 | Mapowanie listy firm na listę DTO | `_mapper.Map<List<FirmDto>>(firms)` |

### Szczegół kroku 1 — tożsamość użytkownika

Plik: `InvoiceJet.Application/Services/Impl/UserService.cs › UserService.GetCurrentUserId`

```csharp
var userIdString = httpContext.User.FindFirst("userId")?.Value;
return Guid.TryParse(userIdString, out var userId) ? userId : Guid.Empty;
```

Odczytuje claim `"userId"`. Zwraca `Guid.Empty` gdy niezalogowany — ale endpoint chroniony `[Authorize]`.

### Szczegół kroku 2 — zapytanie repozytorium

Plik: `InvoiceJet.Infrastructure/Persistence/Repositories/UserFirmRepository.cs › UserFirmRepository.GetUserFirmClients`

```csharp
return await _dbSet
    .Where(u => u.UserId.Equals(userId) && u.IsClient)
        .Include(f => f.Firm)
    .ToListAsync();
```

Zwraca listę relacji `UserFirm` (z eager-loaded `Firm`), w których użytkownik jest właścicielem relacji, a flaga `IsClient == true`. Pusta lista gdy brak dopasowań.

### Szczegół kroku 3 — wczesny zwrot pustej listy

```csharp
if (clients.Count == 0)
{
    return new List<FirmDto>();
}
```

Gdy brak firm-klientów — zwracana jest pusta lista `[]`, kontroler opakowuje w `200 OK`.

> [UWAGA: Sprawdzenie `clients.Count == 0` jest funkcjonalnie redundantne — `_mapper.Map<List<FirmDto>>` na pustej liście również zwróciłby pustą listę. Nie jest to błąd, lecz nadmiarowa gałąź — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Szczegół kroku 4 — projekcja w pamięci

```csharp
var firms = clients.Select(u => u.Firm).ToList();
```

LINQ to Objects (po materializacji z kroku 2) — wyciąga nawigację `Firm` z każdego `UserFirm`. Encje `Firm` są już załadowane (`Include`), więc brak dodatkowych zapytań do DB.

### Szczegół kroku 5 — mapowanie listy

```csharp
return _mapper.Map<List<FirmDto>>(firms);
```

Mapuje `List<Firm>` na `List<FirmDto>` przez `FirmProfile` (`CreateMap<Firm, FirmDto>().ReverseMap()`).

## 3. Walidacje wejścia (WAL)

| ID | Walidacja | Gdzie sprawdzana | Wynik naruszenia |
|---|---|---|---|
| `WAL-01` | Ważny JWT z rolą `"User"` | `[Authorize(Roles = "User")]` na `FirmController` | `401` / `403` |

Poza autoryzacją proces nie ma żadnych walidacji domenowych — brak danych wejściowych do walidowania.

## 4. Obsługa przypadków brzegowych

| Scenariusz | Zachowanie kodu | Wynik |
|---|---|---|
| Użytkownik ma firmy-klientów | `clients.Count > 0` → projekcja + mapowanie | `200 OK` z listą `FirmDto` |
| Użytkownik bez firm-klientów | `clients.Count == 0` → wczesny zwrot | `200 OK` z `[]` |
| Użytkownik nie istnieje w DB | brak dopasowań w `WHERE` → pusta lista | `200 OK` z `[]` |
| `GetCurrentUserId()` zwraca `Guid.Empty` | `WHERE UserId == Guid.Empty` → brak dopasowań | `200 OK` z `[]` |

## 5. Izolacja danych

Zapytanie filtruje `WHERE UserId.Equals(userId)` — użytkownik widzi wyłącznie własne firmy-klientów. Brak możliwości odczytu klientów innego użytkownika.

## 6. Brak wyjątków i brak zapisu

Proces nie rzuca żadnego wyjątku domenowego i nie wykonuje `CompleteAsync()`. Jest w pełni odczytowy.
