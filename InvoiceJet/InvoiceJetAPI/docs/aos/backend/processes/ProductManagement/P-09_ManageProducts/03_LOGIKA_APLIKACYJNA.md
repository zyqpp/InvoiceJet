# ManageProducts — Logika aplikacyjna

Proces `P-09` obsługuje cztery endpointy CRUD dla zasobu `Product`. Każdy ma osobną sekcję.

---

## Endpoint A — `GET /api/Product/GetAllProductsForUserId`

### 0. Algorytm w skrócie

1. Kontroler odbiera GET bez parametrów, wywołuje `_productService.GetUserFirmProducts()`.
2. Serwis pobiera `userId` z JWT, wywołuje `ProductRepository.GetUserFirmProductsAsync(userId)`.
3. Repozytorium zwraca produkty należące do aktywnej firmy użytkownika.
4. Jeśli lista pusta → zwrot pustej kolekcji (bez wyjątku).
5. AutoMapper mapuje `List<Product>` → `ICollection<ProductDto>`.
6. Kontroler zwraca `200 OK` z kolekcją DTO.

### 1. Wejście do procesu

Kotwica: `ProductController.cs › ProductController.GetAllProductsForUserId`

```csharp
[HttpGet("GetAllProductsForUserId")]
public async Task<ActionResult<ICollection<ProductDto>>> GetAllProductsForUserId()
{
    var productsDto = await _productService.GetUserFirmProducts();
    return Ok(productsDto);
}
```

Brak parametrów — `userId` pobrierany z tokenu JWT w serwisie przez `IUserService.GetCurrentUserId()`.

### 2. Walidacje (faza wejściowa)

> Wymiar nie występuje w tym endpoincie. Endpoint jest read-only. Brak walidacji wejściowych — jeśli użytkownik nie ma firmy lub produktów, zwracana jest pusta kolekcja.

### 3. Logika biznesowa

Kotwica: `ProductService.cs › ProductService.GetUserFirmProducts`

```csharp
public async Task<ICollection<ProductDto>> GetUserFirmProducts()
{
    var products = await _unitOfWork.Products.GetUserFirmProductsAsync(_userService.GetCurrentUserId());
    if (products.Count == 0)
    {
        return new List<ProductDto>();
    }

    var productDtos = _mapper.Map<ICollection<ProductDto>>(products);
    return productDtos;
}
```

**Krok 1:** Pobranie `userId` z JWT — `_userService.GetCurrentUserId()`.

**Krok 2:** Wywołanie `ProductRepository.GetUserFirmProductsAsync(userId)`. Repozytorium wykonuje zapytanie LINQ filtrujące produkty aktywnej firmy:

Kotwica: `ProductRepository.cs › ProductRepository.GetUserFirmProductsAsync`

```csharp
return await _dbSet
    .Where(p => p.UserFirm!.UserId == userId
             && p.UserFirm.User.ActiveUserFirmId == p.UserFirmId)
    .ToListAsync();
```

**Krok 3:** Jeśli `Count == 0` → zwrot `new List<ProductDto>()` (pusta kolekcja, nie `null`).

**Krok 4:** Mapowanie `AutoMapper.Map<ICollection<ProductDto>>(products)`.

### 4. Zapisy do bazy i transakcje

> Wymiar nie dotyczy. Endpoint jest read-only — brak zapisów, brak `CompleteAsync()`.

### 5. Odpowiedź

HTTP `200 OK`. Ciało: `ICollection<ProductDto>` — tablica DTO lub `[]` gdy brak produktów.

---

## Endpoint B — `POST /api/Product/AddProduct`

### 0. Algorytm w skrócie

