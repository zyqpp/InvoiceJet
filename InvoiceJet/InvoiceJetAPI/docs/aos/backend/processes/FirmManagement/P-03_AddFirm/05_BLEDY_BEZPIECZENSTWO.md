# AddFirm — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

`AddFirm` i `ManageUserFirmRelation` nie rzucają wyjątków domenowych. Jedyną jawną walidacją jest autoryzacja JWT egzekwowana przez middleware ASP.NET Core.

| ID | Reguła | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek / odpowiedź | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | Żądanie musi posiadać ważny JWT z rolą `"User"` | `[Authorize(Roles = "User")]` na klasie `FirmController` — `Program.cs › app.UseAuthentication()` + `app.UseAuthorization()` | Brak nagłówka `Authorization`, nieważny token lub brak roli `"User"` | ASP.NET Core odpowiedź (poza `ExceptionMiddleware`) | `401` / `403` | (brak body lub pusty) |

> Poza autoryzacją brak walidacji WAL na polach `FirmDto`. Puste stringi, `null`, zbyt długie wartości — wszystkie trafiają bezpośrednio do EF Core.

### Warunki implicitne (nie walidacje domenowe, ale powodują błędy)

| Sytuacja | Skutek |
|---|---|
| `FirmDto.RegCom = null` | `DbUpdateException` (NOT NULL constraint w DB) → `500` |
| `FirmDto.Name`, `.Cui`, `.Address`, `.County`, `.City` = `null` lub `""` | EF Core akceptuje pusty string (`""`) — zapisuje do DB; `null` → NOT NULL violation → `500` |
| `isClient` w URL nie parsuje się na `bool` | ASP.NET Core ModelState error → `400 Bad Request` (przed dotarciem do serwisu) |
| Seed DocumentType nie istnieje (`"Factura"`, `"Factura Storno"`, `"Factura Proforma"`) | `AddInitialDocumentSeries` zapisze serie z `DocumentTypeId = null` zamiast odpowiedniego Id — brak błędu, ale dane są niekompletne |

---

## 2. Mapowanie wyjątków na HTTP

Wyjątki domenowe nie są rzucane przez `AddFirm`. Wszystkie błędy trafiają do catch-all.

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| `DbUpdateException` (null constraint, FK) | **nie** | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all) |
| `ArgumentNullException` (np. `null` w forgivable operator `user!`) | **nie** | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all) |
| `NullReferenceException` (`user!` gdy user usunięty z DB) | **nie** | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all) |

> Pełen rejestr wyjątek → HTTP: `../../KATALOG_WYJATKOW.md`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze | `[Authorize(Roles = "User")]` na klasie `FirmController` — dotyczy wszystkich metod |
| Wymagana rola | `"User"` |
| Źródło tożsamości | `IUserService.GetCurrentUserId()` — odczytuje claim `"userId"` (Guid) z `HttpContext.User` |
| Fallback gdy nie-zalogowany | `GetCurrentUserId()` zwraca `Guid.Empty` — ale endpoint chroniony przez `[Authorize]`, więc niedostępny bez tokenu |

Kotwica tożsamości: `UserService.cs › UserService.GetCurrentUserId`

```csharp
// UserService.cs › UserService.GetCurrentUserId
var userIdString = httpContext.User.FindFirst("userId")?.Value;
return Guid.TryParse(userIdString, out var userId) ? userId : Guid.Empty;
```

---

## 4. Uwagi bezpieczeństwa

- [UWAGA: Brak walidacji pól `FirmDto` — użytkownik może wysłać dowolnie długi string w polu `Name`, `Address` itp. Kolumny `nvarchar(max)` w SQL Server nie mają limitu długości, więc bardzo duże payload może powodować problemy z wydajnością zapisu i pamięcią — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Brak sprawdzenia unikalności CUI — różni użytkownicy mogą dodać firmę o tym samym CUI niezależnie. Ten sam użytkownik też może dodać tę samą firmę wielokrotnie (każde wywołanie tworzy nowy rekord `Firm`) — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `isClient = true` przy braku aktywnej firmy użytkownika → firma klienta staje się aktywną firmą użytkownika. Może prowadzić do sytuacji, gdzie firma klienta (odbiorca) jest używana jako nadawca faktur — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Tożsamość użytkownika pochodzi wyłącznie z JWT — nie jest weryfikowana ponownie z DB przy każdym żądaniu.
