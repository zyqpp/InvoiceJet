<!--
SZABLON 02 — KONTRAKT API (wymiar API)
Odbiorca priorytetowy: TESTER + DEVELOPER. POWIEL blok "Endpoint" dla KAŻDEGO endpointu procesu.
JSON musi mieć REALNE wartości (nie placeholdery), zgodne z polami DTO (patrz plik 04).
Definicja ukończenia: 03_MARKERY_I_WERYFIKACJA.md → sekcja 3.
-->

# [NAZWA PROCESU] — Kontrakt API

<!-- ===== POCZĄTEK BLOKU ENDPOINTU (powiel dla każdego) ===== -->
## `API-XX` — [HTTP] /api/[Controller]/[Action]

| Atrybut | Wartość |
|---|---|
| Metoda HTTP | `[GET/POST/PUT/DELETE]` |
| Ścieżka | `/api/[Controller]/[Action]/{param}` |
| Kontroler | `[Controller].cs › [Controller].[Method]` |
| Autoryzacja | `[Authorize(Roles = "...")]` / N/D |

### Parametry trasy / zapytania

| Parametr | Typ | Źródło | Opis |
|---|---|---|---|
| `[name]` | `[int]` | `[FromRoute]` / `[FromQuery]` | [opis] |

### Ciało żądania

| Element | Typ | Źródło |
|---|---|---|
| Body | `[Dto]` | `[FromBody]` |

Przykład żądania:
```json
{ "pole": "realna wartość" }
```

### Odpowiedź

| Status | Typ | Warunek |
|---|---|---|
| `200 OK` | `[Dto / plik / komunikat]` | [warunek sukcesu] |
| `400 Bad Request` | `{ "message": "..." }` | [wyjątek] |
| `401 Unauthorized` | — | brak/niepoprawny token |
| `403 Forbidden` | — | brak wymaganej roli |
| `500 Internal Server Error` | `{ "message": "..." }` | [wyjątek niemapowany / inny] |

Przykład odpowiedzi:
```json
{ "pole": "realna wartość" }
```
<!-- ===== KONIEC BLOKU ENDPOINTU ===== -->

---
<!-- ===== PRZYKŁAD (P-01) — usuń przed oddaniem =====
## `API-02` — POST /api/Document/AddDocument
| Metoda HTTP | `POST` | / | Ścieżka | `/api/Document/AddDocument` | Autoryzacja | `[Authorize(Roles = "User")]` |
Body: `DocumentRequestDto` (`[FromBody]`)
Odpowiedź 200: zwraca to samo `DocumentRequestDto` (uwaga: bez Id utworzonego dokumentu — patrz plik 01).
Odpowiedź 400: `{ "message": "User has no associated firm." }` gdy brak aktywnej firmy.
===== KONIEC PRZYKŁADU ===== -->
