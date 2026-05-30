# GetUserActiveFirm — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

| ID | Reguła | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek / odpowiedź | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | Żądanie musi posiadać ważny JWT z rolą `"User"` | `[Authorize(Roles = "User")]` na klasie `FirmController` | Brak `Authorization`, nieważny token lub brak roli `"User"` | ASP.NET Core (poza `ExceptionMiddleware`) | `401` / `403` | (brak body) |

> Poza autoryzacją proces nie ma żadnych walidacji domenowych — brak danych wejściowych do walidowania (endpoint bezparametrowy).

### Brak warunków implicitnych powodujących błędy

Proces jest odczytowy i defensywny:
- Brak aktywnej firmy → pusty `FirmDto`, **nie** wyjątek.
- Brak użytkownika w DB → pusty `FirmDto`, **nie** wyjątek.
- `SingleOrDefaultAsync` po filtrze na PK → brak ryzyka `InvalidOperationException` (max 1 wiersz).

---

## 2. Mapowanie wyjątków na HTTP

Proces **nie rzuca żadnego wyjątku domenowego** ani nie wykonuje operacji DB mogących rzucić `DbUpdateException`. Jedyne potencjalne wyjątki to nieobsługiwane błędy infrastrukturalne (np. utrata połączenia z DB), które trafiają do catch-all.

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło |
|---|---|---|---|
| `SqlException` / błąd połączenia DB (teoretyczny) | **nie** (catch-all) | `500 Internal Server Error` | `ExceptionMiddleware.cs` |
| `NullReferenceException` — `httpContext` null w `GetCurrentUserId` (teoretyczny, niemożliwy w pipeline z `[Authorize]`) | **nie** (catch-all) | `500 Internal Server Error` | `ExceptionMiddleware.cs` |

> Pełen rejestr wyjątek → HTTP: `../../KATALOG_WYJATKOW.md`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze | `[Authorize(Roles = "User")]` na klasie `FirmController` |
| Wymagana rola | `"User"` |
| Źródło tożsamości | `IUserService.GetCurrentUserId()` — claim `"userId"` (Guid) z `HttpContext.User` |
| Fallback gdy niezalogowany | `GetCurrentUserId()` zwraca `Guid.Empty` — ale endpoint chroniony `[Authorize]` |

Kotwica tożsamości:

```csharp
// UserService.cs › UserService.GetCurrentUserId
var httpContext = _httpContextAccessor.HttpContext;
if (httpContext.User.Identity is not { IsAuthenticated: true })
    return Guid.Empty;
var userIdString = httpContext.User.FindFirst("userId")?.Value;
return Guid.TryParse(userIdString, out var userId) ? userId : Guid.Empty;
```

Tożsamość determinuje, czyją aktywną firmę zwraca proces — użytkownik widzi wyłącznie własną aktywną firmę (filtr `WHERE u.Id == userId`).

---

## 4. Uwagi bezpieczeństwa

- Izolacja danych jest zachowana — zapytanie filtruje po `userId` z JWT, więc użytkownik nie może odczytać firmy innego użytkownika tym endpointem.
- [UWAGA: Brak rozróżnienia odpowiedzi między „użytkownik bez aktywnej firmy" a „użytkownik nie istnieje w DB" — oba zwracają pusty `FirmDto` z `200 OK`. Nie stanowi to bezpośredniego ryzyka bezpieczeństwa, ale utrudnia diagnostykę — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Redundantny `.ThenInclude(u => u.User)` w `GetUserFirmAsync` ładuje dane użytkownika nieużywane w odpowiedzi — niepotrzebne ujawnienie/transfer danych z DB do warstwy aplikacji oraz koszt wydajnościowy — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `httpContext.User` w `GetCurrentUserId` jest odczytywane bez sprawdzenia, czy `httpContext` jest `null`. W normalnym pipeline z `[Authorize]` kontekst zawsze istnieje, ale wywołanie poza żądaniem HTTP rzuciłoby `NullReferenceException` → `500` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Tożsamość pochodzi wyłącznie z JWT — nie jest ponownie weryfikowana z DB (prawidłowe dla read-only).
