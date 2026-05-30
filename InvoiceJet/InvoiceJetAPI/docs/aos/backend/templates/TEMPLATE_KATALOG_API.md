<!--
SZABLON KATALOG_API — indeks WSZYSTKICH endpointów (1:1).
Plik docelowy: docs/aos/backend/KATALOG_API.md
Każdy endpoint występuje DOKŁADNIE RAZ. Sortuj po kontrolerze, potem po metodzie.
Aktualizacja: przy każdej zmianie endpointu (patrz 05_KATALOGI_PRZEKROJOWE.md sekcja 3).
-->

# Katalog API — InvoiceJetAPI

**Data aktualizacji:** RRRR-MM-DD
**Źródło prawdy:** `InvoiceJet.Presentation/Controllers/*`

| ID API | Metoda + ścieżka | Kontroler.metoda | Autoryzacja | DTO żądania | DTO odpowiedzi | Proces | Statusy |
|---|---|---|---|---|---|---|---|
| `API-01` | `[HTTP] /api/[...]` | `[Controller].[Method]` | `[Authorize(...)]` / N/D | `[Dto]` | `[Dto]` | [P-XX](processes/P-XX_.../00_METADANE.md) | `200, 400, 401, 500` |

---

## Konwencje

- ID są stałe (raz nadane nie zmieniają się).
- Wiersz „N/D" w kolumnie Autoryzacja sygnalizuje endpoint anonimowy.
- Statusy podaje się jako listę faktycznie zwracanych przez kontroler/middleware.
- Kolumna „Proces" linkuje do `00_METADANE.md` przypisanego procesu (`P-XX`).

---
<!-- ===== PRZYKŁAD (P-01..P-04) — usuń przed oddaniem =====
| API-01 | POST /api/Auth/register | AuthController.Register | N/D | UserRegisterDto | { token } | P-03 | 200, 400, 500 |
| API-02 | POST /api/Auth/login    | AuthController.Login    | N/D | UserLoginDto    | { token } | P-04 | 200, 400, 500 |
| API-03 | POST /api/Document/AddDocument | DocumentController.AddDocument | [Authorize(User)] | DocumentRequestDto | DocumentRequestDto | P-01 | 200, 400, 401, 403, 500 |
===== KONIEC PRZYKŁADU ===== -->
