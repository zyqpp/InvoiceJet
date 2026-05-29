# Edycja firmy — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Aktualizacja istniejącej firmy | `firmDto.id` wskazuje istniejący rekord. | `200 OK`, dane firmy są zaktualizowane. |
| TC-02 | Aktualizacja flagi klienta | Parametr `isClient` zmieniony względem poprzedniej wartości. | Relacja `UserFirm.IsClient` jest zaktualizowana. |

---

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Edycja nieistniejącej firmy | `firmDto.id` nie istnieje. | `500 Internal Server Error`, komunikat `Firm not found.` |
| TC-N02 | Brak tokenu | Żądanie bez `Authorization`. | `401 Unauthorized`. |
