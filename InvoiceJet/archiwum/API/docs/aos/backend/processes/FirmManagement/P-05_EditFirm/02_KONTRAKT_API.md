# EditFirm — Kontrakt API

## Endpoint `API-05`

| Atrybut | Wartość |
|---|---|
| ID endpointu | `API-05` |
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/Firm/EditFirm/{isClient}` |
| Autoryzacja | `Bearer <JWT>` — `[Authorize(Roles = "User")]` dziedziczone z `FirmController` |
| Parametr trasy | `isClient` (bool) — czy firma ma rolę klienta |
| Ciało żądania | `FirmDto` (JSON) |
| Typ odpowiedzi | `FirmDto` (echo wejściowego DTO) |

## Parametr trasy

| Parametr | Typ | Wymagany | Opis |
|---|---|---|---|
| `isClient` | `bool` | tak | `true` → firma oznaczona jako klient (odbiorca faktur); `false` → własna firma użytkownika (wystawca faktur). ASP.NET Core parsuje automatycznie; wartości nierozpoznane (`"yes"`, `"1"`) → `400 Bad Request` |

## Ciało żądania — `FirmDto`

| Pole | Typ JSON | Wymagany | Uwagi |
|---|---|---|---|
| `id` | `number` | **tak** | Musi wskazywać na istniejący rekord `Firm` w DB |
| `name` | `string` | tak (NOT NULL w DB) | Pełna nazwa firmy |
| `cui` | `string` | tak (NOT NULL w DB) | Numer CUI |
| `regCom` | `string\|null` | opcjonalny w DTO, **NOT NULL w DB** | `null` → `500` |
| `address` | `string` | tak (NOT NULL w DB) | Adres |
| `county` | `string` | tak (NOT NULL w DB) | Județ |
| `city` | `string` | tak (NOT NULL w DB) | Miejscowość |

## Przykłady żądania

### Żądanie poprawne — edycja własnej firmy

```
PUT /api/Firm/EditFirm/false
Authorization: Bearer <token z DT-02>
Content-Type: application/json
```

```json
{
  "id": 42,
  "name": "Firma Testowa SRL (zmieniona)",
  "cui": "12345678",
  "regCom": "J40/1234/2020",
  "address": "STR. NOUA NR. 10",
  "county": "ILFOV",
  "city": "VOLUNTARI"
}
```

### Żądanie poprawne — zmiana roli firmy na klienta

```
PUT /api/Firm/EditFirm/true
Authorization: Bearer <token z DT-02>
Content-Type: application/json
```

```json
{
  "id": 42,
  "name": "Firma Testowa SRL",
  "cui": "12345678",
  "regCom": "J40/1234/2020",
  "address": "STR. EXEMPLU NR. 1",
  "county": "ILFOV",
  "city": "VOLUNTARI"
}
```

## Odpowiedź — `200 OK`

Body: `FirmDto` — echo żądania (serwis zwraca wejściowy obiekt bez ponownego odczytu z DB)

```json
{
  "id": 42,
  "name": "Firma Testowa SRL (zmieniona)",
  "cui": "12345678",
  "regCom": "J40/1234/2020",
  "address": "STR. NOUA NR. 10",
  "county": "ILFOV",
  "city": "VOLUNTARI"
}
```

## Tabela statusów HTTP

| Kod | Przyczyna | Body |
|---|---|---|
| `200 OK` | Firma zaktualizowana pomyślnie | `FirmDto` (echo żądania) |
| `400 Bad Request` | `isClient` nie parsuje się na `bool` | ASP.NET Core ModelState error |
| `401 Unauthorized` | Brak nagłówka `Authorization` lub nieważny token | brak body |
| `403 Forbidden` | Token ważny, ale brak roli `"User"` | brak body |
| `500 Internal Server Error` | Firma o `firmDto.Id` nie istnieje w DB (`throw new Exception("Firm not found.")` → catch-all) | `{ "message": "Firm not found." }` |
| `500 Internal Server Error` | `firmDto.RegCom = null` → NOT NULL constraint w DB | `{ "message": "<DbUpdateException message>" }` |
| `500 Internal Server Error` | Dowolny inny błąd EF Core / DB | `{ "message": "<szczegóły błędu>" }` |

> [UWAGA: Nieistniejące `firmDto.Id` zwraca `500` zamiast `404`. `ExceptionMiddleware` mapuje zwykłe `Exception` na `500` — brak dedykowanej klasy `FirmNotFoundException` — WYMAGA WERYFIKACJI Z ZESPOŁEM]

## Uwagi o zachowaniu

- Operacja **aktualizuje pełny zestaw pól** firmy — brak partial update (brak PATCH). Klient musi przesłać wszystkie pola nawet jeśli zmienił tylko jedno.
- Odpowiedź to **echo żądania** (nie odczyt z DB po zapisie) — pole `id` pochodzi z żądania.
- Flaga `isClient` wpływa na relację `UserFirm`, nie na encję `Firm` bezpośrednio.
