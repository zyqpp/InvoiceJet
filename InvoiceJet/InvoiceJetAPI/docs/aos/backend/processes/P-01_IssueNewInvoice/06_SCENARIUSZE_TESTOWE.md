# Wystawienie nowej faktury — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Wystawienie faktury z istniejącym produktem | Użytkownik ma aktywną firmę, aktywne konto bankowe, klienta, serię dokumentów i produkt z nazwą z pozycji. | API zwraca `200 OK`. Powstaje `Document`. Powstaje `DocumentProduct`. `DocumentSeries.CurrentNumber` zwiększa się o `1`. |
| TC-02 | Wystawienie faktury z nowym produktem | Pozycja ma `id <= 0`. | API zwraca `200 OK`. Powstaje nowy `Product` z `UserFirmId`. Powstaje `DocumentProduct`. |
| TC-03 | Wyliczenie sum dokumentu | Body zawiera co najmniej dwie pozycje. | `Document.UnitPrice` jest sumą `UnitPrice * Quantity`. `Document.TotalPrice` jest sumą `TotalPrice`. |
| TC-04 | Nadanie numeru dokumentu | Seria ma `SeriesName = "2026"` i `CurrentNumber = 7`. | `Document.DocumentNumber` ma wartość `20260007`. |

---

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Brak tokenu JWT | Żądanie bez nagłówka `Authorization`. | API zwraca `401 Unauthorized`. |
| TC-N02 | Brak roli `User` | Token nie zawiera wymaganej roli. | API zwraca `403 Forbidden`. |
| TC-N03 | Brak aktywnej firmy | `Users.GetUserFirmIdAsync(...)` zwraca `null`. | API zwraca `400 Bad Request` z komunikatem z `UserHasNoAssociatedFirmException`. |
| TC-N04 | Brak aktywnego konta bankowego | Brak rekordu `BankAccount` z `IsActive = true` dla aktywnej firmy. | API zwraca `400 Bad Request` z komunikatem z `NoBankAccountAddedException`. |
| TC-N05 | Istniejący produkt nie znaleziony | Pozycja ma `id > 0`, ale produkt o danej nazwie nie istnieje dla aktywnej firmy. | API zwraca `500 Internal Server Error` z komunikatem `Product not found.`. |

---

## Dane testowe minimalne

```json
{
  "id": 0,
  "client": {
    "id": 12,
    "name": "ACME TEST S.R.L.",
    "cui": "123456",
    "regCom": "J40/123/2026",
    "address": "STR. TEST 1",
    "county": "Bucuresti",
    "city": "Bucuresti"
  },
  "issueDate": "2026-05-29T00:00:00",
  "dueDate": "2026-06-12T00:00:00",
  "documentSeries": {
    "id": 3,
    "seriesName": "2026",
    "currentNumber": 1,
    "documentType": {
      "id": 1,
      "name": "Factura"
    }
  },
  "products": [
    {
      "id": 0,
      "name": "Consulting",
      "unitPrice": 100,
      "totalPrice": 119,
      "containsTva": true,
      "unitOfMeasurement": "h",
      "tvaValue": 19,
      "quantity": 1
    }
  ]
}
```
