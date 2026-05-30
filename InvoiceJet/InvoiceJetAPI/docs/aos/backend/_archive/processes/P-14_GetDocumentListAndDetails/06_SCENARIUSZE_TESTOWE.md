# Lista i szczegóły dokumentów — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Lista dokumentów dla typu | Użytkownik ma aktywną firmę i dokumenty dla typu. | `200 OK`, lista `DocumentTableRecordDto`. |
| TC-02 | Pusta lista bez aktywnej firmy | Użytkownik nie ma aktywnej firmy. | `200 OK`, pusta lista. |
| TC-03 | Szczegóły dokumentu | Dokument o `documentId` istnieje. | `200 OK`, `DocumentRequestDto` z danymi dokumentu i pozycji. |

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Brak tokenu | Żądanie bez autoryzacji. | `401 Unauthorized`. |
| TC-N02 | Nieistniejący `documentId` | Brak dokumentu o podanym `Id`. | `200 OK` z `null` lub `500` w zależności od mapowania. [WYMAGA WERYFIKACJI] |
