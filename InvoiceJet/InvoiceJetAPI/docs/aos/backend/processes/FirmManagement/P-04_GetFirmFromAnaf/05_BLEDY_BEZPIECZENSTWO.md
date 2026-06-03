# GetFirmFromAnaf — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

| ID | Reguła | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek / odpowiedź | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | Żądanie musi posiadać ważny JWT z rolą `"User"` | `[Authorize(Roles = "User")]` na klasie `FirmController` | Brak nagłówka `Authorization`, nieważny token lub brak roli `"User"` | ASP.NET Core (poza `ExceptionMiddleware`) | `401` / `403` | (brak body) |

> Poza autoryzacją brak jakichkolwiek walidacji wejścia. Parametr `cui` jest przekazywany do ANAF bez weryfikacji formatu, długości ani zawartości.

### Warunki implicitne (nie walidacje domenowe, ale powodują błędy)

| Sytuacja | Skutek |
|---|---|
| ANAF HTTP non-2xx dla podanego CUI | `throw AnafFirmNotFoundException(cui)` → `404` |
| ANAF timeout (domyślny `HttpClient` = 100 s) | `HttpRequestException` → pochłoniięty przez `catch (Exception)` → `throw AnafFirmNotFoundException(cui)` → `404` |
| ANAF zwraca malformed JSON | `JsonException` z `JObject.Parse` → pochłonięty → `404` |
| ANAF HTTP 200 z pustą tablicą `found` (CUI nieznaleziony) | Brak wyjątku — zwracany pusty `FirmDto` → `200 OK` z null polami |
| `cui` = pusty string w URL | ASP.NET Core może zwrócić `404` (route matching) lub `200 OK` ze zwróconym pustym DTO z ANAF |

---

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| `AnafFirmNotFoundException` | **tak** | `404 Not Found` | `ExceptionMiddleware.cs` → `AnafFirmNotFoundException` → `404` |
| `HttpRequestException` (błąd sieci, timeout) | **nie** (pochłonięty przez `catch (Exception)` w `FirmService.GetFirmDataFromAnaf`) | `404 Not Found` (przez rethrow jako `AnafFirmNotFoundException`) | `FirmService.cs:193–196` + `ExceptionMiddleware.cs` |
| `JsonException` / `JsonReaderException` (Newtonsoft) | **nie** (pochłonięty) | `404 Not Found` | j.w. |
| `NullReferenceException` (parsowanie JSON) | **nie** (pochłonięty) | `404 Not Found` | j.w. |

> Pełen rejestr wyjątek → HTTP: `../../KATALOG_WYJATKOW.md`.

**Komunikat błędu `404`:**
```json
{ "message": "Firm with CUI {cui} not found in ANAF database." }
```
gdzie `{cui}` to wartość przekazana w parametrze trasy.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze | `[Authorize(Roles = "User")]` na klasie `FirmController` — dotyczy wszystkich metod |
| Wymagana rola | `"User"` |
| Tożsamość użytkownika | **nie jest używana** w tym procesie — `GetCurrentUserId()` nie jest wywoływane |
| Cel autoryzacji | Wyłącznie guard dostępu do endpointu — CUI jest publicznym identyfikatorem, nieprzypisanym do konkretnego użytkownika |

---

## 4. Uwagi bezpieczeństwa

- [UWAGA: Brak walidacji formatu `cui` — użytkownik może przekazać dowolny string (SQL injection nie dotyczy — `cui` nie trafia do zapytań DB; ale bardzo długi string trafia do body żądania do ANAF jako payload). Zalecana walidacja regex: `^\d{1,10}$` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `catch (Exception)` maskuje rzeczywistą przyczynę błędu. Problem sieciowy z ANAF (niedostępność serwisu zewnętrznego) i nieistniejący CUI zwracają identyczny `404`. Brak mechanizmu retry, circuit breaker ani logowania błędów sieciowych — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `new HttpClient()` tworzony w konstruktorze serwisu Scoped — nowa instancja TCP przy każdym żądaniu HTTP. Przy dużej liczbie jednoczesnych wywołań grozi wyczerpaniem puli gniazd (socket exhaustion). Zalecane: rejestracja przez `IHttpClientFactory` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Brak timeout explicite skonfigurowanego — domyślny timeout `HttpClient` wynosi 100 sekund. Zbyt długi czas odpowiedzi ANAF blokuje wątek przez 100 s, co może prowadzić do wyczerpania puli wątków pod dużym obciążeniem — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Mieszane użycie serializerów JSON w jednym procesie: `PostAsJsonAsync` (`System.Text.Json`) do wysyłania żądania + `JObject.Parse` (Newtonsoft.Json) do parsowania odpowiedzi. Brak spójności — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Tożsamość użytkownika pochodzi wyłącznie z JWT — nie jest weryfikowana z DB (co jest prawidłowe dla read-only procesu bez efektów ubocznych).
