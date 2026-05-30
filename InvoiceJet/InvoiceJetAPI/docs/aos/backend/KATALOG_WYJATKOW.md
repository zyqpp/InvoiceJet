# Katalog wyjątków — InvoiceJetAPI

Rejestr wszystkich wyjątków domenowych i generycznych rzucanych przez serwisy aplikacyjne,
wraz z ich mapowaniem na kody HTTP w `ExceptionMiddleware`.

Kotwica middleware: `ExceptionMiddleware.cs › ExceptionMiddleware.Invoke`

---

## 1. Wyjątki mapowane jawnie (ExceptionMiddleware)

Wyjątki przechwycone przez dedykowane bloki `catch` przed catch-all.
Odpowiedź: `{ "message": "<exception.Message>" }` z odpowiednim kodem HTTP.

| Klasa wyjątku | HTTP | Metoda HTTP | Rzucany w | Używany w procesach |
|---|---|---|---|---|
| `AnafFirmNotFoundException` | `404 Not Found` | `HandleExceptionAsync` | `FirmService.GetFirmDataFromAnaf` | P-04 |
| `UserAlreadyExistsException` | `400 Bad Request` | `HandleExceptionAsync` | `AuthService.RegisterUser` | P-01 |
| `PasswordMismatchException` | `400 Bad Request` | `HandleExceptionAsync` | `AuthService.RegisterUser` | P-01 |
| `UserNotFoundException` | `400 Bad Request` | `HandleExceptionAsync` | `AuthService.LoginUser` | P-02 |
| `IncorrectPasswordException` | `400 Bad Request` | `HandleExceptionAsync` | `AuthService.LoginUser` | P-02 |
| `UserHasNoAssociatedFirmException` | `400 Bad Request` | `HandleExceptionAsync` | `DocumentSeriesService`, `ProductService`, `BankAccountService`, `DocumentService` | P-09, P-10, P-11, P-12, P-13, P-17 |
| `NoBankAccountAddedException` | `400 Bad Request` | `HandleExceptionAsync` | `DocumentService.AddDocument` | P-12 |
| `ProductAssociatedWithInvoiceException` | `400 Bad Request` | `HandleExceptionAsync` | `ProductService.DeleteProducts` | P-09 |
| `BankAccountAssociatedWithDocumentsException` | `400 Bad Request` | `HandleExceptionAsync` | `BankAccountService.DeleteUserFirmBankAccounts` | P-10 |

### Kolejność catch w middleware (istotna — bardziej szczegółowe bloki muszą być pierwsze)

```
AnafFirmNotFoundException          → 404
BankAccountAssociatedWithDocumentsException → 400
UserHasNoAssociatedFirmException   → 400
ProductAssociatedWithInvoiceException → 400
NoBankAccountAddedException        → 400
UserNotFoundException              → 400
IncorrectPasswordException         → 400
UserAlreadyExistsException         → 400
PasswordMismatchException          → 400
Exception (catch-all)              → 500
```

---

## 2. Wyjątki niemapowane — trafiają do catch-all → 500 ⚠️

Poniższe wyjątki (`new Exception(...)` lub brakujące w middleware klasy domenowe)
**nie są przechwycone** przez żaden dedykowany blok `catch` i trafiają do catch-all,
zwracając `500 Internal Server Error` zamiast odpowiedniego kodu semantycznego.

| Komunikat / Klasa | Rzucany w | Oczekiwany kod | Bieżący kod | Proces |
|---|---|---|---|---|
| `new Exception("Firm not found.")` | `FirmService.EditFirm` | `404 Not Found` | **500** ⚠️ | P-05 |
| `new Exception("User firm not found.")` | `DocumentService.TransformToStorno` | `400 Bad Request` | **500** ⚠️ | P-19 |
| `new Exception("Document not found.")` | `DocumentService.TransformToStorno` | `404 Not Found` | **500** ⚠️ | P-19 |

> Wszystkie trzy przypadki używają `new Exception(...)` zamiast dedykowanej klasy domenowej.
> Poprawna obsługa wymagałaby: (1) stworzenia klas domenowych w `Domain/Exceptions/`,
> (2) dodania bloków `catch` w `ExceptionMiddleware`.
> Kotwice: `FirmService.cs › FirmService.EditFirm`,
> `DocumentService.cs › DocumentService.TransformToStorno`.

