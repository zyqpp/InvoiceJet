# LoginUser — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | `Logowanie użytkownika` |
| Numer procesu | `P-02` |
| Kontroler(y) | `AuthController` |
| Serwis(y) aplikacyjny | `AuthService` |
| Metoda(y) serwisu | `AuthService.LoginUser`, `AuthService.CreateToken` |
| DTO żądania | `UserLoginDto` |
| DTO odpowiedzi | N/D — odpowiedź jest anonimowym obiektem `{ token }` |
| Encje | `User` (odczyt) |
| Repozytoria | `IUserRepository` (`_unitOfWork.Users`) |
| Wyjątki | `UserNotFoundException`, `IncorrectPasswordException` (link: `../../KATALOG_WYJATKOW.md`) |
| Integracje | brak |
| Autoryzacja | N/D — endpoint publiczny (brak atrybutu `[Authorize]`) |
| Status dokumentu | Roboczy |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
| Powiązana funkcja frontu | `[POZA ZAKRESEM — ETAP FULLSTACK]` |

## Endpointy procesu

| ID API | Metoda + ścieżka | Metoda kontrolera | Cel |
|---|---|---|---|
| `API-02` | `POST /api/Auth/login` | `AuthController.Login` | Logowanie użytkownika — weryfikacja hasła i wydanie JWT |

## Komponenty (kotwice)

| Rola | Kotwica |
|---|---|
| Kontroler | `AuthController.cs › AuthController.Login` |
| Serwis — logowanie | `AuthService.cs › AuthService.LoginUser` |
| Serwis — token | `AuthService.cs › AuthService.CreateToken` |
| Repozytorium | `UserRepository.cs › UserRepository.Query` (odczyt przez `FirstOrDefaultAsync`) |
