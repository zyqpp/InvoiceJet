# Zarządzanie produktami — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Zarządzanie produktami |
| Numer procesu | `P-09` |
| Kontroler | `ProductController` |
| Endpointy | `GET /api/Product/GetAllProductsForUserId`, `POST /api/Product/AddProduct`, `PUT /api/Product/EditProduct`, `PUT /api/Product/DeleteProducts` |
| Serwis aplikacyjny | `ProductService` |
| Metody serwisu | `GetUserFirmProducts()`, `AddProduct()`, `EditProduct()`, `DeleteProducts()` |
| DTO | `ProductDto` |
| Encje | `Product`, `DocumentProduct` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
