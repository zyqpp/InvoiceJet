# Szablony AOS aplikacyjnego

Ten dokument steruje agentem. Zrodlem formatu nie jest opis ponizej, tylko konkretne pliki szablonow w:

`docs/aos/application/templates/`

Agent nie tworzy dokumentu AOS aplikacyjnego z pustego pliku ani z wlasnego ukladu sekcji.
Kazdy dokument w `docs/aos/application/flows/A-XX_Nazwa/` musi powstac przez wypelnienie odpowiedniego `TEMPLATE_*.md`.

## Komplet dokumentow przeplywu

| Docelowy plik | Szablon obowiazkowy |
|---|---|
| `00_METADANE.md` | [TEMPLATE_00_METADANE.md](../aos/application/templates/TEMPLATE_00_METADANE.md) |
| `01_PRZEGLAD_END_TO_END.md` | [TEMPLATE_01_PRZEGLAD_END_TO_END.md](../aos/application/templates/TEMPLATE_01_PRZEGLAD_END_TO_END.md) |
| `02_MAPA_POL_UI_DO_DANYCH.md` | [TEMPLATE_02_MAPA_POL_UI_DO_DANYCH.md](../aos/application/templates/TEMPLATE_02_MAPA_POL_UI_DO_DANYCH.md) |
| `03_OPERACJE_I_PRZYCISKI.md` | [TEMPLATE_03_OPERACJE_I_PRZYCISKI.md](../aos/application/templates/TEMPLATE_03_OPERACJE_I_PRZYCISKI.md) |
| `04_GRIDY_LISTY_ZAPYTANIA.md` | [TEMPLATE_04_GRIDY_LISTY_ZAPYTANIA.md](../aos/application/templates/TEMPLATE_04_GRIDY_LISTY_ZAPYTANIA.md) |
| `05_WALIDACJE_BLEDY_BEZPIECZENSTWO.md` | [TEMPLATE_05_WALIDACJE_BLEDY_BEZPIECZENSTWO.md](../aos/application/templates/TEMPLATE_05_WALIDACJE_BLEDY_BEZPIECZENSTWO.md) |
| `06_SCENARIUSZE_TESTOWE_E2E.md` | [TEMPLATE_06_SCENARIUSZE_TESTOWE_E2E.md](../aos/application/templates/TEMPLATE_06_SCENARIUSZE_TESTOWE_E2E.md) |
| `07_SLEDZENIE_ZRODEL.md` | [TEMPLATE_07_SLEDZENIE_ZRODEL.md](../aos/application/templates/TEMPLATE_07_SLEDZENIE_ZRODEL.md) |
| `HISTORIA_ZMIAN.md` | [TEMPLATE_HISTORIA_ZMIAN.md](../aos/application/templates/TEMPLATE_HISTORIA_ZMIAN.md) |

## Zasady wypelniania

- Zachowaj nazwy sekcji i kolumn z szablonu.
- Usuwaj tylko sekcje, ktore szablon jawnie pozwala oznaczyc jako niedotyczace.
- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Gdy nie ma potwierdzenia w dokumentacji front/back, uzyj `[BRAK POTWIERDZENIA W DOKUMENTACJI]`.
- Gdy slad UI/API/DB urywa sie przed baza, uzyj `[BRAK MAPOWANIA DO BAZY]`.
- Tabele mapowania musza miec kolumne `Dowod` albo osobna sekcje `Dowody / zrodla`.

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

- czy istnieje komplet wymaganych plikow,
- czy dokumenty zachowuja kolumny z szablonow,
- czy brak danych jest zapisany jako `N/D`,
- czy markery sa zgodne z [05_MARKERY_I_JAKOSC.md](05_MARKERY_I_JAKOSC.md),
- czy linki do dokumentow zrodlowych prowadza do istniejacych plikow.
