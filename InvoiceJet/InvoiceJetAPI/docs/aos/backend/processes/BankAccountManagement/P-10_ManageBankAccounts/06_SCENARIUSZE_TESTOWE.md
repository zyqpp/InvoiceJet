# ManageBankAccounts — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zarejestrowany użytkownik (email + hasło) | API lub seed | `DT-01` |
| Ważny token JWT (`Authorization: Bearer`) | `POST /api/Auth/login` | `DT-02` |
| Użytkownik z aktywną firmą (`UserFirm.IsClient=false`, `User.ActiveUserFirmId != null`) | `POST /api/Firm/AddFirm/false` | `DT-03` |
| Istniejące konto bankowe w aktywnej firmie (do testów Edit/Delete) | `POST /api/BankAccount/AddUserFirmBankAccount` | `DT-05` (nowy) |

Szczegóły `DT-01`, `DT-02`, `DT-03`: `../../KATALOG_DANYCH_TESTOWYCH.md`.

Nowy fixture `DT-05` — definicja poniżej w sekcji 5.

---

## 2. Dane poprawne (happy path)

### `TC-01` — GET lista kont bankowych (z wynikami)

Warunki wstępne: `DT-02` (JWT), `DT-03` (aktywna firma), `DT-05` (co najmniej jedno konto w firmie).

Żądanie:
```
GET /api/BankAccount/GetUserFirmBankAccounts
Authorization: Bearer <jwt_z_DT-02>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: tablica co najmniej jednego `BankAccountDto`, np.:
```json
[
  {
    "id": 5,
    "bankName": "ING Bank Śląski",
    "iban": "RO49AAAA1B31007593840000",
    "currency": 0,
    "isActive": true
  }
]
```
- Skutek w bazie: brak zmian (read-only)

---

### `TC-02` — GET lista kont bankowych (pusta)

Warunki wstępne: `DT-02` (JWT), `DT-03` (aktywna firma), **brak kont** w aktywnej firmie.

Żądanie: jak w TC-01.

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `[]`
- Skutek w bazie: brak zmian

---

### `TC-03` — POST dodanie nowego konta (aktywne, RON)

Warunki wstępne: `DT-02`, `DT-03`.

Żądanie:
```
POST /api/BankAccount/AddUserFirmBankAccount
Authorization: Bearer <jwt_z_DT-02>
Content-Type: application/json

