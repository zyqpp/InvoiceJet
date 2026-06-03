# ManageProducts — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zarejestrowany użytkownik (email + hasło) | API lub seed | `DT-01` |
| Ważny token JWT (`Authorization: Bearer`) | `POST /api/Auth/login` | `DT-02` |
| Użytkownik z aktywną firmą (`UserFirm.IsClient=false`, `User.ActiveUserFirmId != null`) | `POST /api/Firm/AddFirm/false` | `DT-03` |
| Istniejący produkt w aktywnej firmie (do testów Edit/Delete) | `POST /api/Product/AddProduct` | `DT-04` (nowy) |

Szczegóły `DT-01`, `DT-02`, `DT-03`: `../../KATALOG_DANYCH_TESTOWYCH.md`.

Nowy fixture `DT-04` — definicja poniżej w sekcji 5.

---

## 2. Dane poprawne (happy path)

### `TC-01` — GET lista produktów (z wynikami)

Warunki wstępne: `DT-02` (JWT), `DT-03` (aktywna firma), `DT-04` (co najmniej jeden produkt w firmie).

Żądanie:
```
GET /api/Product/GetAllProductsForUserId
Authorization: Bearer <jwt_z_DT-02>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: tablica co najmniej jednego `ProductDto`, np.:
```json
[
  {
    "id": 5,
    "name": "Usługa konsultingowa",
    "price": 500.00,
    "containsTva": false,
    "unitOfMeasurement": "ora",
    "tvaValue": 19
  }
]
```
- Skutek w bazie: brak zmian (read-only)

---

### `TC-02` — GET lista produktów (pusta)

Warunki wstępne: `DT-02` (JWT), `DT-03` (aktywna firma), **brak produktów** w aktywnej firmie.

Żądanie: jak w TC-01.

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `[]`
- Skutek w bazie: brak zmian

---

### `TC-03` — POST dodanie nowego produktu

Warunki wstępne: `DT-02`, `DT-03`. Produkt o nazwie `"Usługa konsultingowa"` **nie istnieje** jeszcze w aktywnej firmie.

Żądanie:
```
POST /api/Product/AddProduct
Authorization: Bearer <jwt_z_DT-02>
Content-Type: application/json

