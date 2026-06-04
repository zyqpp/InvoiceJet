# GetFirmFromAnaf — Dane, modele, mapowania

## 1. DTO żądania

Brak ciała żądania (`[HttpGet]`). Jedyna dana wejściowa to parametr trasy:

| Parametr | Typ w URL | Typ C# | Lokalizacja | Opis |
|---|---|---|---|---|
| `cui` | string | `string` | route (`{cui}`) | Numer identyfikacji podatkowej (CUI) firmy do wyszukania w ANAF |

## 2. DTO odpowiedzi — `FirmDto`

Plik: `InvoiceJet.Application/DTOs/FirmDto.cs`

| Pole | Typ C# | Nullable | Źródło w ANAF JSON | Uwaga |
|---|---|---|---|---|
| `Id` | `int` | nie | — | **zawsze `0`** — pole nie jest ustawiane w tym procesie |
| `Name` | `string` | nie | `found[0].date_generale.denumire` | Pełna nazwa firmy |
| `Cui` | `string` | nie | `found[0].date_generale.cui` | Numer CUI jako string (ANAF zwraca bez prefiksu `RO`) |
| `RegCom` | `string?` | **tak** | `found[0].date_generale.nrRegCom` | Numer rejestru handlowego; może być null dla niektórych podmiotów |
| `Address` | `string` | nie | `found[0].date_generale.adresa` (substr) | Adres po przycięciu do pierwszego rozpoznanego prefiksu ulicy |
| `County` | `string` | nie | `found[0].adresa_domiciliu_fiscal.ddenumire_Judet` | Județ (województwo) |
| `City` | `string` | nie | `found[0].adresa_domiciliu_fiscal.ddenumire_Localitate` | Miejscowość |

> [UWAGA: `FirmDto.Id = 0` w odpowiedzi — pole nie ma znaczenia dla tego endpointu, lecz klient musi to obsłużyć po stronie frontu (np. nie używać Id do zapisu bez wcześniejszego wywołania AddFirm)]

## 3. Baza danych

Proces **nie zapisuje ani nie odczytuje bazy danych**. Zero wywołań `CompleteAsync()`. Jedyną warstwą persystencji jest zewnętrzne ANAF API.

## 4. Integracja zewnętrzna — ANAF REST API

### Konfiguracja

| Klucz konfiguracji | Wartość (appsettings.json) |
|---|---|
| `AppSettings:AnafApiUrl` | `https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva` |

Konfiguracja wczytywana przez: `FirmService.cs:29` — `config.GetSection("AppSettings")?["AnafApiUrl"]`

### Żądanie do ANAF

```
POST https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva
Content-Type: application/json
```

```json
[
  {
    "cui": "12345678",
    "data": "2026-05-30"
  }
]
```

Uwagi:
- Ciało to **tablica** z jednym obiektem
- `data` to bieżąca data: `DateTime.Now.ToString("yyyy-MM-dd")`
- Wywołanie przez `HttpClient.PostAsJsonAsync(_apiUrl, requestBody)` — `System.Net.Http.Json`

### Odpowiedź ANAF — happy path

```json
{
  "found": [
    {
      "date_generale": {
        "denumire": "FIRMA EXEMPLU SRL",
        "cui": "12345678",
        "nrRegCom": "J40/1234/2020",
        "adresa": "SECTOR 1, STR. EXEMPLU NR. 5, AP. 1"
      },
      "adresa_domiciliu_fiscal": {
        "ddenumire_Judet": "ILFOV",
        "ddenumire_Localitate": "VOLUNTARI"
      }
    }
  ],
  "notFound": []
}
```

### Odpowiedź ANAF — CUI nie istnieje w bazie ANAF

```json
{
  "found": [],
  "notFound": [
    { "cui": "99999999", "data": "2026-05-30" }
  ]
}
```

> [UWAGA: ANAF zwraca HTTP 200 z pustą tablicą `found` dla nieistniejącego CUI. Serwis w tym przypadku zwraca pusty `FirmDto` (Id=0, wszystkie pola null/domyślne) zamiast rzucić `AnafFirmNotFoundException`. Klient dostaje `200 OK` z pustym obiektem — WYMAGA WERYFIKACJI Z ZESPOŁEM]

## 5. Mapowanie pól ANAF → FirmDto

### Parsowanie adresu

```csharp
// FirmService.cs:162–169
string[] addressPrefixes = { "STR.", "ŞOS.", "BLD.", "CAL." };
if (address != null)
{
    foreach (var prefix in addressPrefixes)
    {
        var startIndex = address.IndexOf(prefix, StringComparison.Ordinal);
        if (startIndex != -1)
            firmDto.Address = address.Substring(startIndex);
    }
    // ...
}
```

Logika:
- Pełny adres ANAF (np. `"SECTOR 1, STR. EXEMPLU NR. 5"`) jest przycinany do podciągu od pierwszego znalezionego prefiksu
- Prefiksy sprawdzane kolejno: `STR.` → `ŞOS.` → `BLD.` → `CAL.`
- Przy wielu dopasowaniach — **ostatnie znalezione nadpisuje poprzednie** (`firmDto.Address` jest przesłaniany w każdej iteracji)

> [UWAGA: `ŞOS.` zawiera rumuńską literę `Ş` (U+015E, S z cedillą). Adresy ANAF mogą używać `SOS.` (ASCII) lub `ȘOS.` (U+0218) — niedopasowanie znaków Unicode spowoduje pominięcie prefiksu — WYMAGA WERYFIKACJI Z ZESPOŁEM]

> [UWAGA: jeśli `address == null` (pole `adresa` nieobecne w odpowiedzi ANAF), **żadne** z pól `Name`, `Cui`, `RegCom` nie jest ustawiane (są wewnątrz bloku `if (address != null)`) — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Warunkowe ustawianie Name / Cui / RegCom

```csharp
// FirmService.cs:172–177
if (name != null && cuiValue != null && regCom != null)
{
    firmDto.Name = name;
    firmDto.RegCom = regCom;
    firmDto.Cui = cuiValue;
}
```

> [UWAGA: jeśli `regCom == null` (podmioty bez wpisu w rejestrze handlowym — np. PFA), pola `Name` i `Cui` również nie są ustawiane mimo że są dostępne — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### Mapowanie County i City

```csharp
// FirmService.cs:181–189
var adrDomiciliuFiscal = json["found"]?[0]?["adresa_domiciliu_fiscal"];
if (adrDomiciliuFiscal == null) return firmDto;

var county = adrDomiciliuFiscal["ddenumire_Judet"]?.ToString();
var city   = adrDomiciliuFiscal["ddenumire_Localitate"]?.ToString();

if (county == null || city == null) return firmDto;
firmDto.County = county;
firmDto.City   = city;
```

Jeśli `adresa_domiciliu_fiscal` jest null lub brakuje `Judet`/`Localitate` — metoda zwraca częściowo wypełniony `FirmDto` bez County/City (bez wyjątku).

## 6. HttpClient — sposób tworzenia

```csharp
// FirmService.cs:24
_httpClient = new HttpClient();
```

> [UWAGA: `HttpClient` jest tworzony przez `new` w konstruktorze serwisu zamiast przez `IHttpClientFactory`. Przy dużej liczbie żądań może prowadzić do wyczerpania puli gniazd (socket exhaustion). Rejestracja FirmService jako Scoped oznacza tworzenie nowej instancji `HttpClient` przy każdym żądaniu — WYMAGA WERYFIKACJI Z ZESPOŁEM]
