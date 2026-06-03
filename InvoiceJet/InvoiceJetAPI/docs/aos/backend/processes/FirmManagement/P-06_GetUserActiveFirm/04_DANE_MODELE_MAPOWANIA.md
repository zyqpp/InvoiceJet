# GetUserActiveFirm — Dane, modele, mapowania

## 1. DTO żądania

Brak ciała żądania i brak parametrów (`[HttpGet("GetUserActiveFirm")]`). Jedyną daną wejściową jest tożsamość użytkownika odczytana z JWT (claim `"userId"`).

## 2. DTO odpowiedzi — `FirmDto`

Plik: `InvoiceJet.Application/DTOs/FirmDto.cs`

| Pole | Typ C# | Nullable | Źródło | Uwaga |
|---|---|---|---|---|
| `Id` | `int` | nie | `Firm.Id` | `0` gdy brak aktywnej firmy |
| `Name` | `string` | nie (default `""`) | `Firm.Name` | `""` gdy brak aktywnej firmy |
| `Cui` | `string` | nie (default `""`) | `Firm.Cui` | `""` gdy brak aktywnej firmy |
| `RegCom` | `string?` | tak | `Firm.RegCom` | Zawsze non-null z DB (kolumna NOT NULL); `null` tylko w pustym DTO |
| `Address` | `string` | nie (default `""`) | `Firm.Address` | |
| `County` | `string` | nie (default `""`) | `Firm.County` | |
| `City` | `string` | nie (default `""`) | `Firm.City` | |

