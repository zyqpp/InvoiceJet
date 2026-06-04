# RegisterUser — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Rejestracja nowego użytkownika` |
| Numer procesu | `P-01` |
| Kontroler(y) | `AuthController` |
| Serwis(y) aplikacyjny | `AuthService` |
| Metoda(y) serwisu | `AuthService.RegisterUser`, `AuthService.CreateToken` |
| DTO żądania | `UserRegisterDto` |
| DTO odpowiedzi | N/D — odpowiedź jest anonimowym obiektem `{ token }` |
| Encje | `User` |
| Repozytoria | `IUserRepository` (`_unitOfWork.Users`) |
| Wyjątki | `UserAlreadyExistsException`, `InvalidPasswordException`, `PasswordMismatchException` (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | brak |
| Autoryzacja | N/D — endpoint publiczny (brak atrybutu `[Authorize]`) |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `[POZA ZAKRESEM — ETAP FULLSTACK]` |

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-01` | `POST /api/Auth/register` | `AuthController.Register` | Rejestracja nowego konta użytkownika |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler | `AuthController.cs › AuthController.Register` |
| Serwis — rejestracja | `AuthService.cs › AuthService.RegisterUser` |
| Serwis — token | `AuthService.cs › AuthService.CreateToken` |
| Repozytorium | `UserRepository.cs › UserRepository.Query` (odczyt), `GenericRepository.cs › GenericRepository.AddAsync` (zapis) |
