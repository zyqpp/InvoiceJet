# AddFirm — Dane, modele i mapowania

## 1. DTO

### `FirmDto` (wejście i wyjście)

Plik: `Application/DTOs/FirmDto.cs`

| Pole | Typ C# | Wymagane | Opis / rola w procesie |
|---|---|---|---|
| `Id` | `int` | nie | Ignorowane przez EF Core przy tworzeniu (IDENTITY) — po zapisie ustawiane przez serwis na auto-generated Id |
| `Name` | `string` | tak* | Nazwa firmy → `Firm.Name` |
| `Cui` | `string` | tak* | Numer CUI (rumuński NIP) → `Firm.Cui` |
| `RegCom` | `string?` | nie | Numer rejestru handlowego → `Firm.RegCom` — **nullable w DTO, NOT NULL w DB** |
| `Address` | `string` | tak* | Adres → `Firm.Address` |
| `County` | `string` | tak* | Województwo/Judet → `Firm.County` |
| `City` | `string` | tak* | Miasto → `Firm.City` |

> *Brak atrybutów `[Required]` w DTO. Żadna walidacja nie jest wykonywana przed trafieniem do serwisu.

> [UWAGA: `FirmDto.RegCom` jest `string?` (nullable) ale `Firm.RegCom` i kolumna DB są NOT NULL. Wysłanie `null` dla `RegCom` spowoduje próbę zapisu `null` do NOT NULL kolumny → `DbUpdateException` → `500 Internal Server Error` — WYMAGA WERYFIKACJI Z ZESPOŁEM]

Odpowiedź: identyczny `FirmDto` z ustawionym `Id` (auto-generated przez SQL Server po zapisie).

---

## 2. Encje i kolumny

### Encja `Firm` → tabela `Firm`

Kotwica: `Domain/Models/Firm.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("InvoiceJet.Domain.Models.Firm")`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `Id` | `int IDENTITY` | nie | PK | — |
| `Name` | `nvarchar(max)` | nie | — | — |
| `Cui` | `nvarchar(max)` | nie | — | — |
| `RegCom` | `nvarchar(max)` | nie | — | — |
| `Address` | `nvarchar(max)` | nie | — | — |
| `City` | `nvarchar(max)` | nie | — | — |
| `County` | `nvarchar(max)` | nie | — | — |

> Brak unikalnego indeksu na `Cui`, `Name` ani żadnej innej kolumnie. Duplikaty firm są możliwe na poziomie DB.
> Pełne definicje: `../../SLOWNIK_DANYCH.md#Firm`.

---

### Encja `UserFirm` → tabela `UserFirm`

Kotwica: `Domain/Models/UserFirm.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("InvoiceJet.Domain.Models.UserFirm")`.

Tworzona przez `ManageUserFirmRelation` — łączy użytkownika z firmą.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `UserFirmId` | `int IDENTITY` | nie | PK | — |
| `UserId` | `uniqueidentifier` | nie | FK → `User.Id` CASCADE | IX |
| `FirmId` | `int` | nie | FK → `Firm.Id` CASCADE | IX |
| `IsClient` | `bit` | nie | — | — |

> Brak unikalnego indeksu na parze `(UserId, FirmId)` — możliwe jest stworzenie wielu `UserFirm` rekordów dla tej samej pary (choć `AddFirm` zawsze tworzy nową `Firm`, więc `FirmId` jest unikalny per wywołanie).

---

### Encja `User` → tabela `User` (częściowa aktualizacja)

Modyfikowana warunkowo przez `ManageUserFirmRelation` gdy `user.ActiveUserFirm == null`.

| Kolumna | Typ SQL | Nullable | Klucz | Zmiana |
|---|---|---|---|---|
| `ActiveUserFirmId` | `int` | tak | FK → `UserFirm.UserFirmId` | ustawiana na nowy `UserFirm.UserFirmId` gdy to pierwsza firma |

---

### Encja `DocumentSeries` → tabela `DocumentSeries` (efekt uboczny)

Tworzona przez `DocumentSeriesService.AddInitialDocumentSeries` — tylko gdy `user.ActiveUserFirm == null` przed dodaniem.
Kotwica: `Domain/Models/DocumentSeries.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("InvoiceJet.Domain.Models.DocumentSeries")`.

Tworzone są 3 serie (po jednej na typ dokumentu):