1. Kontroler odbiera `ProductDto` z body, wywołuje `_productService.AddProduct(product)`.
2. Serwis pobiera `userId`, wywołuje `GetUserFirmIdAsync` → brak firmy → `UserHasNoAssociatedFirmException` (WAL-01).
3. Serwis sprawdza duplikat nazwy w aktywnej firmie → duplikat → `ProductWithSameNameExistsException` (WAL-02).
4. AutoMapper mapuje `ProductDto` → `Product`, serwis ustawia `product.UserFirmId`.
5. `Products.AddAsync(product)` + `CompleteAsync()`.
6. AutoMapper mapuje `Product` → `ProductDto` (z nadanym `Id` przez DB).
7. Kontroler zwraca `200 OK` z `ProductDto`.

### 1. Wejście do procesu

Kotwica: `ProductController.cs › ProductController.AddProduct`

```csharp
[HttpPost("AddProduct")]
public async Task<ActionResult<ProductDto>> AddProduct(ProductDto product)
{
    var productDto = await _productService.AddProduct(product);
    return Ok(productDto);
}
```

Parametr `ProductDto product` — bindowany z body żądania. Brak jawnego atrybutu `[FromBody]`, ale `[ApiController]` wymusza automatyczny binding z body dla złożonych typów.

### 2. Walidacje (faza wejściowa)

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Użytkownik ma aktywną firmę (`userFirmId != null`) | `ProductService.cs › ProductService.AddProduct` | `UserHasNoAssociatedFirmException` (WAL-01 → 400) |
| 2 | Brak produktu o tej nazwie w aktywnej firmie | `ProductService.cs › ProductService.AddProduct` | `ProductWithSameNameExistsException` (WAL-02 → **500**) |

**WAL-01:**

```csharp
var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
if (!userFirmId.HasValue)
{
    throw new UserHasNoAssociatedFirmException();
}
```

**WAL-02:**

```csharp
var productWithSameName = await _unitOfWork.Products.FindUserFirmProductByName(
    _userService.GetCurrentUserId(), productDto.Name);
if (productWithSameName != null)
{
    throw new ProductWithSameNameExistsException(productDto.Name);
}
```

### 3. Logika biznesowa

Kotwica: `ProductService.cs › ProductService.AddProduct`

```csharp
var product = _mapper.Map<Product>(productDto);
product.UserFirmId = userFirmId.Value;
```

**Krok 1:** `AutoMapper.Map<Product>(productDto)` — mapowanie DTO na nową encję (bez `UserFirmId`, bo pola nie ma w DTO).

**Krok 2:** `product.UserFirmId = userFirmId.Value` — ręczne przypisanie relacji do aktywnej firmy użytkownika.

### Tabela: pole encji `Product` → źródło (AddProduct)

| Pole encji `Product` | Źródło |
|---|---|
| `Id` | generowany przez DB (IDENTITY) po `CompleteAsync()` |
| `Name` | `productDto.Name` |
| `Price` | `productDto.Price` |
| `ContainsTva` | `productDto.ContainsTva` |
| `TvaValue` | `productDto.TvaValue` |
| `UnitOfMeasurement` | `productDto.UnitOfMeasurement` |
| `UserFirmId` | `userFirmId.Value` — wynik `Users.GetUserFirmIdAsync(userId)` |

### 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | `CompleteAsync()` |
|---|---|---|---|
| 1 | `AddAsync(product)` | `ProductRepository` (dziedziczone z `GenericRepository`) | nie |
| 2 | `CompleteAsync()` | `UnitOfWork.CompleteAsync()` | tak — nadaje `product.Id` |

> Jedna para `AddAsync` + `CompleteAsync()` — brak ryzyka częściowego zapisu. Brak jawnej transakcji, ale EF Core automatycznie owija `SaveChangesAsync()` transakcją DB.

### 5. Odpowiedź

Kotwica: `ProductService.cs › ProductService.AddProduct`

```csharp
return _mapper.Map<ProductDto>(product);
```

HTTP `200 OK`. Ciało: `ProductDto` z wypełnionym `Id` (nadanym przez DB). Wszystkie pola odpowiadają zapisanemu produktowi.

### 6. Uwagi techniczne

