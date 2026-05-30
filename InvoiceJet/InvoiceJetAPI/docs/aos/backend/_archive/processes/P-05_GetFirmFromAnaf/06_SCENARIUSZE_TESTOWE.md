# Pobranie firmy z ANAF — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Pobranie danych firmy po poprawnym CUI | ANAF zwraca status sukcesu i poprawny JSON. | `200 OK` i `FirmDto` z polami `Name`, `Cui`, `RegCom`, `Address`, `County`, `City`. |
| TC-02 | Częściowe dane z ANAF | ANAF zwraca brak części pól. | `200 OK` i `FirmDto` z dostępnymi polami, pozostałe pola puste. |

---

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | CUI nie znalezione | ANAF zwraca status błędu. | `404 Not Found`, komunikat z `AnafFirmNotFoundException`. |
| TC-N02 | Niepoprawny JSON z ANAF | Odpowiedź nie daje się sparsować przez `JObject`. | `404 Not Found`, komunikat z `AnafFirmNotFoundException`. |
| TC-N03 | Brak tokenu | Żądanie bez autoryzacji. | `401 Unauthorized`. |

---

## Przykład żądania

```text
GET /api/Firm/fromAnaf/12345678
Authorization: Bearer <token>
```
