# GetDocuments — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji

Żaden z endpointów procesu P-14 nie zawiera jawnych reguł walidacji wejściowych w serwisie ani kontrolerze.

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| — | Brak reguł WAL | — | — | — | — | — |

> Użytkownik bez firmy (`GetUserFirmAsync` zwraca `null`) → `GetDocumentTableRecords` zwraca `200 OK []` bez błędu.
> Nieistniejące `documentId` → `GetDocumentById` zwraca `200 OK null` bez błędu (brak `404`). ⚠️

---

## 2. Mapowanie wyjątków na HTTP

Żaden wyjątek domenowy nie jest rzucany w trakcie wykonania procesu P-14.

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| (brak wyjątków rzucanych przez serwis) | N/D | N/D | N/D |

> Ewentualne wyjątki infrastrukturalne (EF Core, timeout DB) trafiają do `ExceptionMiddleware.cs › ExceptionMiddleware.InvokeAsync` catch-all → `500 Internal Server Error`.

---

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze/akcji | `[Authorize(Roles = "User")]` na klasie `DocumentController` |
| Wymagana rola | `User` |
| Źródło tożsamości | `IUserService.GetCurrentUserId()` (w `GetDocumentTableRecords` via `GetUserFirmAsync`); endpoint `GetDocumentById` **nie pobiera tożsamości** |
| Token | JWT (`JwtBearerDefaults.AuthenticationScheme`) |

---

## 4. Uwagi bezpieczeństwa

- [UWAGA: `GetDocumentById` nie weryfikuje własności dokumentu. `DocumentRepository.GetDocumentWithAllInfo(documentId)` pobiera dowolny dokument po `Id` bez sprawdzenia `UserFirmId`. Zalogowany użytkownik może odczytać dane dokumentu należącego do innej firmy, podając cudze `documentId`. Kotwica: `DocumentService.cs › DocumentService.GetDocumentById`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: Nieistniejące `documentId` → odpowiedź `200 OK` z `null` w body zamiast `404 Not Found`. Frontend musi obsługiwać `null` w odpowiedzi, co jest niestandardowe. Kotwica: `DocumentService.cs › DocumentService.GetDocumentById`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- [UWAGA: `DocumentTableRecordDto.DocumentStatus` to typ encji domenowej `InvoiceJet.Domain.Models.DocumentStatus`, nie dedykowane DTO. Naruszenie separacji warstw — zmiana modelu domenowego wpływa bezpośrednio na kształt API. Kotwica: `DocumentTableRecordDto.cs`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

- `GetDocumentTableRecords` poprawnie filtruje po `UserFirmId` — użytkownik widzi tylko dokumenty swojej firmy.
