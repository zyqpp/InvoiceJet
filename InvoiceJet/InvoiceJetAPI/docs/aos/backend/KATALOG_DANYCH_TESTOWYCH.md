# Katalog danych testowych — InvoiceJetAPI

**Data aktualizacji:** 2026-05-30 (zaktualizowano: DT-08 dodany dla P-13–P-19)
**Cel:** Wielokrotnie używane fixture'y / seed danych do testów .NET, API, E2E i testów ręcznych.

---

## 1. Spis fixture'ów

| ID | Nazwa | Krótki opis | Wymagane przez |
|---|---|---|---|
| `DT-01` | Dane rejestracji nowego użytkownika | Kompletny payload do `POST /api/Auth/register`; użytkownik **nie istnieje** w bazie | `P-01` (happy path) |
| `DT-02` | Zarejestrowany użytkownik + dane logowania | Użytkownik istniejący w bazie (po rejestracji) + payload do `POST /api/Auth/login` | `P-02` (happy path), jako precondition innych procesów wymagających JWT |
| `DT-03` | Użytkownik z aktywną firmą | Stan bazy po pomyślnym `TC-01` z `P-03`: użytkownik ma powiązaną firmę (`IsClient=false`), `ActiveUserFirmId` ustawione, 3 × `DocumentSeries` obecne | `P-03` `TC-02`, przyszłe: `P-05` EditFirm, `P-06` GetUserActiveFirm, `P-07` GetUserClientFirms, procesy dokumentów |
| `DT-04` | Istniejący produkt w aktywnej firmie | Produkt `"Usługa konsultingowa"` (price=500, tvaValue=19) dodany do aktywnej firmy użytkownika przez `POST /api/Product/AddProduct`; **nie jest** powiązany z żadnym dokumentem | `P-09` TC-01, TC-04, TC-05, TC-06, TC-N05 |
| `DT-05` | Istniejące konto bankowe w aktywnej firmie | Konto `"ING Bank Śląski"` (IBAN=RO49AAAA1B31007593840000, Currency=Ron, IsActive=true) dodane przez `POST /api/BankAccount/AddUserFirmBankAccount`; **nie jest** powiązane z żadnym dokumentem | `P-10` TC-01, TC-05, TC-06, TC-07, TC-N02, TC-N04 |
| `DT-06` | Istniejąca seria dokumentów w aktywnej firmie | Seria `"2026-TEST"` (DocumentTypeId=1 → Factura, IsDefault=false) dodana przez `POST /api/DocumentSeries/AddDocumentSeries`; **nie jest** powiązana z żadnym dokumentem | `P-11` TC-03, TC-04, TC-B07 |
| `DT-07` | Firma klienta powiązana z użytkownikiem | Firma `"Firma Klient SRL"` (CUI=87654321) dodana przez `POST /api/Firm/AddFirm/true` (IsClient=true); wymagana jako `Document.ClientId` | `P-12` TC-01, TC-02, TC-N02, TC-N03 |
| `DT-08` | Istniejący dokument faktury | Faktura `"20260001"` (DocumentTypeId=1, DocumentStatusId=1/Unpaid, TotalPrice=595.00) utworzona przez `POST /api/Document/AddDocument`; wymagana do edycji, usunięcia, stornu i odczytu | `P-13`–`P-19` TC używające istniejącego dokumentu |

---

## 2. Szczegóły fixture'ów

### `DT-01` — Dane rejestracji nowego użytkownika

Cel: rejestracja świeżego konta w środowisku testowym.

Dane (payload `POST /api/Auth/register`):
```json
{
  "firstName": "Anna",
  "lastName":  "Testowa",
  "email":     "tester+01@invoicejet.test",
  "password":              "Strong@123",
  "passwordConfirmation":  "Strong@123"
}
```

Oczekiwany stan bazy przed: brak rekordu `User` z `Email = "tester+01@invoicejet.test"`.

Oczekiwany stan bazy po: nowy rekord w tabeli `User`:
```
Id             = <generowany Guid>
FirstName      = "Anna"
LastName       = "Testowa"
Email          = "tester+01@invoicejet.test"
PasswordHash   = <BCrypt hash "Strong@123">
Role           = "User"
ActiveUserFirmId = NULL
```

