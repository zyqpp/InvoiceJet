# ManageDocumentSeries — Historia zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| `1.0` | 2026-05-30 | Agent AI | Utworzono kompletną dokumentację procesu P-11 (8 plików): kontrakt API-18–API-21, logika aplikacyjna 4 endpointów, dane/modele/mapowania, błędy/bezpieczeństwo, scenariusze testowe TC-01–TC-05 + TC-N01–TC-N02 + TC-B01–TC-B07, przegląd z diagramami mermaid, metadane. Zidentyfikowano 9 anomalii architektonicznych oznaczonych `[UWAGA: ... — WYMAGA WERYFIKACJI Z ZESPOŁEM]`. |

## Notatki do katalogów przekrojowych

- `KATALOG_DANYCH_TESTOWYCH.md` — **wymaga dodania** fixture'u `DT-06` (istniejąca seria dokumentów `"2026-TEST"` do edycji/usunięcia; precondition: `DT-03`). Definicja skrótowa w `06_SCENARIUSZE_TESTOWE.md § Definicja fixture'u DT-06`.
- `KATALOG_API.md` — **wymaga dodania** endpointów `API-18` (GET GetAllDocumentSeriesForUserId), `API-19` (POST AddDocumentSeries), `API-20` (PUT UpdateDocumentSeries), `API-21` (PUT DeleteDocumentSeries).
- `KATALOG_WYJATKOW.md` — wyjątek `UserHasNoAssociatedFirmException` już zarejestrowany (P-09, P-10). Brak nowych wyjątków do rejestracji — generyczny `Exception("Document Series not found")` w WAL-02 nie ma dedykowanego typu.
