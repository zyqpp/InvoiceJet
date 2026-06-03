# {TYTUL_OPERACJI} — operacja

| Pole | Wartość |
|---|---|
| ID dokumentu | {OP-NAZWA_EKRANU-NAZWA_OPERACJI} |
| Typ dokumentu | operacja |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Czym jest ta operacja z perspektywy biznesowej. Co osiąga użytkownik, gdy ją wywołuje. */}
{OPIS_BIZNESOWY_OPERACJI}

## Kontekst biznesowy

{/* Instrukcja: 2–4 zdania wyjaśniające, w jakim kontekście biznesowym operacja ma sens. Kiedy użytkownik jej używa, jaki problem rozwiązuje. */}
{KONTEKST_BIZNESOWY}

## Charakterystyka operacji

| Atrybut | Wartość |
|---|---|
| ID operacji | {OP-NAZWA_EKRANU-NAZWA_OPERACJI} |
| Wyzwalacz w UI | {przycisk / link / skrót klawiaturowy / zdarzenie} |
| Wywoływane API | {LINKI_DO_DOKUMENTOW_API} |
| Powiązany proces | {LINK_DO_02_PROCESY} |
| Wymagana rola | {ROLA_LUB_Nie dotyczy} |

## Pola wejściowe

{/* Instrukcja: Wymień pola, które operacja odczytuje/wysyła. Kolumna "Walidacje" podaje reguły aktywne w momencie wywołania operacji. */}

| Pole | DTO | Walidacje |
|---|---|---|
| {NAZWA_POLA} | {LINK_DO_DTO} — `{NazwaPola}` | {OPIS_WALIDACJI} |

## Pola wyjściowe

{/* Instrukcja: Wymień pola, które operacja aktualizuje w UI po zakończeniu. */}

| Pole | DTO | Wpływ na UI |
|---|---|---|
| {NAZWA_POLA} | {LINK_DO_DTO} — `{NazwaPola}` | {OPIS_WPLYWU} |

## Możliwe wyniki

| Wynik | Warunki | Komunikat | Następna akcja UI |
|---|---|---|---|
| Sukces | {WARUNKI_SUKCESU} | {TRESC_KOMUNIKATU_LUB_Brak} | {AKCJA_PO_SUKCESIE} |
| Błąd walidacji | {WARUNKI_BLEDU_WALIDACJI} | {TRESC_KOMUNIKATU} | {AKCJA_PO_BLEDZIE} |
| Błąd serwera | {WARUNKI_BLEDU_SERWERA} | {TRESC_KOMUNIKATU} | {AKCJA_PO_BLEDZIE} |

## Powiązania

- Ekran nadrzędny: {LINK_DO_EKRANU}
- Powiązane modale: {LINKI_DO_MODALI_LUB_Nie dotyczy}
- Powiązane powiadomienia: {LINKI_DO_POWIADOMIEN}

## Powiązania z kodem

- Handler w komponencie: {LINK_DO_METODY_W_TS}
- Serwis Angular: {LINK_DO_SERWISU}

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych z kodu lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