Sposób przygotowania:
- **Wariant A (test integracyjny .NET):** bezpośrednie wstawienie przez `DbContext` bez wywoływania API; upewnij się, że PasswordHash jest zahashowany BCrypt.
- **Wariant B (API black-box):** wywołanie `POST /api/Auth/register` z powyższym body; odpowiedź zawiera `{ "token": "..." }`.
- **Wariant C (E2E / ręcznie):** rejestracja przez formularz w UI Angular.

Sprzątanie: usunięcie rekordu `User` z `Email = "tester+01@invoicejet.test"` po teście.

Zależności: brak.

---

### `DT-02` — Zarejestrowany użytkownik + dane logowania

Cel: zalogowanie istniejącego użytkownika i uzyskanie JWT do dalszych testów.

Precondition: `DT-01` — użytkownik `"tester+01@invoicejet.test"` musi istnieć w bazie.

Dane (payload `POST /api/Auth/login`):
```json
{
  "email":    "tester+01@invoicejet.test",
  "password": "Strong@123"
}
```

Oczekiwany rezultat: odpowiedź `{ "token": "<jwt>" }` — token ważny 10 minut.

Sposób przygotowania:
- **Wariant A (.NET):** seed `DT-01` przez `DbContext`, następnie wywołanie `POST /api/Auth/login` w teście lub ekstrakcja JWT z claims serwisu.
- **Wariant B (API):** wywołanie `POST /api/Auth/register` z `DT-01`, potem `POST /api/Auth/login` — użyj zwróconego `token` jako `Bearer` w nagłówku `Authorization`.
- **Wariant C (E2E / ręcznie):** zalogowanie przez formularz UI Angular.

Sprzątanie: po zakończeniu testów usuń użytkownika `DT-01`.

Zależności: `DT-01`.

---

### `DT-03` — Użytkownik z aktywną firmą

Cel: dostarczenie stanu bazy, w którym użytkownik ma już aktywną własną firmę — precondition dla scenariuszy wymagających `user.ActiveUserFirm != null`.

Precondition: `DT-02` — użytkownik `"tester+01@invoicejet.test"` musi istnieć w bazie. Seed `DocumentType` (Factura / Factura Proforma / Factura Storno) musi być obecny.

Sposób przygotowania — wywołanie `POST /api/Firm/AddFirm/false` z `DT-02` JWT i poniższym body:
```json
{
  "id": 0,
  "name": "Firma Testowa SRL",
  "cui": "12345678",
  "regCom": "J40/1234/2020",
  "address": "STR. EXEMPLU NR. 1",
  "county": "ILFOV",
  "city": "VOLUNTARI"
}
```

Oczekiwany stan bazy po:
```
Firm:
  Id             = <generowany int>
  Name           = "Firma Testowa SRL"
  Cui            = "12345678"
  RegCom         = "J40/1234/2020"
  Address        = "STR. EXEMPLU NR. 1"
  County         = "ILFOV"
  City           = "VOLUNTARI"

UserFirm:
  UserFirmId     = <generowany int>
  UserId         = <Guid użytkownika DT-02>
  FirmId         = <Id Firm powyżej>
  IsClient       = false

User (aktualizacja):
  ActiveUserFirmId = <UserFirmId powyżej>

DocumentSeries (3 rekordy):
  SeriesName     = "2026"   (rok bieżący w momencie testu)
  FirstNumber    = 1
  CurrentNumber  = 1
  IsDefault      = true
  DocumentTypeId = 1  (Factura)   / 2  (Factura Proforma)   / 3  (Factura Storno)
  UserFirmId     = <UserFirmId powyżej>
```

