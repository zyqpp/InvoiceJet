# {TYTUL_POLA} — pole

| Pole | Wartość |
|---|---|
| ID dokumentu | {POLE-NAZWA_EKRANU-NAZWA_POLA} |
| Typ dokumentu | pole |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Czym jest to pole z perspektywy biznesowej. Do czego służy, co reprezentuje w domenie. */}
{OPIS_BIZNESOWY_POLA}

## Charakterystyka pola

| Atrybut | Wartość |
|---|---|
| ID pola | {POLE-NAZWA_EKRANU-NAZWA_POLA} |
| Nazwa w UI | {POLSKA_ETYKIETA_W_INTERFEJSIE} |
| Nazwa w kodzie | {NAZWA_ZMIENNEJ_1_1_Z_KODU_KOMPONENTU} |
| Typ pola UI | {input / select / checkbox / date / textarea / radio / ...} |
| Źródło danych | {ENDPOINT_API + DTO + NAZWA_POLA} |
| Pole DTO | {LINK_DO_DTO} — `{NazwaPola}` |
| Pole w bazie | {schema.tabela.kolumna} — {LINK_DO_TABELI_DB} |
| Typ danych | {string / int / decimal / date / bool / enum} |
| Walidacja frontowa | {OPIS_WALIDACJI_LUB_LINK} |
| Walidacja backendowa | {OPIS_WALIDACJI_LUB_LINK} |
| Wymagalność | {wymagane / opcjonalne / warunkowe} |
| Domyślna wartość | {WARTOSC_LUB_ALGORYTM_LUB_Nie dotyczy} |

## Zachowanie warunkowe

{/* Instrukcja: Opisz sytuacje, w których pole zmienia swój stan (staje się wymagane, ukryte, zablokowane) w zależności od wartości innych pól lub stanu ekranu. Jeśli brak — wpisz: "Brak". */}

| Warunek | Stan pola | Opis |
|---|---|---|
| {WARUNEK} | {widoczne / ukryte / wymagane / zablokowane} | {OPIS} |

## Powiązania

- Ekran nadrzędny: {LINK_DO_EKRANU}
- Powiązane pola: {LISTA_LINKOW_DO_POWIAZANYCH_POL}
- Powiązane operacje: {LISTA_LINKOW_DO_OPERACJI_UZYWAJACYCH_TEGO_POLA}

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
