# dedykowane — Algorytmy dedykowane

Algorytmy specyficzne dla domeny biznesowej InvoiceJet, nieprzypadające do kategorii ogólnych — generowanie numerów, integracje zewnętrzne, transformacje, obsługa błędów i izolacja danych.

## Drzewo zawartości

```
dedykowane/
├── README.md
├── generowanie_numeru_dokumentu.md  ← SeriesName + CurrentNumber.D4 (race condition!)
├── integracja_anaf.md               ← POST do ANAF API po CUI (rumuński US)
├── transformacja_na_storno.md       ← masowa zmiana DocumentTypeId=3 (bug atomowości)
├── pipeline_obslugi_wyjatkow.md     ← ExceptionMiddleware → mapa wyjątek → HTTP
├── izolacja_danych_userfirm.md      ← UserFirm-based data isolation pattern
└── seed_typow_dokumentow.md         ← DbSeeder.SeedDocumentTypes() przy starcie
```

## Kluczowe dokumenty

- [`generowanie_numeru_dokumentu.md`](generowanie_numeru_dokumentu.md) — **race condition** przy równoległych żądaniach (brak blokady na `CurrentNumber`).
- [`transformacja_na_storno.md`](transformacja_na_storno.md) — **brak atomowości** (`CompleteAsync()` wewnątrz pętli).
- [`izolacja_danych_userfirm.md`](izolacja_danych_userfirm.md) — wzorzec izolacji danych; luka przy edycji zasobu bez weryfikacji właściciela.
- [`pipeline_obslugi_wyjatkow.md`](pipeline_obslugi_wyjatkow.md) — mapa wszystkich wyjątków domenowych → kody HTTP.

## Powiązane katalogi

- [`../../02_procesy/dokumenty/`](../../02_procesy/dokumenty/) — procesy dokumentów
- [`../../04_api_i_integracje/02_systemy_dziedzinowe/anaf/`](../../04_api_i_integracje/02_systemy_dziedzinowe/anaf/) — integracja ANAF

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
