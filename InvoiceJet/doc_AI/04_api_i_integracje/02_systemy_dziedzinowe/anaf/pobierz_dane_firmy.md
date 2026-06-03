# Integracja ANAF — pobieranie danych firmy po CUI

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| Autor | Agent Claudiusz Sonte 4.6 max |
| Wersja | 1.0 |
| Data | 2026-05-31 |
| Status | Obowiązujący |
| System zewnętrzny | ANAF — Agenția Națională de Administrare Fiscală |
| Kraj | Rumunia |
| Endpoint InvoiceJet | `GET /api/Firm/GetFirmFromAnaf` (API-04) |

## Cel integracji

Autouzupełnienie danych firmy rumuńskiej w formularzach InvoiceJet na podstawie numeru CUI (Cod Unic de Înregistrare — rumuński odpowiednik NIP). Użytkownik podaje CUI, system odpytuje ANAF i zwraca nazwę firmy, adres, numer rejestracyjny oraz dane geograficzne.

## Konfiguracja

Adres URL zewnętrznego API jest parametryzowany w `appsettings.json`:

```json
{
  "AppSettings": {
    "AnafApiUrl": "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva"
  }
}
```

## Endpoint zewnętrzny

```
POST https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva
Content-Type: application/json
```

ANAF API jest publicznie dostępne bez klucza API ani autoryzacji.

## Format żądania

```json
[
  {
    "cui": 12345678,
    "data": "2026-05-31"
  }
]
```

| Pole | Typ | Opis |
|---|---|---|
| `cui` | integer | Numer CUI firmy (nie string — wymagany typ liczbowy) |
| `data` | string (YYYY-MM-DD) | Bieżąca data zapytania |

Uwaga: ANAF API obsługuje batch queries (tablica wielu elementów), ale InvoiceJet zawsze wysyła dokładnie jeden element.

## Format odpowiedzi

```json
{
  "found": [
    {
      "date_generale": {
        "denumire": "EXAMPLE SRL",
        "cui": 12345678,
        "nrRegCom": "J40/1234/2020",
        "adresa": "STR. EXEMPLU NR. 1, SECTOR 1, BUKARESZT",
        "stare_inregistrare": "INREGISTRAT din data 01.01.2020",
        "data_inregistrare": "2020-01-01",
        "cod_postal": "010001",
        "telefon": "0211234567",
        "fax": "",
        "E_mail": "contact@example.ro",
        "forma_juridica": "SOCIETATE CU RASPUNDERE LIMITATA",
        "scpTVA": false
      },
      "adresa_domiciliu_fiscal": {
        "ddenumire_Judet": "ILFOV",
        "ddenumire_Localitate": "BUKARESZT",
        "dstrada": "STR. EXEMPLU",
        "dnumar": "1",
        "dcod_Postal": "010001"
      }
    }
  ],
  "notFound": []
}
```

Gdy firma nie zostanie znaleziona, `found` jest pustą tablicą, a `notFound` zawiera podany CUI.

## Pola mapowane na FirmRequestDto

| Pole InvoiceJet (`FirmRequestDto`) | Ścieżka JSON ANAF | Typ |
|---|---|---|
| `firmName` | `found[0].date_generale.denumire` | string |
| `cuiValue` | `found[0].date_generale.cui` | int → string |
| `regCom` | `found[0].date_generale.nrRegCom` | string |
| `address` | `found[0].date_generale.adresa` | string |
| `county` | `found[0].adresa_domiciliu_fiscal.ddenumire_Judet` | string |
| `city` | `found[0].adresa_domiciliu_fiscal.ddenumire_Localitate` | string |

InvoiceJet używa wyłącznie `found[0]` — pierwszy wynik z tablicy.

## Obsługa błędów

| Scenariusz | Zachowanie InvoiceJet |
|---|---|
| Firma nieznaleziona (`found` puste) | `throw FirmNotFoundException()` → HTTP 404 |
| Błąd HTTP ze strony ANAF | Błąd propagowany bez obsługi — użytkownik widzi błąd HTTP |
| Timeout ANAF | Brak skonfigurowanego timeout — żądanie może blokować wątek bezterminowo |

## Anomalie i braki

| ID | Anomalia | Wpływ |
|---|---|---|
| ANAF-01 | Brak timeout dla `HttpClient` | Możliwe blokowanie wątków serwera przy niedostępności ANAF |
| ANAF-02 | Brak cache odpowiedzi | Każde kliknięcie "Wyszukaj po CUI" wysyła nowe żądanie do ANAF |
| ANAF-03 | Brak retry logic | Jeden timeout lub błąd sieciowy = błąd widoczny dla użytkownika |
| ANAF-04 | Używany wyłącznie `found[0]` | Brak obsługi sytuacji, gdy ANAF zwróci więcej niż jeden wynik |
| ANAF-05 | Wersja API: `v8` (hardcoded w konfiguracji) | Zmiana wersji API ANAF bez aktualizacji konfiguracji zerwie integrację |

## Wątpliwości i otwarte pytania

1. Czy ANAF ma limity rate limiting? Dokumentacja nie określa limitów — brak obsługi po stronie InvoiceJet.
2. Czy wersja `v8` API ANAF jest stabilna? Wersjonowanie URL sugeruje możliwość deprecacji starszych wersji.
3. Czy ANAF jest dostępny z infrastruktury hostingowej? Integracja zakłada bezpośredni dostęp bez proxy.
4. Czy `cui` powinien być walidowany po stronie InvoiceJet przed wysłaniem do ANAF? Brak walidacji formatu CUI.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny — zaadaptowany z `02_anaf/ANAF_integracja.md` do docelowej lokalizacji. |
