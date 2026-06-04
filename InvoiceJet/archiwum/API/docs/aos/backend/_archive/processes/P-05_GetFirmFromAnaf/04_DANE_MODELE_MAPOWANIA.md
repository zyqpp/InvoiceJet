# Pobranie firmy z ANAF — Dane, modele i mapowania

## DTO wyjściowe

| DTO | Rola |
|---|---|
| `FirmDto` | Odpowiedź procesu z danymi firmy z ANAF. |

---

## Integracja zewnętrzna

| Element | Wartość |
|---|---|
| Serwis | `FirmService` |
| Klient HTTP | `HttpClient` |
| Adres URL | `_apiUrl` z `AppSettings:AnafApiUrl` |
| Serializacja żądania | `PostAsJsonAsync` |
| Parsowanie odpowiedzi | `Newtonsoft.Json.Linq.JObject` |

---

## Pola mapowane

| Pole `FirmDto` | Źródło w JSON |
|---|---|
| `Name` | `found[0].date_generale.denumire` |
| `Cui` | `found[0].date_generale.cui` |
| `RegCom` | `found[0].date_generale.nrRegCom` |
| `Address` | `found[0].date_generale.adresa` po filtrze prefiksu |
| `County` | `found[0].adresa_domiciliu_fiscal.ddenumire_Judet` |
| `City` | `found[0].adresa_domiciliu_fiscal.ddenumire_Localitate` |

---

## Zapis do bazy

Proces nie zapisuje danych w bazie. Serwis tylko pobiera i mapuje dane.
