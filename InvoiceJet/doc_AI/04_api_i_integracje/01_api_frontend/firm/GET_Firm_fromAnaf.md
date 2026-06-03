# GET /api/Firm/fromAnaf/{cui} — Dane firmy z ANAF

| Atrybut | Wartość |
|---|---|
| ID | API-04 |
| Metoda | GET |
| URL | `/api/Firm/fromAnaf/{cui}` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `FirmController.GetFirmDataFromAnaf` |
| Serwis | `FirmService.GetFirmDataFromAnaf` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Path Parameters

| Parametr | Typ | Wymagane | Opis |
|---|---|---|---|
| `cui` | `string` | TAK | Cod Unic de Înregistrare — rumuński numer NIP firmy |

### Headers
| Nagłówek | Wartość |
|---|---|
| `Authorization` | `Bearer {token}` |

**Przykład URL:** `GET /api/Firm/fromAnaf/12345678`

## Response

### 200 OK

Zwraca `FirmDto` z danymi wypełnionymi z ANAF:

```json
{
  "id": 0,
  "name": "SC EXAMPLE SRL",
  "cui": "12345678",
  "regCom": "J12/345/2020",
  "address": "STR. EXEMPLU NR. 1",
  "county": "BUCURESTI",
  "city": "SECTOR 1"
}
```

**Uwaga:** `id` jest `0` — to dane z ANAF, nie encja DB.

### Błędy

| Status HTTP | Wyjątek | Warunek |
|---|---|---|
| 400 Bad Request | `AnafFirmNotFoundException` | CUI nie znaleziony w ANAF lub ANAF API niedostępne |
| 401 Unauthorized | — | Brak/wygaśnięty token |

## Integracja z ANAF

**Zewnętrzne API:** `AppSettings:AnafApiUrl` z konfiguracji (appsettings.json)

**Wewnętrzne żądanie do ANAF:** `POST {AnafApiUrl}` z body:
```json
[{ "cui": "12345678", "data": "2026-05-31" }]
```

**Mapowanie odpowiedzi ANAF:**
| Pole ANAF | Pole FirmDto | Ścieżka JSON |
|---|---|---|
| `denumire` | `Name` | `found[0].date_generale.denumire` |
| `cui` | `Cui` | `found[0].date_generale.cui` |
| `nrRegCom` | `RegCom` | `found[0].date_generale.nrRegCom` |
| `adresa` | `Address` | `found[0].date_generale.adresa` (obcięta do od prefixu STR./ŞOS./BLD./CAL.) |
| `ddenumire_Judet` | `County` | `found[0].adresa_domiciliu_fiscal.ddenumire_Judet` |
| `ddenumire_Localitate` | `City` | `found[0].adresa_domiciliu_fiscal.ddenumire_Localitate` |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny z detalami ANAF. |
