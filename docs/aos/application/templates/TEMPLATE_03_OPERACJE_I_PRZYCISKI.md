# [A-XX_NAZWA] - Operacje i przyciski

## 1. Tabela operacji

| Operacja | Element UI | Handler frontend | Serwis frontend | Endpoint | Kontroler | Serwis backend | Skutek w bazie | Reakcja UI | Dowod |
|---|---|---|---|---|---|---|---|---|---|
| `[Nazwa operacji]` | `[Przycisk / ikona / menu]` | `[handler()]` / N/D | `[Service.method()]` / N/D | `[HTTP] /api/[path]` / N/D | `[Controller.Action]` / N/D | `[Service.Method]` / N/D | `[Tabela.kolumna / rekord]` / N/D | `[Komunikat / nawigacja / odswiezenie]` / N/D | `[link]` |

## 2. Szczegoly operacji

### Operacja: [Nazwa]

| Krok | Warstwa | Opis | Dowod |
|---|---|---|---|
| 1 | UI | `[Walidacja lub akcja uzytkownika]` | `[link]` |
| 2 | Frontend service | `[Wywolanie serwisu]` / N/D | `[link]` |
| 3 | API | `[Endpoint / kontroler]` / N/D | `[link]` |
| 4 | Backend | `[Metoda / algorytm]` / N/D | `[link]` |
| 5 | DB | `[Skutek danych]` / N/D | `[link]` |
| 6 | UI | `[Reakcja koncowa]` / N/D | `[link]` |

## 3. Operacje bez backendu

| Operacja | Powod braku backendu | Skutek UI | Dowod |
|---|---|---|---|
| `[Nazwa]` | `[TYLKO FRONTEND]` / N/D | `[Opis]` | `[link]` |

## 4. Reguly wypelniania

- Brak danych zapisuj jako `N/D`.
- Operacje bez API oznaczaj `[TYLKO FRONTEND]`.
- Operacje backendowe niewidoczne w UI oznaczaj `[TYLKO BACKEND]`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Gdy brak potwierdzenia w dokumentacji zrodlowej, uzyj `[BRAK POTWIERDZENIA W DOKUMENTACJI]`.
- Szczegolowe markery: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
