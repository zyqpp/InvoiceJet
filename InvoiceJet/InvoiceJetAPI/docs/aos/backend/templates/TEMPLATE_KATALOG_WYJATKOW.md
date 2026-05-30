<!--
SZABLON KATALOG_WYJATKOW — rejestr WSZYSTKICH wyjątków domenowych i ich mapowania na HTTP.
Plik docelowy: docs/aos/backend/KATALOG_WYJATKOW.md
ŹRÓDŁA: Domain/Exceptions/*, Presentation/Middleware/ExceptionMiddleware.cs.
KRYTYCZNE: oznacz wyjątki NIEMAPOWANE jawnie — wpadają w "catch (Exception)" → 500.
-->

# Katalog wyjątków — InvoiceJetAPI

**Data aktualizacji:** RRRR-MM-DD
**Źródło prawdy:** `InvoiceJet.Domain/Exceptions/*` + `InvoiceJet.Presentation/Middleware/ExceptionMiddleware.cs`

---

## 1. Wyjątki domenowe — mapowanie na HTTP

| Wyjątek | Plik | Mapowany jawnie? | Status HTTP | Komunikat (template) | Wywoływany przez |
|---|---|---|---|---|---|
| `[Exception]` | `[Domain/Exceptions/...cs]` | [tak/nie] | `[400/404/500]` | `[treść z konstruktora]` | `P-XX, P-YY` |

> Wyjątek „nie mapowany jawnie" = trafia do `catch (Exception)` w `ExceptionMiddleware` → **`500 Internal Server Error`**.

---

## 2. Wyjątki obsługiwane lokalnie w kontrolerze
<!-- Np. własny try/catch w kontrolerze omijający middleware — wymaga osobnego potraktowania. -->

| Kontroler.metoda | Obsługa | Status zwracany | Uwaga |
|---|---|---|---|
| `[Controller].[Method]` | własny `try/catch` | `BadRequest` | omija `ExceptionMiddleware` — [marker UWAGA] |

---
<!-- ===== PRZYKŁAD — usuń przed oddaniem =====
| UserHasNoAssociatedFirmException | Domain/Exceptions/.../...cs | tak | 400 | "User has no associated firm." | P-01, P-13, P-14, P-15 |
| InvalidPasswordException | Domain/Exceptions/InvalidPasswordException.cs | NIE | 500 | "Invalid password format." | P-03 — [UWAGA: brak mapowania w ExceptionMiddleware — WYMAGA WERYFIKACJI Z ZESPOŁEM] |
| ProductWithSameNameExistsException | ... | NIE | 500 | ... | P-09 — [UWAGA: brak mapowania] |
Wyjątki obsługiwane lokalnie: DocumentController.GenerateDocument — try/catch → BadRequest. [UWAGA: ...]
===== KONIEC PRZYKŁADU ===== -->
