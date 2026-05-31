# wyliczeniowe — Algorytmy wyliczeniowe

Algorytmy odpowiedzialne za obliczenia finansowe i matematyczne na danych biznesowych dokumentów.

## Drzewo zawartości

```
wyliczeniowe/
├── README.md
└── obliczanie_wartosci_dokumentu.md   ← TotalPrice = Σ(Price × Qty × (1 + VAT/100))
```

## Kluczowe dokumenty

- [`obliczanie_wartosci_dokumentu.md`](obliczanie_wartosci_dokumentu.md) — wzór obliczania sumy brutto dokumentu; implementacja backend (LINQ) i frontend (Angular reactive form).

## Powiązane katalogi

- [`../../02_procesy/dokumenty/dodaj_dokument/`](../../02_procesy/dokumenty/dodaj_dokument/) — proces dodawania dokumentu
- [`../../05_model_danych/01_db/dbo/`](../../05_model_danych/01_db/dbo/) — encje Document i DocumentProduct

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
