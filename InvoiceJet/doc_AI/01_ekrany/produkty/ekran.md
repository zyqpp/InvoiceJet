# ProductsComponent — Lista produktów

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-Produkty |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran zarządzania katalogiem produktów i usług firmy użytkownika. Prezentuje tabelę z sortowaniem, paginacją i filtrowaniem. Operacje dodawania i edycji realizowane przez dialog Angular Material (`AddOrEditProductDialogComponent`). Usunięcie zaznaczonych produktów wywołuje API batch. Produkty używane są jako pozycje w formularzach dokumentów. Chroniony przez AuthGuard (rola: User).

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────────────┐
│ Produkty                                 [+ Dodaj produkt]   │
├──┬─────────────┬────────┬──────────────┬──────────┬──────────┤
│☐ │ Nazwa       │ Cena   │ J.m.         │ VAT %    │ Zawiera  │
│  │             │        │              │          │ VAT      │
├──┼─────────────┼────────┼──────────────┼──────────┼──────────┤
│☐ │ ...         │ ...    │ ...          │ ...      │ ...      │
├──┴─────────────┴────────┴──────────────┴──────────┴──────────┤
│ [Usuń zaznaczone]                          [Paginacja]        │
└──────────────────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/products` |
| Wymagana rola/uprawnienie | User (AuthGuard) |
| Punkty wejścia | Klik „Produkty" w Sidebar |
| Powiązany kod komponentu | `src/app/components/products/products.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| Modal AddOrEditProductDialog | Klik „Dodaj produkt" | Zawsze | User |
| Modal AddOrEditProductDialog (edycja) | Klik „Edytuj" przy wierszu | Zawsze | User |

## Sekcje ekranu

### Filtry

| ID filtru | Nazwa w UI | Typ | Link do dokumentu |
|---|---|---|---|
| FILTR-Produkty-Szukaj | Filtr wyszukiwania | input (MatTableDataSource filter) | — |

### Tabele i listy

| ID tabeli | Nazwa | Link do dokumentu |
|---|---|---|
| TAB-Produkty-ListaProduktow | Lista produktów | — |

### Kolumny tabeli

| Kolumna | Źródło danych | Opis |
|---|---|---|
| Checkbox (select) | `selection` | Zaznaczanie do operacji batch |
| `name` | `IProduct.name` | Nazwa produktu/usługi |
| `price` | `IProduct.price` | Cena jednostkowa |
| `unitOfMeasurement` | `IProduct.measureUnit` | Jednostka miary |
| `tvaValue` | `IProduct.vatRate` | Stawka VAT (%) |
| `containsTva` | `IProduct.containsTva` | Czy cena zawiera VAT |

### Pola

Brak (ekran listowy).

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-Produkty-DodajProdukt | Dodaj produkt | — |
| OP-Produkty-EdytujProdukt | Edytuj (przy wierszu) | — |
| OP-Produkty-UsunZaznaczone | Usuń zaznaczone | — |

### Modale

| ID modalu | Nazwa | Wywołane przez | Link do dokumentu |
|---|---|---|---|
| MODAL-Produkty-DodajProdukt | AddOrEditProductDialog (dodaj) | OP-Produkty-DodajProdukt | `dialog_dodaj_produkt/modal.md` |
| MODAL-Produkty-EdytujProdukt | AddOrEditProductDialog (edytuj) | OP-Produkty-EdytujProdukt | `dialog_dodaj_produkt/modal.md` |

### Powiadomienia

Brak.

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie (ngOnInit) | [GET /api/Product/GetAll](../../../04_api_i_integracje/01_api_frontend/product/GET_Product_GetAll.md) |
| Usunięcie zaznaczonych | [PUT /api/Product/Delete](../../../04_api_i_integracje/01_api_frontend/product/PUT_Product_Delete.md) (query string) |

## Powiązania

- Powiązane procesy: [pobierz_produkty](../../../02_procesy/produkty/pobierz_produkty/proces.md), [usun_produkty](../../../02_procesy/produkty/usun_produkty/proces.md)
- Powiązane API: [GET /api/Product/GetAll](../../../04_api_i_integracje/01_api_frontend/product/GET_Product_GetAll.md)
- Powiązane UC: Brak

## Powiązania z kodem

- Komponent: `src/app/components/products/products.component.ts`
- Szablon HTML: `src/app/components/products/products.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `products/products.md`. |