{
  "id": 0,
  "bankName": "ING Bank Śląski",
  "iban": "RO49AAAA1B31007593840000",
  "currency": 0,
  "isActive": true
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `BankAccountDto` z wypełnionym `id` (int > 0):
```json
{
  "id": 5,
  "bankName": "ING Bank Śląski",
  "iban": "RO49AAAA1B31007593840000",
  "currency": 0,
  "isActive": true
}
```
- Skutek w bazie:
  - Nowy rekord `BankAccount`: `BankName = "ING Bank Śląski"`, `Iban = "RO49AAAA1B31007593840000"`, `Currency = 0 (Ron)`, `IsActive = true`, `UserFirmId = <Id aktywnej UserFirm>`
  - Wszystkie inne konta firmowe (jeśli istniały) mają `IsActive = false`

---

### `TC-04` — POST dodanie nieaktywnego konta (EUR)

Warunki wstępne: `DT-02`, `DT-03`.

Żądanie:
```
POST /api/BankAccount/AddUserFirmBankAccount
Authorization: Bearer <jwt_z_DT-02>
Content-Type: application/json

{
  "id": 0,
  "bankName": "BRD - Groupe Société Générale",
  "iban": "RO49BRDE410SV04411864100",
  "currency": 1,
  "isActive": false
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `BankAccountDto` z `id > 0` i `isActive = false`
- Skutek w bazie: nowy rekord `BankAccount` z `IsActive = false`; inne konta bez zmian (dezaktywacja nie jest wywoływana gdy `IsActive = false`)

---

### `TC-05` — PUT edycja konta bankowego

Warunki wstępne: `DT-02`, `DT-05` (konto o `Id=5` istnieje).

Żądanie:
```
PUT /api/BankAccount/EditUserFirmBankAccount
Authorization: Bearer <jwt_z_DT-02>
Content-Type: application/json

{
  "id": 5,
  "bankName": "ING Bank Śląski (zaktualizowany)",
  "iban": "RO49AAAA1B31007593840001",
  "currency": 1,
  "isActive": true
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `BankAccountDto` z zaktualizowanymi polami:
```json
{
  "id": 5,
  "bankName": "ING Bank Śląski (zaktualizowany)",
  "iban": "RO49AAAA1B31007593840001",
  "currency": 1,
  "isActive": true
}
```
- Skutek w bazie: rekord `BankAccount` z `Id=5` zaktualizowany; `UserFirmId` bez zmian; inne konta firmy dezaktywowane (`IsActive = false`)

---

### `TC-06` — PUT usunięcie jednego konta

Warunki wstępne: `DT-02`, `DT-05` (konto o `Id=5` istnieje, **nie jest powiązane** z żadnym dokumentem).

Żądanie:
```
PUT /api/BankAccount/DeleteUserFirmBankAccounts
Authorization: Bearer <jwt_z_DT-02>
Content-Type: application/json

[5]
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: puste ciało
- Skutek w bazie: rekord `BankAccount` z `Id=5` usunięty

---

### `TC-07` — PUT usunięcie wielu kont naraz

Warunki wstępne: `DT-02`, konta o `Id=5` i `Id=6` istnieją, oba niepowiązane z dokumentami.

Żądanie:
```
PUT /api/BankAccount/DeleteUserFirmBankAccounts
Authorization: Bearer <jwt_z_DT-02>
Content-Type: application/json

[5, 6]
```

Oczekiwany rezultat:
- Status: `200 OK`
- Skutek w bazie: oba rekordy usunięte z tabeli `BankAccount`

---

## 3. Dane niepoprawne (po jednej na regułę walidacji)

### `TC-N01` — łamie `WAL-01`: użytkownik bez aktywnej firmy

Warunki wstępne: `DT-02` (JWT), ale `User.ActiveUserFirmId = NULL`.

Żądanie:
```
POST /api/BankAccount/AddUserFirmBankAccount
Authorization: Bearer <jwt_bez_firmy>
Content-Type: application/json

{
  "id": 0,
  "bankName": "Bank Testowy",
  "iban": "RO49AAAA1B31007593840000",
  "currency": 0,
  "isActive": false
}
```

Oczekiwany rezultat:
- Status: `400 Bad Request`
- Komunikat: `{ "message": "User has no associated firm." }`
- Skutek w bazie: brak zmian

---

### `TC-N02` — łamie `WAL-02`: edycja nieistniejącego konta

Warunki wstępne: `DT-02`, `DT-03`. Brak konta o `Id=99999`.

Żądanie:
```
PUT /api/BankAccount/EditUserFirmBankAccount
Authorization: Bearer <jwt_z_DT-02>
Content-Type: application/json

{
  "id": 99999,
  "bankName": "Bank Nieistniejący",
  "iban": "RO49AAAA1B31007593840000",
  "currency": 0,
  "isActive": false
}
```

Oczekiwany rezultat:
- Status: `500 Internal Server Error` ⚠️ [powinno być `400` lub `404`]
- Komunikat: `{ "message": "Bank account not found." }`
- Skutek w bazie: brak zmian

---

### `TC-N03` — łamie `WAL-03`: usunięcie nieistniejącego konta

Warunki wstępne: `DT-02`. Brak konta o `Id=99999`.

Żądanie:
```
PUT /api/BankAccount/DeleteUserFirmBankAccounts
Authorization: Bearer <jwt_z_DT-02>
Content-Type: application/json

[99999]
```

Oczekiwany rezultat:
- Status: `500 Internal Server Error` ⚠️ [powinno być `400`]
- Komunikat: `{ "message": "Bank account not found." }`
- Skutek w bazie: brak zmian

---

### `TC-N04` — łamie `WAL-04`: usunięcie konta powiązanego z fakturą

Warunki wstępne: `DT-02`, konto o `Id=5` istnieje i jest powiązane z co najmniej jednym rekordem `Document`.

Żądanie:
```
PUT /api/BankAccount/DeleteUserFirmBankAccounts
Authorization: Bearer <jwt_z_DT-02>
Content-Type: application/json

[5]
```

Oczekiwany rezultat:
- Status: `400 Bad Request`
- Komunikat: `{ "message": "Can't delete. Bank account is associated with documents." }`
- Skutek w bazie: brak zmian (konto pozostaje)

---

## 4. Wartości brzegowe

| ID | Endpoint | Pole | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|---|
| `TC-B01` | AddUserFirmBankAccount | `bankName` | `""` (pusty string) | `200 OK` — brak walidacji pustej nazwy; rekord z `BankName = ""` zapisany [UWAGA: brak walidacji — WYMAGA WERYFIKACJI] |
| `TC-B02` | AddUserFirmBankAccount | `iban` | `""` (pusty string) | `200 OK` — brak walidacji pustego IBAN; rekord zapisany |
| `TC-B03` | AddUserFirmBankAccount | `currency` | `99` (nieistniejąca wartość enum) | `200 OK` lub błąd deserializacji — zależy od konfiguracji JSON serializer; może zapisać wartość `99` jako int do DB [UWAGA — WYMAGA WERYFIKACJI] |
| `TC-B04` | AddUserFirmBankAccount | `isActive` | `true` (gdy istnieje jedno inne aktywne konto) | `200 OK` — inne konto zostaje dezaktywowane (`IsActive = false`); reguła jednego aktywnego konta egzekwowana |
| `TC-B05` | AddUserFirmBankAccount | `isActive` | `false` | `200 OK` — brak dezaktywacji innych kont; firma może mieć wiele kont z `IsActive = false` |
| `TC-B06` | DeleteUserFirmBankAccounts | body | `[]` (pusta tablica) | `200 OK` — pętla nie wykonana; `CompleteAsync()` bez zmian |
| `TC-B07` | EditUserFirmBankAccount | `isActive` | `false` → `false` (konto było nieaktywne, pozostaje nieaktywne) | `200 OK` — brak dezaktywacji innych kont; tylko `CompleteAsync()` ze zmianą tracked encji |
| `TC-B08` | EditUserFirmBankAccount | `isActive` | `true` → `true` (konto już było aktywne, edytowane do `true`) | `200 OK` — `DeactivateOtherBankAccounts` wywoływana (dezaktywuje inne, nie samo edytowane bo `excludeAccountId = bankAccount.Id`) |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-01` | Dane rejestracji użytkownika | precondition wszystkich TC |
| `DT-02` | Zarejestrowany użytkownik + JWT | precondition wszystkich TC |
| `DT-03` | Użytkownik z aktywną firmą | TC-01, TC-03, TC-04, TC-N01 |
| `DT-05` | Istniejące konto bankowe w aktywnej firmie | TC-01, TC-05, TC-06, TC-07, TC-N02, TC-N04 |

### Definicja `DT-05` — Istniejące konto bankowe w aktywnej firmie

**Cel:** Konto bankowe gotowe do edycji lub usunięcia; niepowiązane z dokumentami.

**Precondition:** `DT-03` (aktywna firma musi istnieć).

**Sposób przygotowania:** `POST /api/BankAccount/AddUserFirmBankAccount` z tokenem JWT z `DT-02`:
```json
{
  "id": 0,
  "bankName": "ING Bank Śląski",
  "iban": "RO49AAAA1B31007593840000",
  "currency": 0,
  "isActive": true
}
```

**Oczekiwany stan bazy po:**
```
BankAccount:
  Id             = <generowany int>   ← zapamiętaj do użycia w TC-05, TC-06
  BankName       = "ING Bank Śląski"
  Iban           = "RO49AAAA1B31007593840000"
  Currency       = 0 (Ron)
  IsActive       = true
  UserFirmId     = <Id aktywnej UserFirm z DT-03>
```

**Sprzątanie:** `PUT /api/BankAccount/DeleteUserFirmBankAccounts` z body `[<Id>]` lub bezpośrednie usunięcie z DB.

**Zależności:** `DT-01`, `DT-02`, `DT-03`.
