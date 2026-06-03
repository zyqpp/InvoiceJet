# Zarządzanie produktami — Kontrakt API

## Endpointy

| Operacja | HTTP | Ścieżka | Wejście | Wyjście |
|---|---|---|---|---|
| Pobranie listy | `GET` | `/api/Product/GetAllProductsForUserId` | Brak | `ICollection<ProductDto>` |
| Dodanie | `POST` | `/api/Product/AddProduct` | `ProductDto` | `ProductDto` |
| Edycja | `PUT` | `/api/Product/EditProduct` | `ProductDto` | `ProductDto` |
| Usuwanie | `PUT` | `/api/Product/DeleteProducts` | `int[] productIds` | `200 OK` |

---

## Uwagi kontraktowe

- `DeleteProducts(int[] productIds)` nie ma atrybutu `[FromBody]`. [UWAGA: źródło bindowania tablicy `productIds` wymaga potwierdzenia testem endpointu — WYMAGA WERYFIKACJI Z ZESPOŁEM]