Warianty przygotowania:
- **Wariant A (test integracyjny .NET):** seed `DT-01` przez `DbContext`, następnie wywołaj `POST /api/Firm/AddFirm/false` w teście lub bezpośrednio zainicjalizuj encje (`Firm`, `UserFirm`, `User.ActiveUserFirmId`, 3 × `DocumentSeries`) przez `DbContext` bez wywoływania serwisów — pamiętaj o wypełnieniu `DocumentTypeId`.
- **Wariant B (API black-box):** 1) `POST /api/Auth/register` z `DT-01`, 2) `POST /api/Auth/login` z `DT-02` → pobierz `token`, 3) `POST /api/Firm/AddFirm/false` z powyższym body i nagłówkiem `Authorization: Bearer <token>`.
- **Wariant C (E2E / ręcznie):** rejestracja przez UI (formularz rejestracji), logowanie, następnie dodanie firmy przez formularz UI Angular.

Sprzątanie: usunięcie rekordów `DocumentSeries` powiązanych z `UserFirmId`, rekordu `UserFirm`, rekordu `Firm` oraz wyzerowanie `User.ActiveUserFirmId`; na koniec usuń użytkownika `DT-01`.

Zależności: `DT-01`, `DT-02`, seed `DocumentType`.

---

---

### `DT-04` — Istniejący produkt w aktywnej firmie

**Cel:** Produkt gotowy do edycji lub usunięcia; niepowiązany z dokumentami.

**Precondition:** `DT-03` — aktywna firma musi istnieć (`User.ActiveUserFirmId != null`).

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
  Id             = <generowany int>   ← zapamiętaj do użycia w TC-04, TC-05, TC-06
  Name           = "Usługa konsultingowa"
  Price          = 500.00
  ContainsTva    = false
  UnitOfMeasurement = "ora"
  TvaValue       = 19
  UserFirmId     = <Id aktywnej UserFirm z DT-03>
```

**Warianty przygotowania:**
- **Wariant A (test integracyjny .NET):** bezpośrednie wstawienie encji `Product` przez `DbContext` z powyższymi wartościami i poprawnym `UserFirmId`.
- **Wariant B (API black-box):** 1) przygotuj `DT-03`, 2) wywołaj `POST /api/Product/AddProduct` z body powyżej i `Authorization: Bearer <jwt_DT-02>` — w odpowiedzi pobierz `id` produktu.
- **Wariant C (E2E / ręcznie):** po zalogowaniu i dodaniu firmy, dodaj produkt przez formularz UI Angular.

**Sprzątanie:** `PUT /api/Product/DeleteProducts?productIds=<Id>` lub bezpośrednie usunięcie z DB.

**Zależności:** `DT-01`, `DT-02`, `DT-03`.

---

### `DT-05` — Istniejące konto bankowe w aktywnej firmie

**Cel:** Konto bankowe gotowe do edycji lub usunięcia; niepowiązane z dokumentami.

**Precondition:** `DT-03` — aktywna firma musi istnieć (`User.ActiveUserFirmId != null`).

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
  Id             = <generowany int>   ← zapamiętaj do użycia w TC-05, TC-06, TC-07
  BankName       = "ING Bank Śląski"
  Iban           = "RO49AAAA1B31007593840000"
  Currency       = 0 (Ron)
  IsActive       = true
  UserFirmId     = <Id aktywnej UserFirm z DT-03>
```

**Warianty przygotowania:**
- **Wariant A (test integracyjny .NET):** bezpośrednie wstawienie encji `BankAccount` przez `DbContext` z powyższymi wartościami i poprawnym `UserFirmId`.
- **Wariant B (API black-box):** 1) przygotuj `DT-03`, 2) wywołaj `POST /api/BankAccount/AddUserFirmBankAccount` z body powyżej i `Authorization: Bearer <jwt_DT-02>` — w odpowiedzi pobierz `id` konta.
- **Wariant C (E2E / ręcznie):** po zalogowaniu i dodaniu firmy, dodaj konto bankowe przez formularz UI Angular.

**Sprzątanie:** `PUT /api/BankAccount/DeleteUserFirmBankAccounts` z body `[<Id>]` lub bezpośrednie usunięcie z DB.

**Zależności:** `DT-01`, `DT-02`, `DT-03`.

---

### `DT-06` — Istniejąca seria dokumentów w aktywnej firmie

