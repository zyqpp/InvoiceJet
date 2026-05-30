# ManageDocumentSeries — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

### Endpoint `GET /api/DocumentSeries/GetAllDocumentSeriesForUserId`

Brak walidacji wejściowych. Użytkownik bez firmy otrzymuje `200 OK` z pustą listą `[]`.

### Endpoint `POST /api/DocumentSeries/AddDocumentSeries`

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | Użytkownik musi mieć aktywną firmę | `DocumentSeriesService.cs › DocumentSeriesService.AddDocumentSeries` | `GetUserFirmIdAsync(userId)` zwraca `null` | `UserHasNoAssociatedFirmException` | `400` (przez try/catch kontrolera, nie middleware) | `"User has no associated firm."` (plain text w body) |

> WAL-01: wyjątek przechwycony przez `catch (Exception ex)` w `DocumentSeriesController.AddDocumentSeries` → `BadRequest(ex.Message)`. Ciało odpowiedzi to **plain string**, nie JSON `{ "message": "..." }`. Niespójność z pozostałymi endpointami. [UWAGA — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Endpoint `PUT /api/DocumentSeries/UpdateDocumentSeries`

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-02` | Seria o danym `Id` musi istnieć w bazie | `DocumentSeriesService.cs › DocumentSeriesService.UpdateDocumentSeries` | `Query().FirstOrDefaultAsync(ds => ds.Id == documentSeriesDto.Id)` zwraca `null` | `Exception` (generyczny) | `500` ⚠️ | `"Document Series not found"` |

> WAL-02: generyczny `Exception` trafia do catch-all → `500 Internal Server Error`. Powinien być dedykowany `DocumentSeriesNotFoundException` zwracający `400` lub `404`. [UWAGA — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Endpoint `PUT /api/DocumentSeries/DeleteDocumentSeries`

Brak walidacji. Nieistniejące IDs są po cichu ignorowane — `200 OK` nawet gdy żadna seria nie istnieje.

---

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| `UserHasNoAssociatedFirmException` | tak (pośrednio) | `400 Bad Request` | `DocumentSeriesController.cs › AddDocumentSeries` — `catch (Exception ex) { return BadRequest(ex.Message); }` — **omija ExceptionMiddleware** |
| `Exception` (generyczny — WAL-02) | **nie** ⚠️ | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all `Exception`) |

> Pełen rejestr: `../../KATALOG_WYJATKOW.md`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze | `[Authorize(Roles = "User")]` na klasie `DocumentSeriesController` |
| Wymagana rola | `"User"` |
| Źródło tożsamości użytkownika | `IUserService.GetCurrentUserId()` — odczyt z JWT claim `userId` z `HttpContext` |
| Token | JWT (`JwtBearerDefaults.AuthenticationScheme`), czas ważności 10 minut |

Wszystkie 4 endpointy wymagają autoryzacji. Brak tokenu → `401 Unauthorized`; błędna rola → `403 Forbidden`.

---

## 4. Uwagi bezpieczeństwa

- [UWAGA: `AddDocumentSeries` ma własny `try/catch (Exception ex)` w kontrolerze — przechwytuje WSZYSTKIE wyjątki z serwisu i zwraca `400 BadRequest(ex.Message)`. Omija `ExceptionMiddleware`. Ciało błędu to plain string, nie JSON. Niespójność architektoniczna. Kotwica: `DocumentSeriesController.cs › DocumentSeriesController.AddDocumentSeries`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `UpdateDocumentSeries` i `DeleteDocumentSeries` nie weryfikują, czy operowane serie należą do aktywnej firmy bieżącego użytkownika. Użytkownik znający `Id` serii mógłby edytować lub usunąć serię innego użytkownika. Brak ownership check. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `DeleteDocumentSeries` nie sprawdza powiązania serii z dokumentami przed usunięciem. Brak odpowiednika `BankAccountAssociatedWithDocumentsException` / `ProductAssociatedWithInvoiceException`. Usunięcie serii może osierocić dokumenty. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `DeleteDocumentSeries` używa `PUT` zamiast `DELETE`. Kotwica: `DocumentSeriesController.cs` — `[HttpPut("DeleteDocumentSeries")]`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Nieistniejące `documentSeriesIds` w `DeleteDocumentSeries` są po cichu ignorowane — klient nie wie, które serie faktycznie zostały usunięte. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `DocumentSeriesDto` zawiera pole `DocumentType` o typie `InvoiceJet.Domain.Models.DocumentType` (encja domenowa, nie DTO) — narusza separację warstw. Null reference możliwy gdy `documentSeriesDto.DocumentType` = null przy `documentSeriesDto.DocumentType!.Id`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