| Kolumna | Typ SQL | Nullable | Wartość zapisana |
|---|---|---|---|
| `Id` | `int IDENTITY` | nie | auto |
| `SeriesName` | `nvarchar(max)` | nie | `DateTime.Now.Year.ToString()` np. `"2026"` |
| `FirstNumber` | `int` | nie | `1` |
| `CurrentNumber` | `int` | nie | `1` |
| `IsDefault` | `bit` | nie | `true` |
| `DocumentTypeId` | `int` | tak | Id typu: `Factura` / `Factura Storno` / `Factura Proforma` (z lookup) |
| `UserFirmId` | `int` | tak | Id nowo utworzonego `UserFirm` |

---

### Encja `DocumentType` → tabela `DocumentType` (lookup, odczyt)

Używana przez `AddInitialDocumentSeries` — zapytania o Id typów `"Factura"`, `"Factura Storno"`, `"Factura Proforma"`.
Seeded przez `DbSeeder` przy starcie aplikacji.

---

## 3. Relacje i kaskady

| Z encji | Pole FK | Do encji | Kierunek | Kaskada |
|---|---|---|---|---|
| `UserFirm` | `FirmId` | `Firm` | N:1 | CASCADE (delete UserFirm when Firm deleted) |
| `UserFirm` | `UserId` | `User` | N:1 | CASCADE |
| `User` | `ActiveUserFirmId` | `UserFirm` | N:1 opcjonalna | brak kaskady (`IsRequired(false)`) |
| `DocumentSeries` | `UserFirmId` | `UserFirm` | N:1 opcjonalna | brak kaskady |
| `DocumentSeries` | `DocumentTypeId` | `DocumentType` | N:1 opcjonalna | brak kaskady |

---

## 4. Mapowania AutoMapper

| Źródło | Cel | Profil | Uwagi |
|---|---|---|---|
| `FirmDto` | `Firm` | `FirmProfile.cs` — `CreateMap<Firm, FirmDto>().ReverseMap()` | Wszystkie pola mapowane 1:1 po nazwach; `Id` w FirmDto jest mapowany do `Firm.Id`, ale EF Core IDENTITY ignoruje go i generuje własny |
| `Firm` | `FirmDto` | `FirmProfile.cs` — `CreateMap<Firm, FirmDto>()` | Używane przy zwrocie (ale serwis zwraca wejściowy `firmDto` z poprawionym `Id`, nie mapuje Firm→FirmDto) |

---

## 5. Zapytania (LINQ/SQL)

**Sprawdzenie istniejącej relacji UserFirm:**
```csharp
// FirmService.cs › FirmService.ManageUserFirmRelation (via UserFirmRepository)
var existingUserFirm = await _unitOfWork.UserFirms.GetUserFirmById(userId, firmId);
// UserFirmRepository: _dbSet.Where(uf => uf.UserId == userId && uf.FirmId == userFirmId).FirstOrDefaultAsync()
```
SQL: `SELECT TOP(1) ... FROM [UserFirm] WHERE UserId = @userId AND FirmId = @firmId`.

**Pobranie użytkownika z aktywną firmą:**
```csharp
// FirmService.cs › FirmService.ManageUserFirmRelation (via UserRepository)
var user = await _unitOfWork.Users.GetUserByIdAsync(_userService.GetCurrentUserId());
// UserRepository: _dbSet.Where(u => u.Id == userId).Include(uf => uf.ActiveUserFirm).SingleOrDefaultAsync()
```

**Lookup typów dokumentów (3 osobne zapytania w AddInitialDocumentSeries):**
```csharp
// DocumentSeriesService.cs › DocumentSeriesService.AddInitialDocumentSeries
DocumentType = await _unitOfWork.DocumentTypes.Query()
    .Where(d => d.Name.Equals("Factura")).FirstOrDefaultAsync()
// (analogicznie dla "Factura Storno" i "Factura Proforma")
```

---

## 6. Użyte enumy i lookupy

| Element | Rodzaj | Plik | Wartości istotne dla procesu |
|---|---|---|---|
| `DocumentType` (lookup) | tabela słownikowa, seeded | `Domain/Models/DocumentType.cs` + `Seeders/DbSeeder.cs` | `"Factura"` (Id=1), `"Factura Proforma"` (Id=2), `"Factura Storno"` (Id=3) — kolejność inserta z seedera |

> Pełne wartości: `../../SLOWNIK_DANYCH.md#DocumentType`.
