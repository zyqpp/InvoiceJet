# AddDocument — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

### Endpoint `POST /api/Document/AddDocument`

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | Użytkownik musi mieć aktywną firmę | `DocumentService.cs › DocumentService.AddDocument` | `GetUserFirmIdAsync(userId)` zwraca `null` | `UserHasNoAssociatedFirmException` | `400` | `"User has no associated firm."` |
| `WAL-02` | Aktywna firma musi mieć co najmniej jedno aktywne konto bankowe | `DocumentService.cs › DocumentService.AddDocument` | `BankAccounts.Query().Where(IsActive).FirstOrDefaultAsync()` zwraca `null` (null-coalescing `??`) | `NoBankAccountAddedException` | `400` | `"Please add a bank account, before generating a document."` |
| `WAL-03` | Istniejący produkt (`Id > 0`) musi istnieć w DB dla aktywnej firmy | `DocumentService.cs › DocumentService.UpdateDocumentProducts` | `Products.Query().FirstOrDefaultAsync(p => p.Name == dto.Name && p.UserFirmId == userFirmId)` zwraca `null` | `Exception` (generyczny) | `500` ⚠️ | `"Product not found."` |

> WAL-01 i WAL-02: mapowane jawnie w `ExceptionMiddleware.cs` → `400 Bad Request`. Ciało: `{ "message": "..." }` (JSON).

> WAL-03: generyczny `Exception` trafia do catch-all w `ExceptionMiddleware` → `500 Internal Server Error`. Powinien być `400`/`404`. Brak dedykowanego `DocumentProductNotFoundException`. [UWAGA — WYMAGA WERYFIKACJI Z ZESPOŁEM]

> WAL-03 dodatkowy problem: szukanie produktu po `Name + UserFirmId`, nie po `Id`. Jeśli produkt zmienił nazwę od czasu wypełnienia formularza, walidacja nieprawidłowo wyrzuca `500`. [UWAGA — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| `UserHasNoAssociatedFirmException` | tak | `400 Bad Request` | `ExceptionMiddleware.cs` |
| `NoBankAccountAddedException` | tak | `400 Bad Request` | `ExceptionMiddleware.cs` |
| `Exception` (generyczny — WAL-03) | **nie** ⚠️ | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all `Exception`) |
| `NullReferenceException` (brak serii w `IncreaseDocumentSeriesNumber`) | **nie** ⚠️ | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all `Exception`) |

> Pełen rejestr: `../../KATALOG_WYJATKOW.md`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze | `[Authorize(Roles = "User")]` na klasie `DocumentController` |
| Wymagana rola | `"User"` |
| Źródło tożsamości użytkownika | `IUserService.GetCurrentUserId()` — odczyt z JWT claim `userId` z `HttpContext` |
| Token | JWT (`JwtBearerDefaults.AuthenticationScheme`), czas ważności 10 minut |

Brak tokenu → `401 Unauthorized`; błędna rola → `403 Forbidden`.

---

## 4. Uwagi bezpieczeństwa

- [UWAGA: Dwa `CompleteAsync()` bez jawnej transakcji (`BeginTransactionAsync`). Pierwsza transakcja zapisuje `Document` z `Id`. Jeśli druga transakcja zawiedzie (WAL-03, błąd w `IncreaseDocumentSeriesNumber`), `Document` pozostaje w DB bez pozycji i ze `UnitPrice=0`, `TotalPrice=0`. Brak mechanizmu rollbacku. Kotwica: `DocumentService.cs › DocumentService.AddDocument`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: WAL-03 zwraca `500` zamiast `400`/`404`. Generyczny `Exception("Product not found.")` nie jest mapowany w `ExceptionMiddleware`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Produkt wyszukiwany po `Name + UserFirmId` gdy `Id > 0` — możliwa pomyłka gdy nazwa produktu zmieniona po otwarciu formularza. Kotwica: `DocumentService.cs › DocumentService.UpdateDocumentProducts`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Brak sprawdzenia, czy `documentRequestDto.Client.Id` faktycznie jest klientem aktywnej firmy użytkownika. Możliwe przypisanie dokumentu do firmy innego użytkownika znając `ClientId`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `IncreaseDocumentSeriesNumber` nie sprawdza, czy seria istnieje (null forgiving `!`). Brak null check → `NullReferenceException` → `500` gdy seria usunięta między pobraniem autofill a wystawieniem faktury. Kotwica: `DocumentService.cs › DocumentService.IncreaseDocumentSeriesNumber`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `DocumentNumber` generowany z wartości `CurrentNumber` z DTO (przesłanej przez klienta), nie z DB. Klient może przesłać błędny `CurrentNumber` i wygenerować zduplikowany lub niespójny numer dokumentu. Brak weryfikacji unikalności `DocumentNumber`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Nowe produkty (`Id == 0`) tworzone są w tabeli `Product` bez sprawdzania, czy produkt o tej samej nazwie już istnieje (jest unikalny per `UserFirmId`). Może prowadzić do wyjątku naruszenia unikalności indeksu na poziomie DB. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
