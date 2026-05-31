# {TYTUL_FILTRU} — filtr

| Pole | Wartość |
|---|---|
| ID dokumentu | {FILTR-NAZWA_EKRANU-NAZWA_FILTRU} |
| Typ dokumentu | filtr |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Czym jest ten filtr z perspektywy biznesowej. Jakie dane zawęża i po co użytkownik go używa. */}
{OPIS_BIZNESOWY_FILTRU}

## Charakterystyka filtru

| Atrybut | Wartość |
|---|---|
| ID filtru | {FILTR-NAZWA_EKRANU-NAZWA_FILTRU} |
| Nazwa w UI | {POLSKA_ETYKIETA_W_INTERFEJSIE} |
| Nazwa w kodzie | {NAZWA_ZMIENNEJ_1_1_Z_KODU_KOMPONENTU} |
| Typ kontrolki | {input / select / date-range / checkbox / multi-select / ...} |
| Zawęża tabelę / listę | {LINK_DO_DOKUMENTU_TABELI_LUB_EKRANU} |
| Parametr query API | {NAZWA_PARAMETRU_QUERY_STRING} |
| Pole DTO filtra | {LINK_DO_DTO} — `{NazwaPola}` |
| Pole w bazie (filtrowane) | {schema.tabela.kolumna} — {LINK_DO_TABELI_DB} |
| Wartości dopuszczalne | {OPIS_ZAKRESU_LUB_WARTOSCI_ENUM_LUB_Dowolny_tekst} |
| Domyślna wartość | {WARTOSC_LUB_Puste_brak_filtru} |
| Czy wymagany | {tak / nie} |

## Zachowanie filtru

{/* Instrukcja: Opisz, kiedy filtr jest aktywowany (np. po kliknięciu przycisku "Szukaj", na bieżąco przy wpisywaniu, po wybraniu wartości). Opisz efekt boczny (np. reset paginacji). */}

| Aspekt | Opis |
|---|---|
| Moment zastosowania | {po_kliknieciu_przycisku / na_biezaco / po_wybraniu_wartosci} |
| Efekt na paginację | {reset do strony 1 / Nie dotyczy} |
| Łączenie z innymi filtrami | {AND / OR / Nie dotyczy} |

## Powiązania

- Ekran nadrzędny: {LINK_DO_EKRANU}
- Tabela filtrowana: {LINK_DO_DOKUMENTU_TABELI}
- Powiązane API: {LINK_DO_ENDPOINTU_API}

## Powiązania z kodem

- Komponent Angular: {LINK_DO_PLIKU_TS}
- Szablon HTML (binding): {LINK_DO_PLIKU_HTML}

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych z kodu lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
