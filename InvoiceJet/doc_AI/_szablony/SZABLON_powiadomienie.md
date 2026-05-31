# {TYTUL_POWIADOMIENIA} — powiadomienie

| Pole | Wartość |
|---|---|
| ID dokumentu | {POW-NAZWA_EKRANU-NAZWA_POWIADOMIENIA} |
| Typ dokumentu | powiadomienie |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Czym jest to powiadomienie z perspektywy biznesowej. W jakiej sytuacji się pojawia i co informuje użytkownika. */}
{OPIS_BIZNESOWY_POWIADOMIENIA}

## Charakterystyka powiadomienia

| Atrybut | Wartość |
|---|---|
| ID powiadomienia | {POW-NAZWA_EKRANU-NAZWA_POWIADOMIENIA} |
| Typ wyświetlania | {toast / alert-inline / banner / dialog} |
| Poziom / kategoria | {sukces / błąd / ostrzeżenie / informacja} |
| Treść komunikatu | {DOKLADNA_TRESC_LUB_WZORZEC_Z_DYNAMICZNA_WARTOSCIA} |
| Czas wyświetlania | {AUTO_X_SEKUND / manualnie / trwałe} |
| Możliwość zamknięcia | {tak / nie} |
| Ekran wyświetlający | {LINK_DO_EKRANU} |

## Warunki wyświetlenia

{/* Instrukcja: Opisz dokładnie, kiedy powiadomienie się pojawia. Powiąż z operacją lub zdarzeniem. */}

| Warunek | Wywołane przez |
|---|---|
| {OPIS_WARUNKU_WYSWIETLENIA} | {LINK_DO_OPERACJI_LUB_ZDARZENIA} |

## Treść komunikatów

{/* Instrukcja: Jeśli powiadomienie ma wariantowe treści (np. różna treść dla różnych kodów błędu) — wymień wszystkie warianty. Jeśli jedna treść — wpisz ją powyżej i zostaw tabelę pustą lub usuń sekcję. */}

| Wariant | Treść komunikatu | Kod błędu / warunek |
|---|---|---|
| {NAZWA_WARIANTU} | {DOKLADNA_TRESC} | {KOD_BLEDU_HTTP_LUB_WARUNEK} |

## Powiązania

- Wywołane przez operację: {LINK_DO_OPERACJI}
- Ekran nadrzędny: {LINK_DO_EKRANU}

## Powiązania z kodem

- Serwis powiadomień: {LINK_DO_SERWISU_POWIADOMIEN}
- Miejsce wywołania: {LINK_DO_PLIKU_TS_I_METODY}

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych z kodu lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
