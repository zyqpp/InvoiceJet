# Dane autouzupełniania dokumentu — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Pobranie danych autouzupełniania | Użytkownik ma aktywną firmę i dane słownikowe. | `200 OK`, odpowiedź zawiera listy `Clients`, `DocumentSeries`, `DocumentStatuses`, `Products`. |
| TC-02 | Brak aktywnej firmy | `userFirmId` nie istnieje. | `200 OK`, pusty `DocumentAutofillDto`. |

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Brak tokenu | Żądanie bez autoryzacji. | `401 Unauthorized`. |
| TC-N02 | Brak roli | Token bez roli `User`. | `403 Forbidden`. |
