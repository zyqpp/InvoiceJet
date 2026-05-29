# Generowanie dokumentu PDF — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Generowanie PDF dla poprawnego DTO | Aktywna firma użytkownika istnieje. | `200 OK`, plik PDF pojawia się w katalogu `Documents`. |

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Brak aktywnej firmy | `GetUserFirmAsync` zwraca `null`. | `400 Bad Request`, komunikat z wyjątku. |
| TC-N02 | Błąd wewnętrzny generatora | Generator zwraca `null` bez wyjątku. | `200 OK`, brak pliku lub niepełny plik. [WYMAGA WERYFIKACJI] |
