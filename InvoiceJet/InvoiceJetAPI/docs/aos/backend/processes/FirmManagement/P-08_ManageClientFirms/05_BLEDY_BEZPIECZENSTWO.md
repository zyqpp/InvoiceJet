# ManageClientFirms — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

### Endpoint GET `/api/Firm/GetUserClientFirms`

Proces jest read-only, bez walidacji wejścia:

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| — | Wymiar nie dotyczy (read-only) | — | — | — | — | — |

### Endpoint PUT `/api/Firm/DeleteFirms`

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | Firma o danym ID musi istnieć w bazie | `FirmService.cs › FirmService.DeleteFirms, linia 114` | `GetByIdAsync(firmId)` zwraca `null` | `Exception` [UWAGA: błędny typ] | `500` [UWAGA: powinno 400] | `"Product not found."` [UWAGA: błędny tekst] |
| `WAL-02` | Firma nie może być powiązana z dokumentami | `FirmService.cs › FirmService.DeleteFirms, linie 117-123` | `Documents.Query().AnyAsync(d => d.ClientId == firmId)` zwraca `true` | `FirmAssociatedWithDocumentException` | `400` | `"Can't delete. Firm {firmName} is associated with a document."` |

> **Uwagi:**
> - WAL-01: Wyjątek `Exception` jest generyczny i nie jest jawnie mapowany w `ExceptionMiddleware` — trafia do catch-all (500). Powinien być dedykowany `FirmNotFoundException` lub przynajmniej zwracać 400.
> - WAL-02: Mapowany jawnie w `ExceptionMiddleware` → 400 OK.

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| `Exception` (generyczny, WAL-01) | **nie** | `500` | `ExceptionMiddleware.cs` (catch-all) |
| `FirmAssociatedWithDocumentException` (WAL-02) | **tak** | `400` | `ExceptionMiddleware.cs` (wiersz dla tej klasy) |

Pełen rejestr: `../../KATALOG_WYJATKOW.md`.

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze | `[Authorize(Roles = "User")]` (klasa `FirmController`, linia 10) |
| Wymagana rola | `"User"` |
| Źródło tożsamości użytkownika | `IUserService.GetCurrentUserId()` — odczyt z JWT claim `userId` |
| Token | JWT (`JwtBearerDefaults.AuthenticationScheme`) — czas ważności 10 minut |

Oba endpointy wymagają autoryzacji. Brak tokenu lub niepoprawna rola → `401 Unauthorized` lub `403 Forbidden` (obsłużone przez ASP.NET Core framework).

## 4. Uwagi bezpieczeństwa

- [UWAGA: Generyczny typ wyjątku `Exception` w WAL-01 trafia do catch-all middleware (500) zamiast 400. Powinien być dedykowany `FirmNotFoundException`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Komunikat błędu w WAL-01 mówi "Product not found." zamiast "Firm not found." — WYMAGA POPRAWY]
- [UWAGA: Brak jawnej transakcji w DELETE. Jeśli `CompleteAsync()` się nie powiedzie, częściowy zapis pozostanie w bazie. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Brak innych uwag bezpieczeństwa (autoryzacja prawidłowa, dane w odpowiedzi bezpieczne, brak własnych try/catch omijających middleware).
