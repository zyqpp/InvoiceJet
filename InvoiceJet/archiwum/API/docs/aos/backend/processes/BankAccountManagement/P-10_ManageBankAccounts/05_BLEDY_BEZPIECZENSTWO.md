# ManageBankAccounts — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

Walidacje pogrupowane per endpoint. Kolejność odpowiada kolejności sprawdzania w kodzie.

### Endpoint `GET /api/BankAccount/GetUserFirmBankAccounts`

Brak walidacji wejściowych. Endpoint read-only — pusta kolekcja jest poprawnym wynikiem.

### Endpoint `POST /api/BankAccount/AddUserFirmBankAccount`

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | Użytkownik musi mieć aktywną firmę | `BankAccountService.cs › BankAccountService.AddUserFirmBankAccount` | `GetUserFirmIdAsync(userId)` zwraca `null` | `UserHasNoAssociatedFirmException` | `400` | `"User has no associated firm."` |

### Endpoint `PUT /api/BankAccount/EditUserFirmBankAccount`

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-02` | Konto o danym `Id` musi istnieć w bazie | `BankAccountService.cs › BankAccountService.EditUserFirmBankAccount` | `GetByIdAsync(bankAccountDto.Id)` zwraca `null` | `Exception` (generyczny) | `500` ⚠️ | `"Bank account not found."` |

> WAL-02: generyczny `Exception` trafia do catch-all → `500`. Powinien być dedykowany `BankAccountNotFoundException` zwracający `400` lub `404`. [UWAGA — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Endpoint `PUT /api/BankAccount/DeleteUserFirmBankAccounts`

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-03` | Każde konto z tablicy musi istnieć w bazie | `BankAccountService.cs › BankAccountService.DeleteUserFirmBankAccounts` | `GetByIdAsync(bankAccountId)` zwraca `null` (per iteracja) | `Exception` (generyczny) | `500` ⚠️ | `"Bank account not found."` |
| `WAL-04` | Konto nie może być powiązane z dokumentem (`Document`) | `BankAccountService.cs › BankAccountService.DeleteUserFirmBankAccounts` | `Documents.Query().AnyAsync(d => d.BankAccountId == bankAccountId)` zwraca `true` | `BankAccountAssociatedWithDocumentsException` | `400` | `"Can't delete. Bank account is associated with documents."` |

> WAL-03: generyczny `Exception` trafia do catch-all → `500`. [UWAGA — WYMAGA WERYFIKACJI Z ZESPOŁEM]
> WAL-04: sprawdzenie jest po WAL-03 (kolejność z kodu). Konto musi najpierw istnieć, żeby sprawdzić powiązania.

---

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| `UserHasNoAssociatedFirmException` | **tak** | `400 Bad Request` | `ExceptionMiddleware.cs` (catch blok) |
| `BankAccountAssociatedWithDocumentsException` | **tak** | `400 Bad Request` | `ExceptionMiddleware.cs` (catch blok) |
| `Exception` (generyczny — WAL-02, WAL-03) | **nie** ⚠️ | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all `Exception`) |

Pełen rejestr: `../../KATALOG_WYJATKOW.md`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze | `[Authorize(Roles = "User")]` na klasie `BankAccountController` |
| Wymagana rola | `"User"` |
| Źródło tożsamości użytkownika | `IUserService.GetCurrentUserId()` — odczyt z JWT claim `userId` z `HttpContext` |
| Token | JWT (`JwtBearerDefaults.AuthenticationScheme`), czas ważności 10 minut |

Wszystkie 4 endpointy wymagają autoryzacji. Brak tokenu → `401 Unauthorized`; błędna rola → `403 Forbidden` (obsługa przez ASP.NET Core framework, nie `ExceptionMiddleware`).

---

## 4. Uwagi bezpieczeństwa

- [UWAGA: Generyczny `Exception("Bank account not found.")` (WAL-02 EditUserFirmBankAccount, WAL-03 DeleteUserFirmBankAccounts) zwraca `500` zamiast `400`/`404`. Brak jawnego mapowania w `ExceptionMiddleware`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `EditUserFirmBankAccount` i `DeleteUserFirmBankAccounts` nie weryfikują, czy konto o danym `Id` należy do aktywnej firmy bieżącego użytkownika. `GetByIdAsync(id)` zwraca każde konto z DB — użytkownik znający `Id` mógłby edytować lub usunąć konto innego użytkownika. Brak kontroli własności zasobu (ownership check). — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `DeleteUserFirmBankAccounts` używa `PUT` zamiast `DELETE` — niezgodność z konwencją REST. Kotwica: `BankAccountController.cs › BankAccountController.DeleteUserFirmBankAccounts` — `[HttpPut("DeleteUserFirmBankAccounts")]`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Relacja `Document → BankAccount` ma `OnDelete(DeleteBehavior.Cascade)` w snapshosie. Oznacza to, że usunięcie konta na poziomie DB pociągnie usunięcie dokumentów. Serwis blokuje to przez WAL-04, ale kaskada istnieje jako zabezpieczenie DB. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Brak własnego `try/catch` w kontrolerze — wszystkie wyjątki trafiają do `ExceptionMiddleware`.
