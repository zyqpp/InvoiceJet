# DTO: BankAccountRequestDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-04 |
| Plik | `InvoiceJet.Application/DTOs/BankAccountRequestDto.cs` |
| Kierunek | Request + Response (dwukierunkowy) |
| Endpointy | [GET /api/BankAccount/GetAll](../../04_api_i_integracje/01_api_frontend/bank_account/GET_BankAccount_GetAll.md), [POST /api/BankAccount/Add](../../04_api_i_integracje/01_api_frontend/bank_account/POST_BankAccount_Add.md), [PUT /api/BankAccount/Edit](../../04_api_i_integracje/01_api_frontend/bank_account/PUT_BankAccount_Edit.md) |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `Id` | `int` | NIE | ID konta (0 przy dodawaniu) |
| `BankName` | `string` | NIE | Nazwa banku |
| `Iban` | `string` | NIE | Numer IBAN |
| `Currency` | `string` | NIE | Waluta (np. RON, EUR, USD) |

## Mapowanie AutoMapper

| Kierunek | Profile |
|---|---|
| `BankAccountRequestDto` → `BankAccount` | `BankAccountProfile` |
| `BankAccount` → `BankAccountRequestDto` | `BankAccountProfile` |

## Przykład JSON

```json
{
  "id": 3,
  "bankName": "BRD - Groupe Société Générale",
  "iban": "RO49AAAA1B31007593840000",
  "currency": "RON"
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
