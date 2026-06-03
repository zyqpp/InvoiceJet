# DTO: FirmRequestDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-03 |
| Plik | `InvoiceJet.Application/DTOs/FirmRequestDto.cs` |
| Kierunek | Request + Response (dwukierunkowy) |
| Endpointy | [POST /api/Firm/AddFirm](../../04_api_i_integracje/01_api_frontend/firm/POST_Firm_AddFirm.md), [PUT /api/Firm/EditFirm](../../04_api_i_integracje/01_api_frontend/firm/PUT_Firm_EditFirm.md), [GET /api/Firm/fromAnaf](../../04_api_i_integracje/01_api_frontend/firm/GET_Firm_fromAnaf.md), [GET /api/Firm/GetUserActiveFirm](../../04_api_i_integracje/01_api_frontend/firm/GET_Firm_GetUserActiveFirm.md) |
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

Przy [GET /api/Firm/GetUserActiveFirm](../../04_api_i_integracje/01_api_frontend/firm/GET_Firm_GetUserActiveFirm.md) i [GET /api/Firm/fromAnaf](../../04_api_i_integracje/01_api_frontend/firm/GET_Firm_fromAnaf.md) — zwracany jako odpowiedź.

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
