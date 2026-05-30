# Wystawienie nowej faktury — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/Document/AddDocument` |
| Kontroler | `DocumentController` |
| Metoda kontrolera | `AddDocument(DocumentRequestDto documentRequestDto)` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Content-Type | `application/json` |

---

## Żądanie

Body żądania ma typ `DocumentRequestDto`.

| Pole | Typ | Wymagane z perspektywy kodu | Wykorzystanie |
|---|---|---|---|
| `id` | `int` | Nie | Przypisywane do `Document.Id`. Dla nowego dokumentu oczekiwana wartość wejściowa to `0`. [WYMAGA WERYFIKACJI] |
| `documentNumber` | `string?` | Nie | Nie jest używane przy zapisie nowego dokumentu. Numer jest tworzony z serii. |
| `seller` | `FirmDto?` | Nie | Nie jest używane w `AddDocument`. |
| `client` | `FirmDto` | Tak | `client.id` trafia do `Document.ClientId`. |
| `issueDate` | `DateTime` | Tak | Trafia do `Document.IssueDate`. |
| `dueDate` | `DateTime?` | Nie | Trafia do `Document.DueDate`. |
| `bankAccount` | `BankAccountDto?` | Nie | Nie jest używane z body. Konto jest pobierane z aktywnego konta firmy użytkownika. |
| `documentSeries` | `DocumentSeriesDto?` | Tak dla numeru i typu dokumentu | Ustala `DocumentNumber`, `DocumentTypeId` i serię do zwiększenia numeru. |
| `documentType` | `DocumentType?` | Nie | Nie jest używane w `AddDocument`. |
| `documentStatus` | `DocumentStatus?` | Nie | Nie jest używane w `AddDocument`. Status jest ustawiany na `Unpaid`. |
| `products` | `List<DocumentProductRequestDto>` | Tak | Lista pozycji dokumentu zapisywana jako `DocumentProduct`. |

---

## Struktura pozycji dokumentu

| Pole | Typ | Wykorzystanie |
|---|---|---|
| `id` | `int` | Gdy `id > 0`, serwis szuka istniejącego produktu po `name` i `userFirmId`. Gdy `id <= 0`, serwis tworzy nowy `Product`. |
| `name` | `string` | Nazwa produktu. |
| `unitPrice` | `decimal` | Cena jednostkowa użyta do wyliczenia `Document.UnitPrice`. |
| `totalPrice` | `decimal` | Wartość pozycji użyta do wyliczenia `Document.TotalPrice`. |
| `containsTva` | `bool` | Używane przy mapowaniu nowego produktu. |
| `unitOfMeasurement` | `string` | Używane przy mapowaniu nowego produktu. |
| `tvaValue` | `int` | Używane przy mapowaniu nowego produktu. |
| `quantity` | `int` | Ilość pozycji i składnik wyliczenia `UnitPrice * Quantity`. |

---

## Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `DocumentRequestDto` | Dokument został zapisany. |
| `400 Bad Request` | `{ "message": string }` | `UserHasNoAssociatedFirmException` lub `NoBankAccountAddedException`. |
| `401 Unauthorized` | N/D | Brak poprawnego tokenu JWT. |
| `403 Forbidden` | N/D | Token nie spełnia wymogu roli `User`. |
| `500 Internal Server Error` | `{ "message": string }` | Nieobsłużony wyjątek, na przykład `Product not found.`. |

---

## Przykład żądania

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
