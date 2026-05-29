# [NAZWA PROCESU] — Błędy i bezpieczeństwo

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut | `[Authorize]` |
| Rola | `[Role]` |
| Źródło użytkownika | `[IUserService]` |

## Błędy

| Wyjątek / warunek | Status HTTP | Źródło |
|---|---|---|
| `[Exception]` | `[status]` | `[ExceptionMiddleware]` |
