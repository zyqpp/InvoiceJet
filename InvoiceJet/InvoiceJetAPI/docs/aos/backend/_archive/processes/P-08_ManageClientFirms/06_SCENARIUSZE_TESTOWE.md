# Zarządzanie firmami-klientami — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Pobranie listy klientów | Użytkownik ma firmy-klientów. | `200 OK`, lista `FirmDto` zawiera rekordy. |
| TC-02 | Pobranie pustej listy | Użytkownik nie ma klientów. | `200 OK`, pusta lista. |
| TC-03 | Usunięcie klienta bez dokumentów | Klient nie występuje w `Document.ClientId`. | `200 OK`, rekord firmy usunięty. |

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Usunięcie klienta powiązanego z dokumentem | Istnieje `Document` z `ClientId = firmId`. | `500 Internal Server Error`, komunikat z `FirmAssociatedWithDocumentException`. |
| TC-N02 | Usunięcie nieistniejącego klienta | `firmId` nie istnieje. | `500 Internal Server Error`, komunikat `Product not found.` |
