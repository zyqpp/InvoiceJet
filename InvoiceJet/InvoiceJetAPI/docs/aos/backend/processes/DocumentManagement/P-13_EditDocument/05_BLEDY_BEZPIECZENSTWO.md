# EditDocument — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

### Endpoint `PUT /api/Document/EditDocument`

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | Użytkownik musi mieć aktywną firmę | `DocumentService.cs › DocumentService.EditDocument` | `GetUserFirmIdAsync(userId)` zwraca `null` | `UserHasNoAssociatedFirmException` | `400` | `"User has no associated firm."` |
| `WAL-02` | Dokument o podanym `Id` musi istnieć w DB | `DocumentService.cs › DocumentService.EditDocument` | `GetByIdAsync(dto.Id)` zwraca `null` | `Exception` (generyczny) | `500` ⚠️ | `"Document not found."` |
| `WAL-03` | Istniejące produkty (`Id > 0`) muszą istnieć wg `Name+UserFirmId` | `DocumentService.cs › DocumentService.UpdateDocumentProducts` | `FirstOrDefaultAsync(Name+UserFirmId)` zwraca `null` | `Exception` (generyczny) | `500` ⚠️ | `"Product not found."` |

---

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| `UserHasNoAssociatedFirmException` | tak | `400 Bad Request` | `ExceptionMiddleware.cs` |
| `Exception("Document not found.")` | **nie** ⚠️ | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all) |
| `Exception("Product not found.")` | **nie** ⚠️ | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all) |

> Pełen rejestr: `../../KATALOG_WYJATKOW.md`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze | `[Authorize(Roles = "User")]` na klasie `DocumentController` |
| Wymagana rola | `"User"` |
| Źródło tożsamości | `IUserService.GetCurrentUserId()` — JWT claim `userId` |
| Token | JWT, ważność 10 minut |

---

## 4. Uwagi bezpieczeństwa

- [UWAGA: `GetByIdAsync(documentRequestDto.Id)` nie sprawdza, czy dokument należy do aktywnej firmy użytkownika. Możliwa edycja dokumentu innego użytkownika znając `Id`. Kotwica: `DocumentService.cs › DocumentService.EditDocument`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: WAL-02 i WAL-03 zwracają `500` zamiast `404`/`400`. Brak dedykowanych wyjątków. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Produkt wyszukiwany po `Name + UserFirmId` — nie po `Id`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
