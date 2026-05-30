# Katalog wyjątków — InvoiceJetAPI

Rejestr wszystkich wyjątków domenowych i generycznych rzucanych przez serwisy aplikacyjne,
wraz z ich mapowaniem na kody HTTP w `ExceptionMiddleware` oraz **dokładnymi komunikatami**
widocznymi użytkownikowi w portalu.

Format odpowiedzi błędu (zawsze): `{ "message": "<treść poniżej>" }` — `Content-Type: application/json`

Kotwica middleware: `ExceptionMiddleware.cs › ExceptionMiddleware.Invoke`

---

## 1. Wyjątki mapowane jawnie → właściwy kod HTTP ✅

| Klasa wyjątku | HTTP | Komunikat wyświetlany użytkownikowi | Rzucany w | Procesy |
|---|---|---|---|---|
| `AnafFirmNotFoundException` | `404` | `Firm with CUI {cui} not found in ANAF database.` | `FirmService.GetFirmDataFromAnaf` | P-04 |
| `UserAlreadyExistsException` | `400` | `User with email {email} already exists.` | `AuthService.RegisterUser` | P-01 |
| `PasswordMismatchException` | `400` | `Password confirmation doesn't match.` | `AuthService.RegisterUser` | P-01 |
| `UserNotFoundException` | `400` | `User with email {email} not found.` | `AuthService.LoginUser` | P-02 |
| `IncorrectPasswordException` | `400` | `Password is incorrect.` | `AuthService.LoginUser` | P-02 |
| `UserHasNoAssociatedFirmException` | `400` | `User has no associated firm. Add a firm in Firm Details page.` | `DocumentSeriesService`, `ProductService`, `BankAccountService`, `DocumentService` | P-09, P-10, P-11, P-12, P-13, P-17 |
| `NoBankAccountAddedException` | `400` | `Please add a bank account, before generating a document.` | `DocumentService.AddDocument` | P-12 |
| `ProductAssociatedWithInvoiceException` | `400` | `Can't delete. Product {productName} is associated with an invoice.` | `ProductService.DeleteProducts` | P-09 |
| `BankAccountAssociatedWithDocumentsException` | `400` | `Can't delete. Bank account is associated with documents.` | `BankAccountService.DeleteUserFirmBankAccounts` | P-10 |

> `{email}`, `{cui}`, `{productName}` — wartości dynamiczne wstawiane przez kod w momencie rzucania wyjątku.

### Kolejność bloków catch w middleware (istotna)

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

## 2. Wyjątki niemapowane → catch-all → 500 ⚠️

Klasy domenowe istniejące w `Domain/Exceptions/`, rzucane przez serwisy,
ale **bez dedykowanego bloku catch** w `ExceptionMiddleware` → trafiają do catch-all → `500`.

| Klasa wyjątku | Komunikat wyświetlany użytkownikowi | Oczekiwany HTTP | Rzucany w | Procesy |
|---|---|---|---|---|
| `FirmAssociatedWithDocumentException` | `Can't delete. Firm {firmName} is associated with a document.` | `400` | `FirmService.DeleteFirms` | P-08 |
| `InvalidPasswordException` | `Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.` | `400` | `AuthService.RegisterUser` | P-01 |
| `ProductWithSameNameExistsException` | `Product with name {productName} already exists.` | `400` | `ProductService.AddProduct` | P-09 |

> ⚠️ Wszystkie trzy klasy istnieją w `InvoiceJet.Domain/Exceptions/`, są rzucane przez serwisy,
> ale brakuje ich w `ExceptionMiddleware`. Użytkownik widzi `500` zamiast czytelnego `400`.
> Naprawa: dodać trzy bloki `catch` do middleware.

---

## 3. Wyjątki generyczne (`new Exception`) → catch-all → 500 ⚠️

Serwisy rzucające `new Exception(...)` zamiast dedykowanej klasy domenowej.
Brak możliwości odróżnienia od nieoczekiwanych błędów systemowych.

