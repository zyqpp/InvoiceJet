# LoginUser — Dane, modele i mapowania

## 1. DTO

### `UserLoginDto` (wejście)

Plik: `Application/DTOs/UserLoginDto.cs`

| Pole | Typ C# | Wymagane | Opis |
|---|---|---|---|
| `Email` | `string` | tak* | Adres e-mail — klucz wyszukiwania użytkownika |
| `Password` | `string` | tak* | Hasło jawne — weryfikowane BCrypt względem `User.PasswordHash` |

> Atrybuty walidacyjne DTO: brak. [UWAGA: pola `null` nie są odrzucane przez model validation — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Odpowiedź (brak dedykowanego DTO)

Kontroler zwraca `Ok(new { token })` — anonimowy typ:

| Pole | Typ | Opis |
|---|---|---|
| `token` | `string` | JWT — ciąg znaków Base64url |

---

## 2. Encje i kolumny

### Encja `User` → tabela `User` (odczyt)

Kotwica: `Domain/Models/User.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("InvoiceJet.Domain.Models.User")`.

Proces **odczytuje** istniejący rekord `User`. Nie tworzy ani nie modyfikuje rekordów.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks | Użycie w P-02 |
|---|---|---|---|---|---|
| `Id` | `uniqueidentifier` | nie | PK | — | claim `userId` w JWT |
| `Email` | `nvarchar(max)` | nie | — | brak unikalnego IX | klucz wyszukiwania + claim `email` |
| `FirstName` | `nvarchar(max)` | nie | — | — | claim `firstName` w JWT |
| `LastName` | `nvarchar(max)` | nie | — | — | claim `lastName` w JWT |
| `PasswordHash` | `nvarchar(max)` | nie | — | — | wejście do `BC.Verify` |
| `Role` | `nvarchar(max)` | nie | — | — | nie odczytywany (claim Role hardcoded `"User"`) |
| `ActiveUserFirmId` | `int` | tak | FK → `UserFirm` | IX | nie odczytywany w tym procesie |

> Pełne definicje: `../../SLOWNIK_DANYCH.md#User`.

---

## 3. Relacje i kaskady

> Sekcja nie dotyczy tego procesu. Logowanie odczytuje wyłącznie tabelę `User` — relacja `User → UserFirm` nie jest dołączana (brak `.Include()` w zapytaniu).

---

## 4. Mapowania AutoMapper

> Sekcja nie dotyczy tego procesu. `AuthService.LoginUser` nie używa AutoMapper.

---

## 5. Zapytania (LINQ/SQL)

**Wyszukanie użytkownika po e-mailu:**
```csharp
// AuthService.cs › AuthService.LoginUser (via GenericRepository.Query)
var user = await _unitOfWork.Users.Query()
    .FirstOrDefaultAsync(u => u.Email == userDto.Email);
```
Odpowiada SQL: `SELECT TOP(1) ... FROM [User] WHERE Email = @email`.

Zapytanie nie dołącza żadnych relacji (brak `.Include()`). Kolumna `ActiveUserFirmId` jest pobierana, ale nie jest używana w procesie logowania.

---

## 6. Użyte enumy i lookupy

> Sekcja nie dotyczy tego procesu. Logowanie nie używa żadnych enumów, tabel słownikowych ani seed danych.
