# EditFirm — Dane, modele, mapowania

## 1. DTO żądania — `FirmDto`

Plik: `InvoiceJet.Application/DTOs/FirmDto.cs`

| Pole | Typ C# | Nullable | Atrybut walidacji | Opis |
|---|---|---|---|---|
| `Id` | `int` | nie | — | **wymagany** — identyfikuje firmę do edycji; musi odpowiadać istniejącemu rekordowi `Firm.Id` w DB |
| `Name` | `string` | nie (default `""`) | brak | Pełna nazwa firmy |
| `Cui` | `string` | nie (default `""`) | brak | Numer identyfikacji podatkowej |
| `RegCom` | `string?` | **tak** | brak | Numer rejestru handlowego |
| `Address` | `string` | nie (default `""`) | brak | Adres siedziby |
| `County` | `string` | nie (default `""`) | brak | Județ (województwo) |
| `City` | `string` | nie (default `""`) | brak | Miejscowość |

> DTO nie zawiera atrybutów `[Required]`, `[MaxLength]` ani żadnych adnotacji walidacyjnych — brak walidacji domenowej po stronie API.

**Parametr trasy:**

| Parametr | Typ C# | Lokalizacja | Opis |
|---|---|---|---|
| `isClient` | `bool` | route (`{isClient}`) | Czy firma ma być oznaczona jako klient (`true`) czy własna firma użytkownika (`false`) |

## 2. DTO odpowiedzi — `FirmDto`

Odpowiedź zwraca **ten sam obiekt `FirmDto`**, który przyszedł w żądaniu — bez modyfikacji poza tym co zostało przesłane. Pole `Id` zachowuje wartość z żądania.

```csharp
// FirmService.cs › FirmService.EditFirm
return firmDto;
```

> [UWAGA: Serwis zwraca wejściowy `firmDto` bez ponownego odczytu z DB — klient dostaje echo swojego żądania. Jeśli AutoMapper zmodyfikował jakieś pola podczas `_mapper.Map(firmDto, firm)`, nie są one odzwierciedlone w odpowiedzi — WYMAGA WERYFIKACJI Z ZESPOŁEM]

## 3. Encja domenowa — `Firm`

Plik: `InvoiceJet.Domain/Models/Firm.cs`

```csharp
public sealed class Firm : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string Cui { get; set; } = string.Empty;
    public string RegCom { get; set; } = string.Empty;
    public string Address { get; set; } = string.Empty;
    public string County { get; set; } = string.Empty;
    public string City { get; set; } = string.Empty;

    public ICollection<UserFirm>? UserFirms { get; set; }
}
```

`BaseEntity`: `InvoiceJet.Domain/Models/BaseEntity.cs` — `public int Id { get; set; }`

## 4. Tabela `Firm` — schemat DB (snapshot migracji)

Plik: `InvoiceJet.Infrastructure/Migrations/InvoiceJetDbContextModelSnapshot.cs`

| Kolumna | Typ SQL | Nullable | Klucz / Indeks | Uwaga |
|---|---|---|---|---|
| `Id` | `int` | NOT NULL | PK, IDENTITY | Auto-inkrementowany |
| `Name` | `nvarchar(max)` | NOT NULL | — | Brak limitu długości |
| `Cui` | `nvarchar(max)` | NOT NULL | — | Brak unikalnego indeksu |
| `RegCom` | `nvarchar(max)` | NOT NULL | — | NOT NULL w DB, lecz `string?` w DTO — patrz [UWAGA] |
| `Address` | `nvarchar(max)` | NOT NULL | — | |
| `County` | `nvarchar(max)` | NOT NULL | — | |
| `City` | `nvarchar(max)` | NOT NULL | — | |

> [UWAGA: `Firm.RegCom` — typ `string` NOT NULL w encji i DB, ale `string?` (nullable) w `FirmDto`. Klient może wysłać `null` → EF Core rzuci `DbUpdateException` → ExceptionMiddleware → `500` zamiast `400` — WYMAGA WERYFIKACJI Z ZESPOŁEM]

## 5. Encja powiązana — `UserFirm`

Plik: `InvoiceJet.Domain/Models/UserFirm.cs`