**Cel:** Seria dokumentów gotowa do edycji lub usunięcia; niepowiązana z dokumentami.

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

**Warianty przygotowania:**
- **Wariant A (test integracyjny .NET):** bezpośrednie wstawienie encji `DocumentSeries` przez `DbContext` z powyższymi wartościami i poprawnym `UserFirmId` oraz `DocumentTypeId = 1`.
- **Wariant B (API black-box):** 1) przygotuj `DT-03`, 2) wywołaj `POST /api/DocumentSeries/AddDocumentSeries` z body powyżej i `Authorization: Bearer <jwt_DT-02>` — odpowiedź nie zwraca `Id`; pobierz go przez `GET /api/DocumentSeries/GetAllDocumentSeriesForUserId` (seria `"2026-TEST"`).
- **Wariant C (E2E / ręcznie):** po zalogowaniu i dodaniu firmy, dodaj serię przez formularz UI Angular.

**Sprzątanie:** `PUT /api/DocumentSeries/DeleteDocumentSeries?documentSeriesIds=<Id>` lub bezpośrednie usunięcie z DB.

**Zależności:** `DT-01`, `DT-02`, `DT-03`.

---

### `DT-07` — Firma klienta powiązana z użytkownikiem

**Cel:** Firma z `IsClient=true` powiązana z kontem testowym — wymagana jako `Document.ClientId` przy wystawianiu faktur.

**Precondition:** `DT-03` — użytkownik musi mieć aktywną firmę (tylko użytkownicy z firmą mogą dodawać klientów).

**Sposób przygotowania:** `POST /api/Firm/AddFirm/true` (isClient=true w ścieżce) z tokenem JWT z `DT-02`:
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
  Id             = <generowany int>   ← zapamiętaj jako clientId do użycia w DocumentRequestDto.client.id
  Name           = "Firma Klient SRL"
  Cui            = "87654321"
  RegCom         = "J40/5678/2021"
  Address        = "STR. CLIENTULUI NR. 2"
  County         = "ILFOV"
  City           = "VOLUNTARI"

UserFirm:
  UserFirmId     = <generowany int>
  UserId         = <Guid użytkownika DT-02>
  FirmId         = <Id Firm powyżej>
  IsClient       = true
```

**Warianty przygotowania:**
- **Wariant A (test integracyjny .NET):** bezpośrednie wstawienie encji `Firm` i `UserFirm` (IsClient=true) przez `DbContext`.
- **Wariant B (API black-box):** 1) przygotuj `DT-03`, 2) wywołaj `POST /api/Firm/AddFirm/true` z body powyżej i `Authorization: Bearer <jwt_DT-02>` — pobierz `clientId` przez `GET /api/Firm/GetUserClientFirms`.
- **Wariant C (E2E / ręcznie):** po zalogowaniu i dodaniu firmy, dodaj klienta przez formularz UI Angular.

**Sprzątanie:** bezpośrednie usunięcie rekordów `UserFirm` (IsClient=true) i `Firm` z DB lub przez endpointy P-08 (jeśli dostępne dla klientów).

**Zależności:** `DT-01`, `DT-02`, `DT-03`.

---

### `DT-08` — Istniejący dokument faktury

**Cel:** Faktura gotowa do edycji, usunięcia, stornu, odczytu lub generowania PDF. Używana jako precondition we wszystkich procesach operujących na istniejących dokumentach (P-13–P-19).

**Precondition:** `DT-03` (firma z aktywnymi seriami), `DT-04` lub `DT-05` (konto bankowe, wymagane przez AddDocument), `DT-07` (firma klienta).

**Sposób przygotowania:** `POST /api/Document/AddDocument` z tokenem JWT z `DT-02`:
```json
{
  "id": 0,
  "documentNumber": "20260001",
  "seller": null,
  "client": { "id": "<id firmy DT-07>", "name": "Firma Klient SRL", "cui": "87654321", "regCom": "J40/5678/2021", "address": "STR. CLIENTULUI NR. 2", "county": "ILFOV", "city": "VOLUNTARI" },
  "issueDate": "2026-05-30T00:00:00",
  "dueDate": "2026-06-30T00:00:00",
  "bankAccount": { "id": "<id konta DT-05>", "bankName": "ING Bank Śląski", "iban": "RO49AAAA1B31007593840000" },
  "documentSeries": { "id": "<id serii DT-03 lub DT-06>", "name": "2026", "currentNumber": 1, "documentType": { "id": 1 } },
  "documentType": { "id": 1, "type": "Factura" },
  "documentStatus": { "id": 1, "status": "Unpaid" },
  "products": [
    { "id": 0, "name": "Consultanță IT", "unitPrice": 500.00, "totalPrice": 595.00, "containsTva": false, "unitOfMeasurement": "ora", "tvaValue": 19, "quantity": 1 }
  ]
}
```

**Oczekiwany stan bazy po:**
```
Document:
  Id                 = <generowany int>   ← zapamiętaj do użycia w TC procesów P-13–P-19
  DocumentNumber     = "20260001"
  IssueDate          = 2026-05-30
  DueDate            = 2026-06-30
  TotalPrice         = 595.00
  DocumentTypeId     = 1 (Factura)
  DocumentStatusId   = 1 (Unpaid)
  UserFirmId         = <Id UserFirm z DT-03>
  ClientId           = <Id Firm z DT-07>
  BankAccountId      = <Id BankAccount z DT-05>

