# {TYTUL_PROCESU_BIZNESOWEGO} — proces biznesowy

| Pole | Wartość |
|---|---|
| ID dokumentu | {BPMN-NAZWA_PROCESU} |
| Typ dokumentu | BPMN |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Czym jest ten proces biznesowy. Jaki cel osiąga organizacja/użytkownik po jego zakończeniu. */}
{OPIS_BIZNESOWY_PROCESU}

## Charakterystyka procesu

| Atrybut | Wartość |
|---|---|
| ID procesu BPMN | {BPMN-NAZWA_PROCESU} |
| Typ procesu | {główny / podproces / pomocniczy} |
| Inicjator | {NAZWA_AKTORA_LUB_ZDARZENIA} |
| Zdarzenie startowe | {OPIS_ZDARZENIA_STARTOWEGO} |
| Zdarzenie końcowe (sukces) | {OPIS_ZDARZENIA_KONCZACEGO_SUKCES} |
| Zdarzenie końcowe (błąd) | {OPIS_ZDARZENIA_KONCZACEGO_BLAD_LUB_Nie dotyczy} |
| Uczestnicy (pule/tory) | {LISTA_AKTOROW_I_SYSTEMOW} |

## Diagram procesu (Mermaid)

{/* Instrukcja: Diagram Mermaid flowchart lub sequenceDiagram odwzorowujący proces biznesowy. Dla procesów BPMN zalecamy flowchart LR lub TD z podziałem na uczestników za pomocą subgraph. Docelowo plik .bpmn może zastąpić ten diagram. */}

```mermaid
flowchart TD
    S([Zdarzenie startowe:\n{OPIS}]) --> A

    subgraph "{NAZWA_AKTORA_1}"
        A["{ZADANIE_1}"] --> B{"{BRAMKA_DECYZYJNA}"}
        B -- Tak --> C["{ZADANIE_2A}"]
        B -- Nie --> D["{ZADANIE_2B}"]
    end

    subgraph "{NAZWA_AKTORA_2}"
        C --> E["{ZADANIE_3}"]
        D --> E
    end

    E --> Z([Zdarzenie końcowe:\n{OPIS}])
```

## Opis kroków procesu

{/* Instrukcja: Lista kroków odpowiadających elementom diagramu. Każdy krok ma uczestnika, akcję i wynik. */}

| Krok | Uczestnik | Akcja | Wynik / wymagania wyjścia |
|---|---|---|---|
| 1 | {AKTOR_1} | {OPIS_AKCJI_1} | {WYNIK_1} |
| 2 | {AKTOR_2} | {OPIS_AKCJI_2} | {WYNIK_2} |

## Zdarzenia i bramki

{/* Instrukcja: Opisz bramki decyzyjne i zdarzenia pośrednie procesu. */}

| Element | Typ | Warunek / opis |
|---|---|---|
| {NAZWA_BRAMKI} | {bramka wyłączna / równoległa / zdarzenie pośrednie} | {WARUNEK_LUB_OPIS} |

## Reguły biznesowe procesu

{/* Instrukcja: Wymień reguły biznesowe egzekwowane w procesie. Jeśli brak — wpisz: "Brak". */}

| ID reguły | Treść reguły | Krok |
|---|---|---|
| {RB-NUMER} | {TRESC_REGULY} | {NUMER_KROKU} |

## Powiązania

- Powiązane UC: {LINKI_DO_DOKUMENTOW_UC}
- Realizowany przez ekrany: {LINKI_DO_EKRANOW}
- Powiązane procesy techniczne: {LINKI_DO_02_PROCESY}

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
