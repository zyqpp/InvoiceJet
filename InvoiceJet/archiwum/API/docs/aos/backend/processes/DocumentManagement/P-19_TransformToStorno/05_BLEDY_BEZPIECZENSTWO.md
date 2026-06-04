# TransformToStorno — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | Użytkownik ma aktywną firmę | `DocumentService.cs › DocumentService.TransformToStorno` | `GetUserFirmIdAsync` zwraca `null` | `new Exception("User firm not found.")` | `500` ⚠️ | `"User firm not found."` |
| `WAL-02` | Dokument istnieje i należy do firmy | `DocumentService.cs › DocumentService.TransformToStorno` | `Query().Where(Id && UserFirmId).FirstOrDefaultAsync()` zwraca `null` | `new Exception("Document not found.")` | `500` ⚠️ | `"Document not found."` |

> ⚠️ Oba wyjątki to `new Exception(...)` — niemapowane w `ExceptionMiddleware` → catch-all → **500**. W pozostałych procesach P-12/P-13/P-17 brak firmy powoduje `400` via `UserHasNoAssociatedFirmException`. Niespójność z całym API.

---

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| `Exception("User firm not found.")` | **nie** | `500 Internal Server Error` | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` (catch-all) |
| `Exception("Document not found.")` | **nie** | `500 Internal Server Error` | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` (catch-all) |

> Pełen rejestr wyjątek→HTTP: `../../KATALOG_WYJATKOW.md`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze/akcji | `[Authorize(Roles = "User")]` na klasie `DocumentController` |
| Wymagana rola | `User` |
| Źródło tożsamości | `IUserService.GetCurrentUserId()` → `userId` → `GetUserFirmIdAsync` |
| Token | JWT (`JwtBearerDefaults.AuthenticationScheme`) |

---

## 4. Uwagi bezpieczeństwa

- Ownership check obecny ✅ — `Where(d => d.Id == documentId && d.UserFirmId == activeUserFirmId)` — użytkownik może stornować tylko własne dokumenty.

- [UWAGA: WAL-01 i WAL-02 zwracają **500** zamiast odpowiednio **400** i **404** — użyto `new Exception(...)` zamiast domenowych wyjątków. Klient otrzymuje HTTP 500 w przypadku sytuacji oczekiwanych (brak firmy, brak dokumentu). Kotwica: `DocumentService.cs › DocumentService.TransformToStorno`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: `CompleteAsync()` wewnątrz `foreach` — przy N dokumentach wykonywane jest N transakcji. Błąd w połowie operacji powoduje częściowe storno bez możliwości rollbacku. Kotwica: `DocumentService.cs › DocumentService.TransformToStorno`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: Pusta tablica `[]` → `200 OK` bez zmian i bez sygnalizacji. — UWAGA informacyjna]
