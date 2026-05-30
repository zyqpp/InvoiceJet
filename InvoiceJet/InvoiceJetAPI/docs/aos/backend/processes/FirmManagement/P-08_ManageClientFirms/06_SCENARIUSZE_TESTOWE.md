# ManageClientFirms — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zalogowany użytkownik z rolą `User` | rejestracja lub seed | `DT-01` |
| Relacja `UserFirm` (1 lub więcej), gdzie `IsClient=true` | seed / rejestracja | `DT-08` (UserFirm z IsClient=true) |
| (dla DELETE): Względna Firm bez dokumentów | seed | `DT-09` (Firm isolated) |

Notatka: Aby testować obie operacje (GET i DELETE), potrzebujesz co najmniej jednej firmy-klienta (IsClient=true) zawiązanej z zalogowanym użytkownikiem.

## 2. Dane poprawne (happy path)

### `TC-01` — GET /api/Firm/GetUserClientFirms (lista firm-klientów)

Warunki wstępne: `DT-01` (zalogowany user), `DT-08` (relacja UserFirm z IsClient=true).

Żądanie:
```
GET /api/Firm/GetUserClientFirms
Authorization: Bearer {JWT_TOKEN}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź (tablica `FirmDto[]`):
```json
[
  {
    "id": 2,
    "name": "Acme Corporation",
    "cui": "12345678",
    "regCom": "J40/2020/123",
    "address": "STR. Marticel Ion Dragomir, nr. 10",
    "county": "Bihor",
    "city": "Oradea"
  }
]
```
- Skutek w bazie: brak zmian (read-only)

### `TC-02` — GET /api/Firm/GetUserClientFirms (brak firm-klientów)

Warunki wstępne: `DT-01` (zalogowany user bez firm-klientów).

Żądanie: jak wyżej.

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: pusta tablica `[]`
- Skutek w bazie: brak zmian

### `TC-03` — PUT /api/Firm/DeleteFirms (usunięcie jednej firmy)

Warunki wstępne: `DT-01` (zalogowany user), `DT-09` (Firm Id=5, bez powiązań z Document).

Żądanie:
```
PUT /api/Firm/DeleteFirms?firmIds=5
Authorization: Bearer {JWT_TOKEN}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: puste ciało
- Skutek w bazie: 
  - Rekord `Firm` z Id=5 usunięty z tabeli `Firm`
  - Relacje `UserFirm` z `FirmId=5` usunięte z tabeli `UserFirm` (kaskada)

### `TC-04` — PUT /api/Firm/DeleteFirms (usunięcie wielu firm)

Warunki wstępne: `DT-01`, `DT-09` (Id=5), `DT-10` (Firm Id=7, bez powiązań).

Żądanie:
```
PUT /api/Firm/DeleteFirms?firmIds=5&firmIds=7
Authorization: Bearer {JWT_TOKEN}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Skutek w bazie: oba rekordy `Firm` usunięte, wraz z relacjami `UserFirm`

## 3. Dane niepoprawne (po jednej na regułę walidacji)

### `TC-N01` — łamie `WAL-01`: Firma o danym ID nie istnieje

Warunki wstępne: `DT-01` (zalogowany user).

Żądanie:
```
PUT /api/Firm/DeleteFirms?firmIds=99999
Authorization: Bearer {JWT_TOKEN}
```

Oczekiwany rezultat:
- Status: `500 Internal Server Error` [UWAGA: powinno 400]
- Komunikat: `{ "message": "Product not found." }` [UWAGA: powinno "Firm not found." i 400]
- Skutek w bazie: brak zmian

### `TC-N02` — łamie `WAL-02`: Firma powiązana z dokumentami

Warunki wstępne: `DT-01`, `DT-11` (Firm Id=3 z powiązanym Document gdzie ClientId=3).

Żądanie:
```
PUT /api/Firm/DeleteFirms?firmIds=3
Authorization: Bearer {JWT_TOKEN}
```

Oczekiwany rezultat:
- Status: `400 Bad Request`
- Komunikat: `{ "message": "Can't delete. Firm Acme Corporation is associated with a document." }`
- Skutek w bazie: brak zmian (Firm Id=3 pozostaje w bazie)

## 4. Wartości brzegowe

### GET endpoint (read-only, brak wartości brzegowych)

> GET jest read-only, brak parametrów wejściowych — wymiar nie dotyczy.

### DELETE endpoint

| ID | Test | Parametr | Wartość | Oczekiwany rezultat |
|---|---|---|---|---|
| `TC-B01` | Pusta tablica ID | `firmIds=` (brak wartości) | `int[] {}` | Status `200 OK`, brak zmian w bazie (pętla nie wykonana) |
| `TC-B02` | Ujemne ID | `firmIds=-1` | `-1` | Status `500` (lub 400 — zależy od mapowania), Firm nie znaleziona |
| `TC-B03` | Zero | `firmIds=0` | `0` | Status `500` (lub 400), Firm o Id=0 nie istnieje |
| `TC-B04` | Bardzo duży ID | `firmIds=2147483647` | `int.MaxValue` | Status `500` (lub 400), Firm nie znaleziona |

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-01` | Zalogowany użytkownik (JWT token ważny 10 minut) | Wszystkie TC |
| `DT-08` | `UserFirm` (IsClient=true) z powiązaną `Firm` | TC-01, TC-04 |
| `DT-09` | `Firm` (Id=5) bez powiązań z `Document` | TC-03, TC-B02 |
| `DT-10` | `Firm` (Id=7) bez powiązań z `Document` | TC-04 |
| `DT-11` | `Firm` (Id=3) z `Document` gdzie `ClientId=3` | TC-N02 |

---

## Uwagi

- [UWAGA: Błędy WAL-01 zwracają 500 zamiast 400 — czy komunikat "Product not found." powinien być wpisany? — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- TC brak specjalnych zależności poza preconditions.
- Wszystkie `firmIds` w DELETE mogą być testowane rozdzielnie (zestaw wartości oraz kombinacje).
