# Rejestracja użytkownika — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Rejestracja użytkownika |
| Numer procesu | `P-03` |
| Kontroler | `AuthController` |
| Endpoint główny | `POST /api/Auth/register` |
| Metoda kontrolera | `Register([FromBody] UserRegisterDto userDto)` |
| Serwis aplikacyjny | `AuthService` |
| Metoda serwisu | `RegisterUser(UserRegisterDto userDto)` |
| DTO żądania | `UserRegisterDto` |
| DTO odpowiedzi | Obiekt anonimowy `{ token }` |
| Encje | `User` |
| Repozytoria | `Users` |
| Autoryzacja | Brak |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |

---

## Pliki źródłowe

| Obszar | Plik |
|---|---|
| Kontroler | `InvoiceJet.Presentation/Controllers/AuthController.cs` |
| Serwis | `InvoiceJet.Application/Services/Impl/AuthService.cs` |
| DTO | `InvoiceJet.Application/DTOs/UserRegisterDto.cs` |
| Encja | `InvoiceJet.Domain/Models/User.cs` |
| Middleware błędów | `InvoiceJet.Presentation/Middleware/ExceptionMiddleware.cs` |
