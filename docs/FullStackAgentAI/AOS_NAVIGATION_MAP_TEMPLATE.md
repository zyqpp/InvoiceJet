# Szablony Mapy Nawigacji i Makiet

Ten dokument steruje agentem. Źródłem formatu dla map nawigacji są konkretne pliki szablonów w:

`docs/aos/application/templates/`

Agent nie twórzy mapy sekcji ani mapy pozycji menu z własnego ukladu.
Każdy dokument w `docs/aos/application/navigation/` musi powstac przez wypełnienie odpowiedniego `TEMPLATE_NAV_*.md` albo `TEMPLATE_HISTORIA_ZMIAN.md`.

## Folder sekcji menu

| Docelowy plik | Szablon obowiązkowy |
|---|---|
| `00_METADANE.md` | [TEMPLATE_NAV_00_METADANE.md](../aos/application/templates/TEMPLATE_NAV_00_METADANE.md) |
| `01_DIAGRAM_SEKCJI.md` | [TEMPLATE_NAV_01_DIAGRAM_SEKCJI.md](../aos/application/templates/TEMPLATE_NAV_01_DIAGRAM_SEKCJI.md) |
| `HISTORIA_ZMIAN.md` | [TEMPLATE_HISTORIA_ZMIAN.md](../aos/application/templates/TEMPLATE_HISTORIA_ZMIAN.md) |

## Folder pozycji menu

| Docelowy plik | Szablon obowiązkowy |
|---|---|
| `00_METADANE.md` | [TEMPLATE_NAV_00_METADANE.md](../aos/application/templates/TEMPLATE_NAV_00_METADANE.md) |
| `01_MAPA_MAKIET_POZYCJI.md` | [TEMPLATE_NAV_01_MAPA_MAKIET_POZYCJI.md](../aos/application/templates/TEMPLATE_NAV_01_MAPA_MAKIET_POZYCJI.md) |
| `02_ELEMENTY_ELEMENTARNE.md` | [TEMPLATE_NAV_02_ELEMENTY_ELEMENTARNE.md](../aos/application/templates/TEMPLATE_NAV_02_ELEMENTY_ELEMENTARNE.md) |
| `HISTORIA_ZMIAN.md` | [TEMPLATE_HISTORIA_ZMIAN.md](../aos/application/templates/TEMPLATE_HISTORIA_ZMIAN.md) |

## Zasady wypełniania

- Diagram Mermaid jest obowiązkowy dla sekcji menu i pozycji menu.
- Tabela linków Markdown jest obowiązkowa i jest stabilnym źródłem nawigacji.
- Każdy element mapy musi mieć typ: sekcja, pozycja menu, ekran, dialog, podgląd albo akcja.
- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Gdy nie ma potwierdzenia w dokumentacji front/back, użyj `[BRAK POTWIERDZENIA W DOKUMENTACJI]`.
- Gdy element wymaga śladu danych, ale brakuje powiązania z baza, użyj `[BRAK MAPOWANIA DO BAZY]`.

## Standard historii zmian

Każdy `HISTORIA_ZMIAN.md` ma używać tabeli:

`Wersja | Data | Autor | Model | Poziom inteligencji | Tryb / kontekst wykonania | Opis zmian`

Reguły:

- `Autor`: `Agent AI:Codex`,
- model wpisuj tylko wtedy, gdy jest jawnie znany; w przeciwnym razie `N/D [WYMAGA WERYFIKACJI]`,
- poziom inteligencji wpisuj tylko wtedy, gdy runtime go ujawnia; w przeciwnym razie `N/D [WYMAGA WERYFIKACJI]`,
- nie zgaduj rozmiaru kontekstu ani poziomu reasoning.

## Kontrola jakości

Przed oddaniem agent sprawdza:

- czy istnieja wymagane pliki sekcji albo pozycji menu,
- czy diagram Mermaid i tabela linków są obecne,
- czy linki Markdown prowadza do istniejacych dokumentów,
- czy markery są zgodne z [05_MARKERY_I_JAKOSC.md](05_MARKERY_I_JAKOSC.md).
