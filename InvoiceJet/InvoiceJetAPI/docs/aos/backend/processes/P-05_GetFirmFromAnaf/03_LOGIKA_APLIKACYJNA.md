# Pobranie firmy z ANAF — Logika aplikacyjna

## Przepływ wykonania

1. `FirmController.GetFirmDataFromAnaf(cui)` wywołuje `FirmService.GetFirmDataFromAnaf(cui)`.
2. Serwis tworzy `requestBody` z `cui` i bieżącą datą (`DateTime.Now.ToString("yyyy-MM-dd")`).
3. Serwis wysyła żądanie `PostAsJsonAsync(_apiUrl, requestBody)`.
4. Jeżeli odpowiedź ANAF ma status inny niż sukces, serwis rzuca `AnafFirmNotFoundException`.
5. Serwis parsuje `response.Content` przez `JObject.Parse(...)`.
6. Serwis odczytuje:
   - `found[0].date_generale`,
   - `found[0].adresa_domiciliu_fiscal`.
7. Serwis mapuje pola do `FirmDto`.
8. Kontroler zwraca `200 OK` i obiekt `FirmDto`.

---

## Mapowanie pól JSON -> `FirmDto`

| Pole JSON | Pole `FirmDto` |
|---|---|
| `date_generale.denumire` | `Name` |
| `date_generale.cui` | `Cui` |
| `date_generale.nrRegCom` | `RegCom` |
| `date_generale.adresa` | `Address` (po odcięciu prefiksu) |
| `adresa_domiciliu_fiscal.ddenumire_Judet` | `County` |
| `adresa_domiciliu_fiscal.ddenumire_Localitate` | `City` |

---

## Uwagi z implementacji

- Serwis inicjalizuje `HttpClient` bezpośrednio w konstruktorze klasy.
- Adres jest ustawiany na podstawie pierwszego znalezionego prefiksu z listy `STR.`, `ŞOS.`, `BLD.`, `CAL.`.
- Dla błędów i wyjątków w metodzie obowiązuje `catch (Exception)` i ponowne rzucenie `AnafFirmNotFoundException`.
