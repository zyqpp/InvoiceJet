# Markery i jakosc AOS aplikacyjnego

## 1. Markery

| Sytuacja | Marker |
|---|---|
| Informacja nie wynika z dostepnych plikow | `[WYMAGA WERYFIKACJI]` |
| Element istnieje w UI, ale brak potwierdzenia w dokumentacji | `[BRAK POTWIERDZENIA W DOKUMENTACJI]` |
| Pelny slad UI do bazy urywa sie przed baza | `[BRAK MAPOWANIA DO BAZY]` |
| Zachowanie istnieje tylko we frontendzie | `[TYLKO FRONTEND]` |
| Zachowanie istnieje tylko w backendzie | `[TYLKO BACKEND]` |
| Kod zawiera niespojnosc | `[UWAGA: opis niespojnosci - WYMAGA WERYFIKACJI Z ZESPOLEM]` |
| Sekcja nie ma zastosowania | `> Sekcja nie dotyczy tego przeplywu. [powod]` |

## 2. Reguly jakosci

- Kazdy dokument ma jeden cel i jeden poziom szczegolowosci.
- Tabele nie zawieraja pustych komorek. Brak wartosci zapisuje sie jako `N/D`.
- Linki do dokumentow zrodlowych prowadza do istniejacych plikow.
- Endpointy i nazwy techniczne sa zapisane w backtickach.
- Diagram nie zastepuje tabeli. Tabela linkow i mapowan jest obowiazkowa.

## 3. Kategorie sformulowan niedozwolonych

Nie uzywac w dokumentach AOS aplikacyjnego:

- fraz spekulacyjnych bez markera,
- potocznych opisow klikniecia i wpisywania,
- skrotow oznaczajacych niepelne wyliczenie,
- rekomendacji agenta,
- opisow oczekiwanego zachowania zamiast stanu z dokumentacji.

## 4. Kontrola przed oddaniem

Agent sprawdza:

- zgodnosc mapy z AOS `E-00_AppShell`,
- zgodnosc tras z dokumentacja frontendu,
- zgodnosc endpointow z AOS backendu,
- zgodnosc DTO z dokumentacja procesow backendowych,
- zgodnosc tabel i kolumn z dokumentacja backendu oraz `docs/stos-technologiczny.md`,
- komplet wymaganych plikow,
- brak pustych tabel i martwych linkow lokalnych.
