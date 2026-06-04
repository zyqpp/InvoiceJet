# ManageBankAccounts — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Zarządzanie kontami bankowymi aktywnej firmy` |
| Numer procesu | `P-10` |
| Kontroler(y) | `BankAccountController` |
| Serwis(y) aplikacyjny | `BankAccountService` |
| Metoda(y) serwisu | `BankAccountService.GetUserFirmBankAccounts`, `BankAccountService.AddUserFirmBankAccount`, `BankAccountService.EditUserFirmBankAccount`, `BankAccountService.DeleteUserFirmBankAccounts`, `BankAccountService.DeactivateOtherBankAccounts` |
| DTO żądania | `BankAccountDto` (AddUserFirmBankAccount, EditUserFirmBankAccount); `int[]` (DeleteUserFirmBankAccounts) |
| DTO odpowiedzi | `BankAccountDto`, `ICollection<BankAccountDto>` |
| Encje | `BankAccount`, `UserFirm`, `Document` |
| Repozytoria | `IBankAccountRepository` (`BankAccountRepository`), `IUserRepository` (`GetUserFirmIdAsync`), `IDocumentRepository` (`Query`) |
| Wyjątki | `UserHasNoAssociatedFirmException`, `BankAccountAssociatedWithDocumentsException` (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | brak |
| Autoryzacja | `[Authorize(Roles = "User")]` na klasie `BankAccountController` |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-30 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `POZA ZAKRESEM — ETAP FULLSTACK` |

---

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-14` | `GET /api/BankAccount/GetUserFirmBankAccounts` | `BankAccountController.GetUserFirmBankAccounts` | Pobierz listę kont bankowych aktywnej firmy |
| `API-15` | `POST /api/BankAccount/AddUserFirmBankAccount` | `BankAccountController.AddUserFirmBankAccount` | Dodaj nowe konto bankowe do aktywnej firmy |
| `API-16` | `PUT /api/BankAccount/EditUserFirmBankAccount` | `BankAccountController.EditUserFirmBankAccount` | Edytuj dane istniejącego konta bankowego |
| `API-17` | `PUT /api/BankAccount/DeleteUserFirmBankAccounts` | `BankAccountController.DeleteUserFirmBankAccounts` | Usuń jedno lub wiele kont bankowych (batch) |

---

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler — GetAll | `BankAccountController.cs › BankAccountController.GetUserFirmBankAccounts` |
| Kontroler — Add | `BankAccountController.cs › BankAccountController.AddUserFirmBankAccount` |
| Kontroler — Edit | `BankAccountController.cs › BankAccountController.EditUserFirmBankAccount` |
| Kontroler — Delete | `BankAccountController.cs › BankAccountController.DeleteUserFirmBankAccounts` |
| Serwis — GetAll | `BankAccountService.cs › BankAccountService.GetUserFirmBankAccounts` |
| Serwis — Add | `BankAccountService.cs › BankAccountService.AddUserFirmBankAccount` |
| Serwis — Edit | `BankAccountService.cs › BankAccountService.EditUserFirmBankAccount` |
| Serwis — Delete | `BankAccountService.cs › BankAccountService.DeleteUserFirmBankAccounts` |
| Serwis — dezaktywacja kont | `BankAccountService.cs › BankAccountService.DeactivateOtherBankAccounts` |
| Repozytorium — GetAll kont firmy | `BankAccountRepository.cs › BankAccountRepository.GetUserFirmBankAccountsAsync` |
| Repozytorium — GetById | `GenericRepository.cs › GenericRepository.GetByIdAsync` |
| Repozytorium — Add | `GenericRepository.cs › GenericRepository.AddAsync` |
| Repozytorium — Update | `GenericRepository.cs › GenericRepository.UpdateAsync` |
| Repozytorium — Remove | `GenericRepository.cs › GenericRepository.RemoveAsync` |
| Repozytorium — sprawdź powiązanie z dokumentem | `BankAccountService.cs › BankAccountService.DeleteUserFirmBankAccounts` — `_unitOfWork.Documents.Query().AnyAsync(...)` |
| Profil mapowania | `BankAccountProfile.cs › BankAccountProfile` — `CreateMap<BankAccount, BankAccountDto>().ReverseMap()` |
| Middleware wyjątków | `ExceptionMiddleware.cs` — mapowanie `UserHasNoAssociatedFirmException` i `BankAccountAssociatedWithDocumentsException` |
| Tożsamość użytkownika | `UserService.cs › UserService.GetCurrentUserId` |
| Unit of Work | `UnitOfWork.cs › UnitOfWork.CompleteAsync` |
