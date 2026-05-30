# RegisterUser — Dane, modele i mapowania

## 1. DTO

### `UserRegisterDto` (wejście)

Plik: `Application/DTOs/UserRegisterDto.cs`

| Pole | Typ C# | Wymagane | Opis / źródło wartości |
|---|---|---|---|
| `Id` | `Guid?` | nie | Ignorowane przez serwis; id generuje baza |
| `FirstName` | `string` | tak* | Imię — trafia do `User.FirstName` |
| `LastName` | `string` | tak* | Nazwisko — trafia do `User.LastName` |
| `Email` | `string` | tak* | E-mail — trafia do `User.Email`; sprawdzany na unikalność |
| `Password` | `string` | tak* | Hasło jawne — haszowane BCrypt → `User.PasswordHash` |
| `PasswordConfirmation` | `string` | tak* | Powtórzenie hasła — używane tylko do walidacji, nie zapisywane |

> Atrybuty walidacyjne DTO: brak. Żadne pole nie ma `[Required]`, `[MinLength]`, `[EmailAddress]` itp. [UWAGA: brak model validation oznacza, że ASP.NET Core nie odrzuci żądania z brakującymi polami przed dotarciem do serwisu — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Odpowiedź (brak dedykowanego DTO)

Kontroler zwraca `Ok(new { token })` — anonimowy typ. Kształt odpowiedzi:

| Pole | Typ | Opis |
|---|---|---|
| `token` | `string` | JWT — ciąg znaków Base64url |

---

## 2. Encje i kolumny

### Encja `User` → tabela `User`

Kotwica: `Domain/Models/User.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("InvoiceJet.Domain.Models.User")`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `Id` | `uniqueidentifier` (auto-generated) | nie | PK | — |
| `Email` | `nvarchar(max)` | nie | — | brak (brak unikalności na poziomie DB) |
| `FirstName` | `nvarchar(max)` | nie | — | — |
| `LastName` | `nvarchar(max)` | nie | — | — |
| `PasswordHash` | `nvarchar(max)` | nie | — | — |
| `Role` | `nvarchar(max)` | nie | — | — |
| `ActiveUserFirmId` | `int` | tak (nullable) | FK → `UserFirm.UserFirmId` | IX (`HasIndex("ActiveUserFirmId")`) |

Jawna konfiguracja EF Core (`InvoiceJetDbContext.cs › OnModelCreating`):
```csharp
modelBuilder.Entity<User>()
    .HasOne(u => u.ActiveUserFirm)
    .WithMany()
    .HasForeignKey(u => u.ActiveUserFirmId)
    .IsRequired(false);  // nullable — user bez firmy jest dopuszczalny
```

> `Email` **nie ma** unikalnego indeksu DB. Unikalność jest egzekwowana wyłącznie przez walidację w serwisie. Pełne definicje: `../../SLOWNIK_DANYCH.md#User`.

---

## 3. Relacje i kaskady

Tylko relacje istotne dla procesu rejestracji:

| Z encji | Pole FK | Do encji | Kierunek | Kaskada |
|---|---|---|---|---|
| `User` | `ActiveUserFirmId` | `UserFirm` | N:1 (opcjonalna) | brak kaskady (FK bez OnDelete) |

Przy rejestracji `ActiveUserFirmId = NULL` — relacja nie jest aktywna.

---

## 4. Mapowania AutoMapper

> Sekcja nie dotyczy tego procesu. `AuthService.RegisterUser` nie używa AutoMapper. Mapowanie `UserRegisterDto → User` jest realizowane ręcznie w serwisie (patrz plik 03, sekcja 3).

---

## 5. Zapytania (LINQ/SQL)

**Sprawdzenie unikalności e-mail:**
```csharp
// AuthService.cs › AuthService.RegisterUser (via UserRepository)
var existingUser = await _unitOfWork.Users.Query()
    .FirstOrDefaultAsync(u => u.Email == userDto.Email);
```
Odpowiada SQL: `SELECT TOP(1) ... FROM [User] WHERE Email = @email`.

**Zapis nowego użytkownika:**
```csharp
// GenericRepository.cs › GenericRepository.AddAsync
await _dbSet.AddAsync(entity);
// potem: UnitOfWork.CompleteAsync() → _context.SaveChangesAsync()
```
Odpowiada SQL: `INSERT INTO [User] (Id, Email, FirstName, LastName, PasswordHash, Role, ActiveUserFirmId) VALUES (...)`.

---

## 6. Użyte enumy i lookupy

> Sekcja nie dotyczy tego procesu. Rejestracja nie używa żadnych enumów, tabel słownikowych ani seed danych. Rola `"User"` jest ustawiana jako stała `string`, nie jako enum.
