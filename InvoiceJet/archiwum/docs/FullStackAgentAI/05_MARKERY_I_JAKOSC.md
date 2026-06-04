# Markery i jakość AOS aplikacyjnego

## 1. Markery

| Sytuacja | Marker |
|---|---|
| Informacja nie wynika z dostepnych plików | `[WYMAGA WERYFIKACJI]` |
| Element istnieje w UI, ale brak potwierdzenia w dokumentacji | `[BRAK POTWIERDZENIA W DOKUMENTACJI]` |
| Pełny ślad UI do bazy urywa sie przed baza | `[BRAK MAPOWANIA DO BAZY]` |
| Zachowanie istnieje tylko we frontendzie | `[TYLKO FRONTEND]` |
| Zachowanie istnieje tylko w backendzie | `[TYLKO BACKEND]` |
| Kod zawiera niespojnosc | `[UWAGA: opis niespojnosci - WYMAGA WERYFIKACJI Z ZESPOLEM]` |
| Sekcja nie ma zastosowania | `> Sekcja nie dotyczy tego przepływu. [powod]` |

## 2. Reguły jakości

- Każdy dokument ma jeden cel i jeden poziom szczegółówosci.
- Tabele nie zawieraja pustych komórek. Brak wartości zapisuje sie jako `N/D`.
- Linki do dokumentów źródłowych prowadza do istniejacych plików.
- Endpointy i nazwy techniczne są zapisane w backtickach.
- Diagram nie zastępuje tabeli. Tabela linków i mapowań jest obowiązkowa.

## 3. Kategorie sformulowan niedozwolonych

Nie używać w dokumentach AOS aplikacyjnego:

- fraz spekulacyjnych bez markera,
- potocznych opisow klikniecia i wpisywania,
- skrotow oznaczajacych niepełne wyliczenie,
- rekomendacji agenta,
- opisow oczekiwanego zachowania zamiast stanu z dokumentacji.

## 4. Kontrola przed oddaniem

Agent sprawdza:

- zgodność mapy z AOS `E-00_AppShell`,
- zgodność tras z dokumentacja frontendu,
- zgodność endpointów z AOS backendu,
- zgodność DTO z dokumentacja procesow backendowych,
- zgodność tabel i kolumn z dokumentacją backendu oraz `docs/stos-technologiczny.md`,
- komplet wymaganych plików,
- brak pustych tabel i martwych linków lokalnych.
