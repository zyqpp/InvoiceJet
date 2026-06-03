# GetUserClientFirms — Scenariusze testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zalogowany użytkownik z ważnym JWT | Rejestracja (P-01) + logowanie (P-02) | `DT-02` |
| Użytkownik z co najmniej jedną firmą-klientem | `POST /api/Firm/AddFirm/true` (P-03) | `DT-04` (nowy) |

---

## 2. Dane poprawne (happy path)

### `TC-01` — Użytkownik z firmami-klientami zwraca listę

Warunki wstępne: `DT-04` — użytkownik ma 2 firmy z `IsClient=true`.

Żądanie:
```
GET /api/Firm/GetUserClientFirms
Authorization: Bearer <token z DT-02>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: tablica 2 obiektów `FirmDto`:
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
- Skutek w bazie: brak (read-only)

---

### `TC-02` — Użytkownik bez firm-klientów zwraca pustą listę

Warunki wstępne: `DT-03` — użytkownik ma tylko własną firmę (`IsClient=false`), brak klientów.

Żądanie:
```
GET /api/Firm/GetUserClientFirms
Authorization: Bearer <token z DT-02>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `[]`
- Skutek w bazie: brak

---

## 3. Dane niepoprawne

### `TC-N01` — łamie `WAL-01`: brak tokenu JWT

Żądanie bez nagłówka `Authorization`:
```
GET /api/Firm/GetUserClientFirms
(brak nagłówka Authorization)
```
Oczekiwany rezultat:
- Status: `401 Unauthorized`
- Skutek w bazie: brak

---

### `TC-N02` — łamie `WAL-01`: token bez roli `"User"`

Żądanie z ważnym tokenem, ale rola w claimach inna niż `"User"`:
```
GET /api/Firm/GetUserClientFirms
Authorization: Bearer <token z inną rolą>
```
Oczekiwany rezultat:
- Status: `403 Forbidden`
- Skutek w bazie: brak

---

## 4. Wartości brzegowe

| ID | Sytuacja | Oczekiwany rezultat |
|---|---|---|
| `TC-B01` | Użytkownik ma tylko własną firmę (`IsClient=false`) | `200 OK` + `[]` (filtr `IsClient` wyklucza) |
| `TC-B02` | Użytkownik usunięty z DB po wystawieniu JWT | `200 OK` + `[]` (brak dopasowań w `WHERE`) |
| `TC-B03` | Użytkownik ma 1 firmę-klienta z `RegCom` = `""` | `200 OK` + lista z `regCom=""` |
| `TC-B04` | Użytkownik ma mieszane firmy (1 własna + 2 klientów) | `200 OK` + lista 2 firm-klientów (własna pominięta) |
| `TC-B05` | Użytkownik ma 100+ firm-klientów | `200 OK` + pełna lista (brak paginacji) [UWAGA: brak limitu zwracanych rekordów] |

> [UWAGA: `TC-B05` — brak paginacji/limitu. Użytkownik z bardzo dużą liczbą klientów otrzyma wszystkie rekordy w jednej odpowiedzi, co może obciążyć pamięć i sieć — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-02` | Zarejestrowany użytkownik + JWT | Wszystkie scenariusze |
| `DT-03` | Użytkownik z aktywną własną firmą (bez klientów) | `TC-02`, `TC-B01` |
| `DT-04` | Użytkownik z firmami-klientami (`IsClient=true`) | `TC-01`, `TC-B03`, `TC-B04` |

> `DT-04` należy dodać do `../../KATALOG_DANYCH_TESTOWYCH.md` — opisuje stan bazy po dodaniu firm przez `POST /api/Firm/AddFirm/true`.
