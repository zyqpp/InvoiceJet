# Zarządzanie kontami bankowymi — Kontrakt API

## Endpointy

| Operacja | HTTP | Ścieżka | Wejście | Wyjście |
|---|---|---|---|---|
| Pobranie listy | `GET` | `/api/BankAccount/GetUserFirmBankAccounts` | Brak | `ICollection<BankAccountDto>` |
| Dodanie konta | `POST` | `/api/BankAccount/AddUserFirmBankAccount` | `BankAccountDto` (`[FromBody]`) | `BankAccountDto` |
| Edycja konta | `PUT` | `/api/BankAccount/EditUserFirmBankAccount` | `BankAccountDto` (`[FromBody]`) | `BankAccountDto` |
| Usuwanie kont | `PUT` | `/api/BankAccount/DeleteUserFirmBankAccounts` | `int[] bankAccountIds` (`[FromBody]`) | `200 OK` |

---

## Kody odpowiedzi

| Status | Warunek |
|---|---|
| `200 OK` | Operacja zakończona sukcesem. |
| `400 Bad Request` | `UserHasNoAssociatedFirmException` lub `BankAccountAssociatedWithDocumentsException`. |
| `401 Unauthorized` | Brak poprawnego tokenu. |
| `403 Forbidden` | Brak roli `User`. |
| `500 Internal Server Error` | Błędy typu `Exception("Bank account not found.")` oraz inne wyjątki. |
