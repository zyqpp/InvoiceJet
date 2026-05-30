# GetFirmFromAnaf — Scenariusze testowe

## 1. Warunki wstępne (preconditions / seed)

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| Zalogowany użytkownik z ważnym JWT | Rejestracja (P-01) + logowanie (P-02) | `DT-02` |
| Dostęp do sieci — ANAF API osiągalne | środowisko z dostępem do internetu | — |
| Znany istniejący CUI w bazie ANAF | publicznie dostępny (np. firma testowa z rejestru rumuńskiego) | `CUI-VALID = 14399840` (przykład) |
| Znany nieistniejący CUI | dowolna liczba nieprzypisana w ANAF | `CUI-INVALID = 99999999` |

> **Uwaga:** testy integracyjne wymagają połączenia z zewnętrznym ANAF API. Testy jednostkowe powinny mockować `HttpClient` lub `IFirmService`.

---

## 2. Dane poprawne (happy path)

### `TC-01` — Istniejące CUI z pełnymi danymi

Warunki wstępne: `DT-02` — użytkownik z JWT. Sieć dostępna. CUI istniejący w ANAF z pełnymi danymi (Name, Cui, RegCom, Address z prefiksem STR./ŞOS./BLD./CAL., County, City).

Żądanie:
```
GET /api/Firm/fromAnaf/14399840
Authorization: Bearer <token z DT-02>
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: `FirmDto` z:
  - `id = 0`
  - `name` — niepusty string
  - `cui = "14399840"`
  - `regCom` — niepusty string (lub null jeśli podmiot bez KRS)
  - `address` — przycinany od prefiksu ulicy (nie zawiera „SECTOR X, " na początku)
  - `county` — niepusty string
  - `city` — niepusty string
- Skutki w bazie: **brak** (zero rekordów created/updated)

---

### `TC-02` — CUI firmy bez `nrRegCom` (np. PFA)

Warunki wstępne: `DT-02`. CUI podmiotu bez wpisu w rejestrze handlowym (np. PFA — persoană fizică autorizată).

Żądanie:
```
GET /api/Firm/fromAnaf/<CUI-PFA>
Authorization: Bearer <token z DT-02>
```

Oczekiwany rezultat (aktualny stan kodu — patrz UWAGI):
- Status: `200 OK`
- Odpowiedź: `FirmDto` z `id=0`, `name=null`, `cui=null`, `regCom=null`, `address=null` — mimo że ANAF zwraca `denumire` i `cui`
- **[UWAGA: Bug — gdy `nrRegCom == null`, warunek `if (name != null && cuiValue != null && regCom != null)` jest fałszywy → Name i Cui nie są ustawiane — WYMAGA WERYFIKACJI Z ZESPOŁEM]**
- Skutki w bazie: brak

---

## 3. Dane niepoprawne

### `TC-N01` — łamie `WAL-01`: brak tokenu JWT

Żądanie bez nagłówka `Authorization`:
```
GET /api/Firm/fromAnaf/12345678
(brak nagłówka Authorization)
```
Oczekiwany rezultat:
- Status: `401 Unauthorized`
- Skutek w bazie: brak

---

### `TC-N02` — Nieistniejące CUI (ANAF HTTP non-2xx)

Warunki wstępne: `DT-02`. CUI nieistniejący w ANAF, gdzie ANAF zwraca błąd HTTP.

Żądanie:
```
GET /api/Firm/fromAnaf/99999999
Authorization: Bearer <token z DT-02>
```
Oczekiwany rezultat:
- Status: `404 Not Found`
- Odpowiedź: `{ "message": "Firm with CUI 99999999 not found in ANAF database." }`
- Skutek w bazie: brak

---

### `TC-N03` — Nieistniejące CUI (ANAF HTTP 200 z pustą tablicą `found`)

Warunki wstępne: `DT-02`. CUI nieistniejący, ale ANAF zwraca `HTTP 200` z `{ "found": [], "notFound": [...] }`.

Żądanie:
```
GET /api/Firm/fromAnaf/99999999
Authorization: Bearer <token z DT-02>
```
Oczekiwany rezultat (aktualny stan kodu):
- Status: `200 OK` — **[UWAGA: powinien być 404]**
- Odpowiedź: `{ "id": 0, "name": null, "cui": null, "regCom": null, "address": null, "county": null, "city": null }`
- Skutek w bazie: brak

---

### `TC-N04` — ANAF API niedostępne (timeout / błąd sieci)

Warunki wstępne: `DT-02`. Symulacja niedostępności ANAF (np. przez mockowanie `HttpClient`).

Oczekiwany rezultat:
- Status: `404 Not Found`
- Odpowiedź: `{ "message": "Firm with CUI ... not found in ANAF database." }`
- **[UWAGA: Błąd sieci i nieistniejący CUI mają identyczną odpowiedź — nierozróżnialne dla klienta]**

---

## 4. Wartości brzegowe

| ID | Pole / parametr | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|
| `TC-B01` | `cui` | Pusty string (`""`) | ASP.NET route matching może zwrócić `404` (brak dopasowania trasy) lub ANAF error → `404` |
| `TC-B02` | `cui` | String alfanumeryczny (np. `"RO12345678"`) | ANAF może nie rozpoznać formatu — `404` lub `200` z pustym DTO |
| `TC-B03` | `cui` | Bardzo długi string (1000 znaków) | ANAF zwróci błąd → `404` |
| `TC-B04` | `cui` | CUI z adresem zawierającym `ŞOS.` (U+015E) | Prefix `ŞOS.` rozpoznany poprawnie jeśli ANAF zwraca dokładnie ten znak; niezgodność Unicode → address nie przycinany |
| `TC-B05` | `cui` | CUI z adresem zawierającym tylko `SECTOR X` bez prefiksu ulicy | `address == null` po pętli → `Name`, `Cui`, `RegCom` nie ustawiane — zwracany pusty DTO |
| `TC-B06` | `cui` | CUI firmy z `County` ale bez `City` | `200 OK`, `county=null`, `city=null` (warunek `county != null && city != null` jest fałszywy) |

---

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-02` | Zarejestrowany użytkownik + ważny JWT | Wszystkie scenariusze |
| `CUI-VALID` | Istniejący CUI w bazie ANAF z pełnymi danymi | `TC-01` |
| `CUI-PFA` | CUI podmiotu bez `nrRegCom` | `TC-02` |
| `CUI-INVALID` | CUI nieistniejący w ANAF | `TC-N02`, `TC-N03` |
