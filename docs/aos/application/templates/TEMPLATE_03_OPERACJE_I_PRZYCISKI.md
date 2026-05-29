# [A-XX_NAZWA] - Operacje i przyciski

## 1. Tabela operacji

| Operacja | Element UI | Handler frontend | Serwis frontend | Endpoint | Kontroler | Serwis backend | Skutek w bazie | Reakcja UI | Dowód |
|---|---|---|---|---|---|---|---|---|---|
| `[Nazwa operacji]` | `[Przycisk / ikona / menu]` | `[handler()]` / N/D | `[Service.method()]` / N/D | `[HTTP] /api/[path]` / N/D | `[Controller.Action]` / N/D | `[Service.Method]` / N/D | `[Tabela.kolumna / rekord]` / N/D | `[Komunikat / nawigacja / odświeżenie]` / N/D | `[link]` |

## 2. Szczegóły operacji

### Operacja: [Nazwa]

| Krok | Warstwa | Opis | Dowód |
|---|---|---|---|
| 1 | UI | `[Walidacja lub akcja użytkownika]` | `[link]` |
| 2 | Frontend service | `[Wywołanie serwisu]` / N/D | `[link]` |
| 3 | API | `[Endpoint / kontroler]` / N/D | `[link]` |
| 4 | Backend | `[Metoda / algorytm]` / N/D | `[link]` |
| 5 | DB | `[Skutek danych]` / N/D | `[link]` |
| 6 | UI | `[Reakcja końcowa]` / N/D | `[link]` |

## 3. Operacje bez backendu

| Operacja | Powod braku backendu | Skutek UI | Dowód |
|---|---|---|---|
| `[Nazwa]` | `[TYLKO FRONTEND]` / N/D | `[Opis]` | `[link]` |

## 4. Reguły wypełniania

- Brak danych zapisuj jako `N/D`.
- Operacje bez API oznaczaj `[TYLKO FRONTEND]`.
- Operacje backendowe niewidoczne w UI oznaczaj `[TYLKO BACKEND]`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Gdy brak potwierdzenia w dokumentacji źródłowej, użyj `[BRAK POTWIERDZENIA W DOKUMENTACJI]`.
- Szczegółowe markery: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