| Kolumna | Typ SQL | Nullable | Klucz / Indeks | Uwaga |
|---|---|---|---|---|
| `UserFirmId` | `int` | NOT NULL | PK, IDENTITY | |
| `UserId` | `uniqueidentifier` | NOT NULL | IX | FK → `User.Id` |
| `FirmId` | `int` | NOT NULL | IX | FK → `Firm.Id` |
| `IsClient` | `bit` | NOT NULL | — | Domyślnie `true` w encji |

Brak unikalnego indeksu złożonego na `(UserId, FirmId)` — możliwe duplikaty relacji.

## 6. AutoMapper — `FirmProfile`

Plik: `InvoiceJet.Application/MappingProfiles/FirmProfile.cs`

```csharp
CreateMap<Firm, FirmDto>().ReverseMap();
```

`ReverseMap()` rejestruje oba kierunki: `Firm → FirmDto` i `FirmDto → Firm`.

W `EditFirm` używany jest formularz **"update in place"**:

```csharp
// FirmService.cs › FirmService.EditFirm
firm = _mapper.Map(firmDto, firm);
```

`_mapper.Map(source, destination)` — mapuje `firmDto` (source) na istniejącą instancję `firm` (destination), nadpisując **wszystkie** pola:

| Pole DTO → Encja | Kierunek mapowania | Uwaga |
|---|---|---|
| `FirmDto.Id` → `Firm.Id` | DTO → Encja | EF Core śledzi encję po `Id` — zmiana `Id` przez mapper jest groźna jeśli `firmDto.Id != firm.Id` (w praktyce niemożliwe przy normalnym użyciu, ale brak zabezpieczenia) |
| `FirmDto.Name` → `Firm.Name` | DTO → Encja | |
| `FirmDto.Cui` → `Firm.Cui` | DTO → Encja | |
| `FirmDto.RegCom` → `Firm.RegCom` | DTO → Encja | Nullable `string?` → NOT NULL `string`; `null` → `null` w encji → DB constraint → `500` |
| `FirmDto.Address` → `Firm.Address` | DTO → Encja | |
| `FirmDto.County` → `Firm.County` | DTO → Encja | |
| `FirmDto.City` → `Firm.City` | DTO → Encja | |

## 7. Repozytoria używane w procesie

| Repozytorium | Interfejs | Metoda | Opis |
|---|---|---|---|
| `FirmRepository` | `IFirmRepository` | `GetByIdAsync(int id)` | `DbSet.FindAsync(id)` — odczyt encji `Firm` po kluczu głównym |
| `UserFirmRepository` | `IUserFirmRepository` | `GetUserFirmById(Guid userId, int firmId)` | LINQ WHERE `UserId == userId && FirmId == firmId` → pierwsza lub null |
| `UserFirmRepository` | `IUserFirmRepository` | `AddAsync(UserFirm)` | Tylko gdy `existingUserFirm == null` (scenariusz niestandardowy dla EditFirm) |

`GetByIdAsync` zaimplementowane w `GenericRepository<T>`:
```csharp
// GenericRepository.cs › GenericRepository<T>.GetByIdAsync
return await _dbSet.FindAsync(id);
```

`GetUserFirmById` zaimplementowane w `UserFirmRepository`:
```csharp
// UserFirmRepository.cs › UserFirmRepository.GetUserFirmById
return await _dbSet
    .Where(uf => uf.UserId == userId && uf.FirmId == userFirmId)
    .FirstOrDefaultAsync();
```

## 8. Zapisy do bazy (`CompleteAsync`)

| Kolejność | Wywołanie | Co zapisuje | Gdzie w kodzie |
|---|---|---|---|
| #1 | `CompleteAsync()` | Zaktualizowany rekord `Firm` (wszystkie pola) | `FirmService.cs › FirmService.EditFirm` |
| #2 | `CompleteAsync()` | Rekord `UserFirm` (update `IsClient` lub insert nowego) | `FirmService.cs › FirmService.ManageUserFirmRelation` |

Dwa wywołania `CompleteAsync()` bez jawnej transakcji — awaria między #1 a #2 pozostawi zaktualizowaną firmę bez zaktualizowanej relacji `UserFirm`.

> [UWAGA: Brak jawnej transakcji obejmującej oba `CompleteAsync()`. Częściowa awaria między zapisem #1 (Firm) a #2 (UserFirm) pozostawi dane w stanie niespójnym — WYMAGA WERYFIKACJI Z ZESPOŁEM]
