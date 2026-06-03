# GetUserClientFirms — Dane, modele, mapowania

## 1. DTO żądania

Brak ciała żądania i brak parametrów (`[HttpGet("GetUserClientFirms")]`). Jedyną daną wejściową jest tożsamość użytkownika odczytana z JWT (claim `"userId"`).

## 2. DTO odpowiedzi — `List<FirmDto>`

Plik: `InvoiceJet.Application/DTOs/FirmDto.cs`

Odpowiedź to **tablica** obiektów `FirmDto` (po jednym na każdą firmę-klienta użytkownika).

| Pole | Typ C# | Nullable | Źródło | Uwaga |
|---|---|---|---|---|
| `Id` | `int` | nie | `Firm.Id` | Identyfikator firmy klienta |
| `Name` | `string` | nie (default `""`) | `Firm.Name` | |
| `Cui` | `string` | nie (default `""`) | `Firm.Cui` | |
| `RegCom` | `string?` | tak | `Firm.RegCom` | Zawsze non-null z DB (kolumna NOT NULL) |
| `Address` | `string` | nie (default `""`) | `Firm.Address` | |
| `County` | `string` | nie (default `""`) | `Firm.County` | |
| `City` | `string` | nie (default `""`) | `Firm.City` | |

Pusta lista `[]` jest zwracana, gdy użytkownik nie ma żadnych firm-klientów.

## 3. Encje domenowe

### `UserFirm` — łącznik z filtrem `IsClient`

Plik: `InvoiceJet.Domain/Models/UserFirm.cs`

```csharp
public sealed class UserFirm
{
    public int UserFirmId { get; set; }
    public Guid UserId { get; set; }
    public int FirmId { get; set; }
    public bool IsClient { get; set; } = true;
    public User User { get; set; } = null!;
    public Firm Firm { get; set; } = null!;
    // ...
}
```

Proces filtruje `UserFirm` po `UserId` i `IsClient == true`, a następnie czyta nawigację `Firm`.

### `Firm` — źródło danych odpowiedzi

Plik: `InvoiceJet.Domain/Models/Firm.cs` — pola `Name`, `Cui`, `RegCom`, `Address`, `County`, `City` mapowane na `FirmDto`.

## 4. Tabele DB — schemat (snapshot migracji)

Plik: `InvoiceJet.Infrastructure/Migrations/InvoiceJetDbContextModelSnapshot.cs`

### Tabela `UserFirm` (punkt wejścia + filtr)

| Kolumna | Typ SQL | Nullable | Klucz / Indeks | Uwaga |
|---|---|---|---|---|
| `UserFirmId` | `int` | NOT NULL | PK, IDENTITY | |
| `UserId` | `uniqueidentifier` | NOT NULL | IX | filtr `WHERE UserId == userId` |
| `FirmId` | `int` | NOT NULL | IX, FK → `Firm.Id` (cascade) | nawigacja `Firm` |
| `IsClient` | `bit` | NOT NULL | — | filtr `WHERE IsClient` |

Relacja `UserFirm → Firm` (snapshot):
```csharp
b.HasOne("InvoiceJet.Domain.Models.Firm", "Firm")
    .WithMany("UserFirms")
    .HasForeignKey("FirmId")
    .OnDelete(DeleteBehavior.Cascade)
    .IsRequired();
```

> Brak indeksu na kolumnie `IsClient` — filtr `WHERE IsClient` wykonuje skanowanie po indeksie `UserId` + ewaluację predykatu na `IsClient`.

### Tabela `Firm` (źródło odpowiedzi)

| Kolumna | Typ SQL | Nullable | Klucz / Indeks |
|---|---|---|---|
| `Id` | `int` | NOT NULL | PK, IDENTITY |
| `Name`, `Cui`, `RegCom`, `Address`, `County`, `City` | `nvarchar(max)` | NOT NULL | — |

## 5. AutoMapper — `FirmProfile`

Plik: `InvoiceJet.Application/MappingProfiles/FirmProfile.cs`

```csharp
CreateMap<Firm, FirmDto>().ReverseMap();
```

W tym procesie używany jest kierunek **`Firm → FirmDto`** dla listy:

```csharp
// FirmService.cs › FirmService.GetUserClientFirms
return _mapper.Map<List<FirmDto>>(firms);
```

AutoMapper mapuje `List<Firm>` na `List<FirmDto>` element po elemencie, używając rejestracji `CreateMap<Firm, FirmDto>()`.

## 6. Zapytanie LINQ — `UserFirmRepository.GetUserFirmClients`

Plik: `InvoiceJet.Infrastructure/Persistence/Repositories/UserFirmRepository.cs › UserFirmRepository.GetUserFirmClients`

```csharp
public async Task<List<UserFirm>> GetUserFirmClients(Guid userId)
{
    return await _dbSet
        .Where(u => u.UserId.Equals(userId) && u.IsClient)
            .Include(f => f.Firm)
        .ToListAsync();
}
```

Charakterystyka zapytania:
- `_dbSet` to `DbSet<UserFirm>` — start od tabeli `UserFirm`
- `Where(u => u.UserId.Equals(userId) && u.IsClient)` — filtr po użytkowniku i fladze klienta
- `.Include(f => f.Firm)` — eager load encji `Firm` (JOIN)
- `.ToListAsync()` — materializacja listy `UserFirm`

Następnie w serwisie:
```csharp
// FirmService.cs › FirmService.GetUserClientFirms
var firms = clients.Select(u => u.Firm).ToList();
```

Projekcja w pamięci (LINQ to Objects) z listy `UserFirm` na listę `Firm` przez nawigację.

## 7. Brak zapisu do bazy

Proces jest **wyłącznie odczytowy** — zero wywołań `CompleteAsync()`. Brak modyfikacji jakiejkolwiek encji.
