# GetDocumentAutofillInfo — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| — | Brak reguł WAL (brak wyjątków) | `DocumentService.cs › DocumentService.GetDocumentAutofillInfo` | `userFirmId == null` → `return new DocumentAutofillDto()` | brak | `200 OK` (null pola) | — |

> Serwis nie rzuca wyjątku gdy brak firmy — zwraca cichy obiekt z polami `null`.

---

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| Wyjątki EF Core / infrastrukturalne | nie | `500 Internal Server Error` | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` (catch-all) |

> Pełen rejestr wyjątek→HTTP: `../../KATALOG_WYJATKOW.md`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze/akcji | `[Authorize(Roles = "User")]` na klasie `DocumentController` |
| Wymagana rola | `User` |
| Źródło tożsamości | `IUserService.GetCurrentUserId()` → `userId` |
| Token | JWT (`JwtBearerDefaults.AuthenticationScheme`) |

---

## 4. Uwagi bezpieczeństwa

- [UWAGA: Gdy `GetUserFirmIdAsync` zwraca `null`, serwis zwraca `new DocumentAutofillDto()` z czterema polami `null` zamiast pustych list. Frontend może dostać `{ clients: null, ... }` i crashować przy iteracji. Kotwica: `DocumentService.cs › DocumentService.GetDocumentAutofillInfo`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- Klienci filtrowany przez `UserFirms.Any(uf => uf.UserId == userId && uf.IsClient)` — użytkownik widzi tylko swoje firmy klienckie. ✅

- Serie dokumentów filtrowane przez `UserFirmId` — użytkownik widzi tylko swoje serie. ✅

- Produkty filtrowane przez `UserFirmId` — użytkownik widzi tylko swoje produkty. ✅

- `DocumentStatuses` bez filtra firmy — wszystkie statusy globalne (seed: 2 rekordy). Brak danych wrażliwych. ✅
