# Wystawienie nowej faktury - Walidacje, błędy i bezpieczeństwo

## 1. Walidacje frontendowe

| Pole | Walidatory | Skutek |
|---|---|---|
| `client` | `Validators.required` | Brak klienta ustawia formularz w stanie `invalid`. |
| `issueDate` | `Validators.required` | Brak daty wystawienia ustawia formularz w stanie `invalid`. |
| `dueDate` | `dueDateValidator` | Data terminu podlega walidatorowi niestandardowemu. |
| `products[].name` | `Validators.required` | Brak nazwy produktu blokuje `onSubmit()`. |
| `products[].unitPrice` | `Validators.required`, `Validators.min(0)` | Cena mniejsza od `0` blokuje `onSubmit()`. |
| `products[].totalPrice` | `Validators.required`, `Validators.min(0)` | Wartość mniejsza od `0` blokuje `onSubmit()`. |
| `products[].quantity` | `Validators.required`, `Validators.min(1)` | Ilość mniejsza od `1` blokuje `onSubmit()`. |
| `products[].unitOfMeasurement` | `Validators.required` | Brak jednostki blokuje `onSubmit()`. |
| `products[].tvaValue` | `Validators.required`, `Validators.min(0)` | TVA mniejsze od `0` blokuje `onSubmit()`. |

## 2. Walidacje backendowe i wyjatki

| Warunek | Miejsce | Skutek |
|---|---|---|
| Brak aktywnej firmy użytkownika | `AddDocument()` | `UserHasNoAssociatedFirmException` |
| Brak aktywnego konta bankowego | `AddDocument()` | `NoBankAccountAddedException` |
| Produkt o `Id > 0` nie zostal znaleziony | `UpdateDocumentProducts()` | `Exception("Product not found.")` |
| Brak dokumentu w edycji | `EditDocument()` | `Exception("Document not found.")` |

## 3. Bezpieczeństwo

| Obszar | Mechanizm |
|---|---|
| Dostep do route | `AuthGuard` |
| Dostep do API | `[Authorize(Roles = "User")]` na `DocumentController` |
| Token | `AuthInterceptor` dodaje `Authorization: Bearer {token}` |
| Zakres danych | Backend pobiera `userFirmId` z aktualnego użytkownika. |

## 4. Uwagi

| Obszar | Uwaga |
|---|---|
| DTO | `DocumentRequestDto` nie zawiera atrybutow walidacyjnych. |
| Transakcja | `AddDocument()` wykonuje dwa wywołania `CompleteAsync()`: po zapisie `Document` i po zapisaniu pozycji oraz serii. |
| Komunikaty błędów UI | W `addDocument()` nie zdefiniowano lokalnej obslugi `error`. Obsluga zalezy od interceptorow. |
