# AddDocument — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zarejestrowany użytkownik z rolą `User` | rejestracja / seed | `DT-01` |
| Aktywny token JWT | logowanie | `DT-02` |
| Aktywna firma użytkownika + 3 domyślne serie (Factura, Proforma, Storno) | `POST /api/Firm/AddFirm/false` | `DT-03` |
| Aktywne konto bankowe w firmie | `POST /api/BankAccount/AddUserFirmBankAccount` | `DT-05` |
| Firma klienta (IsClient=true) powiązana z użytkownikiem | `POST /api/Firm/AddFirm/true` | `DT-07` (nowy) |

Dla TC-N02 (WAL-02): użytkownik z firmą, ale **bez** konta bankowego — nie stosować `DT-05`.
Dla TC-N03 (WAL-03): istniejący produkt (`DT-04`) z Id > 0, ale przesłany z błędną `name` w DTO.

---

## 2. Dane poprawne (happy path)

### `TC-01` — Wystawienie faktury z jednym nowym produktem

Warunki wstępne: `DT-01`, `DT-02`, `DT-03`, `DT-05`, `DT-07`.

Pobierz przez `GET /api/Document/GetDocumentAutofillInfo/1` (dokumentType=1, Factura):
- `documentSeries[0].id` → zapamiętaj jako `<seriesId>`
- `documentSeries[0].currentNumber` → zapamiętaj jako `<currentNumber>`
- `clients[0].id` → zapamiętaj jako `<clientId>`

