# AddOrEditProductDialogComponent — Dialog dodaj/edytuj produkt

| Pole | Wartość |
|---|---|
| ID dokumentu | MODAL-Produkty-DodajProdukt |
| Typ dokumentu | modal |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Modal Angular Material do dodawania i edycji produktu lub usługi w katalogu firmy. Otwierany z ekranu listy produktów przez `MatDialog.open()`. Dane produktu przekazywane przez `MAT_DIALOG_DATA`. Działa w trybie dodawania lub edycji. Uwaga: pole `name` ma globalny indeks UNIQUE w bazie danych (nie per użytkownik), co może powodować błędy 500 przy duplikatach między różnymi użytkownikami.

## Charakterystyka modalu

| Atrybut | Wartość |
|---|---|
| ID modalu | MODAL-Produkty-DodajProdukt |
| Nazwa / tytuł w UI | Dodaj produkt / Edytuj produkt |
| Wywołany przez operację | OP-Produkty-DodajProdukt, OP-Produkty-EdytujProdukt |
| Ekran nadrzędny | `../ekran.md` (ProductsComponent) |
| Typ modalu | formularz |
| Zamknięcie przez Escape | tak |
| Zamknięcie przez klik tła | tak |

## Wizualizacja układu

```
┌──────────────────────────────────────────┐
│ Dodaj produkt / Edytuj produkt       [X] │
├──────────────────────────────────────────┤
│ Nazwa:         [__________________________]│
│ Jednostka m.:  [__________________________]│
│ Cena:          [__________________________]│
│ Stawka VAT:    [19% ▼]                    │
├──────────────────────────────────────────┤
│ [Anuluj]                    [Zapisz]     │
└──────────────────────────────────────────┘
```

## Pola modalu

| ID pola | Nazwa w UI | Typ | Wymagalność | Link do dokumentu |
|---|---|---|---|---|
| POLE-DodajProdukt-name | Nazwa produktu | mat-form-field (input) | wymagane | — |
| POLE-DodajProdukt-measureUnit | Jednostka miary | mat-form-field (input) | wymagane | — |
| POLE-DodajProdukt-price | Cena jednostkowa | mat-form-field (input number) | wymagane | — |
| POLE-DodajProdukt-vatRate | Stawka VAT (%) | mat-form-field / mat-select | wymagane | — |

## Dane wejściowe (MAT_DIALOG_DATA)

| Pole | Typ | Opis |
|---|---|---|
| `product` | `IProduct \| null` | `null` = tryb dodawania; obiekt = tryb edycji |

## Operacje modalu

| Przycisk | Akcja | Wywołuje operację | Zamyka modal |
|---|---|---|---|
| Zapisz (tryb dodaj) | Wywołuje `POST /api/Product/Add` | Tak | tak (z wynikiem) |
| Zapisz (tryb edytuj) | Wywołuje `PUT /api/Product/Edit` | Tak | tak (z wynikiem) |
| Anuluj | Zamknięcie bez zmian | Nie | tak |

## Przepływ

### Tryb dodawania
1. Formularz pusty
2. Submit → `POST /api/Product/Add`
3. Dialog zamknięty z wynikiem → lista produktów odświeżona

### Tryb edycji
1. Formularz wypełniony danymi produktu
2. Submit → `PUT /api/Product/Edit`
3. Dialog zamknięty z wynikiem → lista produktów odświeżona

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Dodanie produktu | `POST /api/Product/Add` |
| Edycja produktu | `PUT /api/Product/Edit` |

## Możliwe wyniki

| Wynik | Warunki | Komunikat | Następna akcja |
|---|---|---|---|
| Sukces dodania | API zwróci 200/201 | Brak komunikatu | Modal zamknięty; lista produktów odświeżona |
| Sukces edycji | API zwróci 200 | Brak komunikatu | Modal zamknięty; lista produktów odświeżona |
| Błąd duplikatu nazwy | Constraint violation (500) | Brak komunikatu dla użytkownika (anomalia) | Modal może pozostać otwarty |
| Anulowanie | Użytkownik klika Anuluj lub Escape | Brak | Modal zamknięty, brak zmian |

## Powiązania z kodem

- Komponent modalu: `src/app/components/products/add-or-edit-product-dialog/add-or-edit-product-dialog.component.ts`
- Szablon HTML: `src/app/components/products/add-or-edit-product-dialog/add-or-edit-product-dialog.component.html`

## Wątpliwości i braki

- DP-01: `Product.Name` ma indeks UNIQUE w bazie danych — globalny, nie per UserFirm. Dwóch różnych użytkowników nie może mieć produktu o tej samej nazwie. Błąd objawi się jako 500 (constraint violation) bez czytelnego komunikatu dla użytkownika — wymaga naprawy (indeks powinien być UNIQUE per UserFirm lub per Firm).

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `products/add-or-edit-product-dialog.md`. |
