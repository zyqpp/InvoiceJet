# PUT /api/BankAccount/EditUserFirmBankAccount — Edycja konta bankowego

| Atrybut | Wartość |
|---|---|
| ID | API-16 |
| Metoda | PUT |
| URL | `/api/BankAccount/EditUserFirmBankAccount` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `BankAccountController.EditUserFirmBankAccount` |
| Serwis | `IBankAccountService.EditUserFirmBankAccount` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Body (JSON) — `[FromBody] BankAccountDto` z `id > 0`

```json
{
  "id": 1,
  "bankName": "ING Bank Romania",
  "iban": "RO49INGB1B31007593840001",
  "currency": 1,
  "isActive": false
}
```

## Response

### 200 OK — zwraca zaktualizowany `BankAccountDto`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
