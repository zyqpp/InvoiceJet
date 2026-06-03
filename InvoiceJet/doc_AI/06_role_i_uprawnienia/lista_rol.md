# Lista ról

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Zidentyfikowane role (1)

| ID | Rola | Opis | Dokument |
|---|---|---|---|
| ROLA-01 | `User` | Jedyna rola w systemie. Zalogowany użytkownik. Pełny dostęp do swoich zasobów. | [User.md](User.md) |

## Macierz ról × endpointów

| Endpoint | Anonimowy | User |
|---|---|---|
| `POST /api/Auth/register` | ✅ | ✅ |
| `POST /api/Auth/login` | ✅ | ✅ |
| Wszystkie pozostałe (29) | ❌ | ✅ |

## Uwagi

- System nie implementuje ról administracyjnych
- Rola `User` nadawana hardcoded przy rejestracji: `Role = "User"`
- Rola zawarta w JWT claim `ClaimTypes.Role`
- `[Authorize(Roles = "User")]` na wszystkich 4 kontrolerach (wszystkie metody chroniące zasoby)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
