# EditFirm — Scenariusze testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zalogowany użytkownik z ważnym JWT | Rejestracja (P-01) + logowanie (P-02) | `DT-02` |
| Użytkownik z aktywną firmą (Id znany) | Stan po P-03 `TC-01` | `DT-03` |
| `DocumentType` seeded | `DbSeeder.SeedDocumentTypes` | seed produkcyjny |

---

## 2. Dane poprawne (happy path)

### `TC-01` — Edycja danych firmy (zmiana nazwy i adresu, `isClient=false`)

Warunki wstępne: `DT-03` — użytkownik z aktywną firmą `Id=42` (`IsClient=false`).

Żądanie (`PUT /api/Firm/EditFirm/false`), nagłówek `Authorization: Bearer <token z DT-02>`:
```json
{
  "id": 42,
  "name": "Firma Testowa SRL (nowa nazwa)",
  "cui": "12345678",
  "regCom": "J40/1234/2020",
  "address": "STR. NOUA NR. 10",
  "county": "ILFOV",
  "city": "VOLUNTARI"
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: echo żądania (`FirmDto` z `id=42`, nową nazwą i adresem)
- Skutki w bazie:
  - `Firm` (`Id=42`): `Name="Firma Testowa SRL (nowa nazwa)"`, `Address="STR. NOUA NR. 10"` — zaktualizowane
  - `UserFirm`: `IsClient=false` — bez zmian (wartość ta sama)

---

### `TC-02` — Zmiana roli firmy na klienta (`isClient=true`)

Warunki wstępne: `DT-03` — firma `Id=42` z `IsClient=false`.

Żądanie (`PUT /api/Firm/EditFirm/true`), nagłówek `Authorization: Bearer <token z DT-02>`:
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

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: echo żądania
- Skutki w bazie:
  - `Firm` (`Id=42`): dane bez zmian (te same wartości)
  - `UserFirm`: `IsClient=true` — zaktualizowany flag

---

## 3. Dane niepoprawne

### `TC-N01` — łamie `WAL-01`: brak tokenu JWT

Żądanie bez nagłówka `Authorization`:
```
PUT /api/Firm/EditFirm/false
(brak nagłówka Authorization)
{ "id": 42, "name": "Test", ... }
```
Oczekiwany rezultat:
- Status: `401 Unauthorized`
- Skutek w bazie: brak zmian

---

### `TC-N02` — łamie `WAL-02`: nieistniejące `id` firmy

Warunki wstępne: `DT-02`. Firma o `Id=99999` nie istnieje w DB.

Żądanie (`PUT /api/Firm/EditFirm/false`):
```json
{
  "id": 99999,
  "name": "Firma Nieistniejąca",
  "cui": "11111111",
  "regCom": "J40/9999/2020",
  "address": "STR. INEXISTENTA NR. 1",
  "county": "ILFOV",
  "city": "VOLUNTARI"
}
```
Oczekiwany rezultat (aktualny stan kodu):
- Status: `500 Internal Server Error` — **[UWAGA: powinien być `404`]**
- Odpowiedź: `{ "message": "Firm not found." }`
- Skutek w bazie: brak zmian

---

### `TC-N03` — `isClient` nieparsowany na `bool`

Żądanie:
```
PUT /api/Firm/EditFirm/yes
```
Oczekiwany rezultat:
- Status: `400 Bad Request` — ModelState error (ASP.NET Core, przed serwisem)
- Skutek w bazie: brak zmian

---

### `TC-N04` — `RegCom = null` → naruszenie NOT NULL w DB

Warunki wstępne: `DT-03`.

Żądanie (`PUT /api/Firm/EditFirm/false`):
```json
{
  "id": 42,
  "name": "Firma Testowa SRL",
  "cui": "12345678",
  "regCom": null,
  "address": "STR. EXEMPLU NR. 1",
  "county": "ILFOV",
  "city": "VOLUNTARI"
}
```
Oczekiwany rezultat:
- Status: `500 Internal Server Error`
- Odpowiedź: `{ "message": "<DbUpdateException message>" }`
- Skutek w bazie: brak zmian (rollback EF Core)

---

## 4. Wartości brzegowe

| ID | Pole / parametr | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|
| `TC-B01` | `id` | `0` (domyślna wartość `int`) | `500` — `Firm` o `Id=0` nie istnieje → `"Firm not found."` |
| `TC-B02` | `id` | `null` (pominięte pole w JSON) | `200 OK` z `id=0` w żądaniu → `500` jw. |
| `TC-B03` | `name` | `""` (pusty string) | `200 OK` — EF Core zapisuje pusty string |
| `TC-B04` | `name` | `null` | `500` — NOT NULL DB constraint |
| `TC-B05` | `name` | String 10 000 znaków | `200 OK` — `nvarchar(max)` akceptuje |
| `TC-B06` | `regCom` | `""` (pusty string) | `200 OK` — zapisane jako `""` (NOT NULL spełnione) |
| `TC-B07` | `regCom` | `null` | `500` — NOT NULL DB constraint |
| `TC-B08` | `isClient` | `false` → `true` (zmiana roli) | `200 OK` — `UserFirm.IsClient` zaktualizowane na `true` |
| `TC-B09` | `isClient` | `true` → `false` (zmiana roli) | `200 OK` — `UserFirm.IsClient` zaktualizowane na `false` |
| `TC-B10` | `cui` | Duplikat CUI istniejącej innej firmy | `200 OK` — brak unikalnego indeksu, duplikat zapisany [UWAGA] |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-02` | Zarejestrowany użytkownik + JWT | Wszystkie scenariusze |
| `DT-03` | Użytkownik z aktywną firmą (`Id=42`, `IsClient=false`) | `TC-01`, `TC-02`, `TC-N04`, wszystkie `TC-B` |
