# {TYTUL_EKRANU}

| Pole | Wartość |
|---|---|
| ID dokumentu | {EKRAN-NAZWA_EKRANU} |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Czym jest ten ekran z perspektywy biznesowej. Co użytkownik może na nim zrobić. */}
{OPIS_BIZNESOWY_EKRANU}

## Wizualizacja układu

{/* Instrukcja: Diagram Mermaid lub blok ASCII-art przedstawiający rozkład sekcji ekranu. Może to być prosty prostokąt podzielony na strefy. */}

```
┌─────────────────────────────────┐
│ Nagłówek / tytuł ekranu         │
├─────────────────────────────────┤
│ Filtry                          │
├─────────────────────────────────┤
│ Tabela / lista wyników          │
├─────────────────────────────────┤
│ Operacje (przyciski akcji)      │
└─────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | {WZORZEC_URL} |
| Wymagana rola/uprawnienie | {LINK_DO_DOKUMENTU_ROLI} |
| Punkty wejścia | {LISTA_EKRANOW_I_AKCJI_PROWADZACYCH_DO_TEGO_EKRANU} |
| Powiązany kod komponentu | {LINK_DO_PLIKU_TS_W_REPO} |

## Przejścia z ekranu

{/* Instrukcja: Każdy wiersz to jedno możliwe przejście nawigacyjne z tego ekranu. */}

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| {NAZWA_EKRANU_DOCELOWEGO} | {AKCJA_WYWOLUJACA_PRZEJSCIE} | {WARUNEK_LUB_BRAK} | {ROLA_LUB_BRAK} |

## Sekcje ekranu

### Filtry

{/* Instrukcja: Wymień filtry lub wstaw link do dokumentów SZABLON_filtr.md. Jeśli brak filtrów — wpisz: "Brak". */}

| ID filtru | Nazwa w UI | Typ | Link do dokumentu |
|---|---|---|---|
| {FILTR-NAZWA_EKRANU-NAZWA_FILTRU} | {ETYKIETA_FILTRU} | {TYP_FILTRU} | {LINK} |

### Tabele i listy

{/* Instrukcja: Wymień tabele/listy lub wstaw link do dokumentów SZABLON_tabela.md. Jeśli brak — wpisz: "Brak". */}

| ID tabeli | Nazwa | Link do dokumentu |
|---|---|---|
| {TAB-NAZWA_EKRANU-NAZWA_TABELI} | {NAZWA_TABELI} | {LINK} |

### Pola

{/* Instrukcja: Wymień pola formularza lub wstaw linki do dokumentów SZABLON_pole.md. Jeśli ekran nie ma pól — wpisz: "Brak". */}

| ID pola | Nazwa w UI | Wymagalność | Link do dokumentu |
|---|---|---|---|
| {POLE-NAZWA_EKRANU-NAZWA_POLA} | {ETYKIETA_POLA} | {wymagane / opcjonalne} | {LINK} |

### Operacje

{/* Instrukcja: Wymień operacje dostępne na ekranie lub wstaw linki do dokumentów SZABLON_operacja.md. */}

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| {OP-NAZWA_EKRANU-NAZWA_OPERACJI} | {ETYKIETA_PRZYCISKU} | {LINK} |

### Modale

{/* Instrukcja: Wymień okna modalne otwierane z tego ekranu lub wstaw linki do dokumentów SZABLON_modal.md. Jeśli brak — wpisz: "Brak". */}

| ID modalu | Nazwa | Wywołane przez | Link do dokumentu |
|---|---|---|---|
| {MODAL-NAZWA_EKRANU-NAZWA_MODALU} | {NAZWA_MODALU} | {OPERACJA_WYWOLUJACA} | {LINK} |

### Powiadomienia

{/* Instrukcja: Wymień powiadomienia wyświetlane na ekranie lub wstaw linki do dokumentów SZABLON_powiadomienie.md. Jeśli brak — wpisz: "Brak". */}

| ID powiadomienia | Typ | Treść / opis | Link do dokumentu |
|---|---|---|---|
| {POW-NAZWA_EKRANU-NAZWA_POWIADOMIENIA} | {toast / alert / inline} | {OPIS_TRESCI} | {LINK} |

## Powiązania

- Powiązane procesy: {LINKI_DO_02_PROCESY}
- Powiązane API: {LINKI_DO_04_API_I_INTEGRACJE}
- Powiązane UC: {LINKI_DO_07_USE_CASE}

## Powiązania z kodem

- Komponent: {LINK_DO_PLIKU_TS}
- Szablon HTML: {LINK_DO_PLIKU_HTML}

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | {LISTA_SELEKTOROW_DATA_CY_LUB_ARIA} |

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych z kodu lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
