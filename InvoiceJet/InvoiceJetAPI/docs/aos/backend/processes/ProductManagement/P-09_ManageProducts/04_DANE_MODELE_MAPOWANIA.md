# ManageProducts — Dane, modele i mapowania

## 1. DTO

### `ProductDto` (wejście: AddProduct, EditProduct; wyjście: GetAllProductsForUserId, AddProduct, EditProduct)

Źródło: `ProductDto.cs`

| Pole | Typ | Wymagane | Opis / źródło wartości |
|---|---|---|---|
| `Id` | `int` | tak (Edit/Delete), nie (Add) | Identyfikator produktu; przy Add wypełniany przez serwis po zapisie |
| `Name` | `string` | tak | Nazwa produktu; inicjalizator `string.Empty`; unikalność w aktywnej firmie walidowana w serwisie |
| `Price` | `decimal` | tak | Cena jednostkowa netto; atrybut `[Column(TypeName = "decimal(18,2)")]` |
| `ContainsTva` | `bool` | nie | Czy cena zawiera TVA; domyślnie `false` |
| `UnitOfMeasurement` | `string?` | nie | Jednostka miary; nullable — może być `null` lub pusty string |
| `TvaValue` | `int` | nie | Stawka TVA w procentach; domyślnie `19` w DTO |

> Atrybuty walidacyjne DTO: brak atrybutów z przestrzeni `System.ComponentModel.DataAnnotations` poza `[Column(TypeName = "decimal(18,2)")]` (adnotacja mapowania, nie walidacja). Cała walidacja biznesowa (unikalność nazwy, istnienie aktywnej firmy) realizowana jest w `ProductService`.

## 2. Encje i kolumny

### Encja `Product` → tabela `Product`

Kotwica: `Product.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("InvoiceJet.Domain.Models.Product", b => ...)`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `Id` | `int` | nie | PK | IDENTITY |
| `Name` | `nvarchar(450)` | nie | — | unikalny (`HasIndex(p => p.Name).IsUnique()`) |
| `Price` | `decimal(18,2)` | nie | — | — |
| `ContainsTva` | `bit` | nie | — | — |
| `TvaValue` | `int` | nie | — | — |
| `UnitOfMeasurement` | `nvarchar(max)` | tak | — | — |
| `UserFirmId` | `int` | tak | FK→`UserFirm` | tak |

Uwagi do schematu:
- `Name` ma typ `nvarchar(450)` (nie `nvarchar(max)`) — wymagany przez SQL Server dla kolumn z indeksem unikalnym.
- Indeks unikalny na `Name` jest **globalny** (nie per `UserFirmId`). Walidacja unikalności per firma (`FindUserFirmProductByName`) jest realizowana w serwisie na poziomie aplikacji, nie DB.
- `UserFirmId` jest nullable (`int?`) w encji i bazie — produkt może istnieć bez przypisania do firmy (choć serwis zawsze ustawia `UserFirmId` przy tworzeniu).

