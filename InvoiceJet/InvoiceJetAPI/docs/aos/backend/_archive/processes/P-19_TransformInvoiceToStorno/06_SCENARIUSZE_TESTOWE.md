# Transformacja faktury do storna — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Transformacja pojedynczego dokumentu | Dokument należy do aktywnej firmy użytkownika. | `200 OK`, `DocumentTypeId` ustawione na `3`. |
| TC-02 | Transformacja wielu dokumentów | Wszystkie dokumenty z listy należą do aktywnej firmy. | `200 OK`, wszystkie rekordy mają typ `StornoInvoice`. |

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Brak aktywnej firmy | `GetUserFirmIdAsync` zwraca `null`. | `500 Internal Server Error`, komunikat `User firm not found.` |
| TC-N02 | Dokument nie należy do aktywnej firmy | Brak rekordu spełniającego filtr `Id + UserFirmId`. | `500 Internal Server Error`, komunikat `Document not found.` |
