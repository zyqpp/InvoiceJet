# GET /api/BankAccount/GetUserFirmBankAccounts — Lista kont bankowych

| Atrybut | Wartość |
|---|---|
| ID | API-14 |
| Metoda | GET |
| URL | `/api/BankAccount/GetUserFirmBankAccounts` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `BankAccountController.GetUserFirmBankAccounts` |
| Serwis | `IBankAccountService.GetUserFirmBankAccounts` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

Brak parametrów. userFirmId pobierany z JWT tokenu.

## Response

### 200 OK

```json
[
  {
    "id": 1,
    "bankName": "BRD Groupe Societe Generale",
    "iban": "RO49AAAA1B31007593840000",
    "currency": 0,
    "isActive": true
  }
]
```

**Currency enum:** `0 = Ron`, `1 = Eur`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
