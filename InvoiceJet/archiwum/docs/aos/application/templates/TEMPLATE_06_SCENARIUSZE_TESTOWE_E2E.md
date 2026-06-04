# [A-XX_NAZWA] - Scenariusze testowe E2E

## 1. Scenariusz pozytywny

| Krok | Akcja testera | Walidacja frontendu | Wywołanie API | Logika backendu | Skutek DB | Oczekiwany wynik UI |
|---|---|---|---|---|---|---|
| 1 | `[Akcja]` | `[Walidacja]` / N/D | `[HTTP] /api/[path]` / N/D | `[Service.Method]` / N/D | `[Tabela.kolumna]` / N/D | `[Rezultat]` |

## 2. Scenariusze negatywne

| Krok | Akcja testera | Walidacja frontendu | Wywołanie API | Logika backendu | Skutek DB | Oczekiwany wynik UI |
|---|---|---|---|---|---|---|
| 1 | `[Akcja]` | `[Walidacja]` / N/D | `[HTTP] /api/[path]` / N/D | `[Service.Method]` / N/D | `[Brak zmiany / tabela]` / N/D | `[Rezultat]` |

## 3. Dane testowe

| Obiekt | Wymagane dane | Źródło | Uwagi |
|---|---|---|---|
| `[Obiekt]` | `[Wymagane pola]` | `[Dokument AOS / tabela]` | N/D |

## 4. Kryteria akceptacji

| Kryterium | Warstwa | Dowód |
|---|---|---|
| `[Kryterium]` | UI/API/Backend/DB | `[link]` |

## 5. Reguły wypełniania

- Każdy scenariusz musi obejmowac UI, API, backend i DB albo mieć marker wyjasniajacy brak warstwy.
- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Brak mapowańia do bazy oznacz `[BRAK MAPOWANIA DO BAZY]`.
- Szczegółowe markery: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
