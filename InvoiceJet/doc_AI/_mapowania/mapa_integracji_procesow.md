# Mapa: Integracje zewnętrzne ↔ procesy (M-09)

| Pole | Wartość |
|---|---|
| ID dokumentu | M-09 |
| Typ dokumentu | mapa krzyżowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

InvoiceJet posiada jedną integrację zewnętrzną — z API ANAF (rumuńska administracja podatkowa). Integracja służy do autouzupełniania danych firmy na podstawie numeru CUI (odpowiednik NIP). Mapa opisuje przepływ danych od akcji użytkownika przez wewnętrzny endpoint do zewnętrznego API i z powrotem.

## Tabela mapowań

| Integracja | Endpoint zewnętrzny | Endpoint API wewnętrzny | Klasa serwisu | Metoda serwisu | Proces techniczny | Proces biznesowy |
|---|---|---|---|---|---|---|
| ANAF API | `POST https://webservicesp.anaf.ro/prod/FCTEL/rest/tva` (lub odpowiednik CUI lookup) | `GET /api/Firm/GetFirmFromAnaf` (API-04) | `FirmService` | `GetFirmFromAnaf(cui)` | Frontend → `GET /api/Firm/GetFirmFromAnaf?cui={cui}` → `FirmService.GetFirmFromAnaf()` → `HttpClient.PostAsync(ANAF_URL)` → mapowanie odpowiedzi → `FirmDto` → frontend | Użytkownik wpisuje numer CUI w formularzu firmy/klienta → klik „Pobierz dane z ANAF" → dane firmy (nazwa, adres, miasto, okręg) autouzupełniają formularz |

## Diagram przepływu (ANAF)

```
Użytkownik (przeglądarka)
    │  wpisuje CUI, klik "Pobierz z ANAF"
    ▼
Angular FirmService.getFirmFromAnaf(cui)
    │  GET /api/Firm/GetFirmFromAnaf?cui={cui}
    │  Nagłówek: Authorization: Bearer {JWT}
    ▼
FirmController.GetFirmDataFromAnaf
    │  [Authorize(Roles = "User")]
    │  wyodrębnia userId z JWT
    ▼
FirmService.GetFirmFromAnaf(cui)
    │  HttpClient.PostAsync(ANAF_ENDPOINT, {cui})
    ▼
ANAF API (zewnętrzny)
    │  POST https://webservicesp.anaf.ro/...
    │  Odpowiedź: dane firmy w formacie JSON
    ▼
FirmService → mapowanie → FirmDto
    ▼
FirmController → HTTP 200 FirmDto
    ▼
Angular → autouzupełnienie formularza (pola: Name, Address, City, County)
```

## Szczegóły integracji

| Właściwość | Wartość |
|---|---|
| Nazwa integracji | ANAF — Agenția Națională de Administrare Fiscală |
| Typ | REST API (zewnętrzny serwis HTTP) |
| Protokół | HTTPS POST |
| Parametr wejściowy | `cui` — numer identyfikacji podatkowej (Rumunia) |
| Pola wynikowe mapowane do `FirmDto` | `Name`, `Address`, `City`, `County` |
| Autoryzacja po stronie ANAF | brak (publiczny endpoint ANAF) |
| Autoryzacja po stronie InvoiceJet | `[Authorize]` — JWT wymagany |
| Endpoint wewnętrzny | `GET /api/Firm/GetFirmFromAnaf` (API-04) |
| Kontroler | `FirmController.GetFirmDataFromAnaf` |
| Serwis | `FirmService.GetFirmFromAnaf()` |
| Obsługa błędów | [Do weryfikacji] — brak informacji o fallback przy niedostępności ANAF |

## Ekrany korzystające z integracji

| Ekran | Komponent | Scenariusz użycia |
|---|---|---|
| EKRAN-04 Dane firmy | `FirmDetailsComponent` | Autouzupełnienie danych własnej firmy po CUI |
| DIALOG-01 Dodaj/Edytuj klienta | `AddEditClientDialogComponent` | Autouzupełnienie danych klienta po CUI |

## Uwagi

- ANAF API jest jedyną integracją zewnętrzną w projekcie — brak integracji z systemami płatności, pocztą e-mail, magazynami chmury itp.
- Dokładny URL endpointu ANAF należy zweryfikować w konfiguracji backendu (`appsettings.json` lub `HttpClient` w serwisie). [Do weryfikacji]
- Brak mechanizmu cache'owania odpowiedzi ANAF — każde kliknięcie generuje nowe żądanie do zewnętrznego API.
- Generowanie PDF (QuestPDF) jest procesem wewnętrznym — nie jest integracją zewnętrzną.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
