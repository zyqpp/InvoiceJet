# Zarządzanie kontami bankowymi — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Zarządzanie kontami bankowymi |
| Numer procesu | `P-10` |
| Kontroler | `BankAccountController` |
| Endpointy | `GET /api/BankAccount/GetUserFirmBankAccounts`, `POST /api/BankAccount/AddUserFirmBankAccount`, `PUT /api/BankAccount/EditUserFirmBankAccount`, `PUT /api/BankAccount/DeleteUserFirmBankAccounts` |
| Serwis aplikacyjny | `BankAccountService` |
| Metody serwisu | `GetUserFirmBankAccounts()`, `AddUserFirmBankAccount()`, `EditUserFirmBankAccount()`, `DeleteUserFirmBankAccounts()` |
| DTO | `BankAccountDto` |
| Encje | `BankAccount`, `Document` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
