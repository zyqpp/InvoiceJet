# {TYTUL_PRZYPADKU_UZYCIA} — przypadek użycia

| Pole | Wartość |
|---|---|
| ID dokumentu | {UC-NAZWA_PRZYPADKU_UZYCIA} |
| Typ dokumentu | UC |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Czym jest ten przypadek użycia z perspektywy biznesowej. Jaki cel użytkownik osiąga. */}
{OPIS_BIZNESOWY_UC}

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| ID przypadku użycia | {UC-NAZWA_PRZYPADKU_UZYCIA} |
| Aktor główny | {NAZWA_AKTORA_NP_Użytkownik_zalogowany / Administrator} |
| Aktorzy pomocniczy | {LISTA_LUB_Brak} |
| Cel aktora | {CO_AKTOR_CHCE_OSIAGNAC} |
| Warunki wstępne | {WARUNKI_KTORE_MUSZA_BYC_SPELNIONE_PRZED_UC} |
| Warunki końcowe (sukces) | {STAN_SYSTEMU_PO_POMYSLNYM_ZAKONCZENIU} |
| Warunki końcowe (niepowodzenie) | {STAN_SYSTEMU_PRZY_NIEPOWODZENIU} |
| Priorytet biznesowy | {wysoki / średni / niski} |
| Powiązana rola | {LINK_DO_DOKUMENTU_ROLI} |

## Scenariusz główny

{/* Instrukcja: Lista numerowana kroków scenariusza głównego (ścieżka optymistyczna). Numeracja: 1, 2, 3 ... */}

1. {OPIS_KROKU_1_AKTOR}
2. {OPIS_KROKU_2_SYSTEM}
3. {OPIS_KROKU_3_AKTOR}
4. {OPIS_KROKU_4_SYSTEM}

## Scenariusze alternatywne

{/* Instrukcja: Opisz każde odgałęzienie od scenariusza głównego. Format: "A1. Od kroku N: ...". Jeśli brak — wpisz: "Brak". */}

**A1. Od kroku {NUMER_KROKU}: {WARUNEK_ALTERNATYWNY}**

1. {OPIS_KROKU_ALTERNATYWNEGO_1}
2. {OPIS_KROKU_ALTERNATYWNEGO_2}

## Scenariusze wyjątkowe

{/* Instrukcja: Opisz sytuacje błędów, wyjątków, niepowodzeń. Format: "E1. ...". Jeśli brak — wpisz: "Brak". */}

**E1. {OPIS_WYJATKU}**

1. {OPIS_KROKU_WYJATKOWEGO}
2. {REAKCJA_SYSTEMU}

## Reguły biznesowe

{/* Instrukcja: Wymień reguły biznesowe, które obowiązują w tym UC. Każda reguła powinna być zidentyfikowana. Jeśli brak — wpisz: "Brak". */}

| ID reguły | Treść reguły |
|---|---|
| {RB-NUMER} | {TRESC_REGULY_BIZNESOWEJ} |

## Powiązania

- Realizowany przez ekran: {LINK_DO_EKRANU}
- Realizowany przez operację: {LINK_DO_OPERACJI}
- Realizowany przez proces: {LINK_DO_PROCESU}
- Powiązane scenariusze testowe: {LINKI_DO_SCENARIUSZY_TEST}

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
