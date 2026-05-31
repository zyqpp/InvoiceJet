# 04. Język, styl i konwencje

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| Autor | Właściciel projektu + Agent Claudiusz Sonte 4.6 max |
| Wersja | 0.1 |
| Status | Obowiązujący |

## A. Język

Dokumentacja powstaje w języku polskim z pełnymi znakami diakrytycznymi. Wyjątkami od polszczyzny są nazwy własne technologii, terminy techniczne, dla których polski odpowiednik byłby nieprecyzyjny lub niepowszechny (`endpoint`, `DTO`, `LINQ`, `cache`, `payload`, `commit`), oraz nazwy artefaktów cytowane z kodu (klasy, metody, pliki, kolumny, endpointy). Pisownia tych ostatnich jest **identyczna** z kodem — nie zmieniamy ich wielkości liter, nie polonizujemy, nie skracamy.

W tekście opisowym preferujemy formę bezosobową lub trzecioosobową. Unikamy form osobowych typu „kliknij" na rzecz „użytkownik klika" lub „operacja wywołuje".

## B. Ton

Ton formalny, neutralny, rzeczowy. Bez ironii, bez kolokwializmów, bez emoji, bez wykrzykników. Dokumentacja nie jest miejscem na żarty ani na ekspresję autora. Jednocześnie ton ma być **prosty i zrozumiały** — preferujemy krótkie zdania nad długie.

Zakazane są frazy puste znaczeniowo: „warto wspomnieć", „należy zauważyć", „jak wiadomo", „w dzisiejszych czasach". Każde zdanie wnosi informację albo go nie ma.

## C. Konwencje nazewnicze plików i katalogów

Nazwy katalogów i plików w `doc_AI/` są w `snake_case`, bez polskich znaków, bez spacji. Prefiksy numeryczne porządkujące stosujemy na najwyższym poziomie sekcji i wewnątrz tam, gdzie kolejność ma znaczenie. Dokumenty opisujące konkretny obiekt z kodu nazywamy zgodnie z nazwą obiektu w kodzie z zachowaniem oryginalnej wielkości liter (np. `AuthController.md`, `dbo.User.md`, `RegisterUserDto.md`).

## D. Konwencje linkowania

Wszystkie linki w dokumentacji są **względne**. Każdy link ma czytelny tekst. Linki do plików kodu prowadzą do plików w repo (`../../InvoiceJetAPI/InvoiceJet.Presentation/Controllers/AuthController.cs`).

## E. Konwencje diagramów

Domyślnym formatem diagramów jest **Mermaid**, osadzany inline w blokach kodu Markdown:

- `flowchart` lub `graph` — dla algorytmów, przepływów logicznych, map przejść.
- `sequenceDiagram` — dla procesów technicznych i endpointów API.
- `erDiagram` — dla modelu danych.
- `stateDiagram-v2` — dla stanów obiektów.
- `classDiagram` — dla modelu biznesowego.

Wyjątek: diagramy procesów biznesowych w `09_procesy_biznesowe/` — BPMN 2.0.

## F. Konwencje tabel

Tabela opisu elementu jest dwukolumnowa: lewa kolumna to nazwa atrybutu, prawa kolumna to wartość. Komórki tabel nie zawierają długich akapitów.

## G. Konwencje identyfikatorów

Format: `<TYP>-<RodzicNazwa>-<Nazwa>`.

Zamknięta lista typów: `EKRAN`, `POLE`, `OP`, `FILTR`, `TAB`, `MODAL`, `POW`, `PROC`, `ALG`, `API`, `INT`, `TAB-DB`, `DTO`, `LINQ`, `SKRYPT`, `ROLA`, `UPR`, `UC`, `KLASA-BIZ`, `BPMN`, `TEST`.

Identyfikatory są **niezmienne**. Zmiana etykiety w UI nie powoduje zmiany ID.

## H. Konwencje formatu dat i wersji

Daty zawsze w formacie ISO 8601: `YYYY-MM-DD`. Wersje dokumentów: `MAJOR.MINOR`.

## I. Konwencja oznaczania statusu dokumentu

Zamknięta lista statusów: `szkic`, `w_recenzji`, `zaakceptowany`, `do_aktualizacji`, `archiwalny`.

## J. Konwencja oznaczania braków

Tam, gdzie wartość nie ma zastosowania: `Nie dotyczy`. Tam, gdzie nie udało się ustalić: `Do ustalenia` + wpis w „Wątpliwości i braki".

## K. Konwencja cytowania kodu

Krótkie cytaty w backtickach: `AuthController.Register(RegisterUserDto dto)`. Dłuższe fragmenty w blokach kodu z oznaczeniem języka (`csharp`, `typescript`, `json`). W dokumentach **nie wklejamy pełnych implementacji** — linkujemy do pliku.

## L. Konwencja autorska w rejestrze zmian

Format: **„Agent Claudiusz Sonte 4.6 max"**. Brak podpisu modelowego jest błędem.

## M. Konwencja długości dokumentu

Pojedynczy dokument nie powinien przekraczać **400 linii** Markdownu. Przekroczenie — sygnał do podziału.

## N. Konwencja używania pojęć

Każde pojęcie biznesowe lub techniczne użyte w dokumentacji musi mieć wpis w odpowiednim słowniku (`_slowniki/`). Pojęcie zdefiniowane w słowniku ma jedną, jednoznaczną definicję.

## Rejestr zmian dokumentu

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Właściciel projektu + Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
