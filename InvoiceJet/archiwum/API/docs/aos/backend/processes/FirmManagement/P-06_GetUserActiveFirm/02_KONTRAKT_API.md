# GetUserActiveFirm — Kontrakt API

## Endpoint `API-06`

| Atrybut | Wartość |
|---|---|
| ID endpointu | `API-06` |
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Firm/GetUserActiveFirm` |
| Autoryzacja | `Bearer <JWT>` — `[Authorize(Roles = "User")]` dziedziczone z `FirmController` |
| Parametry | brak |
| Ciało żądania | brak |
| Typ odpowiedzi | `FirmDto` |

## Żądanie

Brak parametrów i ciała. Tożsamość użytkownika pobierana jest z tokenu JWT (claim `"userId"`).

```
GET /api/Firm/GetUserActiveFirm
Authorization: Bearer <token z DT-02>
```

## Odpowiedź — `200 OK` (użytkownik ma aktywną firmę)

Body: `FirmDto`

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

## Odpowiedź — `200 OK` (użytkownik bez aktywnej firmy)

Gdy użytkownik nie ma ustawionej aktywnej firmy (`User.ActiveUserFirmId == null`), serwis zwraca **pusty `FirmDto`** z kodem `200 OK`:

```json
{
  "id": 0,
  "name": "",
  "cui": "",
  "regCom": null,
  "address": "",
  "county": "",
  "city": ""
}
```

> [UWAGA: Pusty `FirmDto` z `200 OK` zamiast `404`/`204`. Klient musi rozpoznać „brak aktywnej firmy" po `id == 0` lub pustym `name`. Ta sama odpowiedź pojawia się również, gdy użytkownik nie istnieje w DB — WYMAGA WERYFIKACJI Z ZESPOŁEM]

## Tabela statusów HTTP

| Kod | Przyczyna | Body |
|---|---|---|
| `200 OK` | Użytkownik ma aktywną firmę | `FirmDto` z danymi firmy |
| `200 OK` | Użytkownik nie ma aktywnej firmy (lub nie istnieje w DB) | pusty `FirmDto` (`id=0`, stringi `""`, `regCom=null`) |
| `401 Unauthorized` | Brak nagłówka `Authorization` lub nieważny token | brak body |
| `403 Forbidden` | Token ważny, ale brak roli `"User"` | brak body |

> Proces nie zwraca `4xx`/`5xx` poza autoryzacją — nie rzuca wyjątków domenowych ani błędów DB (operacja czysto odczytowa).

## Uwagi o zachowaniu

- Operacja **read-only** — brak efektów ubocznych w bazie danych.
- Odpowiedź zawsze ma kod `200 OK` (poza błędami autoryzacji), nawet gdy brak danych.
- Pole `regCom` jest jedynym polem nullable; pozostałe pola tekstowe w pustym DTO mają wartość `""` (nie `null`).
