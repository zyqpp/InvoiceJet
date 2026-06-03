# DeleteDocuments — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zalogowany użytkownik z rolą `User` + JWT | seed / rejestracja | `DT-01` |
| Aktywna firma użytkownika (`UserFirm`) | `POST /api/Firm/AddFirm/false` | `DT-03` |
| Firma klienta | `POST /api/Firm/AddFirm/true` | `DT-07` |
| Istniejący dokument (faktura) do usunięcia | `POST /api/Document/AddDocument` | `DT-08` |

---

## 2. Dane poprawne (happy path)

### `TC-01` — Usunięcie jednego dokumentu

Warunki wstępne: `DT-01`, `DT-03`, `DT-07`, `DT-08` (dokument `id=3` należący do user A).

Żądanie:
```http
PUT /api/Document/DeleteDocuments
Authorization: Bearer <token>
Content-Type: application/json

[3]
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `{ "message": "Documents deleted successfully." }`
- Skutek w bazie: rekord `Document(id=3)` usunięty; rekordy `DocumentProduct` powiązane z `DocumentId=3` usunięte

---

### `TC-02` — Usunięcie wielu dokumentów

Warunki wstępne: `DT-01`, `DT-03`, `DT-07`, dwa dokumenty: `id=3`, `id=4`.

Żądanie:
```http
PUT /api/Document/DeleteDocuments
Authorization: Bearer <token>
Content-Type: application/json

[3, 4]
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `{ "message": "Documents deleted successfully." }`
- Skutek w bazie: oba dokumenty i ich pozycje usunięte

---

### `TC-03` — Pusta tablica (brak efektu)

Warunki wstępne: `DT-01`.

Żądanie:
```http
PUT /api/Document/DeleteDocuments
Authorization: Bearer <token>
Content-Type: application/json

[]
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `{ "message": "Documents deleted successfully." }`
- Skutek w bazie: brak zmian
- Uwaga: brak sygnalizacji, że nic nie usunięto

---

## 3. Dane niepoprawne (po jednej na regułę walidacji)

Brak reguł WAL. Poniżej przypadki bezpieczeństwa:

### `TC-N01` — Nieistniejące `documentId` ⚠️

Warunki wstępne: `DT-01`.

Żądanie:
```http
PUT /api/Document/DeleteDocuments
Authorization: Bearer <token>
Content-Type: application/json

[999999]
```

Oczekiwany rezultat (faktyczne, niestandardowe):
- Status: `200 OK`
- Odpowiedź: `{ "message": "Documents deleted successfully." }`
- Skutek w bazie: brak zmian

> Brak informacji, że dokument nie istniał.

---

### `TC-N02` — Brak JWT

Żądanie:
```http
PUT /api/Document/DeleteDocuments
Content-Type: application/json

[3]
```

Oczekiwany rezultat:
- Status: `401 Unauthorized`
- Skutek w bazie: brak zmian

---

### `TC-N03` — Usunięcie dokumentu innego użytkownika ⚠️

Warunki wstępne: `DT-01` (user A), user B z dokumentem `id=7`.

Żądanie (user A z własnym JWT):
```http
PUT /api/Document/DeleteDocuments
Authorization: Bearer <token-user-A>
Content-Type: application/json

[7]
```

Oczekiwany rezultat (faktyczne — luka bezpieczeństwa):
- Status: `200 OK`
- Odpowiedź: `{ "message": "Documents deleted successfully." }`
- Skutek w bazie: dokument użytkownika B usunięty — **krytyczna luka** ⚠️

---

## 4. Wartości brzegowe

| ID | Pole | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|
| `TC-B01` | `documentIds` | `[]` | `200 OK` bez zmian |
| `TC-B02` | `documentIds` | `[0]` | `200 OK` bez zmian (id=0 nie istnieje) |
| `TC-B03` | `documentIds` | `[-1]` | `200 OK` bez zmian |
| `TC-B04` | `documentIds` | `[3, 3, 3]` | `200 OK`; dokument `id=3` usunięty raz (EF deduplikuje lub ignoruje duplikaty) |
| `TC-B05` | Body | `null` | `400 Bad Request` (framework nie może deserializować `null` → `int[]`) |
| `TC-B06` | Dokument z pozycjami | `id=3` z 5 pozycjami `DocumentProduct` | `200 OK`; wszystkie pozycje i dokument usunięte |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-01` | Zalogowany użytkownik + JWT | `TC-01`–`TC-03`, `TC-N01`–`TC-N03`, `TC-B01`–`TC-B06` |
| `DT-03` | Aktywna firma użytkownika (UserFirm) | `TC-01`, `TC-02` |
| `DT-07` | Firma klienta | `TC-01`, `TC-02` |
| `DT-08` | Istniejący dokument `id=3` | `TC-01`, `TC-B04`, `TC-B06` |
