# Zarządzanie seriami dokumentów — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Pobranie listy serii | Użytkownik ma aktywną firmę. | `200 OK` i lista `DocumentSeriesDto`. |
| TC-02 | Dodanie serii | Poprawny `DocumentSeriesDto` z `DocumentType.Id`. | `200 OK`, nowa seria zapisana. |
| TC-03 | Aktualizacja serii | Seria o `Id` istnieje. | `200 OK`, dane serii zaktualizowane. |
| TC-04 | Usunięcie serii | `Id` istnieje w bazie. | `200 OK`, seria usunięta. |

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Dodanie bez aktywnej firmy | `Users.GetUserFirmIdAsync(...)` zwraca `null`. | `400 Bad Request`, komunikat z `UserHasNoAssociatedFirmException`. |
| TC-N02 | Aktualizacja nieistniejącej serii | Brak serii dla `Id`. | `500 Internal Server Error`, komunikat `Document Series not found`. |
