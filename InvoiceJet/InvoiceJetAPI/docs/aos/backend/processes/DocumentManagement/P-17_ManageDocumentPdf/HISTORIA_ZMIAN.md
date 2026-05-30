# ManageDocumentPdf — Historia zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| `1.0` | 2026-05-30 | Agent AI | Utworzono kompletną dokumentację procesu P-17 (8 plików): kontrakt API-28 i API-29, WAL-01A/WAL-01B/WAL-02B, dane/modele, bezpieczeństwo (kontrolerowy try/catch omijający middleware, połknięty błąd PDF, błędne konto bankowe, null-forgiving), scenariusze testowe, przegląd z 2 diagramami mermaid, metadane. |

## Notatki do katalogów przekrojowych

- `KATALOG_API.md` — **wymaga dodania** `API-28` i `API-29`.
- `KATALOG_WYJATKOW.md` — `UserHasNoAssociatedFirmException` już zarejestrowany w P-12; uwaga: w API-28 jest obsługiwany przez kontrolerowy try/catch (nie middleware).
- `KATALOG_DANYCH_TESTOWYCH.md` — brak nowych fixture'ów; używane `DT-01`, `DT-03`, `DT-05`, `DT-07`, `DT-08`.
