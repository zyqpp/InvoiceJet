# ManageProducts — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

Walidacje pogrupowane per endpoint. Kolejność odpowiada kolejności sprawdzania w kodzie.

### Endpoint `GET /api/Product/GetAllProductsForUserId`

Brak walidacji wejściowych. Endpoint read-only — pusta kolekcja jest poprawnym wynikiem.

### Endpoint `POST /api/Product/AddProduct`

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | Użytkownik musi mieć aktywną firmę | `ProductService.cs › ProductService.AddProduct` | `GetUserFirmIdAsync(userId)` zwraca `null` | `UserHasNoAssociatedFirmException` | `400` | `"User has no associated firm."` |
| `WAL-02` | Nazwa produktu musi być unikalna w aktywnej firmie użytkownika | `ProductService.cs › ProductService.AddProduct` | `FindUserFirmProductByName(userId, productDto.Name)` zwraca != `null` | `ProductWithSameNameExistsException` | `500` ⚠️ | `"Product with name {name} already exists."` |

> WAL-02: wyjątek `ProductWithSameNameExistsException` **nie jest jawnie mapowany** w `ExceptionMiddleware` → trafia do catch-all → `500 Internal Server Error`. Powinien zwracać `400 Bad Request`. [UWAGA — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Endpoint `PUT /api/Product/EditProduct`

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-03` | Produkt o danym `Id` musi istnieć w bazie | `ProductService.cs › ProductService.EditProduct` | `GetByIdAsync(productDto.Id)` zwraca `null` | `Exception` (generyczny) | `500` ⚠️ | `"Product not found."` |

> WAL-03: generyczny `Exception` trafia do catch-all → `500`. Powinien być dedykowany `ProductNotFoundException` zwracający `400` lub `404`. [UWAGA — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Endpoint `PUT /api/Product/DeleteProducts`

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-04` | Każdy produkt z tablicy musi istnieć w bazie | `ProductService.cs › ProductService.DeleteProducts` | `GetByIdAsync(productId)` zwraca `null` (per iteracja) | `Exception` (generyczny) | `500` ⚠️ | `"Product not found."` |
| `WAL-05` | Produkt nie może być powiązany z fakturą (`DocumentProduct`) | `ProductService.cs › ProductService.DeleteProducts` | `DocumentProducts.Query().AnyAsync(dp => dp.ProductId == productId)` zwraca `true` | `ProductAssociatedWithInvoiceException` | `400` | `"Can't delete. Product {name} is associated with an invoice."` |

> WAL-04: generyczny `Exception` trafia do catch-all → `500`. [UWAGA — WYMAGA WERYFIKACJI Z ZESPOŁEM]
> WAL-05: sprawdzenie jest po WAL-04 (kolejność z kodu). Produkt musi najpierw istnieć, żeby sprawdzić powiązania.

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| `UserHasNoAssociatedFirmException` | **tak** | `400 Bad Request` | `ExceptionMiddleware.cs` (catch blok) |
| `ProductAssociatedWithInvoiceException` | **tak** | `400 Bad Request` | `ExceptionMiddleware.cs` (catch blok) |
| `ProductWithSameNameExistsException` | **nie** ⚠️ | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all `Exception`) |
| `Exception` (generyczny — WAL-03, WAL-04) | **nie** ⚠️ | `500 Internal Server Error` | `ExceptionMiddleware.cs` (catch-all `Exception`) |

Pełen rejestr: `../../KATALOG_WYJATKOW.md`.

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze | `[Authorize(Roles = "User")]` na klasie `ProductController` |
| Wymagana rola | `"User"` |
| Źródło tożsamości użytkownika | `IUserService.GetCurrentUserId()` — odczyt z JWT claim `userId` z `HttpContext` |
| Token | JWT (`JwtBearerDefaults.AuthenticationScheme`), czas ważności 10 minut |

Wszystkie 4 endpointy wymagają autoryzacji. Brak tokenu → `401 Unauthorized`; błędna rola → `403 Forbidden` (obsługa przez ASP.NET Core framework, nie `ExceptionMiddleware`).

## 4. Uwagi bezpieczeństwa

- [UWAGA: `ProductWithSameNameExistsException` (WAL-02) zwraca `500` zamiast `400`. Brak jawnego mapowania w `ExceptionMiddleware` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Generyczny `Exception("Product not found.")` (WAL-03, WAL-04) zwraca `500` zamiast `400`/`404`. Zamiast komunikatu domenowego klient otrzymuje błąd serwera — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: `EditProduct` nie sprawdza, czy zmieniona nazwa produktu jest unikalna — możliwy duplikat lub naruszenie globalnego indeksu DB → `DbUpdateException` → `500` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- Brak własnego `try/catch` w kontrolerze — wszystkie wyjątki trafiają do `ExceptionMiddleware`.
- `DeleteProducts` używa `PUT` zamiast `DELETE` — niezgodność z konwencją REST. Nie wpływa na bezpieczeństwo, ale może mylić klientów API.
