# Statystyki dashboardu — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Pobranie statystyk dla roku i typu | Aktywna firma istnieje. | `200 OK`, liczby agregatów i `monthlyTotals` zgodne z danymi. |
| TC-02 | Brak aktywnej firmy | Użytkownik bez `ActiveUserFirm`. | `200 OK`, pusty `DashboardStatsDto`. |

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Brak tokenu | Żądanie bez autoryzacji. | `401 Unauthorized`. |
| TC-N02 | Brak roli | Token bez roli `User`. | `403 Forbidden`. |
