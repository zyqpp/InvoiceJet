# Pobranie aktywnej firmy użytkownika — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Aktywna firma istnieje | Użytkownik ma ustawione `ActiveUserFirm`. | `200 OK` i `FirmDto` z danymi firmy. |
| TC-02 | Brak aktywnej firmy | Użytkownik nie ma ustawionego `ActiveUserFirm`. | `200 OK` i pusty `FirmDto`. |

---

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Brak tokenu | Żądanie bez autoryzacji. | `401 Unauthorized`. |
| TC-N02 | Brak roli `User` | Token bez roli `User`. | `403 Forbidden`. |
