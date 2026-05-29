# Zarządzanie produktami — Przegląd procesu

## Cel

Proces obsługuje listowanie produktów aktywnej firmy użytkownika oraz operacje dodania, edycji i usunięcia produktów.

---

## Diagram

```mermaid
flowchart TD
  A["GET produkty"] --> B["ProductService.GetUserFirmProducts()"]
  C["POST produkt"] --> D["ProductService.AddProduct()"]
  E["PUT produkt"] --> F["ProductService.EditProduct()"]
  G["PUT usuwanie"] --> H["ProductService.DeleteProducts()"]
```

---

## Wynik procesu

| Operacja | Wynik sukcesu |
|---|---|
| Pobranie listy | `200 OK` i `ICollection<ProductDto>` |
| Dodanie | `200 OK` i `ProductDto` |
| Edycja | `200 OK` i `ProductDto` |
| Usunięcie | `200 OK` |
