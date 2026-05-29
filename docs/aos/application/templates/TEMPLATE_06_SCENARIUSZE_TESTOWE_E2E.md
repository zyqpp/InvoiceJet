# [A-XX_NAZWA] - Scenariusze testowe E2E

## 1. Scenariusz pozytywny

| Krok | Akcja testera | Walidacja frontendu | Wywolanie API | Logika backendu | Skutek DB | Oczekiwany wynik UI |
|---|---|---|---|---|---|---|
| 1 | `[Akcja]` | `[Walidacja]` / N/D | `[HTTP] /api/[path]` / N/D | `[Service.Method]` / N/D | `[Tabela.kolumna]` / N/D | `[Rezultat]` |

## 2. Scenariusze negatywne

| Krok | Akcja testera | Walidacja frontendu | Wywolanie API | Logika backendu | Skutek DB | Oczekiwany wynik UI |
|---|---|---|---|---|---|---|
| 1 | `[Akcja]` | `[Walidacja]` / N/D | `[HTTP] /api/[path]` / N/D | `[Service.Method]` / N/D | `[Brak zmiany / tabela]` / N/D | `[Rezultat]` |

## 3. Dane testowe

| Obiekt | Wymagane dane | Zrodlo | Uwagi |
|---|---|---|---|
| `[Obiekt]` | `[Wymagane pola]` | `[Dokument AOS / tabela]` | N/D |

## 4. Kryteria akceptacji

| Kryterium | Warstwa | Dowod |
|---|---|---|
| `[Kryterium]` | UI/API/Backend/DB | `[link]` |

## 5. Reguly wypelniania

- Kazdy scenariusz musi obejmowac UI, API, backend i DB albo miec marker wyjasniajacy brak warstwy.
- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Brak mapowania do bazy oznacz `[BRAK MAPOWANIA DO BAZY]`.
- Szczegolowe markery: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
