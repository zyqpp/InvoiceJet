# [A-XX_NAZWA] - Walidacje, bledy i bezpieczenstwo

## 1. Walidacje frontendu

| Element UI | Walidacja | Blokuje API | Komunikat UI | Dowod |
|---|---|---|---|---|
| `[Pole / formularz]` | `[Validator / warunek]` / N/D | Tak / Nie / N/D | `[Komunikat]` / N/D | `[link]` |

## 2. Walidacje API i backendu

| Obszar | Walidacja / warunek | Status / wyjatek | Skutek UI | Dowod |
|---|---|---|---|---|
| DTO | `[Atrybut / regule]` / N/D | `[HTTP / Exception]` / N/D | `[Komunikat / stan]` / N/D | `[link]` |
| Serwis backend | `[Regula]` / N/D | `[HTTP / Exception]` / N/D | `[Komunikat / stan]` / N/D | `[link]` |

## 3. Bledy i obsluga

| Blad | Warstwa | Reakcja systemu | Reakcja UI | Dowod |
|---|---|---|---|---|
| `[Nazwa bledu]` | UI/API/Backend/DB | `[Opis]` / N/D | `[Opis]` / N/D | `[link]` |

## 4. Bezpieczenstwo

| Mechanizm | Warstwa | Opis | Dowod |
|---|---|---|---|
| Autoryzacja | API | `[Authorize / rola / brak]` / N/D | `[link]` |
| Token / sesja | Frontend/API | `[Opis]` / N/D | `[link]` |
| Dane wrazliwe | UI/API/DB | `[Opis]` / N/D | `[link]` |

## 5. Reguly wypelniania

- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Gdy dokumentacja front/back nie potwierdza zachowania, uzyj `[BRAK POTWIERDZENIA W DOKUMENTACJI]`.
- Szczegolowe markery: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
