# produkty

Procesy techniczne związane z zarządzaniem katalogiem produktów i usług firmy w systemie InvoiceJet.

## Drzewo zawartości

```
produkty/
├── README.md                    # ten plik
├── pobierz_produkty/
│   └── proces.md                # PROC-GetAllProducts — lista produktów firmy
├── dodaj_produkt/
│   └── proces.md                # PROC-AddProduct — dodanie nowego produktu
├── edytuj_produkt/
│   └── proces.md                # PROC-EditProduct — edycja danych produktu
└── usun_produkty/
    └── proces.md                # PROC-DeleteProducts — usunięcie produktów (wsadowe)
```

## Kluczowe dokumenty

- `dodaj_produkt/proces.md` — POST /api/Product/Add (uwaga: globalna unikalność nazwy — anomalia PD-01)
- `usun_produkty/proces.md` — PUT /api/Product/Delete (tablicowe usuwanie)

## Powiązane katalogi

- `../../04_api_i_integracje/01_api_frontend/product/` — dokumentacja endpointów API produktów
- `../../01_ekrany/produkty/` — ekran zarządzania produktami
- `../../05_model_danych/01_db/dbo/dbo.Product.md` — tabela Product (UNIQUE INDEX na Name)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — struktura podfolderów produkty (z P-06). |
