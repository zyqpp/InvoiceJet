# Dialog: Dodaj/Edytuj produkt (Add/Edit Product Dialog)

| Atrybut | Wartość |
|---|---|
| ID | DIALOG-03 |
| Komponent | `AddOrEditProductDialogComponent` |
| Plik | `src/app/components/products/add-or-edit-product-dialog/add-or-edit-product-dialog.component.ts` |
| Otwierany z | EKRAN-07 (lista produktów) |
| Typ | `MatDialog` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Modal Angular Material do dodawania i edycji produktu/usługi katalogowej. Dane produktu przekazywane przez `MAT_DIALOG_DATA`.

## Pola formularza

| Pole | Kontrolka | Walidacja | Opis |
|---|---|---|---|
| `name` | `mat-form-field` | required | Nazwa produktu (UNIQUE w bazie!) |
| `measureUnit` | `mat-form-field` | required | Jednostka miary (np. buc, kg, ore) |
| `price` | `mat-form-field` | required | Cena jednostkowa |
| `vatRate` | `mat-form-field` / `mat-select` | required | Stawka VAT (%) |

## Dane wejściowe (MAT_DIALOG_DATA)

| Pole | Typ | Opis |
|---|---|---|
| `product` | `IProduct \| null` | `null` = tryb dodawania; obiekt = tryb edycji |

## Przepływ

### Tryb dodawania
1. Formularz pusty
2. Submit → `POST /api/Product/Add`
3. Dialog zamknięty z wynikiem → lista odświeżona

### Tryb edycji
1. Formularz wypełniony danymi produktu
2. Submit → `PUT /api/Product/Edit`
3. Dialog zamknięty z wynikiem → lista odświeżona

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Dodanie produktu | `POST /api/Product/Add` |
| Edycja produktu | `PUT /api/Product/Edit` |

## Anomalie / ograniczenia

| # | Anomalia |
|---|---|
| DP-01 | `Product.Name` ma indeks UNIQUE w bazie — globalny, nie per UserFirm. Dwóch różnych użytkowników nie może mieć produktu o tej samej nazwie. Błąd objawi się jako 500 (constraint violation) bez komunikatu dla użytkownika |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