Żądanie:
```
POST /api/Document/AddDocument
Authorization: Bearer <jwt_DT-02>
Content-Type: application/json
```
```json
{
  "id": 0,
  "documentNumber": null,
  "seller": null,
  "client": {
    "id": <clientId>,
    "name": "Firma Klient SRL",
    "cui": "87654321",
    "regCom": "J40/5678/2021",
    "address": "STR. CLIENTULUI NR. 2",
    "county": "ILFOV",
    "city": "VOLUNTARI"
  },
  "issueDate": "2026-05-30T00:00:00",
  "dueDate": "2026-06-30T00:00:00",
  "bankAccount": null,
  "documentSeries": {
    "id": <seriesId>,
    "seriesName": "2026",
    "firstNumber": 1,
    "currentNumber": <currentNumber>,
    "isDefault": true,
    "documentTypeId": 1,
    "documentType": { "id": 1, "name": "Factura" }
  },
  "documentType": null,
  "documentStatus": null,
  "products": [
    {
      "id": 0,
      "name": "Consultanță IT",
      "unitPrice": 500.00,
      "totalPrice": 595.00,
      "containsTva": false,
      "unitOfMeasurement": "ora",
      "tvaValue": 19,
      "quantity": 1
    }
  ]
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: oryginalny DTO żądania (z `id=0`, bez wygenerowanego Id dokumentu)
- Skutek w bazie:
  - Nowy rekord `Document`: `DocumentNumber = "2026000<currentNumber>"`, `DocumentStatusId = 1` (Unpaid), `BankAccountId = <Id DT-05>`, `ClientId = <clientId>`, `UnitPrice = 500.00`, `TotalPrice = 595.00`
  - Nowy rekord `Product`: `Name = "Consultanță IT"`, `Price = 500.00`, `UserFirmId = <UserFirmId DT-03>`
  - Nowy rekord `DocumentProduct`: powiązany z nowym `Document.Id` i nowym `Product.Id`
  - Rekord `DocumentSeries` z `id = <seriesId>`: `CurrentNumber = <currentNumber + 1>`

---

### `TC-02` — Wystawienie faktury z istniejącym produktem (`Id > 0`)

Warunki wstępne: `DT-01`, `DT-02`, `DT-03`, `DT-04`, `DT-05`, `DT-07`.

Pobierz `Id` produktu z `DT-04` przez `GET /api/Document/GetDocumentAutofillInfo/1` (pole `products[0].id`).

Żądanie: jak `TC-01`, ale w `products` użyj:
```json
{
  "id": <Id_DT-04>,
  "name": "Usługa konsultingowa",
  "unitPrice": 500.00,
  "totalPrice": 595.00,
  "containsTva": false,
  "unitOfMeasurement": "ora",
  "tvaValue": 19,
  "quantity": 1
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Skutek w bazie: nowy `Document` + nowy `DocumentProduct` powiązany z istniejącym `Product` (z `DT-04`); `Product` **nie jest** tworzony ponownie

---

## 3. Dane niepoprawne (po jednej na regułę walidacji)

### `TC-N01` — łamie `WAL-01`: brak aktywnej firmy

Warunki wstępne: `DT-01`, `DT-02` (brak `DT-03`).

Żądanie: jak `TC-01` (dowolny client id, dowolna seria).

Oczekiwany rezultat:
- Status: `400 Bad Request`
- Ciało: `{ "message": "User has no associated firm." }`
- Skutek w bazie: brak zmian

---

### `TC-N02` — łamie `WAL-02`: brak aktywnego konta bankowego

Warunki wstępne: `DT-01`, `DT-02`, `DT-03`, `DT-07` (brak `DT-05` lub konto z `IsActive=false`).

Żądanie: jak `TC-01`.

Oczekiwany rezultat:
- Status: `400 Bad Request`
- Ciało: `{ "message": "Please add a bank account, before generating a document." }`
- Skutek w bazie: brak zmian

---

### `TC-N03` — łamie `WAL-03`: istniejący produkt (`Id > 0`) z błędną nazwą

Warunki wstępne: `DT-01`, `DT-02`, `DT-03`, `DT-04`, `DT-05`, `DT-07`.

Żądanie: jak `TC-02`, ale w polu `products[0].name` użyj wartości innej niż faktyczna nazwa produktu w DB:
```json
{
  "id": <Id_DT-04>,
  "name": "BŁĘDNA NAZWA PRODUKTU",
  "unitPrice": 500.00,
  "totalPrice": 595.00,
  "containsTva": false,
  "unitOfMeasurement": "ora",
  "tvaValue": 19,
  "quantity": 1
}
```

Oczekiwany rezultat:
- Status: `500 Internal Server Error` ⚠️
- Ciało: `{ "message": "Product not found." }`
- Skutek w bazie: **CZĘŚCIOWY ZAPIS** — `Document` z `id = <nowe Id>` i `DocumentStatusId=1` już istnieje w DB (po pierwszym `CompleteAsync()`), ale bez pozycji i z `UnitPrice=0`, `TotalPrice=0`. Seria **nie** została zinkrementowana.

> [UWAGA: Partial commit — nieatomowy zapis. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 4. Wartości brzegowe

| ID | Endpoint | Pole / warunek | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|---|
| `TC-B01` | `POST AddDocument` | `products = []` (pusta lista) | Faktura bez pozycji | `200 OK`; `Document.UnitPrice = 0`, `Document.TotalPrice = 0`; seria zinkrementowana; brak `DocumentProduct` |
| `TC-B02` | `POST AddDocument` | `documentSeries = null` | Brak serii w DTO | `200 OK` (?) lub `500` — `DocumentNumber = null + null = ""`; `DocumentTypeId = null`; `IncreaseDocumentSeriesNumber(documentRequestDto.DocumentSeries.Id)` → `NullReferenceException` → `500` ⚠️ |
| `TC-B03` | `POST AddDocument` | `products[0].id = 0` z `name` istniejącego produktu (duplikat) | Próba tworzenia nowego produktu o tej samej nazwie | `500` (naruszenie unikalnego indeksu `Name+UserFirmId` w tabeli `Product`) |
| `TC-B04` | `POST AddDocument` | `client = null` | Brak klienta w DTO | `500` — `document.ClientId = documentRequestDto.Client.Id` → `NullReferenceException` |
| `TC-B05` | `POST AddDocument` | `documentSeries.currentNumber` ≠ wartość z DB | Klient przesyła stary `currentNumber` | `200 OK` — `DocumentNumber` wygenerowany z błędnym numerem; seria zinkrementowana o 1 od DB-currentNumber (nie od DTO) |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-01` | Dane rejestracji użytkownika | Wszystkie TC |
| `DT-02` | Zarejestrowany użytkownik + JWT | Wszystkie TC |
| `DT-03` | Użytkownik z aktywną firmą + 3 domyślne serie | TC-01, TC-02, TC-N02, TC-N03, TC-B01–TC-B05 |
| `DT-04` | Istniejący produkt `"Usługa konsultingowa"` | TC-02, TC-N03 |
| `DT-05` | Istniejące aktywne konto bankowe | TC-01, TC-02, TC-N03, TC-B01–TC-B05 |
| `DT-07` | Firma klienta (IsClient=true) powiązana z użytkownikiem | TC-01, TC-02, TC-N02, TC-N03, TC-B01–TC-B05 |

---

## Definicja fixture'u `DT-07`

> Pełna definicja zostanie dodana do `KATALOG_DANYCH_TESTOWYCH.md`. Poniżej skrót.

**Cel:** Firma klienta (IsClient=true) powiązana z użytkownikiem testowym — wymagana jako `document.ClientId`.

**Precondition:** `DT-03` — użytkownik musi mieć aktywną firmę.

**Sposób przygotowania:** `POST /api/Firm/AddFirm/true` (isClient=true) z JWT z `DT-02`:
```json
{
  "id": 0,
  "name": "Firma Klient SRL",
  "cui": "87654321",
  "regCom": "J40/5678/2021",
  "address": "STR. CLIENTULUI NR. 2",
  "county": "ILFOV",
  "city": "VOLUNTARI"
}
```

**Oczekiwany stan bazy po:**
```
Firm:
  Id             = <generowany int>   ← zapamiętaj jako clientId
  Name           = "Firma Klient SRL"
  Cui            = "87654321"

UserFirm:
  UserFirmId     = <generowany int>
  UserId         = <Guid użytkownika DT-02>
  FirmId         = <Id Firm powyżej>
  IsClient       = true
```

**Sprzątanie:** bezpośrednie usunięcie rekordów `UserFirm` i `Firm` z DB (brak dedykowanego endpointu DELETE firm-klienta przez API w tym procesie).

**Zależności:** `DT-01`, `DT-02`, `DT-03`.