---

## 3. Wyjątki wymagające weryfikacji ⚠️

Wyjątki wzmiankowane w dokumentacji procesów, których status w kodzie wymaga potwierdzenia.

| Klasa wyjątku | Wzmianka w | Status w ExceptionMiddleware | Uwaga |
|---|---|---|---|
| `InvalidPasswordException` | P-01 `00_METADANE.md` | **brak** | Nie pojawia się w ExceptionMiddleware; middleware zawiera `IncorrectPasswordException` (P-02). Możliwa pomyłka w dokumentacji P-01 lub wyjątek istnieje ale nie jest obsługiwany — **wymaga weryfikacji z zespołem** |
| `FirmAssociatedWithDocumentException` | P-08 `00_METADANE.md` | **brak** | Wzmiankowany jako WAL-02 w P-08; jeśli klasa istnieje w `Domain/Exceptions/` ale nie ma bloku `catch` → trafia do 500; jeśli klasa nie istnieje → dokumentacja P-08 jest błędna — **wymaga weryfikacji z zespołem** |

---

## 4. Format odpowiedzi błędu

Wszystkie błędy (jawnie mapowane i catch-all) zwracają jednolity format JSON:

```json
{
  "message": "<treść exception.Message>"
}
```

`Content-Type: application/json`

Kotwica: `ExceptionMiddleware.cs › ExceptionMiddleware.HandleExceptionAsync`

---

## 5. Pokrycie procesów

| Proces | Wyjątki domenowe | Status mapowania |
|---|---|---|
| P-01 RegisterUser | `UserAlreadyExistsException`, `PasswordMismatchException` | ✅ zmapowane → 400 |
| P-02 LoginUser | `UserNotFoundException`, `IncorrectPasswordException` | ✅ zmapowane → 400 |
| P-03 AddFirm | brak — błędy jako `DbUpdateException` | ⚠️ → 500 catch-all |
| P-04 GetFirmFromAnaf | `AnafFirmNotFoundException` | ✅ zmapowany → 404 |
| P-05 EditFirm | `new Exception("Firm not found.")` | ❌ niemapowany → 500 |
| P-06 GetUserActiveFirm | brak | — |
| P-07 GetUserClientFirms | brak | — |
| P-08 ManageClientFirms | `Exception` (WAL-01), `FirmAssociatedWithDocumentException` (WAL-02) | ❌ wymaga weryfikacji |
| P-09 ManageProducts | `UserHasNoAssociatedFirmException`, `ProductWithSameNameExistsException`, `ProductAssociatedWithInvoiceException` | ✅ częściowo (`ProductWithSameNameExistsException` — zweryfikować) |
| P-10 ManageBankAccounts | `UserHasNoAssociatedFirmException`, `BankAccountAssociatedWithDocumentsException` | ✅ zmapowane → 400 |
| P-11 ManageDocumentSeries | `UserHasNoAssociatedFirmException` | ✅ zmapowany → 400 |
| P-12 AddDocument | `UserHasNoAssociatedFirmException`, `NoBankAccountAddedException` | ✅ zmapowane → 400 |
| P-13 EditDocument | `UserHasNoAssociatedFirmException` | ✅ zmapowany → 400 |
| P-14 GetDocuments | brak | — |
| P-15 DeleteDocuments | brak | — |
| P-16 GetDocumentAutofillInfo | brak | — |
| P-17 ManageDocumentPdf | `UserHasNoAssociatedFirmException` | ✅ zmapowany → 400 |
| P-18 GetDashboardStats | brak | — |
| P-19 TransformToStorno | `new Exception("User firm not found.")`, `new Exception("Document not found.")` | ❌ niemapowane → 500 |

---

## Metadane katalogu

| Atrybut | Wartość |
|---|---|
| Źródło | `ExceptionMiddleware.cs › ExceptionMiddleware.Invoke` |
| Wyjątki mapowane jawnie | 9 |
| Wyjątki niemapowane (→ 500) | 3 |
| Wyjątki do weryfikacji | 2 |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
