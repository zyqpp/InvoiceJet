# Integracja zewnętrzna: ANAF API

| Atrybut | Wartość |
|---|---|
| System zewnętrzny | ANAF — Agenția Națională de Administrare Fiscală |
| Kraj | Rumunia |
| Cel | Autouzupełnienie danych firmy na podstawie numeru CUI |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

ANAF to rumuński urząd skarbowy udostępniający publiczne API do weryfikacji firm rumuńskich na podstawie numeru CUI (Cod Unic de Înregistrare — odpowiednik NIP). InvoiceJet używa tego API do autouzupełnienia danych firmy w formularzach.

## Konfiguracja

```json
// appsettings.json
{
  "AppSettings": {
    "AnafApiUrl": "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva"
  }
}
```

## Format żądania

```http
POST https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva
Content-Type: application/json

[
  {
    "cui": 12345678,
    "data": "2026-05-31"
  }
]
```

**Uwagi:**
- `cui` — integer (nie string!)
- `data` — data w formacie `YYYY-MM-DD` (bieżąca data)
- Tablica — ANAF API obsługuje batch queries, ale InvoiceJet zawsze wysyła jeden element

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
      },
      "inregistrare_scop_Tva": { ... },
      "stare_inregistrare_scop_Tva": { ... }
    }
  ],
  "notFound": []
}
```

## Mapowanie pól InvoiceJet ← ANAF

| Pole InvoiceJet | Ścieżka JSON ANAF | Typ |
|---|---|---|
| `firmName` | `found[0].date_generale.denumire` | string |
| `cuiValue` | `found[0].date_generale.cui` | int → string |
| `regCom` | `found[0].date_generale.nrRegCom` | string |
| `address` | `found[0].date_generale.adresa` | string |
| `county` | `found[0].adresa_domiciliu_fiscal.ddenumire_Judet` | string |
| `city` | `found[0].adresa_domiciliu_fiscal.ddenumire_Localitate` | string |

## Obsługa błędów

| Scenariusz | Zachowanie |
|---|---|
| Firma nieznaleziona (`found` puste) | `throw FirmNotFoundException()` → 404 |
| HTTP error z ANAF | Propagowany jako błąd HTTP |
| Timeout ANAF | Brak timeout — blokuje żądanie |

## Endpointy InvoiceJet korzystające z ANAF

| Endpoint | Kontekst |
|---|---|
| `GET /api/Firm/fromAnaf/{cui}` | Autouzupełnienie danych firmy i klientów |

## Ograniczenia i anomalie

| # | Anomalia |
|---|---|
| ANAF-01 | Brak timeout dla HttpClient — możliwe blokowanie wątków |
| ANAF-02 | Brak cache — każde kliknięcie wysyła żądanie do ANAF |
| ANAF-03 | Brak retry logic — jeden timeout = błąd użytkownika |
| ANAF-04 | Używany jest tylko `found[0]` — brak obsługi wielu wyników |
| ANAF-05 | Wersja API: `v8` — zmiany API ANAF mogą zepsuć integrację |

## Dostępność publiczna

ANAF API jest publicznie dostępne bez klucza API ani autoryzacji — wystarczy znać numer CUI.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
