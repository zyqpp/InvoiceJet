# ManageProducts — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Zarządzanie produktami aktywnej firmy` |
| Numer procesu | `P-09` |
| Kontroler(y) | `ProductController` |
| Serwis(y) aplikacyjny | `ProductService` |
| Metoda(y) serwisu | `ProductService.GetUserFirmProducts`, `ProductService.AddProduct`, `ProductService.EditProduct`, `ProductService.DeleteProducts` |
| DTO żądania | `ProductDto` (AddProduct, EditProduct) |
| DTO odpowiedzi | `ProductDto`, `ICollection<ProductDto>` |
| Encje | `Product`, `UserFirm`, `DocumentProduct` |
| Repozytoria | `IProductRepository` (`ProductRepository`), `IUserRepository` (`GetUserFirmIdAsync`), `IDocumentProductRepository` (`Query`) |
| Wyjątki | `UserHasNoAssociatedFirmException`, `ProductWithSameNameExistsException`, `ProductAssociatedWithInvoiceException` (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | brak |
| Autoryzacja | `[Authorize(Roles = "User")]` na klasie `ProductController` |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `POZA ZAKRESEM — ETAP FULLSTACK` |

---

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-10` | `GET /api/Product/GetAllProductsForUserId` | `ProductController.GetAllProductsForUserId` | Pobierz listę produktów aktywnej firmy użytkownika |
| `API-11` | `POST /api/Product/AddProduct` | `ProductController.AddProduct` | Dodaj nowy produkt do aktywnej firmy |
| `API-12` | `PUT /api/Product/EditProduct` | `ProductController.EditProduct` | Edytuj dane istniejącego produktu |
| `API-13` | `PUT /api/Product/DeleteProducts` | `ProductController.DeleteProducts` | Usuń jeden lub wiele produktów (batch) |

---

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler — GetAll | `ProductController.cs › ProductController.GetAllProductsForUserId` |
| Kontroler — Add | `ProductController.cs › ProductController.AddProduct` |
| Kontroler — Edit | `ProductController.cs › ProductController.EditProduct` |
| Kontroler — Delete | `ProductController.cs › ProductController.DeleteProducts` |
| Serwis — GetAll | `ProductService.cs › ProductService.GetUserFirmProducts` |
| Serwis — Add | `ProductService.cs › ProductService.AddProduct` |
| Serwis — Edit | `ProductService.cs › ProductService.EditProduct` |
| Serwis — Delete | `ProductService.cs › ProductService.DeleteProducts` |
| Repozytorium — GetAll produktów firmy | `ProductRepository.cs › ProductRepository.GetUserFirmProductsAsync` |
| Repozytorium — szukaj po nazwie | `ProductRepository.cs › ProductRepository.FindUserFirmProductByName` |
| Repozytorium — GetById | `GenericRepository.cs › GenericRepository.GetByIdAsync` |
| Repozytorium — Add | `GenericRepository.cs › GenericRepository.AddAsync` |
| Repozytorium — Remove | `GenericRepository.cs › GenericRepository.RemoveAsync` |
| Repozytorium — sprawdź powiązanie z dokumentem | `ProductService.cs › ProductService.DeleteProducts` — `_unitOfWork.DocumentProducts.Query().AnyAsync(...)` |
| Profil mapowania | `ProductProfile.cs › ProductProfile` — `CreateMap<Product, ProductDto>().ReverseMap()` |
| Middleware wyjątków | `ExceptionMiddleware.cs` — mapowanie `UserHasNoAssociatedFirmException` i `ProductAssociatedWithInvoiceException` |
| Tożsamość użytkownika | `UserService.cs › UserService.GetCurrentUserId` |
| Unit of Work | `UnitOfWork.cs › UnitOfWork.CompleteAsync` |
