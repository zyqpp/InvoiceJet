# Edycja dokumentu — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Edycja istniejącego dokumentu | Dokument istnieje i użytkownik ma aktywną firmę. | `200 OK`, pola dokumentu i pozycje zaktualizowane. |
| TC-02 | Aktualizacja statusu i typu | DTO zawiera `DocumentStatus.Id` i `DocumentType.Id`. | `200 OK`, pola `DocumentStatusId` i `DocumentTypeId` zmienione. |

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Brak aktywnej firmy | `Users.GetUserFirmIdAsync(...)` zwraca `null`. | `400 Bad Request`, komunikat z `UserHasNoAssociatedFirmException`. |
| TC-N02 | Nieistniejący dokument | Brak rekordu `Document` dla `Id`. | `500 Internal Server Error`, komunikat `Document not found.` |
| TC-N03 | Pozycja wskazuje brakujący produkt | Pozycja z `id > 0`, brak produktu o podanej nazwie. | `500 Internal Server Error`, komunikat `Product not found.` |