- [UWAGA: `ProductWithSameNameExistsException` (WAL-02) nie jest jawnie mapowany w `ExceptionMiddleware` → trafia do catch-all → `500 Internal Server Error` zamiast `400 Bad Request`. Powinien być dodany do middleware. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Indeks unikalny na `Product.Name` jest globalny (wszystkie firmy). Walidacja w serwisie sprawdza unikalność tylko w aktywnej firmie. W sytuacji gdy dwie firmy mają produkt o tej samej nazwie, DB zgłosi `DbUpdateException` (naruszenie indeksu) — nie obsługiwany jawnie → `500`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## Endpoint C — `PUT /api/Product/EditProduct`

### 0. Algorytm w skrócie

1. Kontroler odbiera `ProductDto` z body (musi zawierać `Id`), wywołuje `_productService.EditProduct(product)`.
2. Serwis pobiera encję z DB po `productDto.Id` → brak → `Exception("Product not found.")` (WAL-03 → 500).
3. AutoMapper mapuje `productDto` na istniejącą encję (EF tracking).
4. `CompleteAsync()` — zapis zmian.
5. AutoMapper mapuje zaktualizowaną encję → `ProductDto`.
6. Kontroler zwraca `200 OK` z zaktualizowanym DTO.

### 1. Wejście do procesu

Kotwica: `ProductController.cs › ProductController.EditProduct`

```csharp
[HttpPut("EditProduct")]
public async Task<ActionResult<ProductDto>> EditProduct(ProductDto product)
{
    var productDto = await _productService.EditProduct(product);
    return Ok(productDto);
}
```

### 2. Walidacje (faza wejściowa)

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Produkt o danym `Id` istnieje w DB | `ProductService.cs › ProductService.EditProduct` | `Exception("Product not found.")` (WAL-03 → **500**) |

```csharp
var product = await _unitOfWork.Products.GetByIdAsync(productDto.Id) ??
              throw new Exception("Product not found.");
```

### 3. Logika biznesowa

Kotwica: `ProductService.cs › ProductService.EditProduct`

```csharp
_mapper.Map(productDto, product);
```

`AutoMapper.Map(productDto, product)` — mapuje pola `ProductDto` na istniejącą tracked encję `product`. EF Core wykryje zmianę i zaplanuje `UPDATE`.

### Tabela: pole encji `Product` → źródło (EditProduct)

| Pole encji `Product` | Źródło |
|---|---|
| `Id` | bez zmian (tracked przez EF Core) |
| `Name` | `productDto.Name` |
| `Price` | `productDto.Price` |
| `ContainsTva` | `productDto.ContainsTva` |
| `TvaValue` | `productDto.TvaValue` |
| `UnitOfMeasurement` | `productDto.UnitOfMeasurement` |
| `UserFirmId` | bez zmian (pole nie istnieje w `ProductDto` — nie mapowane) |

### 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | `CompleteAsync()` |
|---|---|---|---|
| 1 | `CompleteAsync()` | `UnitOfWork.CompleteAsync()` | tak — zapisuje UPDATE encji tracked przez EF |

> Brak jawnej transakcji. Pojedynczy `CompleteAsync()` — pełna atomowość zapisu.

### 5. Odpowiedź

```csharp
return _mapper.Map<ProductDto>(product);
```

HTTP `200 OK`. Ciało: `ProductDto` odzwierciedlający stan encji po zapisie.

### 6. Uwagi techniczne

- [UWAGA: `EditProduct` nie sprawdza, czy nowa nazwa produktu jest unikalna w aktywnej firmie użytkownika. Możliwy zduplikowany `Name` po edycji (obejście walidacji WAL-02 z `AddProduct`). Globalny indeks unikalny w DB może też odrzucić zapis przez `DbUpdateException` → 500. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Wyjątek `Exception("Product not found.")` (WAL-03) trafia do catch-all → `500` zamiast `400`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## Endpoint D — `PUT /api/Product/DeleteProducts`

### 0. Algorytm w skrócie

1. Kontroler odbiera `int[] productIds` z query string, wywołuje `_productService.DeleteProducts(productIds)`.
2. Serwis iteruje po `productIds`:
   a. Pobiera produkt po ID → brak → `Exception("Product not found.")` (WAL-04 → 500).
   b. Sprawdza powiązanie z `DocumentProduct` → istnieje → `ProductAssociatedWithInvoiceException` (WAL-05 → 400).
   c. Oznacza produkt do usunięcia: `RemoveAsync(product)`.
3. Po pętli: `CompleteAsync()` — usuwa wszystkie oznaczone produkty.
4. Kontroler zwraca `200 OK` (puste ciało).

### 1. Wejście do procesu

Kotwica: `ProductController.cs › ProductController.DeleteProducts`

```csharp
[HttpPut("DeleteProducts")]
public async Task<ActionResult<ProductDto>> DeleteProducts(int[] productIds)
{
    await _productService.DeleteProducts(productIds);
    return Ok();
}
```

Parametr `int[] productIds` — bindowany z query string (np. `?productIds=1&productIds=2`).

### 2. Walidacje (faza wejściowa — per iteracja)

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Produkt o danym ID istnieje | `ProductService.cs › ProductService.DeleteProducts` | `Exception("Product not found.")` (WAL-04 → **500**) |
| 2 | Produkt nie jest powiązany z fakturą | `ProductService.cs › ProductService.DeleteProducts` | `ProductAssociatedWithInvoiceException` (WAL-05 → 400) |

**WAL-04:**

```csharp
var product = await _unitOfWork.Products.GetByIdAsync(productId) ??
                  throw new Exception("Product not found.");
```

**WAL-05:**

```csharp
bool isAssociatedWithDocumentProduct = await _unitOfWork.DocumentProducts.Query()
    .AnyAsync(dp => dp.ProductId == productId);

if (isAssociatedWithDocumentProduct)
{
    throw new ProductAssociatedWithInvoiceException(product.Name);
}
```

### 3. Logika biznesowa

Kotwica: `ProductService.cs › ProductService.DeleteProducts`

```csharp
await _unitOfWork.Products.RemoveAsync(product);
```

Każdy produkt przechodzący walidacje jest oznaczany do usunięcia (`RemoveAsync`). EF Core zbiera zmiany w change tracker — rzeczywisty `DELETE` następuje przy `CompleteAsync()`.

### Tabela: pole encji → źródło

> Wymiar nie dotyczy — encje są usuwane, nie tworzone ani modyfikowane.

### 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | `CompleteAsync()` |
|---|---|---|---|
| 1..N | `RemoveAsync(product)` (w pętli) | `ProductRepository` (GenericRepository) | nie — tylko oznaczenie |
| N+1 | `CompleteAsync()` | `UnitOfWork.CompleteAsync()` | tak — wszystkie DELETE naraz |

> Brak jawnej transakcji (`BeginTransactionAsync` nie używany). EF Core automatycznie owija `SaveChangesAsync()` transakcją SQL Server — jeśli którykolwiek `DELETE` się nie powiedzie, cały batch jest wycofywany (EF atomicity). Ryzyko: wyjątek rzucony podczas iteracji przed `CompleteAsync()` przerwie pętlę, ale EF change tracker jest niezatwierdzony — brak częściowego zapisu.

### 5. Odpowiedź

HTTP `200 OK`. Puste ciało.

### 6. Uwagi techniczne

- [UWAGA: Wyjątek `Exception("Product not found.")` (WAL-04) trafia do catch-all → `500` zamiast `400`. Powinien być dedykowany `ProductNotFoundException`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Brak jawnej transakcji. Jeśli `CompleteAsync()` się nie powiedzie (np. timeout sieciowy po iteracji), EF Core change tracker jest niespójny — ale baza nie zostanie zmieniona (niezatwierdzony tracking). Ryzyko jest niskie, ale warto rozważyć `BeginTransactionAsync` przy dużych tablicach. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
