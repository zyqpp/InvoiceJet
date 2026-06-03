# AddFirm — Kontrakt API

## `API-03` — POST /api/Firm/AddFirm/{isClient}

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `POST` |
| Ścieżka | `/api/Firm/AddFirm/{isClient}` |
| Kontroler | `FirmController.cs › FirmController.AddFirm` |
| Autoryzacja | `[Authorize(Roles = "User")]` — dziedziczone z klasy `FirmController` |

### Parametry trasy

| Parametr | Typ | Źródło | Opis |
|---|---|---|---|
| `isClient` | `bool` | `[FromRoute]` (segment URL `{isClient}`) | `false` → firma własna (dostawca); `true` → firma klienta (odbiorca) |

Wartości akceptowane przez ASP.NET Core dla `bool`: `true` / `false` (case-insensitive), `1` / `0`.

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `FirmDto` | `[FromBody]` |

Pola `FirmDto` (`Application/DTOs/FirmDto.cs`):

| Pole | Typ C# | Wymagane | Opis |
|---|---|---|---|
| `Id` | `int` | nie | Ignorowane przy tworzeniu — nadpisywane przez DB IDENTITY |
| `Name` | `string` | tak* | Nazwa firmy |
| `Cui` | `string` | tak* | Numer identyfikacyjny (CUI / NIP) |
| `RegCom` | `string?` | nie | Numer rejestru handlowego — nullable w DTO, NOT NULL w DB |
| `Address` | `string` | tak* | Ulica i numer |
| `County` | `string` | tak* | Województwo / Judet |
| `City` | `string` | tak* | Miasto |

> *Brak atrybutów `[Required]` — pola nie są walidowane przez model validation ASP.NET Core.

Przykład żądania — dodanie własnej firmy (`isClient=false`):
```json
POST /api/Firm/AddFirm/false

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

Przykład żądania — dodanie firmy klienta (`isClient=true`):
```json
POST /api/Firm/AddFirm/true

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

### Odpowiedź

| Status | Typ / kształt | Warunek |
|---|---|---|
| `200 OK` | `FirmDto` (z nadanym `Id`) | Firma zapisana pomyślnie |
| `401 Unauthorized` | — | Brak lub nieważny token JWT |
| `403 Forbidden` | — | Token JWT bez roli `"User"` |
| `500 Internal Server Error` | `{ "message": "<error>" }` | Błąd DB (null constraint, FK violation), NullReferenceException, lub inny nieobsłużony wyjątek |

Przykład odpowiedzi sukcesu (własna firma, `isClient=false`, użytkownik bez aktywnej firmy):
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

> Odpowiedź jest tym samym obiektem co żądanie z uzupełnionym `id`. Pozostałe pola **nie są przeładowywane z DB** po zapisie.

Efekty uboczne widoczne w bazie (nie w odpowiedzi):
- Gdy `isClient=false` i użytkownik nie ma jeszcze aktywnej firmy: tworzony jest `UserFirm`, aktualizowany jest `User.ActiveUserFirmId`, a w tabeli `DocumentSeries` pojawiają się 3 rekordy (Factura, Factura Proforma, Factura Storno) z `SeriesName = "<bieżący rok>"`.
