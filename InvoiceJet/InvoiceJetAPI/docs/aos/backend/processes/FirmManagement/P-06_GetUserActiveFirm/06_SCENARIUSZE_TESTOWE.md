# GetUserActiveFirm — Scenariusze testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zalogowany użytkownik z ważnym JWT | Rejestracja (P-01) + logowanie (P-02) | `DT-02` |
| Użytkownik z aktywną firmą | Stan po P-03 `TC-01` | `DT-03` |

---

## 2. Dane poprawne (happy path)

### `TC-01` — Użytkownik z aktywną firmą zwraca dane firmy

Warunki wstępne: `DT-03` — użytkownik ma aktywną firmę (`Id=42`, `ActiveUserFirmId` ustawione).

Żądanie:
```
GET /api/Firm/GetUserActiveFirm
Authorization: Bearer <token z DT-02>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `FirmDto` z danymi aktywnej firmy:
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
- Skutek w bazie: brak (read-only)

---

### `TC-02` — Użytkownik bez aktywnej firmy zwraca pusty DTO

Warunki wstępne: `DT-02` — świeżo zarejestrowany użytkownik, `ActiveUserFirmId == null` (nie wywołano jeszcze `AddFirm`).

Żądanie:
```
GET /api/Firm/GetUserActiveFirm
Authorization: Bearer <token z DT-02>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: pusty `FirmDto`:
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
- Skutek w bazie: brak

---

## 3. Dane niepoprawne

### `TC-N01` — łamie `WAL-01`: brak tokenu JWT

Żądanie bez nagłówka `Authorization`:
```
GET /api/Firm/GetUserActiveFirm
(brak nagłówka Authorization)
```
Oczekiwany rezultat:
- Status: `401 Unauthorized`
- Skutek w bazie: brak

---

### `TC-N02` — łamie `WAL-01`: token bez roli `"User"`

Żądanie z ważnym tokenem, ale rola w claimach inna niż `"User"`:
```
GET /api/Firm/GetUserActiveFirm
Authorization: Bearer <token z inną rolą>
```
Oczekiwany rezultat:
- Status: `403 Forbidden`
- Skutek w bazie: brak

---

## 4. Wartości brzegowe

| ID | Sytuacja | Oczekiwany rezultat |
|---|---|---|
| `TC-B01` | Użytkownik istnieje, `ActiveUserFirmId == null` | `200 OK` + pusty `FirmDto` |
| `TC-B02` | Użytkownik usunięty z DB po wystawieniu JWT (token jeszcze ważny) | `200 OK` + pusty `FirmDto` (brak wiersza → `null`) |
| `TC-B03` | Użytkownik ma aktywną firmę z `RegCom` = `""` (pusty) | `200 OK` + `FirmDto` z `regCom=""` |
| `TC-B04` | Użytkownik z aktywną firmą oznaczoną jako klient (`IsClient=true`) | `200 OK` + dane firmy (proces nie filtruje po `IsClient` — zwraca aktywną firmę niezależnie od roli) |

> [UWAGA: `TC-B04` — proces zwraca aktywną firmę niezależnie od flagi `IsClient`. Jeśli `ActiveUserFirm` wskazuje na firmę-klienta (możliwe wg [UWAGA] z P-03), endpoint zwróci firmę klienta jako „aktywną firmę użytkownika" — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-02` | Zarejestrowany użytkownik + JWT (bez aktywnej firmy) | `TC-02`, `TC-N01`, `TC-N02`, `TC-B01`, `TC-B02` |
| `DT-03` | Użytkownik z aktywną firmą | `TC-01`, `TC-B03`, `TC-B04` |