> [UWAGA: Gdy użytkownik nie ma aktywnej firmy, serwis zwraca **pusty `FirmDto`** (`Id=0`, stringi `""`, `RegCom=null`) z kodem `200 OK` — nie `404` ani `204`. Klient musi rozpoznać „brak firmy" po `Id==0` lub pustej nazwie — WYMAGA WERYFIKACJI Z ZESPOŁEM]

## 3. Encje domenowe

### `Firm` — źródło danych odpowiedzi

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

### `User` — punkt wejścia zapytania

Plik: `InvoiceJet.Domain/Models/User.cs`

```csharp
public sealed class User
{
    public Guid Id { get; set; }
    // ...
    public int? ActiveUserFirmId { get; set; }
    public UserFirm ActiveUserFirm { get; set; } = null!;
}
```

### `UserFirm` — łącznik User ↔ Firm

Plik: `InvoiceJet.Domain/Models/UserFirm.cs` — nawigacja `Firm` (NOT NULL FK) wykorzystywana w mapowaniu.

## 4. Tabele DB — schemat (snapshot migracji)

Plik: `InvoiceJet.Infrastructure/Migrations/InvoiceJetDbContextModelSnapshot.cs`

### Tabela `User` (punkt wejścia)

| Kolumna | Typ SQL | Nullable | Klucz / Indeks | Uwaga |
|---|---|---|---|---|
| `Id` | `uniqueidentifier` | NOT NULL | PK | Guid |
| `ActiveUserFirmId` | `int` | **NULL** | FK → `UserFirm.UserFirmId`, IX | `null` = brak aktywnej firmy |
| `Email` | `nvarchar(max)` | NOT NULL | — | (nieużywane w procesie) |
| `FirstName`, `LastName`, `PasswordHash`, `Role` | `nvarchar(max)` | NOT NULL | — | (nieużywane w procesie) |

Relacja: `User.ActiveUserFirm → UserFirm` przez FK `ActiveUserFirmId`, `.WithMany()` (brak nawigacji zwrotnej).

```csharp
// InvoiceJetDbContextModelSnapshot.cs
b.HasOne("InvoiceJet.Domain.Models.UserFirm", "ActiveUserFirm")
    .WithMany()
    .HasForeignKey("ActiveUserFirmId");
```

### Tabela `Firm` (źródło odpowiedzi)

| Kolumna | Typ SQL | Nullable | Klucz / Indeks |
|---|---|---|---|
| `Id` | `int` | NOT NULL | PK, IDENTITY |
| `Name`, `Cui`, `RegCom`, `Address`, `County`, `City` | `nvarchar(max)` | NOT NULL | — |

### Tabela `UserFirm` (łącznik)

| Kolumna | Typ SQL | Nullable | Klucz / Indeks |
|---|---|---|---|
| `UserFirmId` | `int` | NOT NULL | PK, IDENTITY |
| `UserId` | `uniqueidentifier` | NOT NULL | IX |
| `FirmId` | `int` | NOT NULL | IX, FK → `Firm.Id` |
| `IsClient` | `bit` | NOT NULL | — |

## 5. AutoMapper — `FirmProfile`

Plik: `InvoiceJet.Application/MappingProfiles/FirmProfile.cs`

```csharp
CreateMap<Firm, FirmDto>().ReverseMap();
```

W tym procesie używany jest kierunek **`Firm → FirmDto`**:

```csharp
// FirmService.cs › FirmService.GetUserActiveFirm
_mapper.Map<FirmDto>(activeUserFirm.Firm);
```

| Pole Encja → DTO | Uwaga |
|---|---|
| `Firm.Id` → `FirmDto.Id` | |
| `Firm.Name` → `FirmDto.Name` | |
| `Firm.Cui` → `FirmDto.Cui` | |
| `Firm.RegCom` (NOT NULL) → `FirmDto.RegCom` (`string?`) | Bezpieczny kierunek — non-null → nullable |
| `Firm.Address` → `FirmDto.Address` | |
| `Firm.County` → `FirmDto.County` | |
| `Firm.City` → `FirmDto.City` | |

## 6. Zapytanie LINQ — `UserRepository.GetUserFirmAsync`

Plik: `InvoiceJet.Infrastructure/Persistence/Repositories/UserRepository.cs › UserRepository.GetUserFirmAsync`

```csharp
public async Task<UserFirm?> GetUserFirmAsync(Guid userId)
{
    var userFirm = await _dbSet
        .Where(u => u.Id == userId)
            .Include(uf => uf.ActiveUserFirm)
                .ThenInclude(uf => uf.Firm)
            .Include(uf => uf.ActiveUserFirm)
                .ThenInclude(u => u.User)
        .Select(uf => uf.ActiveUserFirm)
        .SingleOrDefaultAsync();

    return userFirm;
}
```

Charakterystyka zapytania:
- `_dbSet` to `DbSet<User>` — start od tabeli `User`
- `Where(u => u.Id == userId)` — filtr po kluczu głównym (max 1 wiersz)
- `.Include(ActiveUserFirm).ThenInclude(Firm)` — eager load firmy aktywnej
- `.Include(ActiveUserFirm).ThenInclude(User)` — eager load użytkownika powiązanego z UserFirm
- `.Select(uf => uf.ActiveUserFirm)` — projekcja na nawigację `ActiveUserFirm` (typ `UserFirm`)
- `.SingleOrDefaultAsync()` — zwraca pojedynczy `UserFirm` lub `null`

Zachowanie wynikowe:

| Stan w DB | Wynik zapytania |
|---|---|
| User istnieje + ma `ActiveUserFirmId` | zwraca `UserFirm` (z załadowaną `.Firm`) |
| User istnieje + `ActiveUserFirmId == null` | `Select` projektuje `null` → zwraca `null` |
| User nie istnieje | brak wierszy → zwraca `null` |

> [UWAGA: Drugi `.Include(ActiveUserFirm).ThenInclude(u => u.User)` ładuje encję `User` powiązaną z `UserFirm`, ale dane te **nie są używane** — serwis mapuje wyłącznie `activeUserFirm.Firm`. Redundantny JOIN obciąża zapytanie — WYMAGA WERYFIKACJI Z ZESPOŁEM]

## 7. Brak zapisu do bazy

Proces jest **wyłącznie odczytowy** — zero wywołań `CompleteAsync()`. Brak modyfikacji jakiejkolwiek encji.