{
  "id": 0,
  "name": "Usługa konsultingowa",
  "price": 500.00,
  "containsTva": false,
  "unitOfMeasurement": "ora",
  "tvaValue": 19
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `ProductDto` z wypełnionym `id` (int > 0):
```json
{
  "id": 5,
  "name": "Usługa konsultingowa",
  "price": 500.00,
  "containsTva": false,
  "unitOfMeasurement": "ora",
  "tvaValue": 19
}
```
- Skutek w bazie: nowy rekord w tabeli `Product`:
  - `Name = "Usługa konsultingowa"`, `Price = 500.00`, `ContainsTva = false`, `UnitOfMeasurement = "ora"`, `TvaValue = 19`
  - `UserFirmId = <Id aktywnej UserFirm użytkownika>`

---

### `TC-04` — PUT edycja produktu

Warunki wstępne: `DT-02`, `DT-04` (produkt o `Id=5` istnieje w aktywnej firmie).

Żądanie:
```
PUT /api/Product/EditProduct
Authorization: Bearer <jwt_z_DT-02>
Content-Type: application/json

{
  "id": 5,
  "name": "Usługa konsultingowa (premium)",
  "price": 750.00,
  "containsTva": false,
  "unitOfMeasurement": "ora",
  "tvaValue": 19
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `ProductDto` z zaktualizowanymi polami:
```json
{
  "id": 5,
  "name": "Usługa konsultingowa (premium)",
  "price": 750.00,
  "containsTva": false,
  "unitOfMeasurement": "ora",
  "tvaValue": 19
}
```
- Skutek w bazie: rekord `Product` z `Id=5` ma zaktualizowane `Name` i `Price`; `UserFirmId` bez zmian

---

### `TC-05` — PUT usunięcie jednego produktu

Warunki wstępne: `DT-02`, `DT-04` (produkt o `Id=5` istnieje, **nie jest powiązany** z żadnym `DocumentProduct`).

Żądanie:
```
PUT /api/Product/DeleteProducts?productIds=5
Authorization: Bearer <jwt_z_DT-02>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: puste ciało
- Skutek w bazie: rekord `Product` z `Id=5` usunięty z tabeli `Product`

---

### `TC-06` — PUT usunięcie wielu produktów naraz

Warunki wstępne: `DT-02`, produkty o `Id=5` i `Id=6` istnieją, oba niepowiązane z `DocumentProduct`.

Żądanie:
```
PUT /api/Product/DeleteProducts?productIds=5&productIds=6
Authorization: Bearer <jwt_z_DT-02>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Skutek w bazie: oba rekordy usunięte z tabeli `Product`

---

## 3. Dane niepoprawne (po jednej na regułę walidacji)

### `TC-N01` — łamie `WAL-01`: użytkownik bez aktywnej firmy

Warunki wstępne: `DT-02` (JWT), ale `User.ActiveUserFirmId = NULL` (użytkownik nigdy nie dodał firmy).

Żądanie:
```
POST /api/Product/AddProduct
Authorization: Bearer <jwt_bez_firmy>
Content-Type: application/json

{
  "id": 0,
  "name": "Usługa testowa",
  "price": 100.00,
  "containsTva": false,
  "unitOfMeasurement": "buc",
  "tvaValue": 19
}
```

Oczekiwany rezultat:
- Status: `400 Bad Request`
- Komunikat: `{ "message": "User has no associated firm." }`
- Skutek w bazie: brak zmian

---

### `TC-N02` — łamie `WAL-02`: duplikat nazwy produktu w aktywnej firmie

Warunki wstępne: `DT-02`, `DT-03`, produkt `"Usługa konsultingowa"` **już istnieje** w aktywnej firmie (po wykonaniu TC-03).

Żądanie:
```
POST /api/Product/AddProduct
Authorization: Bearer <jwt_z_DT-02>
Content-Type: application/json

{
  "id": 0,
  "name": "Usługa konsultingowa",
  "price": 200.00,
  "containsTva": true,
  "unitOfMeasurement": "buc",
  "tvaValue": 9
}
```

Oczekiwany rezultat:
- Status: `500 Internal Server Error` ⚠️ [powinno być `400`]
- Komunikat: `{ "message": "Product with name Usługa konsultingowa already exists." }`
- Skutek w bazie: brak zmian

---

### `TC-N03` — łamie `WAL-03`: edycja nieistniejącego produktu

Warunki wstępne: `DT-02`, `DT-03`. Brak produktu o `Id=99999`.

Żądanie:
```
PUT /api/Product/EditProduct
Authorization: Bearer <jwt_z_DT-02>
Content-Type: application/json

{
  "id": 99999,
  "name": "Produkt nieistniejący",
  "price": 100.00,
  "containsTva": false,
  "unitOfMeasurement": "buc",
  "tvaValue": 19
}
```

Oczekiwany rezultat:
- Status: `500 Internal Server Error` ⚠️ [powinno być `400` lub `404`]
- Komunikat: `{ "message": "Product not found." }`
- Skutek w bazie: brak zmian

---

### `TC-N04` — łamie `WAL-04`: usunięcie nieistniejącego produktu

Warunki wstępne: `DT-02`. Brak produktu o `Id=99999`.

Żądanie:
```
PUT /api/Product/DeleteProducts?productIds=99999
Authorization: Bearer <jwt_z_DT-02>
```

Oczekiwany rezultat:
- Status: `500 Internal Server Error` ⚠️ [powinno być `400`]
- Komunikat: `{ "message": "Product not found." }`
- Skutek w bazie: brak zmian

---

### `TC-N05` — łamie `WAL-05`: usunięcie produktu powiązanego z fakturą

Warunki wstępne: `DT-02`, produkt o `Id=5` istnieje i jest powiązany z co najmniej jednym rekordem `DocumentProduct` (tj. był użyty na fakturze).

Żądanie:
```
PUT /api/Product/DeleteProducts?productIds=5
Authorization: Bearer <jwt_z_DT-02>
```

Oczekiwany rezultat:
- Status: `400 Bad Request`
- Komunikat: `{ "message": "Can't delete. Product Usługa konsultingowa is associated with an invoice." }`
- Skutek w bazie: brak zmian (produkt pozostaje)

---

## 4. Wartości brzegowe

| ID | Endpoint | Pole | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|---|
| `TC-B01` | AddProduct | `name` | `""` (pusty string) | `200 OK` — `ProductWithSameNameExistsException` nie wyrzuci jeśli nie ma duplikatu; produkt o nazwie `""` jest zapisywany [UWAGA: brak walidacji pustej nazwy — WYMAGA WERYFIKACJI] |
| `TC-B02` | AddProduct | `price` | `0.00` | `200 OK` — brak walidacji wartości minimalnej ceny |
| `TC-B03` | AddProduct | `price` | `-100.00` | `200 OK` — brak walidacji ujemnej ceny [UWAGA — WYMAGA WERYFIKACJI] |
| `TC-B04` | AddProduct | `tvaValue` | `0` | `200 OK` — stawka 0% (poprawna dla niektórych usług) |
| `TC-B05` | AddProduct | `unitOfMeasurement` | `null` | `200 OK` — pole nullable; baza akceptuje NULL |
| `TC-B06` | AddProduct | `name` | 450-znakowy string | `200 OK` — `nvarchar(450)` to limit DB; dłuższy string spowoduje `DbUpdateException` → 500 |
| `TC-B07` | DeleteProducts | `productIds` | `[]` (pusta tablica) | `200 OK` — pętla nie wykonana, `CompleteAsync()` bez zmian |
| `TC-B08` | AddProduct | `name` | Nazwa unikalna globalnie ale duplikat w innej firmie | `200 OK` — walidacja serwisu sprawdza tylko aktywną firmę; ale globalny indeks DB może odrzucić → `DbUpdateException` → 500 [UWAGA — WYMAGA WERYFIKACJI] |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-01` | Dane rejestracji użytkownika | precondition wszystkich TC |
| `DT-02` | Zarejestrowany użytkownik + JWT | precondition wszystkich TC |
| `DT-03` | Użytkownik z aktywną firmą | TC-01, TC-03, TC-04, TC-05, TC-06, TC-N02 |
| `DT-04` | Istniejący produkt w aktywnej firmie | TC-01, TC-04, TC-05, TC-06, TC-N05 |

### Definicja `DT-04` — Istniejący produkt w aktywnej firmie

**Cel:** Produkt gotowy do edycji lub usunięcia; niepowiązany z dokumentami.

**Precondition:** `DT-03` (aktywna firma musi istnieć).

**Sposób przygotowania:** `POST /api/Product/AddProduct` z tokenem JWT z `DT-02`:
```json
{
  "id": 0,
  "name": "Usługa konsultingowa",
  "price": 500.00,
  "containsTva": false,
  "unitOfMeasurement": "ora",
  "tvaValue": 19
}
```

**Oczekiwany stan bazy po:**
```
Product:
  Id             = <generowany int>   ← zapamiętaj do użycia w TC-04, TC-05
  Name           = "Usługa konsultingowa"
  Price          = 500.00
  ContainsTva    = false
  UnitOfMeasurement = "ora"
  TvaValue       = 19
  UserFirmId     = <Id aktywnej UserFirm z DT-03>
```

**Sprzątanie:** `PUT /api/Product/DeleteProducts?productIds=<Id>` lub bezpośrednie usunięcie z DB.

**Zależności:** `DT-01`, `DT-02`, `DT-03`.
