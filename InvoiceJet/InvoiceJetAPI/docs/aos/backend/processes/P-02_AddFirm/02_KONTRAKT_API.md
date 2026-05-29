# Dodanie firmy — Kontrakt API

## Endpoint

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/Firm/AddFirm/{isClient}` |
| Kontroler | `FirmController` |
| Metoda kontrolera | `AddFirm([FromBody] FirmDto firmDto, bool isClient)` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Content-Type | `application/json` |

---

## Parametry trasy

| Parametr | Typ | Wykorzystanie |
|---|---|---|
| `isClient` | `bool` | Wartość przypisywana do `UserFirm.IsClient`. |

---

## Body żądania

Body żądania ma typ `FirmDto`.

| Pole | Typ | Wymagane z perspektywy kodu | Wykorzystanie |
|---|---|---|---|
| `id` | `int` | Nie | Mapowane do `Firm.Id`. Dla nowej firmy oczekiwana wartość wejściowa to `0`. [WYMAGA WERYFIKACJI] |
| `name` | `string` | Tak | Mapowane do `Firm.Name`. |
| `cui` | `string` | Tak | Mapowane do `Firm.Cui`. |
| `regCom` | `string?` | Nie | Mapowane do `Firm.RegCom`. |
| `address` | `string` | Tak | Mapowane do `Firm.Address`. |
| `county` | `string` | Tak | Mapowane do `Firm.County`. |
| `city` | `string` | Tak | Mapowane do `Firm.City`. |

DTO nie zawiera atrybutów walidacyjnych. Wymagalność pól wynika z użycia pustych wartości domyślnych, nie z walidatorów `DataAnnotations`.

---

## Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `FirmDto` | Firma i relacja użytkownika zostały zapisane. |
| `400 Bad Request` | N/D | Brak specyficznego wyjątku dla `AddFirm` w kodzie procesu. |
| `401 Unauthorized` | N/D | Brak poprawnego tokenu JWT. |
| `403 Forbidden` | N/D | Token nie spełnia wymogu roli `User`. |
| `500 Internal Server Error` | `{ "message": string }` | Nieobsłużony wyjątek w serwisie lub EF Core. |

---

## Przykład żądania

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

Przykładowy endpoint dla firmy użytkownika:

```text
POST /api/Firm/AddFirm/false
```

Przykładowy endpoint dla firmy klienta:

```text
POST /api/Firm/AddFirm/true
```
