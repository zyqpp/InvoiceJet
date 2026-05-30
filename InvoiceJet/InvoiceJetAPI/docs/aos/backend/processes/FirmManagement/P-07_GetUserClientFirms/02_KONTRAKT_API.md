# GetUserClientFirms — Kontrakt API

## Endpoint `API-07`

| Atrybut | Wartość |
|---|---|
| ID endpointu | `API-07` |
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Firm/GetUserClientFirms` |
| Autoryzacja | `Bearer <JWT>` — `[Authorize(Roles = "User")]` dziedziczone z `FirmController` |
| Parametry | brak |
| Ciało żądania | brak |
| Typ odpowiedzi | `List<FirmDto>` |

## Żądanie

Brak parametrów i ciała. Tożsamość użytkownika pobierana jest z tokenu JWT (claim `"userId"`).

```
GET /api/Firm/GetUserClientFirms
Authorization: Bearer <token z DT-02>
```

## Odpowiedź — `200 OK` (użytkownik ma firmy-klientów)

Body: `List<FirmDto>`

```json
[
  {
    "id": 51,
    "name": "Klient Alfa SRL",
    "cui": "87654321",
    "regCom": "J40/5678/2021",
    "address": "STR. CLIENTULUI NR. 5",
    "county": "ILFOV",
    "city": "BUCURESTI"
  },
  {
    "id": 52,
    "name": "Klient Beta SA",
    "cui": "11223344",
    "regCom": "J40/9999/2022",
    "address": "BLD. UNIRII NR. 12",
    "county": "BUCURESTI",
    "city": "BUCURESTI"
  }
]
```

## Odpowiedź — `200 OK` (użytkownik bez firm-klientów)

Gdy użytkownik nie ma żadnych firm oznaczonych jako klient, serwis zwraca **pustą tablicę** z kodem `200 OK`:

```json
[]
```

## Tabela statusów HTTP

| Kod | Przyczyna | Body |
|---|---|---|
| `200 OK` | Użytkownik ma firmy-klientów | `List<FirmDto>` z danymi firm |
| `200 OK` | Użytkownik nie ma firm-klientów (lub nie istnieje w DB) | pusta tablica `[]` |
| `401 Unauthorized` | Brak nagłówka `Authorization` lub nieważny token | brak body |
| `403 Forbidden` | Token ważny, ale brak roli `"User"` | brak body |

> Proces nie zwraca `4xx`/`5xx` poza autoryzacją — nie rzuca wyjątków domenowych ani błędów DB (operacja czysto odczytowa).

## Uwagi o zachowaniu

- Operacja **read-only** — brak efektów ubocznych w bazie danych.
- Zwracane są wyłącznie firmy z relacją `UserFirm.IsClient == true` należące do zalogowanego użytkownika.
- Pusta lista (`[]`) jest poprawnym wynikiem dla użytkownika bez klientów — nie jest to błąd.
- Kolejność firm na liście wynika z domyślnego porządku DB (brak jawnego `OrderBy` w zapytaniu).