| Komunikat wyświetlany użytkownikowi | Oczekiwany HTTP | Rzucany w | Procesy |
|---|---|---|---|
| `Firm not found.` | `404` | `FirmService.EditFirm` | P-05 |
| `User firm not found.` | `400` | `DocumentService.TransformToStorno` | P-19 |
| `Document not found.` | `404` | `DocumentService.TransformToStorno` | P-19 |

> ⚠️ Naprawa: stworzyć klasy domenowe (`FirmNotFoundException`, itd.)
> i dodać bloki `catch` do `ExceptionMiddleware`.

---

## 4. Pokrycie procesów

| Proces | Wyjątki | Status |
|---|---|---|
| P-01 RegisterUser | `UserAlreadyExistsException` ✅, `PasswordMismatchException` ✅, `InvalidPasswordException` ❌→500 | ⚠️ częściowe |
| P-02 LoginUser | `UserNotFoundException` ✅, `IncorrectPasswordException` ✅ | ✅ |
| P-03 AddFirm | brak wyjątków domenowych — błędy jako `DbUpdateException` | ⚠️ →500 |
| P-04 GetFirmFromAnaf | `AnafFirmNotFoundException` ✅ | ✅ |
| P-05 EditFirm | `new Exception("Firm not found.")` ❌→500 | ❌ |
| P-06 GetUserActiveFirm | brak | — |
| P-07 GetUserClientFirms | brak | — |
| P-08 ManageClientFirms | `FirmAssociatedWithDocumentException` ❌→500 | ❌ |
| P-09 ManageProducts | `UserHasNoAssociatedFirmException` ✅, `ProductAssociatedWithInvoiceException` ✅, `ProductWithSameNameExistsException` ❌→500 | ⚠️ częściowe |
| P-10 ManageBankAccounts | `UserHasNoAssociatedFirmException` ✅, `BankAccountAssociatedWithDocumentsException` ✅ | ✅ |
| P-11 ManageDocumentSeries | `UserHasNoAssociatedFirmException` ✅ | ✅ |
| P-12 AddDocument | `UserHasNoAssociatedFirmException` ✅, `NoBankAccountAddedException` ✅ | ✅ |
| P-13 EditDocument | `UserHasNoAssociatedFirmException` ✅ | ✅ |
| P-14 GetDocuments | brak | — |
| P-15 DeleteDocuments | brak | — |
| P-16 GetDocumentAutofillInfo | brak | — |
| P-17 ManageDocumentPdf | `UserHasNoAssociatedFirmException` ✅ | ✅ |
| P-18 GetDashboardStats | brak | — |
| P-19 TransformToStorno | `new Exception("User firm not found.")` ❌→500, `new Exception("Document not found.")` ❌→500 | ❌ |

---

## 5. Podsumowanie anomalii do naprawy

| # | Problem | Naprawa |
|---|---|---|
| 1 | `FirmAssociatedWithDocumentException` — brak w middleware → 500 | Dodać `catch` w `ExceptionMiddleware` |
| 2 | `InvalidPasswordException` — brak w middleware → 500 | Dodać `catch` w `ExceptionMiddleware` |
| 3 | `ProductWithSameNameExistsException` — brak w middleware → 500 | Dodać `catch` w `ExceptionMiddleware` |
| 4 | `new Exception("Firm not found.")` w P-05 | Stworzyć `FirmNotFoundException`, dodać `catch` |
| 5 | `new Exception("User firm not found.")` w P-19 | Użyć istniejącej `UserHasNoAssociatedFirmException` |
| 6 | `new Exception("Document not found.")` w P-19 | Stworzyć `DocumentNotFoundException`, dodać `catch` |

---

## Metadane katalogu

| Atrybut | Wartość |
|---|---|
| Źródło | `ExceptionMiddleware.cs › ExceptionMiddleware.Invoke`, `Domain/Exceptions/*.cs` |
| Wyjątki mapowane jawnie | 9 |
| Wyjątki domenowe niemapowane (→ 500) | 3 |
| Wyjątki generyczne niemapowane (→ 500) | 3 |
| Anomalii do naprawy | 6 |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
