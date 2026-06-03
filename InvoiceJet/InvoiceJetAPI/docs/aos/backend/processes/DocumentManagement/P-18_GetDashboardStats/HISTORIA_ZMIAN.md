# GetDashboardStats — Historia zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| `1.0` | 2026-05-30 | Agent AI | Utworzono kompletną dokumentację procesu P-18 (8 plików): kontrakt API-30, brak WAL (cichy fallback przy braku firmy), dane/modele (DashboardStatsDto + MonthlyTotalDto), bezpieczeństwo (sekwencyjne zapytania, null! MonthlyTotals, UserId zamiast UserFirmId, null-forgiving DocumentType!), scenariusze testowe, przegląd z diagramem mermaid, metadane. |

## Notatki do katalogów przekrojowych

- `KATALOG_API.md` — **wymaga dodania** `API-30`.
- `KATALOG_WYJATKOW.md` — brak nowych wyjątków w P-18.
- `KATALOG_DANYCH_TESTOWYCH.md` — brak nowych fixture'ów; używane `DT-01`, `DT-03`, `DT-07`, `DT-08`.
