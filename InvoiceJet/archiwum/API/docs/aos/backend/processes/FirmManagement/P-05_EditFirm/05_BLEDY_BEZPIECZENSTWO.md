# EditFirm — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

| ID | Reguła | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek / odpowiedź | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | Żądanie musi posiadać ważny JWT z rolą `"User"` | `[Authorize(Roles = "User")]` na klasie `FirmController` | Brak `Authorization`, nieważny token lub brak roli `"User"` | ASP.NET Core (poza `ExceptionMiddleware`) | `401` / `403` | (brak body) |
| `WAL-02` | Firma o `firmDto.Id` musi istnieć w DB | `FirmService.cs › FirmService.EditFirm` — `if (firm == null) throw new Exception("Firm not found.")` | `firmDto.Id` nie odpowiada żadnemu rekordowi `Firm` | `Exception` → catch-all `ExceptionMiddleware` | **`500`** | `"Firm not found."` |

> [UWAGA: `WAL-02` — naruszenie skutkuje `500 Internal Server Error` zamiast `404 Not Found`. `throw new Exception(...)` (nie wyjątek domenowy) trafia do catch-all `Exception ex` w `ExceptionMiddleware` → `HttpStatusCode.InternalServerError`. Poprawne rozwiązanie: dedykowana klasa `FirmNotFoundException` zmapowana na `404` — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Warunki implicitne (nie walidacje domenowe, ale powodują błędy)

| Sytuacja | Skutek |
|---|---|
| `firmDto.RegCom = null` | `DbUpdateException` (NOT NULL constraint) → `500` |
| `firmDto.Name`, `.Cui`, `.Address`, `.County`, `.City` = `null` | `DbUpdateException` (NOT NULL constraint) → `500` |
| `firmDto.Name` / inne pola — pusty string `""` | `200 OK` — EF Core zapisuje pusty string do `nvarchar(max)` |
| `isClient` w URL nieparsowane na `bool` (np. `"yes"`, `"1"`) | ASP.NET Core ModelState error → `400 Bad Request` (przed serwisem) |

---

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie w `ExceptionMiddleware`? | Status HTTP | Komunikat |
|---|---|---|---|
| `Exception("Firm not found.")` | **nie** (catch-all) | `500 Internal Server Error` | `"Firm not found."` |
| `DbUpdateException` (null constraint, FK) | **nie** (catch-all) | `500 Internal Server Error` | EF Core message |
| `NullReferenceException` (`user!` w `ManageUserFirmRelation`) | **nie** (catch-all) | `500 Internal Server Error` | — |
| `ArgumentNullException` | **nie** (catch-all) | `500 Internal Server Error` | — |

> Pełen rejestr wyjątek → HTTP: `../../KATALOG_WYJATKOW.md`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze | `[Authorize(Roles = "User")]` na klasie `FirmController` — dotyczy wszystkich metod |
| Wymagana rola | `"User"` |
| Źródło tożsamości | `IUserService.GetCurrentUserId()` — odczytuje claim `"userId"` (Guid) z `HttpContext.User` |

Tożsamość używana jest w `ManageUserFirmRelation` do identyfikacji relacji `UserFirm` dla aktualnego użytkownika.

```csharp
// UserService.cs › UserService.GetCurrentUserId
var userIdString = httpContext.User.FindFirst("userId")?.Value;
return Guid.TryParse(userIdString, out var userId) ? userId : Guid.Empty;
```

---

## 4. Uwagi bezpieczeństwa

- [UWAGA: Brak weryfikacji, czy firma o `firmDto.Id` należy do aktualnego użytkownika. Zalogowany użytkownik może edytować **dowolną firmę** w systemie — wystarczy znać jej `Id`. `GetByIdAsync(firmDto.Id)` nie filtruje po `userId` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Brak walidacji pól DTO — użytkownik może wysłać bardzo długi string w każdym polu tekstowym. Kolumny `nvarchar(max)` nie mają ograniczenia długości, co może powodować problemy z wydajnością — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Brak unikalnego indeksu na `Firm.Cui` — możliwa edycja firmy w taki sposób, że `Cui` pokrywa się z inną firmą w DB. System nie wykrywa i nie blokuje tej sytuacji — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `ManageUserFirmRelation` tworzy nową relację `UserFirm` gdy `existingUserFirm == null`. W kontekście EditFirm oznacza to, że użytkownik może próbować edytować firmę, z którą nie ma relacji — system milcząco ją tworzy. Brak sprawdzenia, czy firma „należy" do użytkownika przed edycją — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Brak jawnej transakcji między `CompleteAsync()` #1 (zapis Firm) i `CompleteAsync()` #2 (zapis UserFirm). Częściowa awaria pozostawi firmę z zaktualizowanymi danymi, ale bez zaktualizowanej flagi `IsClient` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Tożsamość użytkownika pochodzi wyłącznie z JWT — nie jest weryfikowana ponownie z DB przy każdym żądaniu.
