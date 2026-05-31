# DTO: FirmRequestDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-03 |
| Plik | `InvoiceJet.Application/DTOs/FirmRequestDto.cs` |
| Kierunek | Request + Response (dwukierunkowy) |
| Endpointy | `POST /api/Firm/AddFirm/{isClient}`, `PUT /api/Firm/EditFirm/{isClient}`, `GET /api/Firm/fromAnaf/{cui}`, `GET /api/Firm/GetUserActiveFirm` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `Id` | `int` | NIE | ID firmy (0 przy dodawaniu) |
| `FirmName` | `string` | NIE | Nazwa firmy |
| `CuiValue` | `string` | TAK | CUI / NIP rumuński |
| `RegCom` | `string` | TAK | Numer rejestracji handlowej |
| `Address` | `string` | TAK | Adres |
| `County` | `string` | TAK | Okręg (județ) |
| `City` | `string` | TAK | Miasto |

## Mapowanie AutoMapper

| Kierunek | Profile |
|---|---|
| `FirmRequestDto` → `Firm` | `FirmProfile` |
| `Firm` → `FirmRequestDto` | `FirmProfile` |

## Użycie jako Response

Przy `GET /api/Firm/GetUserActiveFirm` i `GET /api/Firm/fromAnaf/{cui}` — zwracany jako odpowiedź.

## Przykład JSON

```json
{
  "id": 5,
  "firmName": "EXAMPLE SRL",
  "cuiValue": "12345678",
  "regCom": "J40/1234/2020",
  "address": "STR. EXEMPLU NR. 1",
  "county": "ILFOV",
  "city": "BUKARESZT"
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
