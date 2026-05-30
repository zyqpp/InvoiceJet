<!--
SZABLON 05 — WALIDACJE, BŁĘDY I BEZPIECZEŃSTWO (uwaga: nazwa pliku zachowana dla spójności)
Odbiorca priorytetowy: TESTER + ANALITYK + DEVELOPER.
Najważniejsza sekcja: KATALOG WALIDACJI. Każda reguła ma: podstawę w kodzie, warunek wyzwolenia, wyjątek i status (zasada ZB.9).
Definicja ukończenia: 03_MARKERY_I_WERYFIKACJA.md → sekcja 3.
-->

# [NAZWA PROCESU] — Walidacje, błędy i bezpieczeństwo

## 1. Katalog walidacji
<!-- TO JEST GŁÓWNA SEKCJA. Wypisz KAŻDĄ regułę walidacji sprawdzaną w procesie, w kolejności sprawdzania. -->

| ID | Reguła (po polsku) | Podstawa w kodzie | Warunek wyzwolenia błędu | Wyjątek | Status HTTP | Komunikat |
|---|---|---|---|---|---|---|
| `WAL-01` | [Co musi być spełnione] | `[Plik.cs › Klasa.Metoda]` | [Kiedy warunek nie jest spełniony] | `[Exception]` | `400` | `[treść z exception.Message]` |

> Jeżeli reguła pochodzi z atrybutu DTO (np. `[Required]`), zaznacz to w kolumnie „Podstawa w kodzie".
> Jeżeli walidacja jest pośrednia (np. wymóg istnienia rekordu w bazie), zaznacz to wyraźnie.

## 2. Mapowanie wyjątków na HTTP
<!-- Tabela wyjątków występujących w procesie. Sprawdź ExceptionMiddleware — wyjątek niemapowany leci jako 500. -->

| Wyjątek | Mapowany jawnie? | Status HTTP | Źródło mapowania |
|---|---|---|---|
| `[Exception]` | [tak/nie] | `[400/404/500]` | `ExceptionMiddleware.cs` / `[Controller].[Method]` (try/catch) |

> Pełen rejestr wyjątek→HTTP: `../../KATALOG_WYJATKOW.md`.

## 3. Autoryzacja i tożsamość

| Element | Wartość |
|---|---|
| Atrybut na kontrolerze/akcji | `[Authorize(Roles = "...")]` / N/D |
| Wymagana rola | `[User]` |
| Źródło tożsamości | `IUserService.GetCurrentUserId()` / `HttpContext.User` / [inne] |
| Token | JWT (`JwtBearerDefaults.AuthenticationScheme`) |

## 4. Uwagi bezpieczeństwa
<!-- Np. własny try/catch w kontrolerze omijający ExceptionMiddleware, brak walidacji rozmiaru pliku, dane wrażliwe w odpowiedzi. -->

- [Uwaga lub: „Brak uwag bezpieczeństwa."]

---
<!-- ===== PRZYKŁAD (P-01) — usuń przed oddaniem =====
| WAL-01 | Użytkownik ma aktywną firmę | DocumentService.cs › DocumentService.AddDocument | userFirmId == null | UserHasNoAssociatedFirmException | 400 | "User has no associated firm." |
| WAL-02 | Aktywna firma ma aktywne konto bankowe | DocumentService.AddDocument | brak BankAccount z IsActive=true | NoBankAccountAddedException | 400 | "No active bank account added." |
Mapowanie wyjątków: oba mapowane jawnie w ExceptionMiddleware.cs → 400.
Uwaga: DocumentController.GenerateDocument ma własny try/catch → BadRequest, omijając middleware.
[UWAGA: niespójność obsługi błędów — WYMAGA WERYFIKACJI Z ZESPOŁEM]
===== KONIEC PRZYKŁADU ===== -->
