# GetDashboardStats — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

Brak jawnych reguł walidacji. Użytkownik bez firmy → cichy fallback.

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| — | Brak WAL — użytkownik bez firmy → `new DashboardStatsDto()` | `DocumentService.cs › DocumentService.GetDashboardStats` | `GetUserFirmAsync == null` | brak | `200 OK` (zerowe pola) | — |

---

## 2. Mapowanie wyjątków na HTTP

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| Wyjątki EF Core (np. błąd tłumaczenia LINQ z `DocumentType!.Id`) | nie | `500 Internal Server Error` | `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` (catch-all) |

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

- Dane filtrowane po `UserFirmId` — każdy użytkownik widzi tylko statystyki swojej firmy. ✅

- [UWAGA: `GetTotalClientsAsync` przyjmuje `UserId` zamiast `UserFirmId`. W scenariuszu wielu użytkowników jednej firmy może zwracać różne liczby klientów. Kotwica: `DocumentService.cs › DocumentService.GetDashboardStats`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: Null-forgiving `d.DocumentType!.Id` w zapytaniach filtrujących. Dokument bez przypisanego `DocumentTypeId` może spowodować wyjątek EF przy tłumaczeniu do SQL. Kotwica: `DocumentService.cs › DocumentService.GetTotalDocumentsAsync / GetMonthlyTotalsAsync`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: Zapytania wykonywane sekwencyjnie zamiast `Task.WhenAll` — zbędne oczekiwanie na wyniki. Kotwica: `DocumentService.cs › DocumentService.GetDashboardStats`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: Brak firmy → `MonthlyTotals = null` zamiast `[]`. Frontend może crashować. Kotwica: `DashboardStatsDto.cs`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]
