# ManageDocumentSeries — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zarejestrowany użytkownik z rolą `User` | rejestracja / seed | `DT-01` |
| Aktywny token JWT | logowanie | `DT-02` |
| Aktywna firma użytkownika (+ 3 domyślne serie: Factura, Factura Proforma, Factura Storno) | `POST /api/Firm/AddFirm/false` | `DT-03` |
| Istniejąca seria dokumentów gotowa do edycji / usunięcia | `POST /api/DocumentSeries/AddDocumentSeries` | `DT-06` |

Dla TC-N01 (brak firmy) wymagany jest użytkownik **bez** aktywnej firmy — nie stosować `DT-03`, zatrzymać się na `DT-02`.

---

## 2. Dane poprawne (happy path)

### `TC-01` — Pobranie listy serii dla użytkownika z aktywną firmą

Warunki wstępne: `DT-01`, `DT-02`, `DT-03`.

Żądanie:
```
GET /api/DocumentSeries/GetAllDocumentSeriesForUserId
Authorization: Bearer <jwt_DT-02>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: lista 3 obiektów `DocumentSeriesDto` z polami `id`, `seriesName`, `firstNumber`, `currentNumber`, `isDefault`, `documentTypeId`, `documentType`
- Minimalna zawartość (3 serie z `DT-03`):
  ```json
  [
    { "seriesName": "2026", "isDefault": true, "documentType": { "id": 1, "name": "Factura" } },
    { "seriesName": "2026", "isDefault": true, "documentType": { "id": 2, "name": "Factura Proforma" } },
    { "seriesName": "2026", "isDefault": true, "documentType": { "id": 3, "name": "Factura Storno" } }
  ]
  ```
- Skutek w bazie: brak zmian (read-only)

---

### `TC-02` — Dodanie nowej serii dokumentów

Warunki wstępne: `DT-01`, `DT-02`, `DT-03`.

Żądanie:
```
POST /api/DocumentSeries/AddDocumentSeries
Authorization: Bearer <jwt_DT-02>
Content-Type: application/json
```
```json
{
  "id": 0,
  "seriesName": "2026-A",
  "firstNumber": 1,
  "currentNumber": 1,
  "isDefault": false,
  "documentTypeId": 2,
  "documentType": {
    "id": 2,
    "name": "Factura Proforma"
  }
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: puste ciało
- Skutek w bazie: nowy rekord w tabeli `DocumentSeries`:
  ```
  SeriesName     = "2026-A"
  FirstNumber    = 1
  CurrentNumber  = 1
  IsDefault      = false
  DocumentTypeId = 2
  UserFirmId     = <Id aktywnej UserFirm z DT-03>
  ```
- Nowe `Id` serii **nie jest** zwracane w odpowiedzi; aby je pobrać, wywołaj `GET /api/DocumentSeries/GetAllDocumentSeriesForUserId`

---

### `TC-03` — Aktualizacja istniejącej serii

Warunki wstępne: `DT-01`, `DT-02`, `DT-03`, `DT-06` (zapamiętaj `Id` serii pobranego przez GET po dodaniu `DT-06`).

Żądanie:
```
PUT /api/DocumentSeries/UpdateDocumentSeries
Authorization: Bearer <jwt_DT-02>
Content-Type: application/json
```
```json
{
  "id": <Id_DT-06>,
  "seriesName": "2026-UPDATED",
  "firstNumber": 1,
  "currentNumber": 5,
  "isDefault": false,
  "documentTypeId": 1,
  "documentType": {
    "id": 1,
    "name": "Factura"
  }
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: puste ciało
- Skutek w bazie: rekord `DocumentSeries` z `Id = <Id_DT-06>` zmienił `SeriesName = "2026-UPDATED"` i `CurrentNumber = 5`

---

### `TC-04` — Usunięcie pojedynczej serii

Warunki wstępne: `DT-01`, `DT-02`, `DT-03`, `DT-06`.

Żądanie:
```
PUT /api/DocumentSeries/DeleteDocumentSeries?documentSeriesIds=<Id_DT-06>
Authorization: Bearer <jwt_DT-02>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: puste ciało
- Skutek w bazie: rekord `DocumentSeries` z `Id = <Id_DT-06>` usunięty

---

### `TC-05` — Usunięcie wielu serii jednocześnie

Warunki wstępne: `DT-01`, `DT-02`, `DT-03`; najpierw dodaj dwie dodatkowe serie przez `TC-02` (zapamiętaj ich `Id_A` i `Id_B`).

Żądanie:
```
PUT /api/DocumentSeries/DeleteDocumentSeries?documentSeriesIds=<Id_A>&documentSeriesIds=<Id_B>
Authorization: Bearer <jwt_DT-02>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: puste ciało
- Skutek w bazie: obydwa rekordy `DocumentSeries` usunięte jednocześnie (batch `RemoveRangeAsync` + jeden `CompleteAsync`)

---

## 3. Dane niepoprawne (po jednej na regułę walidacji)

### `TC-N01` — łamie `WAL-01`: brak aktywnej firmy użytkownika (AddDocumentSeries)

Warunki wstępne: `DT-01`, `DT-02` (brak `DT-03` — użytkownik **nie ma** aktywnej firmy).

Żądanie:
```
POST /api/DocumentSeries/AddDocumentSeries
Authorization: Bearer <jwt_DT-02>
Content-Type: application/json
```
```json
{
  "id": 0,
  "seriesName": "2026-X",
  "firstNumber": 1,
  "currentNumber": 1,
  "isDefault": false,
  "documentTypeId": 1,
  "documentType": {
    "id": 1,
    "name": "Factura"
  }
}
```

Oczekiwany rezultat:
- Status: `400 Bad Request`
- Ciało odpowiedzi: **plain string** (nie JSON): `User has no associated firm.`
- Mechanizm: `UserHasNoAssociatedFirmException` wychwycony przez `catch (Exception ex)` w `DocumentSeriesController.AddDocumentSeries` → `return BadRequest(ex.Message)` — **omija ExceptionMiddleware**
- Skutek w bazie: brak zmian

> [UWAGA: Odpowiedź `400` zawiera plain string, a nie `{ "message": "..." }`. Niespójność z innymi endpointami obsługiwanymi przez ExceptionMiddleware. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

### `TC-N02` — łamie `WAL-02`: aktualizacja nieistniejącej serii (UpdateDocumentSeries)

Warunki wstępne: `DT-01`, `DT-02`, `DT-03`. Użyj `id = 99999` — nieistniejący rekord.

Żądanie:
```
PUT /api/DocumentSeries/UpdateDocumentSeries
Authorization: Bearer <jwt_DT-02>
Content-Type: application/json
```
```json
{
  "id": 99999,
  "seriesName": "GHOST",
  "firstNumber": 1,
  "currentNumber": 1,
  "isDefault": false,
  "documentTypeId": 1,
  "documentType": {
    "id": 1,
    "name": "Factura"
  }
}
```

Oczekiwany rezultat:
- Status: `500 Internal Server Error` ⚠️
- Ciało odpowiedzi (przez ExceptionMiddleware): `{ "message": "Document Series not found" }`
- Mechanizm: `Query().FirstOrDefaultAsync(ds => ds.Id == 99999)` → null → `throw new Exception("Document Series not found")` → ExceptionMiddleware catch-all → 500
- Skutek w bazie: brak zmian

> [UWAGA: WAL-02 daje `500` zamiast `400`/`404`. Brak `DocumentSeriesNotFoundException`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 4. Wartości brzegowe

| ID | Endpoint | Pole / warunek | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|---|
| `TC-B01` | `GET GetAllDocumentSeriesForUserId` | brak aktywnej firmy | użytkownik bez `UserFirm` (tylko `DT-02`) | `200 OK` z `[]` — serwis zwraca pustą listę, brak wyjątku |
| `TC-B02` | `PUT DeleteDocumentSeries` | brak parametrów w query | żądanie bez `?documentSeriesIds=...` | `200 OK`; `documentSeriesIds = []` → `Where(...Contains)` → `RemoveRangeAsync([])` → `CompleteAsync` bez zmian |
| `TC-B03` | `PUT DeleteDocumentSeries` | nieistniejące ID | `?documentSeriesIds=99999` | `200 OK`; ID zignorowany po cichu; brak informacji, że seria nie istniała |
| `TC-B04` | `POST AddDocumentSeries` | `documentType = null` | `"documentType": null` lub pole pominięte | `400 Bad Request` z `NullReferenceException` (plain text) — `src.DocumentType!.Id` w AutoMapper lub serwisie rzuca null ref; przechwycony przez try/catch kontrolera |
| `TC-B05` | `POST AddDocumentSeries` | duplikat `seriesName` | seria `"2026-A"` z `DocumentTypeId=1` dodana ponownie | `200 OK` — brak indeksu unikalnego w tabeli `DocumentSeries`; zduplikowane serie dozwolone |
| `TC-B06` | `PUT UpdateDocumentSeries` | `documentType = null` | `"documentType": null` lub pole pominięte | `500 Internal Server Error` — `documentSeriesDto.DocumentType!.Id` rzuca null ref w serwisie; brak try/catch w kontrolerze `UpdateDocumentSeries` → ExceptionMiddleware |
| `TC-B07` | `PUT DeleteDocumentSeries` | mix istniejący + nieistniejący ID | `?documentSeriesIds=<Id_DT-06>&documentSeriesIds=99999` | `200 OK`; istniejący rekord usunięty; ID 99999 zignorowany po cichu |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-01` | Dane rejestracji użytkownika | Wszystkie TC |
| `DT-02` | Zarejestrowany użytkownik + JWT | Wszystkie TC |
| `DT-03` | Użytkownik z aktywną firmą + 3 domyślne serie dokumentów | TC-01, TC-02, TC-03, TC-04, TC-05, TC-N02, TC-B03, TC-B04, TC-B05, TC-B06, TC-B07 |
| `DT-06` | Istniejąca seria dokumentów do edycji / usunięcia | TC-03, TC-04, TC-B07 |

---

## Definicja fixture'u `DT-06`

> Pełna definicja dodana do `../../KATALOG_DANYCH_TESTOWYCH.md`. Poniżej skrót dla tego procesu.

**Cel:** Seria dokumentów `"2026-TEST"` gotowa do edycji lub usunięcia; nie powiązana z dokumentami.

**Precondition:** `DT-03` — aktywna firma musi istnieć (`User.ActiveUserFirmId != null`).

**Sposób przygotowania:** `POST /api/DocumentSeries/AddDocumentSeries` z tokenem JWT z `DT-02`:
```json
{
  "id": 0,
  "seriesName": "2026-TEST",
  "firstNumber": 1,
  "currentNumber": 1,
  "isDefault": false,
  "documentTypeId": 1,
  "documentType": {
    "id": 1,
    "name": "Factura"
  }
}
```

**Oczekiwany stan bazy po:**
```
DocumentSeries:
  Id             = <generowany int>   ← zapamiętaj do użycia w TC-03, TC-04
  SeriesName     = "2026-TEST"
  FirstNumber    = 1
  CurrentNumber  = 1
  IsDefault      = false
  DocumentTypeId = 1
  UserFirmId     = <Id aktywnej UserFirm z DT-03>
```

**Sprzątanie:** `PUT /api/DocumentSeries/DeleteDocumentSeries?documentSeriesIds=<Id>` lub bezpośrednie usunięcie z DB.

**Zależności:** `DT-01`, `DT-02`, `DT-03`.
