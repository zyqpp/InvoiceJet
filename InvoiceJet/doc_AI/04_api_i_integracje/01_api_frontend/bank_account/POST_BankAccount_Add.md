# POST /api/BankAccount/AddUserFirmBankAccount — Dodanie konta bankowego

| Atrybut | Wartość |
|---|---|
| ID | API-15 |
| Metoda | POST |
| URL | `/api/BankAccount/AddUserFirmBankAccount` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `BankAccountController.AddUserFirmBankAccount` |
| Serwis | `IBankAccountService.AddUserFirmBankAccount` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Body (JSON) — `[FromBody] BankAccountDto`

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `id` | `int` | TAK (0 dla nowego) | — |
| `bankName` | `string` | TAK | Nazwa banku |
| `iban` | `string` | TAK | Numer IBAN |
| `currency` | `int` | TAK | `0=Ron`, `1=Eur` |
| `isActive` | `bool` | TAK | Czy konto aktywne |

**Przykład:**
```json
{
  "id": 0,
  "bankName": "BRD Groupe Societe Generale",
  "iban": "RO49AAAA1B31007593840000",
  "currency": 0,
  "isActive": true
}
```

## Response

### 200 OK — zwraca `BankAccountDto` z nadanym `Id`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
