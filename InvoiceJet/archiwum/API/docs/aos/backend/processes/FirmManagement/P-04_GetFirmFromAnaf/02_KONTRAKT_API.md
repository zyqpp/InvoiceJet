# GetFirmFromAnaf — Kontrakt API

## Endpoint `API-04`

| Atrybut | Wartość |
|---|---|
| ID endpointu | `API-04` |
| Metoda HTTP | `GET` |
| Ścieżka | `/api/Firm/fromAnaf/{cui}` |
| Autoryzacja | `Bearer <JWT>` — `[Authorize(Roles = "User")]` dziedziczone z `FirmController` |
| Parametry trasy | `cui` (string) — numer CUI firmy do wyszukania w ANAF |
| Ciało żądania | brak |
| Typ odpowiedzi | `FirmDto` |

## Parametr trasy

| Parametr | Typ | Wymagany | Opis |
|---|---|---|---|
| `cui` | `string` | tak | Numer identyfikacji podatkowej (CUI) firmy. ASP.NET Core przyjmuje dowolny string — brak walidacji formatu po stronie API |

## Przykłady żądania

### Żądanie poprawne — istniejące CUI

```
GET /api/Firm/fromAnaf/12345678
Authorization: Bearer <token z DT-02>
```

### Żądanie bez autoryzacji

```
GET /api/Firm/fromAnaf/12345678
(brak nagłówka Authorization)
```

## Odpowiedź — `200 OK`

Body: `FirmDto`

```json
{
  "id": 0,
  "name": "FIRMA EXEMPLU SRL",
  "cui": "12345678",
  "regCom": "J40/1234/2020",
  "address": "STR. EXEMPLU NR. 5, AP. 1",
  "county": "ILFOV",
  "city": "VOLUNTARI"
}
```

> **Uwaga:** pole `id` zawsze wynosi `0` — ten endpoint nie tworzy rekordu w bazie danych. Wartość `id` należy zignorować lub przepisać przed przekazaniem do `POST /api/Firm/AddFirm/{isClient}`.

## Odpowiedź — `200 OK` z częściowymi danymi

Gdy ANAF nie zawiera County/City dla danego CUI:

```json
{
  "id": 0,
  "name": "FIRMA EXEMPLU SRL",
  "cui": "12345678",
  "regCom": "J40/1234/2020",
  "address": "STR. EXEMPLU NR. 5",
  "county": null,
  "city": null
}
```

## Tabela statusów HTTP

| Kod | Przyczyna | Body |
|---|---|---|
| `200 OK` | Firma znaleziona w ANAF — pola mogą być częściowo null jeśli ANAF nie zwrócił wszystkich danych | `FirmDto` (id=0) |
| `200 OK` | CUI nie znaleziony w ANAF (ANAF zwraca HTTP 200 z pustą tablicą `found`) | `FirmDto` ze wszystkimi polami null — [UWAGA: powinien być 404] |
| `401 Unauthorized` | Brak nagłówka `Authorization` lub nieważny token | brak body (ASP.NET Core Identity) |
| `403 Forbidden` | Token ważny, ale rola nie pasuje do `"User"` | brak body |
| `404 Not Found` | ANAF zwrócił HTTP non-2xx dla podanego CUI, lub dowolny wyjątek w trakcie przetwarzania | `{ "message": "Firm with CUI {cui} not found in ANAF database." }` |
| `500 Internal Server Error` | Niespodziewany błąd poza `catch (Exception)` (praktycznie niemożliwy — catch jest all-catching) | `{ "message": "..." }` |

## Uwagi o zachowaniu

- Wywołanie jest **read-only** — brak efektów ubocznych w bazie danych
- Wynik służy do autofill formularza dodania firmy; utrwalenie następuje przez `POST /api/Firm/AddFirm/{isClient}` (P-03)
- ANAF API jest wywoływane synchronicznie w kontekście żądania HTTP — timeout ANAF (domyślny timeout `HttpClient` = 100 sekund) blokuje wątek
