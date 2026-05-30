# Logowanie użytkownika — Metadane

| Atrybut | Wartość |
|---|---|
| Proces | Logowanie użytkownika |
| Numer procesu | `P-04` |
| Kontroler | `AuthController` |
| Endpoint główny | `POST /api/Auth/login` |
| Metoda kontrolera | `Login([FromBody] UserLoginDto userDto)` |
| Serwis aplikacyjny | `AuthService` |
| Metoda serwisu | `LoginUser(UserLoginDto userDto)` |
| DTO żądania | `UserLoginDto` |
| DTO odpowiedzi | Obiekt anonimowy `{ token }` |
| Encje | `User` |
| Repozytoria | `Users` |
| Autoryzacja | Brak |
| Status dokumentu | Do weryfikacji technicznej |
| Data utworzenia | 2026-05-29 |
| Autor | Agent AI |
