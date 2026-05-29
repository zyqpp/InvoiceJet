# Szablony Mapy Nawigacji i Makiet

Ten dokument steruje agentem. Zrodlem formatu dla map nawigacji sa konkretne pliki szablonow w:

`docs/aos/application/templates/`

Agent nie tworzy mapy sekcji ani mapy pozycji menu z wlasnego ukladu.
Kazdy dokument w `docs/aos/application/navigation/` musi powstac przez wypelnienie odpowiedniego `TEMPLATE_NAV_*.md` albo `TEMPLATE_HISTORIA_ZMIAN.md`.

## Folder sekcji menu

| Docelowy plik | Szablon obowiazkowy |
|---|---|
| `00_METADANE.md` | [TEMPLATE_NAV_00_METADANE.md](../aos/application/templates/TEMPLATE_NAV_00_METADANE.md) |
| `01_DIAGRAM_SEKCJI.md` | [TEMPLATE_NAV_01_DIAGRAM_SEKCJI.md](../aos/application/templates/TEMPLATE_NAV_01_DIAGRAM_SEKCJI.md) |
| `HISTORIA_ZMIAN.md` | [TEMPLATE_HISTORIA_ZMIAN.md](../aos/application/templates/TEMPLATE_HISTORIA_ZMIAN.md) |

## Folder pozycji menu

| Docelowy plik | Szablon obowiazkowy |
|---|---|
| `00_METADANE.md` | [TEMPLATE_NAV_00_METADANE.md](../aos/application/templates/TEMPLATE_NAV_00_METADANE.md) |
| `01_MAPA_MAKIET_POZYCJI.md` | [TEMPLATE_NAV_01_MAPA_MAKIET_POZYCJI.md](../aos/application/templates/TEMPLATE_NAV_01_MAPA_MAKIET_POZYCJI.md) |
| `02_ELEMENTY_ELEMENTARNE.md` | [TEMPLATE_NAV_02_ELEMENTY_ELEMENTARNE.md](../aos/application/templates/TEMPLATE_NAV_02_ELEMENTY_ELEMENTARNE.md) |
| `HISTORIA_ZMIAN.md` | [TEMPLATE_HISTORIA_ZMIAN.md](../aos/application/templates/TEMPLATE_HISTORIA_ZMIAN.md) |

## Zasady wypelniania

- Diagram Mermaid jest obowiazkowy dla sekcji menu i pozycji menu.
- Tabela linkow Markdown jest obowiazkowa i jest stabilnym zrodlem nawigacji.
- Kazdy element mapy musi miec typ: sekcja, pozycja menu, ekran, dialog, podglad albo akcja.
- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Gdy nie ma potwierdzenia w dokumentacji front/back, uzyj `[BRAK POTWIERDZENIA W DOKUMENTACJI]`.
- Gdy element wymaga sladu danych, ale brakuje powiazania z baza, uzyj `[BRAK MAPOWANIA DO BAZY]`.

## Standard historii zmian

Kazdy `HISTORIA_ZMIAN.md` ma uzywac tabeli:

`Wersja | Data | Autor | Model | Poziom inteligencji | Tryb / kontekst wykonania | Opis zmian`

Reguly:

- `Autor`: `Agent AI:Codex`,
- model wpisuj tylko wtedy, gdy jest jawnie znany; w przeciwnym razie `N/D [WYMAGA WERYFIKACJI]`,
- poziom inteligencji wpisuj tylko wtedy, gdy runtime go ujawnia; w przeciwnym razie `N/D [WYMAGA WERYFIKACJI]`,
- nie zgaduj rozmiaru kontekstu ani poziomu reasoning.

## Kontrola jakosci

Przed oddaniem agent sprawdza:

- czy istnieja wymagane pliki sekcji albo pozycji menu,
- czy diagram Mermaid i tabela linkow sa obecne,
- czy linki Markdown prowadza do istniejacych dokumentow,
- czy markery sa zgodne z [05_MARKERY_I_JAKOSC.md](05_MARKERY_I_JAKOSC.md).
