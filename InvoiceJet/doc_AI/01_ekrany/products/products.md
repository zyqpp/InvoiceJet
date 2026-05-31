# Ekran: Produkty (Products)

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-07 |
| Trasa | `/dashboard/products` |
| Komponent | `ProductsComponent` |
| Plik | `src/app/components/products/products.component.ts` |
| AuthGuard | TAK |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Katalog produktów/usług firmy. Sortowanie, paginacja, filtrowanie, CRUD przez dialogi.

## Kolumny tabeli

`select`, `name`, `price`, `unitOfMeasurement`, `tvaValue`, `containsTva`

## Dialogi

| Dialog | Cel |
|---|---|
| `AddOrEditProductDialogComponent` | Dodanie / edycja produktu |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie (ngOnInit) | `GET /api/Product/GetAllProductsForUserId` |
| Usunięcie zaznaczonych | `PUT /api/Product/DeleteProducts?productIds=...` (query string) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
