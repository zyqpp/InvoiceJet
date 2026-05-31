# produkty — Katalog produktów i usług

Ekran i modal zarządzania katalogiem produktów i usług firmy. Produkty wykorzystywane są jako pozycje w dokumentach (faktury, proformy, storna). CRUD odbywa się przez dialog Angular Material. Chroniony przez AuthGuard.

## Drzewo zawartości

```
produkty/
├── README.md                        ← Ten plik
├── ekran.md                         ← ProductsComponent — lista produktów
└── dialog_dodaj_produkt/
    └── modal.md                     ← AddOrEditProductDialogComponent — dodaj/edytuj produkt
```

## Kluczowe dokumenty

- `ekran.md` — lista produktów: tabela, CRUD, wywołania API
- `dialog_dodaj_produkt/modal.md` — modal formularza produktu; uwaga: anomalia globalnego indeksu UNIQUE na nazwie produktu

## Powiązane katalogi

- `../dashboard/` — ekran startowy (sidebar: Produkty)
- `../faktury/dodaj_edytuj_fakture/` — produkty wybierane w tabeli pozycji dokumentu

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
