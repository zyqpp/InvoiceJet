# AddDocument — Historia zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| `1.0` | 2026-05-30 | Agent AI | Utworzono kompletną dokumentację procesu P-12 (8 plików): kontrakt API-22, logika aplikacyjna (UpdateDocumentProducts + IncreaseDocumentSeriesNumber), dane/modele/mapowania, błędy/bezpieczeństwo WAL-01–WAL-03, scenariusze testowe TC-01–TC-02 + TC-N01–TC-N03 + TC-B01–TC-B05, przegląd z diagramem mermaid, metadane. Zidentyfikowano 7 anomalii architektonicznych. |

## Notatki do katalogów przekrojowych

- `KATALOG_DANYCH_TESTOWYCH.md` — **wymaga dodania** fixture'u `DT-07` (firma klienta `"Firma Klient SRL"` z `IsClient=true`; precondition: `DT-03`). Definicja skrótowa w `06_SCENARIUSZE_TESTOWE.md § Definicja fixture'u DT-07`.
- `KATALOG_API.md` — **wymaga dodania** endpointu `API-22` (POST AddDocument).
- `KATALOG_WYJATKOW.md` — `UserHasNoAssociatedFirmException` i `NoBankAccountAddedException` już zarejestrowane. Generyczny `Exception("Product not found.")` (WAL-03) — brak dedykowanego wyjątku, trafia do catch-all → 500.
