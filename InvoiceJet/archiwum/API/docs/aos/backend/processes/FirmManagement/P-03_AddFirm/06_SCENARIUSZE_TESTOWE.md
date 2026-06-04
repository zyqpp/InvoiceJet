# AddFirm — Dane testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zalogowany użytkownik z ważnym JWT | Rejestracja (P-01) + logowanie (P-02) | `DT-02` |
| `DocumentType` seeded (Factura / Factura Proforma / Factura Storno) | `DbSeeder.SeedDocumentTypes` przy starcie aplikacji | seed produkcyjny |
| Brak aktywnej firmy użytkownika (dla scenariusza A1 — pierwsza firma) | czyste konto (świeżo po rejestracji) | stan konta `DT-02` |

---

## 2. Dane poprawne (happy path)

### `TC-01` — Dodanie własnej firmy jako pierwszej firmy użytkownika (`isClient=false`, brak aktywnej firmy)

Warunki wstępne: `DT-02` — użytkownik bez aktywnej firmy. Seed DocumentType obecny.

Żądanie (`POST /api/Firm/AddFirm/false`), nagłówek `Authorization: Bearer <token z DT-02>`:
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

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `FirmDto` z nadanym `id` (np. `42`)
- Skutki w bazie:
  - Nowy rekord w `Firm` (`Id=42`, `Name="Firma Testowa SRL"`, `Cui="12345678"`, …)
  - Nowy rekord w `UserFirm` (`FirmId=42`, `UserId=<userId z DT-02>`, `IsClient=false`)
  - `User.ActiveUserFirmId` → Id nowego `UserFirm`
  - 3 nowe rekordy w `DocumentSeries` (`SeriesName="2026"`, `FirstNumber=1`, `CurrentNumber=1`, `IsDefault=true`) — po jednym dla `Factura`, `Factura Proforma`, `Factura Storno`

---

### `TC-02` — Dodanie firmy klienta (`isClient=true`) gdy użytkownik MA już aktywną firmę

Warunki wstępne: `DT-02` + `DT-03` (użytkownik z aktywną własną firmą).

Żądanie (`POST /api/Firm/AddFirm/true`), nagłówek `Authorization: Bearer <token z DT-02>`:
```json
{
  "id": 0,
  "name": "Klient SRL",
  "cui": "87654321",
  "regCom": "J40/5678/2021",
  "address": "STR. CLIENTULUI NR. 5",
  "county": "ILFOV",
  "city": "BUCURESTI"
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `FirmDto` z nadanym `id`
- Skutki w bazie:
  - Nowy rekord w `Firm`
  - Nowy rekord w `UserFirm` (`IsClient=true`)
  - `User.ActiveUserFirmId` — **bez zmian** (activeUserFirm != null → A2, nie A1)
  - `DocumentSeries` — **brak nowych rekordów** (serie tworzone tylko przy pierwszej firmie)

---

## 3. Dane niepoprawne

### `TC-N01` — łamie `WAL-01`: brak tokenu JWT

Żądanie bez nagłówka `Authorization`:
```json
POST /api/Firm/AddFirm/false
(brak nagłówka Authorization)
{ "id": 0, "name": "Test", "cui": "111", "regCom": "J40/1/2020", "address": "STR. 1", "county": "ILFOV", "city": "BUCURESTI" }
```
Oczekiwany rezultat:
- Status: `401 Unauthorized`
- Skutek w bazie: brak zmian

---

### `TC-N02` — `RegCom = null` → naruszenie NOT NULL w DB

Warunki wstępne: `DT-02`.

Żądanie (`POST /api/Firm/AddFirm/false`):
```json
{
  "id": 0,
  "name": "Firma Bez RegCom",
  "cui": "99999999",
  "regCom": null,
  "address": "STR. TEST NR. 1",
  "county": "ILFOV",
  "city": "VOLUNTARI"
}
```
Oczekiwany rezultat:
- Status: `500 Internal Server Error`
- Odpowiedź: `{ "message": "<DbUpdateException message>" }` — szczegóły błędu DB
- Skutek w bazie: brak zmian (rollback EF Core)

---

### `TC-N03` — `isClient` nieparsowany na `bool`

Żądanie:
```
POST /api/Firm/AddFirm/yes
```
Oczekiwany rezultat:
- Status: `400 Bad Request` — ModelState error (ASP.NET Core, przed serwisem)
- Skutek w bazie: brak zmian

---

## 4. Wartości brzegowe

| ID | Pole / parametr | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|
| `TC-B01` | `Name` | `""` (pusty string) | `200 OK` — EF Core zapisuje pusty string do `nvarchar(max)` |
| `TC-B02` | `Name` | `null` | `500` — NOT NULL DB constraint violation |
| `TC-B03` | `Cui` | `""` (pusty string) | `200 OK` — zapisane jako pusty string |
| `TC-B04` | `RegCom` | `""` | `200 OK` — zapisane jako pusty string (RegCom nullable w DTO, NOT NULL w DB → pusty string jest akceptowany) |
| `TC-B05` | `RegCom` | `null` | `500` — NOT NULL DB constraint violation |
| `TC-B06` | `isClient` | `false` + użytkownik nie ma aktywnej firmy | `200 OK` + 3 `DocumentSeries` + `User.ActiveUserFirmId` ustawione |
| `TC-B07` | `isClient` | `true` + użytkownik nie ma aktywnej firmy | `200 OK` + 3 `DocumentSeries` + firma klienta staje się aktywną firmą [UWAGA: potencjalny bug] |
| `TC-B08` | Duplikat `Cui` | Ten sam `Cui` co istniejąca firma | `200 OK` — duplikat Firm zapisany (brak unikalnego indeksu) [UWAGA] |
| `TC-B09` | `Name` | String 10 000 znaków | `200 OK` — `nvarchar(max)` przyjmuje duże wartości |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-02` | Zarejestrowany użytkownik + JWT | `TC-01`, `TC-02`, `TC-N02`, wszystkie `TC-B` |
| `DT-03` | Użytkownik z aktywną firmą (stan po `TC-01`) | `TC-02` (precondition: ActiveUserFirm != null) |

> `DT-03` należy dodać do `../../KATALOG_DANYCH_TESTOWYCH.md` — opisuje stan bazy po pomyślnym `TC-01` (P-03).
