# Usuwanie dokumentów — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Usunięcie jednego dokumentu | `documentIds` zawiera istniejące `Id`. | `200 OK`, dokument i jego pozycje usunięte. |
| TC-02 | Usunięcie wielu dokumentów | `documentIds` zawiera wiele istniejących `Id`. | `200 OK`, wszystkie wskazane dokumenty i pozycje usunięte. |

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Pusta lista identyfikatorów | `documentIds = []`. | `200 OK`, brak zmian w bazie. |
| TC-N02 | Brak tokenu | Żądanie bez autoryzacji. | `401 Unauthorized`. |