> [UWAGA: Indeks unikalny na `Product.Name` jest globalny — obejmuje wszystkie produkty we wszystkich firmach. Jeśli dwie firmy mają produkt o tej samej nazwie, baza zgłosi naruszenie unikalności. Walidacja w serwisie (`FindUserFirmProductByName`) chroni przed duplikatem tylko w obrębie aktywnej firmy użytkownika — ale baza może odrzucić zapis z powodu globalnego konfliktu. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

> Pełne definicje: `../../SLOWNIK_DANYCH.md#Product`.

### Encja `DocumentProduct` → tabela `DocumentProduct` (tylko do walidacji w DeleteProducts)

Kotwica: snapshot `Entity("InvoiceJet.Domain.Models.DocumentProduct", b => ...)`.

Kolumna istotna dla P-09: `ProductId` (`int?`, FK→`Product`).

Rola w procesie: sprawdzenie powiązania produktu z dokumentem przed usunięciem (`DeleteProducts` → WAL-05).

> Pełne definicje: `../../SLOWNIK_DANYCH.md#DocumentProduct`.

## 3. Relacje i kaskady

| Z encji | Pole FK | Do encji | Kierunek | Kaskada |
|---|---|---|---|---|
| `Product` | `UserFirmId` | `UserFirm` | N..1 | brak jawnej kaskady (UserFirmId nullable, `WithMany("Products")`) |
| `DocumentProduct` | `ProductId` | `Product` | N..1 | brak kaskady (nullable FK) |

Szczegół: usunięcie `Product` nie powoduje automatycznego usunięcia `DocumentProduct` — dlatego serwis explicitnie sprawdza powiązanie przed usunięciem (WAL-05).

## 4. Mapowania AutoMapper

Źródło: `ProductProfile.cs › ProductProfile`

```csharp
public class ProductProfile : Profile
{
    public ProductProfile()
    {
        CreateMap<Product, ProductDto>().ReverseMap();
    }
}
```

| Źródło | Cel | Profil | Uwagi |
|---|---|---|---|
| `Product` | `ProductDto` | `ProductProfile` | Wszystkie pola mapowane 1:1 po nazwach |
| `ProductDto` | `Product` | `ProductProfile` (`ReverseMap`) | `UserFirmId` **nie jest** w `ProductDto` — ustawiany ręcznie w serwisie po mapowaniu |

> Ważna uwaga do `AddProduct`: po `_mapper.Map<Product>(productDto)` serwis explicitnie ustawia `product.UserFirmId = userFirmId.Value`. Mapowanie `ReverseMap` nie przenosi `UserFirmId`, bo pole to nie istnieje w `ProductDto`. Kotwica: `ProductService.cs › ProductService.AddProduct`, linia 50.

> Ważna uwaga do `EditProduct`: `_mapper.Map(productDto, product)` mapuje pola DTO na istniejącą encję EF Core (tracking object). AutoMapper nadpisuje wszystkie pola DTO, w tym `Id` — ale `Id` w DTO ma tę samą wartość co encja, więc nie ma skutku ubocznego. `UserFirmId` pozostaje niezmieniony (brak pola w DTO). Kotwica: `ProductService.cs › ProductService.EditProduct`, linia 63.

## 5. Zapytania (LINQ/SQL)

### Query 1: Pobranie produktów aktywnej firmy użytkownika (`GetUserFirmProducts`)

Kotwica: `ProductRepository.cs › ProductRepository.GetUserFirmProductsAsync`

```csharp
return await _dbSet
    .Where(p => p.UserFirm!.UserId == userId
             && p.UserFirm.User.ActiveUserFirmId == p.UserFirmId)
    .ToListAsync();
```

Semantyka: pobiera produkty, gdzie:
- powiązana `UserFirm.UserId` = bieżący użytkownik
- `UserFirm.User.ActiveUserFirmId` = `product.UserFirmId` (produkt należy do aktywnej firmy, nie dowolnej firmy użytkownika)

### Query 2: Wyszukiwanie produktu po nazwie w aktywnej firmie (`AddProduct` — WAL-02)

Kotwica: `ProductRepository.cs › ProductRepository.FindUserFirmProductByName`

```csharp
return await _dbSet
    .Where(p => p.UserFirm!.UserId == userId
             && p.UserFirm.User.ActiveUserFirmId == p.UserFirmId)
    .FirstOrDefaultAsync(p => p.Name == name);
```

Semantyka: ta sama logika filtrowania co Query 1, ale z dodatkowym filtrem `Name == name`. Zwraca `null` jeśli nie znaleziono.

### Query 3: Sprawdzenie powiązania produktu z dokumentem (`DeleteProducts` — WAL-05)

Kotwica: `ProductService.cs › ProductService.DeleteProducts`

```csharp
bool isAssociatedWithDocumentProduct = await _unitOfWork.DocumentProducts.Query()
    .AnyAsync(dp => dp.ProductId == productId);
```

Semantyka: sprawdza czy istnieje choć jeden rekord `DocumentProduct` z danym `ProductId`. Jeśli tak — produkt nie może być usunięty.

## 6. Użyte enumy i lookupy

> Wymiar nie występuje w tym procesie. `Product` nie zawiera pól enum ani nie korzysta z tabel słownikowych.
