# GetUserClientFirms — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

| ID | Reguła | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek / odpowiedź | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | Żądanie musi posiadać ważny JWT z rolą `"User"` | `[Authorize(Roles = "User")]` na klasie `FirmController` | Brak `Authorization`, nieważny token lub brak roli `"User"` | ASP.NET Core (poza `ExceptionMiddleware`) | `401` / `403` | (brak body) |

> Poza autoryzacją proces nie ma żadnych walidacji domenowych — brak danych wejściowych do walidowania (endpoint bezparametrowy).

### Brak warunków implicitnych powodujących błędy

Proces jest odczytowy i defensywny:
- Brak firm-klientów → pusta lista `[]`, **nie** wyjątek.
- Brak użytkownika w DB → pusta lista `[]`, **nie** wyjątek.
- `ToListAsync` zawsze zwraca listę (nigdy `null`).

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
var userIdString = httpContext.User.FindFirst("userId")?.Value;
return Guid.TryParse(userIdString, out var userId) ? userId : Guid.Empty;
```

Tożsamość determinuje, czyje firmy-klientów zwraca proces — filtr `WHERE UserId.Equals(userId)`.

---

## 4. Uwagi bezpieczeństwa

- Izolacja danych jest zachowana — zapytanie filtruje po `userId` z JWT (`UserFirmRepository.GetUserFirmClients` — `Where(u => u.UserId.Equals(userId) && u.IsClient)`), więc użytkownik nie może odczytać klientów innego użytkownika.
- [UWAGA: Sprawdzenie `clients.Count == 0` w serwisie jest redundantne — `_mapper.Map<List<FirmDto>>` na pustej liście zwróciłby pustą listę. Nie stanowi ryzyka, ale jest nadmiarowym kodem — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Brak jawnego `OrderBy` w zapytaniu — kolejność firm na liście jest niezdeterminowana (zależna od planu zapytania DB). Może powodować niespójną kolejność między żądaniami — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `httpContext.User` w `GetCurrentUserId` odczytywane bez sprawdzenia `httpContext != null`. W normalnym pipeline z `[Authorize]` kontekst zawsze istnieje, ale wywołanie poza żądaniem HTTP rzuciłoby `NullReferenceException` → `500` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Tożsamość pochodzi wyłącznie z JWT — nie jest ponownie weryfikowana z DB (prawidłowe dla read-only).
