# Zarządzanie kontami bankowymi — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Pobranie listy kont | Użytkownik ma aktywną firmę. | `200 OK` i lista kont tej firmy. |
| TC-02 | Dodanie aktywnego konta | `isActive = true`. | `200 OK`, nowe konto zapisane, pozostałe konta firmy mają `isActive = false`. |
| TC-03 | Edycja aktywnego konta | Edytowane konto ustawione na `isActive = true`. | `200 OK`, pozostałe konta firmy dezaktywowane. |
| TC-04 | Usunięcie konta bez dokumentów | Konto nie jest użyte w dokumentach. | `200 OK`, konto usunięte. |

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Usunięcie konta użytego w dokumentach | Istnieje `Document` z `BankAccountId`. | `400 Bad Request`, komunikat z `BankAccountAssociatedWithDocumentsException`. |
| TC-N02 | Edycja nieistniejącego konta | Brak rekordu `BankAccount` dla `Id`. | `500 Internal Server Error`, komunikat `Bank account not found.` |
