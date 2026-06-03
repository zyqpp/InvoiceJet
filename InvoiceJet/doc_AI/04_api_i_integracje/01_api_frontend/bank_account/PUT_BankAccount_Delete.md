# PUT /api/BankAccount/DeleteUserFirmBankAccounts — Usunięcie kont bankowych

| Atrybut | Wartość |
|---|---|
| ID | API-17 |
| Metoda | PUT |
| URL | `/api/BankAccount/DeleteUserFirmBankAccounts` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `BankAccountController.DeleteUserFirmBankAccounts` |
| Serwis | `IBankAccountService.DeleteUserFirmBankAccounts` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Body (JSON) — `[FromBody] int[]`

```json
[1, 2, 3]
```

**Uwaga:** Ten endpoint ma `[FromBody]` — różni się od API-09, API-13, API-21, które nie mają `[FromBody]`.

## Response

### 200 OK — pusta odpowiedź

> **⚠️ Uwaga:** Usunięcie konta bankowego, które jest powiązane z dokumentami, wywoła kaskadowe usunięcie tych dokumentów (FK-09 CASCADE DELETE).

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
