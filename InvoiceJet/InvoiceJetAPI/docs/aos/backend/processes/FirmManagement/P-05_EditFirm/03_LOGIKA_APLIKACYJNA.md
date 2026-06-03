# EditFirm — Logika aplikacyjna

## 1. Punkt wejścia — kontroler

Plik: `InvoiceJet.Presentation/Controllers/FirmController.cs › FirmController.EditFirm`

```csharp
[HttpPut("EditFirm/{isClient}")]
public async Task<ActionResult> EditFirm([FromBody] FirmDto firmDto, bool isClient)
{
    var updatedOrNewFirm = await _firmService.EditFirm(firmDto, isClient);
    return Ok(updatedOrNewFirm);
}
```

Kontroler jest bezstanowy: brak walidacji wejścia, brak jawnego `try/catch` — obsługa wyjątków delegowana do `ExceptionMiddleware`.

## 2. Algorytm główny — `FirmService.EditFirm`

Plik: `InvoiceJet.Application/Services/Impl/FirmService.cs › FirmService.EditFirm` (linie 45–59)

```csharp
public async Task<FirmDto> EditFirm(FirmDto firmDto, bool isClient)
{
    var firm = await _unitOfWork.Firms.GetByIdAsync(firmDto.Id);
    if (firm == null)
    {
        throw new Exception("Firm not found.");
    }

    firm = _mapper.Map(firmDto, firm);
    await _unitOfWork.CompleteAsync();

    await ManageUserFirmRelation(firm.Id, isClient);
    
    return firmDto;
}
```

### Kroki algorytmu

| Krok | Opis | Kotwica |
|---|---|---|
| 1 | Odczyt encji `Firm` z DB po `firmDto.Id` | `GenericRepository.GetByIdAsync` → `_dbSet.FindAsync(id)` |
| 2 | Sprawdzenie istnienia firmy | `if (firm == null) throw new Exception("Firm not found.")` |
| 3 | Mapowanie DTO na encję (update in place) | `_mapper.Map(firmDto, firm)` |
| 4 | Zapis do DB — **CompleteAsync #1** | `await _unitOfWork.CompleteAsync()` |
| 5 | Zarządzanie relacją User–Firm | `await ManageUserFirmRelation(firm.Id, isClient)` |
| 6 | Zwrot wejściowego DTO | `return firmDto` |

### Szczegół kroku 1 — odczyt `Firm`

```csharp
var firm = await _unitOfWork.Firms.GetByIdAsync(firmDto.Id);
```

`GetByIdAsync` wywołuje `_dbSet.FindAsync(id)` — najpierw sprawdza Change Tracker (pamięć EF Core), następnie odpytuje DB. Nie ładuje nawigacji (`UserFirms`).

### Szczegół kroku 2 — walidacja istnienia

```csharp
if (firm == null)
{
    throw new Exception("Firm not found.");
}
```