DocumentProduct (1 rekord):
  ProductId          = <Id Product (nowo utworzony lub istniejący)>
  DocumentId         = <Id Document powyżej>
  Quantity           = 1
  UnitPrice          = 500.00
  TotalPrice         = 595.00

DocumentSeries (aktualizacja):
  CurrentNumber      = 2  (zwiększony przez IncreaseDocumentSeriesNumber)
```

**Warianty przygotowania:**
- **Wariant A (test integracyjny .NET):** seed `DT-03`, `DT-05`, `DT-07`, następnie `POST /api/Document/AddDocument` w teście lub bezpośrednie wstawienie encji przez `DbContext`.
- **Wariant B (API black-box):** przygotuj `DT-03`, `DT-05`, `DT-07`, wywołaj `POST /api/Document/AddDocument` z body powyżej — pobierz Id przez `GET /api/Document/GetDocumentTableRecords/1`.
- **Wariant C (E2E / ręcznie):** dodaj fakturę przez formularz UI Angular.

**Sprzątanie:** `PUT /api/Document/DeleteDocuments` z body `[<Id>]` lub bezpośrednie usunięcie `DocumentProduct` i `Document` z DB.

**Zależności:** `DT-01`, `DT-02`, `DT-03`, `DT-05`, `DT-07`.

---

## 3. Konwencje danych

- E-maile testowe: `tester+<numer>@invoicejet.test` (lokalna część `tester+NN` minimalizuje konflikty).
- Hasła testowe: `Strong@123` — spełnia wymagany regex: ≥8 znaków, duża litera, mała litera, cyfra, znak specjalny z `@$!%*?&`.
- Identyfikatory firm (`CUI`) testowe ANAF: `[WYMAGA WERYFIKACJI]` — wpisz konkretne CUI działające w środowisku testowym.
- Numery IBAN testowe: `[WYMAGA WERYFIKACJI]` — wpisz konkretne wartości.

---

## 4. Powiązanie z seedem produkcyjnym (`DbSeeder`)

| Element seedu | Plik | Potrzebny w testach |
|---|---|---|
| `DocumentType` (Factura / Factura Proforma / Factura Storno) | `DbSeeder.cs › SeedDocumentTypes` | tak — wymagany przez procesy wystawiania dokumentów |
| `DocumentStatus` (Unpaid / Paid) | `DbSeeder.cs › SeedDocumentTypes` | tak — wymagany przy tworzeniu i filtrowaniu dokumentów |

Seed uruchamia się automatycznie przy starcie aplikacji przez `await DbSeeder.SeedDocumentTypes(app)`. W testach integracyjnych `.NET` z `WebApplicationFactory` seed jest wywoływany przez startup — baza jest gotowa.
