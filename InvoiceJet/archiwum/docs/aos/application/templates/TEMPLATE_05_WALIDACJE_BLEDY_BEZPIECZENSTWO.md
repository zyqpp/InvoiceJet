# [A-XX_NAZWA] - Walidacje, błędy i bezpieczeństwo

## 1. Walidacje frontendu

| Element UI | Walidacja | Blokuje API | Komunikat UI | Dowód |
|---|---|---|---|---|
| `[Pole / formularz]` | `[Validator / warunek]` / N/D | Tak / Nie / N/D | `[Komunikat]` / N/D | `[link]` |

## 2. Walidacje API i backendu

| Obszar | Walidacja / warunek | Status / wyjatek | Skutek UI | Dowód |
|---|---|---|---|---|
| DTO | `[Atrybut / regule]` / N/D | `[HTTP / Exception]` / N/D | `[Komunikat / stan]` / N/D | `[link]` |
| Serwis backend | `[Reguła]` / N/D | `[HTTP / Exception]` / N/D | `[Komunikat / stan]` / N/D | `[link]` |

## 3. Błędy i obsluga

| Błąd | Warstwa | Reakcja systemu | Reakcja UI | Dowód |
|---|---|---|---|---|
| `[Nazwa błędu]` | UI/API/Backend/DB | `[Opis]` / N/D | `[Opis]` / N/D | `[link]` |

## 4. Bezpieczeństwo

| Mechanizm | Warstwa | Opis | Dowód |
|---|---|---|---|
| Autoryzacja | API | `[Authorize / rola / brak]` / N/D | `[link]` |
| Token / sesja | Frontend/API | `[Opis]` / N/D | `[link]` |
| Dane wrażliwe | UI/API/DB | `[Opis]` / N/D | `[link]` |

## 5. Reguły wypełniania

- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Gdy dokumentacja front/back nie potwierdza zachowania, użyj `[BRAK POTWIERDZENIA W DOKUMENTACJI]`.
- Szczegółowe markery: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
