# TransformToStorno — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zalogowany użytkownik z rolą `User` + JWT | seed / rejestracja | `DT-01` |
| Aktywna firma użytkownika (`UserFirm`) | `POST /api/Firm/AddFirm/false` | `DT-03` |
| Firma klienta | `POST /api/Firm/AddFirm/true` | `DT-07` |
| Istniejący dokument (faktura) — `DocumentTypeId=1` | `POST /api/Document/AddDocument` | `DT-08` |

---

## 2. Dane poprawne (happy path)

### `TC-01` — Storno jednego dokumentu

Warunki wstępne: `DT-01`, `DT-03`, `DT-07`, `DT-08` (dokument `id=3`, `DocumentTypeId=1`).

Żądanie:
```http
PUT /api/Document/TransformToStorno
Authorization: Bearer <token>
Content-Type: application/json

[3]
```

Oczekiwany rezultat:
- Status: `200 OK`
- Body: puste
- Skutek w bazie: `Document(id=3).DocumentTypeId = 3` (Storno); pozostałe pola bez zmian

---

### `TC-02` — Storno wielu dokumentów

Warunki wstępne: `DT-01`, `DT-03`, `DT-07`, dwa dokumenty: `id=3`, `id=4`.

Żądanie:
```http
PUT /api/Document/TransformToStorno
Authorization: Bearer <token>
Content-Type: application/json

[3, 4]
```

Oczekiwany rezultat:
- Status: `200 OK`
- Skutek w bazie: oba dokumenty z `DocumentTypeId=3`

---

### `TC-03` — Pusta tablica (brak efektu)

Warunki wstępne: `DT-01`.

Żądanie:
```http
PUT /api/Document/TransformToStorno
Authorization: Bearer <token>
Content-Type: application/json

[]
```

Oczekiwany rezultat:
- Status: `200 OK`
- Body: puste
- Skutek w bazie: brak zmian

---

## 3. Dane niepoprawne (po jednej na regułę walidacji)

### `TC-N01` — łamie WAL-01: użytkownik bez firmy ⚠️

Warunki wstępne: `DT-01` (user bez `UserFirm`).

Żądanie:
```http
PUT /api/Document/TransformToStorno
Authorization: Bearer <token>
Content-Type: application/json

[3]
```

Oczekiwany rezultat (niestandardowy):
- Status: `500 Internal Server Error`
- Body: `{ "message": "User firm not found." }`

> ⚠️ Powinno być `400 Bad Request` — `new Exception(...)` zamiast `UserHasNoAssociatedFirmException`.

---

### `TC-N02` — łamie WAL-02: nieistniejący documentId ⚠️

Warunki wstępne: `DT-01`, `DT-03`.

Żądanie:
```http
PUT /api/Document/TransformToStorno
Authorization: Bearer <token>
Content-Type: application/json

[999999]
```

Oczekiwany rezultat (niestandardowy):
- Status: `500 Internal Server Error`
- Body: `{ "message": "Document not found." }`

> ⚠️ Powinno być `404 Not Found`.

---

### `TC-N03` — Brak JWT

Żądanie:
```http
PUT /api/Document/TransformToStorno
Content-Type: application/json

[3]
```

Oczekiwany rezultat:
- Status: `401 Unauthorized`

---

## 4. Wartości brzegowe

| ID | Pole | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|
| `TC-B01` | `documentIds` | `[]` | `200 OK` bez zmian |
| `TC-B02` | `documentIds` | `[3, 999999]` — pierwszy poprawny, drugi nieistnieje | `200 OK` dla doc=3 (zapisany!), potem `500` przy 999999 — **częściowe storno** ⚠️ |
| `TC-B03` | Dokument już Storno | `DocumentTypeId=3` → ponowne storno | `200 OK`; `DocumentTypeId` pozostaje `3` (idempotentne) |
| `TC-B04` | Dokument cudzego użytkownika | id dokumentu innego usera | `500 Internal Server Error` ("Document not found.") — ownership check aktywny ✅ |
| `TC-B05` | `documentIds` | `null` | `400 Bad Request` (framework nie może deserializować `null` → `int[]`) |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-01` | Zalogowany użytkownik + JWT | wszystkie TC |
| `DT-03` | Aktywna firma użytkownika (UserFirm) | `TC-01`–`TC-03`, `TC-N02`, `TC-B01`–`TC-B05` |
| `DT-07` | Firma klienta | `TC-01`, `TC-02` |
| `DT-08` | Istniejący dokument faktury `id=3` | `TC-01`, `TC-02`, `TC-B02`, `TC-B03` |
