# Dodanie firmy — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Dodanie firmy użytkownika | Token zawiera rolę `User`. Endpoint wywołany z `isClient = false`. | API zwraca `200 OK` z `FirmDto.Id`. Powstaje `Firm`. Powstaje `UserFirm` z `IsClient = false`. |
| TC-02 | Dodanie firmy klienta | Token zawiera rolę `User`. Endpoint wywołany z `isClient = true`. | API zwraca `200 OK` z `FirmDto.Id`. Powstaje `Firm`. Powstaje `UserFirm` z `IsClient = true`. |
| TC-03 | Dodanie pierwszej firmy użytkownika | `User.ActiveUserFirm` ma wartość `null`. | Nowa relacja zostaje ustawiona jako `ActiveUserFirm`. Powstają trzy serie dokumentów początkowych. |
| TC-04 | Dodanie kolejnej firmy użytkownika | `User.ActiveUserFirm` ma już wartość. | Nowa relacja zostaje zapisana. `ActiveUserFirm` nie jest zmieniana. Serie początkowe nie są tworzone przez ten warunek. |

---

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Brak tokenu JWT | Żądanie bez nagłówka `Authorization`. | API zwraca `401 Unauthorized`. |
| TC-N02 | Brak roli `User` | Token nie zawiera wymaganej roli. | API zwraca `403 Forbidden`. |
| TC-N03 | Puste pola tekstowe w DTO | Body zawiera puste wartości tekstowe. | Kod procesu nie zawiera walidacji DTO. Wynik wymaga testu integracyjnego. [WYMAGA WERYFIKACJI] |
| TC-N04 | Niezerowy `id` dla nowej firmy | Body zawiera `id > 0`. | Zachowanie zależy od EF Core i konfiguracji encji. [WYMAGA WERYFIKACJI] |

---

## Dane testowe minimalne

```json
{
  "id": 0,
  "name": "InvoiceJet Demo S.R.L.",
  "cui": "12345678",
  "regCom": "J40/1234/2026",
  "address": "STR. TEST 1",
  "county": "Bucuresti",
  "city": "Bucuresti"
}
```

---

## Weryfikacja w bazie danych

| Obiekt | Oczekiwana zmiana |
|---|---|
| `Firm` | Nowy rekord z danymi z `FirmDto`. |
| `UserFirm` | Nowy rekord łączący użytkownika z firmą. |
| `User.ActiveUserFirm` | Ustawiony tylko gdy wcześniej miał wartość `null`. |
| `DocumentSeries` | Trzy nowe rekordy tylko dla pierwszej aktywnej firmy. |
