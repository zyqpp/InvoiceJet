# ManageBankAccounts — Kontrakt API

---

## `API-14` — GET /api/BankAccount/GetUserFirmBankAccounts

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `GET` |
| Ścieżka | `/api/BankAccount/GetUserFirmBankAccounts` |
| Kontroler | `BankAccountController.cs › BankAccountController.GetUserFirmBankAccounts` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `BankAccountController`) |

### Parametry trasy / zapytania

Brak parametrów wejściowych. Tożsamość użytkownika pochodzi z JWT claim `userId`.

### Ciało żądania

Brak.

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `ICollection<BankAccountDto>` | Powodzenie; może być pusta kolekcja `[]` |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

Przykład odpowiedzi (`200 OK` — lista kont):
```json
[
  {
    "id": 3,
    "bankName": "ING Bank Śląski",
    "iban": "RO49AAAA1B31007593840000",
    "currency": 0,
    "isActive": true
  },
  {
    "id": 4,
    "bankName": "BRD - Groupe Société Générale",
    "iban": "RO49BRDE410SV04411864100",
    "currency": 1,
    "isActive": false
  }
]
```

Przykład odpowiedzi (`200 OK` — brak kont):
```json
[]
```

> Pole `currency`: `0` = `Ron`, `1` = `Euro` (enum `CurrencyEnum`).

---

## `API-15` — POST /api/BankAccount/AddUserFirmBankAccount

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/BankAccount/AddUserFirmBankAccount` |
| Kontroler | `BankAccountController.cs › BankAccountController.AddUserFirmBankAccount` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `BankAccountController`) |

### Parametry trasy / zapytania

Brak.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `BankAccountDto` | `[FromBody]` |

Pole `id` przy tworzeniu powinno być `0` (lub pominięte) — DB nadaje wartość.

Przykład żądania (dodanie aktywnego konta w EUR):
```json
{
  "id": 0,
  "bankName": "ING Bank Śląski",
  "iban": "RO49AAAA1B31007593840000",
  "currency": 1,
  "isActive": true
}
```

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `BankAccountDto` | Konto dodane; DTO zawiera `Id` nadany przez DB |
| `400 Bad Request` | `{ "message": "User has no associated firm." }` | Brak aktywnej firmy (WAL-01) |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

Przykład odpowiedzi (`200 OK`):
```json
{
  "id": 5,
  "bankName": "ING Bank Śląski",
  "iban": "RO49AAAA1B31007593840000",
  "currency": 1,
  "isActive": true
}
```

> Efekt uboczny: jeśli `isActive = true`, wszystkie inne konta bankowe aktywnej firmy zostaną dezaktywowane (`IsActive = false`) w tym samym commicie.

---

## `API-16` — PUT /api/BankAccount/EditUserFirmBankAccount

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/BankAccount/EditUserFirmBankAccount` |
| Kontroler | `BankAccountController.cs › BankAccountController.EditUserFirmBankAccount` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `BankAccountController`) |

### Parametry trasy / zapytania

Brak. `Id` konta do edycji przekazywany w body w polu `id`.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `BankAccountDto` | `[FromBody]` |

Pole `id` musi odpowiadać istniejącemu kontu bankowemu.

Przykład żądania:
```json
{
  "id": 5,
  "bankName": "ING Bank Śląski",
  "iban": "RO49AAAA1B31007593840000",
  "currency": 0,
  "isActive": true
}
```

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `BankAccountDto` | Konto zaktualizowane |
| `500 Internal Server Error` | `{ "message": "Bank account not found." }` | Konto o danym `id` nie istnieje (WAL-02) [UWAGA: powinno być `400`] |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

Przykład odpowiedzi (`200 OK`):
```json
{
  "id": 5,
  "bankName": "ING Bank Śląski",
  "iban": "RO49AAAA1B31007593840000",
  "currency": 0,
  "isActive": true
}
```

> Efekt uboczny: jeśli `isActive = true`, wszystkie inne konta bankowe firmy zostaną dezaktywowane — poza tym edytowanym.

---

## `API-17` — PUT /api/BankAccount/DeleteUserFirmBankAccounts

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `PUT` |
| Ścieżka | `/api/BankAccount/DeleteUserFirmBankAccounts` |
| Kontroler | `BankAccountController.cs › BankAccountController.DeleteUserFirmBankAccounts` |
| Autoryzacja | `[Authorize(Roles = "User")]` (klasa `BankAccountController`) |

> [UWAGA: Endpoint używa metody `PUT` do usuwania zasobów — niezgodność z konwencją REST (`DELETE`). Odzwierciedlono stan z kodu bez zmiany metody. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Parametry trasy / zapytania

Brak parametrów query/trasy.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `int[]` | `[FromBody]` (tablica ID kont) |

Przykład żądania (usunięcie jednego konta):
```json
[5]
```

Przykład żądania (usunięcie wielu kont):
```json
[5, 6]
```

> Różnica względem `DeleteProducts` (P-09): tam `productIds` były w **query string**, tu `bankAccountIds` są w **body** `[FromBody]`.

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | — | Wszystkie konta usunięte pomyślnie |
| `400 Bad Request` | `{ "message": "Can't delete. Bank account is associated with documents." }` | Konto powiązane z dokumentem (WAL-04) |
| `500 Internal Server Error` | `{ "message": "Bank account not found." }` | Konto o danym ID nie istnieje (WAL-03) [UWAGA: powinno być `400`] |
| `401 Unauthorized` | — | Brak lub niepoprawny token JWT |
| `403 Forbidden` | — | Brak roli `"User"` |

Przykład odpowiedzi (`200 OK`): puste ciało.

Przykład odpowiedzi (`400 Bad Request`):
```json
{
  "message": "Can't delete. Bank account is associated with documents."
}
```
