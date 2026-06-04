# TransformToStorno — Historia zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| `1.0` | 2026-05-30 | Agent AI | Utworzono kompletną dokumentację procesu P-19 (8 plików): kontrakt API-31, WAL-01 i WAL-02 (oba → 500 przez new Exception), dane/modele, bezpieczeństwo (ownership check ✅, non-atomic loop, 500 zamiast 400/404), scenariusze testowe (TC-01–TC-03, TC-N01–TC-N03, TC-B01–TC-B05), przegląd z diagramem mermaid, metadane. |

## Notatki do katalogów przekrojowych

- `KATALOG_API.md` — **wymaga dodania** `API-31`.
- `KATALOG_WYJATKOW.md` — `Exception("User firm not found.")` i `Exception("Document not found.")` nie są mapowane jawnie → **500** catch-all. Wymaga odnotowania jako anomalia.
- `KATALOG_DANYCH_TESTOWYCH.md` — brak nowych fixture'ów; używane `DT-01`, `DT-03`, `DT-07`, `DT-08`.