> [UWAGA: Rzucony jest **zwykły `Exception`**, nie wyjątek domenowy. `ExceptionMiddleware` przechwytuje go w bloku catch-all `Exception ex` → `500 Internal Server Error`. Klient dostaje `500` zamiast oczekiwanego `404 Not Found` dla nieistniejącej firmy. Brakuje dedykowanej klasy `FirmNotFoundException` z mapowaniem na `404` — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Szczegół kroku 3 — AutoMapper "update in place"

```csharp
firm = _mapper.Map(firmDto, firm);
```

Używany jest formularz dwuargumentowy `IMapper.Map<TSource, TDestination>(source, destination)` — mapper nadpisuje pola istniejącej instancji `firm` wartościami z `firmDto`. EF Core Change Tracker śledzi tę samą instancję, więc zmiany zostaną wykryte przy `CompleteAsync`.

Profil mapowania: `FirmProfile.cs` — `CreateMap<Firm, FirmDto>().ReverseMap()` (brak konfiguracji pomijania pól — wszystkie pola są mapowane).

### Szczegół kroku 4 — CompleteAsync #1

```csharp
await _unitOfWork.CompleteAsync();
```

Zapisuje zmiany encji `Firm` (UPDATE w tabeli `Firm`). Zaktualizowane kolumny: `Name`, `Cui`, `RegCom`, `Address`, `County`, `City` (oraz `Id` jeśli AutoMapper go nadpisał — co jest technicznie niegroźne gdy `firmDto.Id == firm.Id`).

## 3. Podprocedura — `ManageUserFirmRelation`

Plik: `InvoiceJet.Application/Services/Impl/FirmService.cs › FirmService.ManageUserFirmRelation` (linie 61–90)

Metoda prywatna **współdzielona** z `AddFirm` (P-03). W kontekście `EditFirm` jest wywoływana po zapisaniu zmian firmy.

```csharp
private async Task ManageUserFirmRelation(int firmId, bool isClient)
{
    var userId = _userService.GetCurrentUserId();
    var existingUserFirm = await _unitOfWork.UserFirms.GetUserFirmById(userId, firmId);
    
    if (existingUserFirm == null)
    {
        // Scenariusz niestandardowy dla EditFirm — patrz UWAGA poniżej
        var newUserFirm = new UserFirm { UserId = userId, FirmId = firmId, IsClient = isClient };
        await _unitOfWork.UserFirms.AddAsync(newUserFirm);

        var user = await _unitOfWork.Users.GetUserByIdAsync(_userService.GetCurrentUserId());
        if (user!.ActiveUserFirm == null)
        {
            user.ActiveUserFirm = newUserFirm;
            await _documentSeriesService.AddInitialDocumentSeries(newUserFirm);
        }
    }
    else
    {
        existingUserFirm.IsClient = isClient;
    }
    
    await _unitOfWork.CompleteAsync();
}
```

### Gałąź A — `existingUserFirm != null` (normalny scenariusz EditFirm)

Relacja `UserFirm` dla pary `(userId, firmId)` istnieje (firma była wcześniej dodana przez tego użytkownika).

```csharp
existingUserFirm.IsClient = isClient;
```

Aktualizowany jest wyłącznie flag `IsClient`. Następnie `CompleteAsync()` zapisuje zmianę.

### Gałąź B — `existingUserFirm == null` (scenariusz niestandardowy)

> [UWAGA: Przy edycji firmy relacja `UserFirm` powinna zawsze istnieć (firma musiała być wcześniej dodana przez użytkownika). Gałąź `existingUserFirm == null` w kontekście `EditFirm` sugeruje próbę edycji cudzej firmy lub błąd w danych — system jednak **milcząco tworzy nową relację** zamiast zwrócić błąd. Może to prowadzić do duplikatów w tabeli `UserFirm` (brak unikalnego indeksu na `(UserId, FirmId)`) — WYMAGA WERYFIKACJI Z ZESPOŁEM]

Gdy relacja nie istnieje — tworzona jest nowa `UserFirm`:
1. `AddAsync(newUserFirm)` — nowy rekord
2. Jeśli `user.ActiveUserFirm == null` → ustawia aktywną firmę i tworzy 3 serie dokumentów (jak w P-03 `AddFirm`)

### CompleteAsync #2

```csharp
await _unitOfWork.CompleteAsync();
```

Zapisuje zmiany `UserFirm` (UPDATE `IsClient` lub INSERT nowej relacji) oraz ewentualnie `User.ActiveUserFirmId` i 3 × `DocumentSeries`.

## 4. Walidacje wejścia (WAL)

| ID | Walidacja | Gdzie sprawdzana | Wynik naruszenia |
|---|---|---|---|
| `WAL-01` | Ważny JWT z rolą `"User"` | `[Authorize(Roles = "User")]` na `FirmController` | `401` / `403` |
| `WAL-02` | Firma o `firmDto.Id` musi istnieć w DB | `FirmService.EditFirm` — `if (firm == null) throw new Exception(...)` | `500` (bug — powinno być `404`) |

## 5. Brak jawnych walidacji pól DTO

DTO `FirmDto` nie zawiera żadnych atrybutów walidacyjnych (`[Required]`, `[MaxLength]`, `[Range]`). Puste stringi, zbyt długie wartości — trafiają bezpośrednio do EF Core. Naruszenie NOT NULL w DB → `DbUpdateException` → `500`.

## 6. Tożsamość użytkownika

```csharp
// UserService.cs › UserService.GetCurrentUserId
var userIdString = httpContext.User.FindFirst("userId")?.Value;
return Guid.TryParse(userIdString, out var userId) ? userId : Guid.Empty;
```

Wywołanie: `_userService.GetCurrentUserId()` — używane w `ManageUserFirmRelation` do określenia, dla którego użytkownika sprawdzana/tworzona jest relacja `UserFirm`. Nie używane bezpośrednio w `EditFirm`.
