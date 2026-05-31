# {TYTUL_TABELI} — tabela/lista

| Pole | Wartość |
|---|---|
| ID dokumentu | {TAB-NAZWA_EKRANU-NAZWA_TABELI} |
| Typ dokumentu | tabela |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Co wyświetla ta tabela/lista z perspektywy biznesowej. Jakie dane prezentuje i po co użytkownik je ogląda. */}
{OPIS_BIZNESOWY_TABELI}

## Charakterystyka tabeli

| Atrybut | Wartość |
|---|---|
| ID tabeli | {TAB-NAZWA_EKRANU-NAZWA_TABELI} |
| Nazwa w UI | {POLSKA_ETYKIETA_LUB_NAGŁÓWEK} |
| Źródło danych (endpoint) | {LINK_DO_DOKUMENTU_API} |
| DTO odpowiedzi | {LINK_DO_DTO} |
| Stronicowanie | {tak (po stronie serwera) / tak (po stronie klienta) / nie} |
| Rozmiar strony domyślny | {LICZBA_LUB_Nie dotyczy} |
| Domyślne sortowanie | {KOLUMNA + kierunek: ASC/DESC / Brak} |
| Selekcja wierszy | {pojedyncza / wielokrotna / brak} |

## Kolumny tabeli

{/* Instrukcja: Każdy wiersz to jedna kolumna wyświetlana w tabeli. "Pole DTO" wskazuje, z którego pola DTO pochodzi wartość. */}

| Kolumna (nagłówek UI) | Pole DTO | Typ | Sortowalna | Opis biznesowy |
|---|---|---|---|---|
| {ETYKIETA_KOLUMNY} | `{NazwaPola}` | {string / decimal / date / bool / enum} | {tak / nie} | {OPIS} |

## Akcje w wierszach

{/* Instrukcja: Przyciski lub linki dostępne w każdym wierszu tabeli. Jeśli brak — wpisz: "Brak". */}

| Akcja | Typ | Wywołuje operację | Wymagana rola |
|---|---|---|---|
| {ETYKIETA_AKCJI} | {przycisk / ikona / link} | {LINK_DO_OPERACJI} | {ROLA_LUB_Brak} |

## Stany tabeli

{/* Instrukcja: Opisz stany specjalne tabeli. */}

| Stan | Warunek | Komunikat / zachowanie |
|---|---|---|
| Pusta | Brak wyników po zastosowaniu filtrów | {TRESC_KOMUNIKATU_O_BRAKU_WYNIKOW} |
| Ładowanie | Trwa pobieranie danych z API | {spinner / szkielet tabeli / Brak wskaźnika} |
| Błąd | Błąd odpowiedzi API | {TRESC_KOMUNIKATU_BLEDU} |

## Powiązania

- Ekran nadrzędny: {LINK_DO_EKRANU}
- Powiązane filtry: {LINKI_DO_FILTROW}
- Powiązane operacje: {LINKI_DO_OPERACJI}

## Powiązania z kodem

- Komponent Angular: {LINK_DO_PLIKU_TS}
- Szablon HTML: {LINK_DO_PLIKU_HTML}

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych z kodu lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
