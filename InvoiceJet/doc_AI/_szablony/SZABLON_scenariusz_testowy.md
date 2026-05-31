# {TYTUL_SCENARIUSZA} — scenariusz testowy

| Pole | Wartość |
|---|---|
| ID dokumentu | {TEST-TYP-NAZWA_SCENARIUSZA} |
| Typ dokumentu | scenariusz_testowy |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Co weryfikuje ten scenariusz testowy. Jaki aspekt systemu jest sprawdzany. */}
{OPIS_SCENARIUSZA_TESTOWEGO}

## Charakterystyka scenariusza

| Atrybut | Wartość |
|---|---|
| ID scenariusza | {TEST-TYP-NAZWA_SCENARIUSZA} |
| Typ | {manualny / API / E2E / jednostkowy} |
| Priorytet | {P0 — krytyczny / P1 — wysoki / P2 — normalny} |
| Powiązany UC | {LINK_DO_DOKUMENTU_UC} |
| Powiązana operacja | {LINK_DO_DOKUMENTU_OPERACJI} |
| Środowisko testowe | {lokalne / staging / produkcyjne} |
| Wymagane uprawnienia | {ROLA_LUB_Nie dotyczy} |

## Warunki początkowe

{/* Instrukcja: Opisz stan systemu i dane, które muszą istnieć przed wykonaniem testu. */}

- {WARUNEK_POCZATKOWY_1}
- {WARUNEK_POCZATKOWY_2}

## Dane testowe

{/* Instrukcja: Podaj konkretne dane wejściowe używane w kroku testowym. Dla testów API — przykład payload. */}

| Pole | Wartość testowa | Uwagi |
|---|---|---|
| {NAZWA_POLA} | `{WARTOSC_TESTOWA}` | {UWAGA_LUB_Brak} |

## Kroki

{/* Instrukcja: Każdy krok to jedna akcja testera lub systemu z oczekiwanym wynikiem. Dla testów API — krok to wywołanie HTTP + weryfikacja odpowiedzi. */}

| Numer | Akcja | Oczekiwany wynik |
|---|---|---|
| 1 | {OPIS_AKCJI_1} | {OCZEKIWANY_WYNIK_1} |
| 2 | {OPIS_AKCJI_2} | {OCZEKIWANY_WYNIK_2} |
| 3 | {OPIS_AKCJI_3} | {OCZEKIWANY_WYNIK_3} |

## Scenariusze negatywne

{/* Instrukcja: Opisz scenariusze, w których system powinien odrzucić operację lub wyświetlić błąd. Jeśli brak — wpisz: "Brak". */}

| ID | Dane wejściowe | Oczekiwany wynik negatywny |
|---|---|---|
| {TEST-TYP-NAZWA_SCENARIUSZA}-NEG-{NR} | {OPIS_DANYCH_WEJSCIOWYCH} | {KOMUNIKAT_BLEDU_LUB_STATUS_HTTP} |

## Warunki końcowe po teście

{/* Instrukcja: Opisz, jak przywrócić stan systemu po teście (sprzątanie danych). Jeśli nie jest potrzebne — wpisz: "Nie dotyczy". */}
{OPIS_SPRZATANIA_LUB_Nie dotyczy}

## Powiązania

- Powiązany UC: {LINK_DO_UC}
- Testowana operacja: {LINK_DO_OPERACJI}
- Testowany endpoint: {LINK_DO_API}

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
