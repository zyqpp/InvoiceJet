# DeleteDocuments — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

Brak jawnych reguł walidacji w serwisie lub kontrolerze.

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| — | Brak reguł WAL | — | — | — | — | — |

> Serwis nie weryfikuje: przynależności dokumentów do firmy użytkownika, istnienia dokumentów, niepustości tablicy.

---

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| `NullReferenceException` (z `d.DocumentProducts!`) | nie | `500 Internal Server Error` | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` (catch-all) |
| Wyjątki EF Core (DB constraint, timeout) | nie | `500 Internal Server Error` | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` (catch-all) |

> Pełen rejestr wyjątek→HTTP: `../../KATALOG_WYJATKOW.md`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze/akcji | `[Authorize(Roles = "User")]` na klasie `DocumentController` |
| Wymagana rola | `User` |
| Źródło tożsamości | Brak — serwis nie pobiera `GetCurrentUserId()` ani `GetUserFirmAsync()` |
| Token | JWT (`JwtBearerDefaults.AuthenticationScheme`) |

---

## 4. Uwagi bezpieczeństwa

- [UWAGA: Krytyczny brak ownership check. `DeleteDocuments` usuwa dokumenty wyłącznie na podstawie listy `Id` bez sprawdzenia `UserFirmId`. Zalogowany użytkownik może usunąć dokumenty innej firmy, znając (lub zgadując) ich `Id`. Kotwica: `DocumentService.cs › DocumentService.DeleteDocuments`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: Endpoint używa metody HTTP `PUT` zamiast semantycznie poprawnego `DELETE`. Wpływa to na dokumentację, mechanizmy CORS i polityki sieciowe. Kotwica: `DocumentController.cs › DocumentController.DeleteDocuments` (`[HttpPut("DeleteDocuments")]`). — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: Null-forgiving `d.DocumentProducts!` w `SelectMany` — przy błędzie Include (np. błędna konfiguracja EF) spowoduje `NullReferenceException → 500`. Kotwica: `DocumentService.cs › DocumentService.DeleteDocuments`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- Serwis nie pobiera tożsamości użytkownika (`GetCurrentUserId()` nie jest wywoływane) — autoryzacja opiera się wyłącznie na JWT, bez powiązania z zasobami użytkownika.
