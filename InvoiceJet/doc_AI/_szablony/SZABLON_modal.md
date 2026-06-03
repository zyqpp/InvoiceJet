# {TYTUL_MODALU} — modal/dialog

| Pole | Wartość |
|---|---|
| ID dokumentu | {MODAL-NAZWA_EKRANU-NAZWA_MODALU} |
| Typ dokumentu | modal |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Czym jest ten modal z perspektywy biznesowej. Jaki cel realizuje, co pozwala użytkownikowi zrobić. */}
{OPIS_BIZNESOWY_MODALU}

## Charakterystyka modalu

| Atrybut | Wartość |
|---|---|
| ID modalu | {MODAL-NAZWA_EKRANU-NAZWA_MODALU} |
| Nazwa / tytuł w UI | {TYTUL_WYSWIETLANY_W_NAGLOWKU_MODALU} |
| Wywołany przez operację | {LINK_DO_OPERACJI} |
| Ekran nadrzędny | {LINK_DO_EKRANU} |
| Typ modalu | {formularz / potwierdzenie / podgląd / informacyjny} |
| Zamknięcie przez Escape | {tak / nie} |
| Zamknięcie przez klik tła | {tak / nie} |

## Wizualizacja układu

{/* Instrukcja: Prosty ASCII-art lub opis układu zawartości modalu. */}

```
┌───────────────────────────────┐
│ Tytuł modalu              [X] │
├───────────────────────────────┤
│ Zawartość (pola / tekst)      │
│                               │
├───────────────────────────────┤
│ [Anuluj]          [Potwierdź] │
└───────────────────────────────┘
```

## Pola modalu

{/* Instrukcja: Wymień pola formularza wewnątrz modalu. Jeśli modal nie ma pól (np. modal potwierdzenia) — wpisz: "Brak". */}

| ID pola | Nazwa w UI | Typ | Wymagalność | Link do dokumentu |
|---|---|---|---|---|
| {POLE-NAZWA_MODALU-NAZWA_POLA} | {ETYKIETA_POLA} | {input / select / ...} | {wymagane / opcjonalne} | {LINK} |

## Operacje modalu

{/* Instrukcja: Przyciski wewnątrz modalu i ich efekt. */}

| Przycisk | Akcja | Wywołuje operację | Zamyka modal |
|---|---|---|---|
| {ETYKIETA_PRZYCISKU} | {OPIS_AKCJI} | {LINK_DO_OPERACJI_LUB_Nie_dotyczy} | {tak / nie} |

## Możliwe wyniki

| Wynik | Warunki | Komunikat | Następna akcja |
|---|---|---|---|
| Potwierdzenie | {WARUNKI} | {TRESC_LUB_Brak} | {AKCJA_PO_POTWIERDZENIU} |
| Anulowanie | Użytkownik klika Anuluj lub Escape | Brak | Modal zamknięty, brak zmian |

## Powiązania z kodem

- Komponent modalu: {LINK_DO_PLIKU_TS}
- Szablon HTML: {LINK_DO_PLIKU_HTML}

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych z kodu lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
