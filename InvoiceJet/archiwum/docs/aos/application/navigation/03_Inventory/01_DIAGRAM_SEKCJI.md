# Inventory - Diagram sekcji

## 1. Diagram

```mermaid
flowchart TD
  Inventory["Menu: Inventory"]
  Inventory --> Clients["Clients"]
  Inventory --> Products["Products"]
  Clients --> ClientDialog["Dialog add/edit client"]
  Products --> ProductDialog["Dialog add/edit product"]
```

## 2. Linki

| Pozycja | Route | Dokument pozycji |
|---|---|---|
| Clients | `/dashboard/clients` | [Clients](./Clients/01_MAPA_MAKIET_POZYCJI.md) |
| Products | `/dashboard/products` | [Products](./Products/01_MAPA_MAKIET_POZYCJI.md) |
