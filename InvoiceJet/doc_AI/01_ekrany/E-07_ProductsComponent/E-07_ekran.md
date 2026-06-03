# E-07 ProductsComponent — Lista produktów

| Pole | Wartość |
|---|---|
| ID dokumentu | E-07 |
| Typ dokumentu | ekran |
| Wersja | 1.0 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 |
| Data ostatniej modyfikacji | 2026-06-02 |

## Streszczenie

Ekran zarządzania katalogiem produktów i usług firmy użytkownika. Prezentuje tabelę z sortowaniem, paginacją i filtrowaniem po stronie klienta. Operacje dodawania i edycji realizowane przez dialog Angular Material (`AddOrEditProductDialogComponent`). Usunięcie zaznaczonych produktów wywołuje API batch. Produkty używane są jako pozycje w formularzach dokumentów (faktura, proforma, storno). Wszystkie dane izolowane per UserFirm. Chroniony przez `AuthGuard` (rola: User).

---

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

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/products` |
| Wymagana rola | User (AuthGuard JWT) |
| Punkty wejścia | Klik „Produkty" w Sidebar |
| Komponent Angular | [`ProductsComponent`](../../../../InvoiceJetUI/src/app/components/products/products.component.ts) |
| Szablon HTML | [`products.component.html`](../../../../InvoiceJetUI/src/app/components/products/products.component.html) |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek | Uprawnienie |
|---|---|---|---|
| Modal AddOrEditProductDialog (dodaj) | [OP-E07-01](E-07_OP-01.md) | zawsze | User |
| Modal AddOrEditProductDialog (edytuj) | [OP-E07-02](E-07_OP-02.md) | zawsze | User |

---

## Filtry

| ID | Nazwa w UI | Typ | Dokument |
|---|---|---|---|
| FILTR-E07-01 | Filtr wyszukiwania | input (MatTableDataSource filter, po stronie klienta) | [E-07_FILTR-01.md](E-07_FILTR-01.md) |

## Tabele i listy

| ID | Nazwa | Dokument |
|---|---|---|
| TAB-E07-01 | Lista produktów | [E-07_TAB-01.md](E-07_TAB-01.md) |

### Kolumny tabeli

| Kolumna | Źródło danych | Opis |
|---|---|---|
| Checkbox | `selection` | Zaznaczanie do operacji batch |
| `name` | `IProduct.name` | Nazwa produktu/usługi |
| `price` | `IProduct.price` | Cena jednostkowa |
| `unitOfMeasurement` | `IProduct.measureUnit` | Jednostka miary |
| `tvaValue` | `IProduct.vatRate` | Stawka VAT (%) |
| `containsTva` | `IProduct.containsTva` | Czy cena zawiera VAT |

## Operacje

| ID | Etykieta UI | Dokument |
|---|---|---|
| OP-E07-01 | Dodaj produkt | [E-07_OP-01.md](E-07_OP-01.md) |
| OP-E07-02 | Edytuj (przy wierszu) | [E-07_OP-02.md](E-07_OP-02.md) |
| OP-E07-03 | Usuń zaznaczone | [E-07_OP-03.md](E-07_OP-03.md) |

## Modale

| ID | Nazwa | Wywołane przez |
|---|---|---|
| MODAL-E07-01 | AddOrEditProductDialog (dodaj) | OP-E07-01 |
| MODAL-E07-02 | AddOrEditProductDialog (edytuj) | OP-E07-02 |

## Scenariusze testowe

→ [E-07_TC.md](E-07_TC.md) — prereq JWT, prereq DB, selektory CSS, 4 scenariusze e2e

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint |
|---|---|---|
| Załadowanie listy (ngOnInit) | GET | `/api/Product/GetAll` |
| Usunięcie zaznaczonych | PUT | `/api/Product/Delete` (query string IDs) |

---

## Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| OP-E07-01 | [ALG-10 Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Produkt tworzony w kontekście UserFirm zalogowanego użytkownika |
| OP-E07-02 | [ALG-10 Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Edycja możliwa wyłącznie dla produktów należących do UserFirm aktualnie zalogowanego użytkownika |
| OP-E07-03 | [ALG-10 Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Usunięcie batch działa tylko na produktach należących do UserFirm aktualnie zalogowanego użytkownika |
| FILTR-E07-01 | — (filtr kliencki MatTable) | Filtrowanie po stronie klienta — brak algorytmu backendowego |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`products.component.ts`](../../../../InvoiceJetUI/src/app/components/products/products.component.ts) |
| Szablon HTML | [`products.component.html`](../../../../InvoiceJetUI/src/app/components/products/products.component.html) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| PA-01 | Brak komunikatów sukcesu/błędu po operacjach CRUD |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
