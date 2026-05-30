# Pobranie firmy z ANAF — Błędy i bezpieczeństwo

## Błędy procesu

| Warunek | Wyjątek | Status HTTP | Źródło mapowania |
|---|---|---|---|
| ANAF zwraca błąd HTTP | `AnafFirmNotFoundException` | `404 Not Found` | `ExceptionMiddleware` |
| Błąd parsowania JSON | `AnafFirmNotFoundException` (po `catch`) | `404 Not Found` | `ExceptionMiddleware` |
| Inny błąd poza zakresem metody | `Exception` | `500 Internal Server Error` | `ExceptionMiddleware` |

---

## Autoryzacja

| Element | Wartość |
|---|---|
| Atrybut | `[Authorize(Roles = "User")]` |
| Skutek braku tokenu | `401 Unauthorized` |
| Skutek braku roli `User` | `403 Forbidden` |

---

## Uwagi bezpieczeństwa

- Proces przekazuje `cui` do zewnętrznego API.
- Proces nie zapisuje wyniku integracji w bazie.
- Brak lokalnego logowania technicznego błędów integracyjnych poza komunikatem wyjątku. [WYMAGA WERYFIKACJI]
