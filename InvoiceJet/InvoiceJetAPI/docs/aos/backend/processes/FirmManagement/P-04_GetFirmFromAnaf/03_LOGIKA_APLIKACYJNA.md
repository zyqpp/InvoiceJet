# GetFirmFromAnaf — Logika aplikacyjna

## 1. Punkt wejścia — kontroler

Plik: `InvoiceJet.Presentation/Controllers/FirmController.cs › FirmController.GetFirmDataFromAnaf`

```csharp
// FirmController.cs:20-25
[HttpGet("fromAnaf/{cui}")]
public async Task<ActionResult<FirmDto>> GetFirmDataFromAnaf(string cui)
{
    var firmDataDto = await _firmService.GetFirmDataFromAnaf(cui);
    return Ok(firmDataDto);
}
```

Kontroler jest bezstanowy: brak walidacji wejścia, brak jawnego `try/catch` — obsługa wyjątków delegowana do `ExceptionMiddleware`.

## 2. Algorytm główny — `FirmService.GetFirmDataFromAnaf`

Plik: `InvoiceJet.Application/Services/Impl/FirmService.cs › FirmService.GetFirmDataFromAnaf` (linie 131–197)

| Krok | Opis | Kod |
|---|---|---|
| 1 | Inicjalizacja pustego `FirmDto` | `var firmDto = new FirmDto()` |
| 2 | Pobranie bieżącej daty | `DateTime.Now.ToString("yyyy-MM-dd")` |
| 3 | Budowa body żądania do ANAF | `new[] { new { cui, data = currentDate } }` |
| 4 | Wywołanie ANAF API | `_httpClient.PostAsJsonAsync(_apiUrl, requestBody)` |
| 5 | Sprawdzenie statusu HTTP | Jeśli `!response.IsSuccessStatusCode` → throw `AnafFirmNotFoundException(cui)` |
| 6 | Parsowanie JSON | `JObject.Parse(responseString)` (Newtonsoft.Json) |
| 7 | Ekstrakcja `date_generale` | `json["found"]?[0]?["date_generale"]` |
| 8 | Parsowanie adresu | Szukanie prefiksów `STR./ŞOS./BLD./CAL.` w polu `adresa` |
| 9 | Ustawienie Name/Cui/RegCom | Warunkowo (gdy address != null i wszystkie trzy != null) |
| 10 | Ekstrakcja `adresa_domiciliu_fiscal` | `json["found"]?[0]?["adresa_domiciliu_fiscal"]` |
| 11 | Ustawienie County/City | Warunkowo (gdy oba != null) |
| 12 | Zwrot `firmDto` | Zawsze — nawet jeśli część pól jest null |

Cały blok 4–12 objęty jest `catch (Exception) { throw new AnafFirmNotFoundException(cui); }` — każdy wyjątek (timeout, błąd parsowania JSON, NullReferenceException) jest tłumaczony na `AnafFirmNotFoundException`.

## 3. Walidacje wejścia (WAL)

W P-04 nie ma jawnych walidacji domenowych poza autoryzacją. `cui` nie jest walidowany przed wywołaniem ANAF.

| ID | Walidacja | Gdzie sprawdzana | Wynik naruszenia |
|---|---|---|---|
| `WAL-01` | Ważny JWT z rolą `"User"` | `[Authorize(Roles = "User")]` na `FirmController` | `401 Unauthorized` / `403 Forbidden` |

## 4. Wywołanie ANAF API — szczegóły

```csharp
// FirmService.cs:136-148
var requestBody = new[]
{
    new
    {
        cui,
        data = currentDate
    }
};

var response = await _httpClient.PostAsJsonAsync(_apiUrl, requestBody);

if (!response.IsSuccessStatusCode)
    throw new AnafFirmNotFoundException(cui);
```

- `_apiUrl`: wartość `AppSettings:AnafApiUrl` z `appsettings.json` = `https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva`
- `PostAsJsonAsync` serializuje body przez `System.Text.Json` (domyślny serializer .NET 8)
- Odpowiedź odczytywana jako string: `response.Content.ReadAsStringAsync()`
- Parsowana przez `JObject.Parse` (Newtonsoft.Json) — mieszane użycie obu serializerów w jednym projekcie

## 5. Obsługa przypadków brzegowych

### Scenariusz: ANAF HTTP non-2xx

```csharp
if (!response.IsSuccessStatusCode)
    throw new AnafFirmNotFoundException(cui);
```
→ `ExceptionMiddleware` mapuje na `404 Not Found`

### Scenariusz: ANAF zwraca 200 z pustą tablicą `found`

Brak sprawdzenia `notFound`. Kod próbuje `json["found"]?[0]?["date_generale"]` — nullowy wynik → `dateGenerale == null` → blok `if` pomijany → zwracany pusty `FirmDto` z `Id=0`.

→ Klient otrzymuje `200 OK` z `{"id":0,"name":null,"cui":null,"regCom":null,"address":null,"county":null,"city":null}`

### Scenariusz: Dowolny wyjątek w trakcie przetwarzania

```csharp
// FirmService.cs:193-196
catch (Exception)
{
    throw new AnafFirmNotFoundException(cui);
}
```
→ `404 Not Found` ze stałym komunikatem `"Firm with CUI {cui} not found in ANAF database."`

> [UWAGA: catch pochłania każdy wyjątek (timeout, `HttpRequestException`, `JsonException`, `NullReferenceException`), maskując rzeczywistą przyczynę błędu. Problem sieciowy z ANAF i nieistniejący CUI są nierozróżnialne z perspektywy klienta — WYMAGA WERYFIKACJI Z ZESPOŁEM]

## 6. Brak zapisu do bazy

Proces jest **czysto read-only z perspektywy lokalnej bazy** — zero wywołań `CompleteAsync()`. Wynik jest zwracany bezpośrednio do klienta w celu wypełnienia formularza; utrwalenie danych firmy następuje osobno przez P-03 (`AddFirm`).

## 7. Tożsamość użytkownika

`GetCurrentUserId()` **nie jest wywoływane** w tym procesie — CUI jest publicznym identyfikatorem firmy, tożsamość użytkownika nie jest potrzebna do wyszukania. Autoryzacja (JWT) służy jedynie jako guard dostępu do endpointu.
