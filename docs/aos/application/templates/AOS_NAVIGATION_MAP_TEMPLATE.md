# Indeks szablonów Mapy Nawigacji i Makiet

Ten katalog jest źródłem formatu dla dokumentów w `docs/aos/application/navigation/`.
Każda sekcja i pozycja menu musi korzystać z poniższych szablonów.

## Folder sekcji menu

| Docelowy plik | Szablon |
|---|---|
| `00_METADANE.md` | [TEMPLATE_NAV_00_METADANE.md](TEMPLATE_NAV_00_METADANE.md) |
| `01_DIAGRAM_SEKCJI.md` | [TEMPLATE_NAV_01_DIAGRAM_SEKCJI.md](TEMPLATE_NAV_01_DIAGRAM_SEKCJI.md) |
| `HISTORIA_ZMIAN.md` | [TEMPLATE_HISTORIA_ZMIAN.md](TEMPLATE_HISTORIA_ZMIAN.md) |

## Folder pozycji menu

| Docelowy plik | Szablon |
|---|---|
| `00_METADANE.md` | [TEMPLATE_NAV_00_METADANE.md](TEMPLATE_NAV_00_METADANE.md) |
| `01_MAPA_MAKIET_POZYCJI.md` | [TEMPLATE_NAV_01_MAPA_MAKIET_POZYCJI.md](TEMPLATE_NAV_01_MAPA_MAKIET_POZYCJI.md) |
| `02_ELEMENTY_ELEMENTARNE.md` | [TEMPLATE_NAV_02_ELEMENTY_ELEMENTARNE.md](TEMPLATE_NAV_02_ELEMENTY_ELEMENTARNE.md) |
| `HISTORIA_ZMIAN.md` | [TEMPLATE_HISTORIA_ZMIAN.md](TEMPLATE_HISTORIA_ZMIAN.md) |

## Reguły obowiązkowe

- Diagram Mermaid jest obowiązkowy w dokumencie sekcji i pozycji menu.
- Tabela linków Markdown jest obowiązkowa i jest stabilnym źródłem nawigacji.
- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Brak potwierdzenia w dokumentacji oznacz `[BRAK POTWIERDZENIA W DOKUMENTACJI]`.
- Brak mapowańia do bazy oznacz `[BRAK MAPOWANIA DO BAZY]`, jeżeli element mapy wymaga śladu danych.
- Szczegółowe markery i kontrola jakości: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
