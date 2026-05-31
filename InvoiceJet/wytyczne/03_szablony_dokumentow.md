# 03. Szablony dokumentów

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| Autor | Właściciel projektu + Agent Claudiusz Sonte 4.6 max |
| Wersja | 0.1 |
| Status | Obowiązujący |

## A. Reguły ogólne dla wszystkich szablonów

Każdy dokument zaczyna się **metryką** i kończy **rejestrem zmian**. Każdy dokument opisujący artefakt z kodu kończy się dodatkowo sekcją **„Wątpliwości i braki"**. Każda sekcja typu „element" (pole, operacja, filtr, modal, powiadomienie, krok procesu, krok BPMN) ma stabilny **ID** w formacie `<typ>-<NazwaRodzica>-<NazwaElementu>`, np. `POLE-ZarzadzajKontrahentami-NIP`, `OP-ZarzadzajKontrahentami-EdytujKontrahenta`. Identyfikatory wielkością liter odpowiadają kodowi. ID jest niezmienne — nie zmienia się nawet przy zmianie etykiety wyświetlanej w UI.

Atrybuty elementów opisujemy w **tabeli dwukolumnowej**: lewa kolumna to nazwa atrybutu z zamkniętej listy zdefiniowanej w szablonie, prawa kolumna to wartość. Kolejność wierszy odpowiada kolejności w szablonie i jest stała.

## B. Blok metryki (wspólny dla wszystkich dokumentów)

```markdown
# {Tytuł dokumentu — np. nazwa ekranu, klasy, procesu}

| Pole | Wartość |
|---|---|
| ID dokumentu | {STAŁY-ID-DOKUMENTU} |
| Typ dokumentu | {ekran / proces / algorytm / API / encja / DTO / ... } |
| Wersja | {0.1, 0.2, 1.0, ...} |
| Status | {szkic / w_recenzji / zaakceptowany / do_aktualizacji} |
| Autor (ostatnia modyfikacja) | {np. Agent Claudiusz Sonte 4.6 max} |
| Data ostatniej modyfikacji | {YYYY-MM-DD} |

## Streszczenie

{2–4 zdania. Czym jest opisywany element z perspektywy biznesowej.}
```

## C. Blok rejestru zmian (wspólny dla wszystkich dokumentów)

```markdown
## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | {YYYY-MM-DD} | {Agent Claudiusz Sonte 4.6 max} | Pierwsza wersja. |
```

## D. Blok „Wątpliwości i braki" (dla dokumentów opisujących artefakty z kodu)

```markdown
## Wątpliwości i braki

{Lista rzeczy, których nie udało się ustalić z kodu, lub które wymagają decyzji właściciela projektu. Jeśli brak — wpisz: "Brak".}
```

## E. Szablon ekranu (`01_ekrany/<grupa>/<ekran>/ekran.md`)

```markdown
{Blok metryki}

## Wizualizacja układu

{Diagram Mermaid lub blok ASCII-art przedstawiający rozkład sekcji ekranu.}

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | {wzorzec URL} |
| Wymagana rola/uprawnienie | {link do dokumentu roli} |
| Punkty wejścia | {lista ekranów + akcji} |
| Powiązany kod komponentu | {link do pliku .ts w repo} |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|

## Sekcje ekranu

### Filtry
### Tabele i listy
### Pola
### Operacje
### Modale
### Powiadomienia

## Powiązania

- Powiązane procesy: {linki do `02_procesy/`}
- Powiązane API: {linki do `04_api_i_integracje/01_api_frontend/`}
- Powiązane UC: {linki do `07_use_case/`}

## Powiązania z kodem

- Komponent: {link}
- Szablon HTML: {link}

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | {lista} |

{Blok „Wątpliwości i braki"}
{Blok rejestru zmian}
```

## F. Szablon pola (`01_ekrany/.../pola/<NazwaPola>.md`)

```markdown
{Blok metryki}

| Atrybut | Wartość |
|---|---|
| ID pola | {POLE-<Ekran>-<NazwaPola>} |
| Nazwa w UI | {polska etykieta} |
| Nazwa w kodzie | {1:1 z kodu komponentu} |
| Typ pola UI | {input / select / checkbox / data / ...} |
| Źródło danych | {API endpoint + DTO + pole} |
| Pole DTO | {link do DTO + nazwa pola} |
| Pole w bazie | {schema.tabela.kolumna; link} |
| Typ danych | {string / int / decimal / date / bool / enum} |
| Walidacja frontowa | {opis lub link} |
| Walidacja backendowa | {opis lub link} |
| Wymagalność | {wymagane / opcjonalne / warunkowe} |
| Domyślna wartość | {wartość lub algorytm} |

{Blok „Wątpliwości i braki"}
{Blok rejestru zmian}
```

## G. Szablon operacji (`01_ekrany/.../operacje/<NazwaOperacji>.md`)

```markdown
{Blok metryki}

## Kontekst biznesowy

{2–4 zdania.}

## Charakterystyka operacji

| Atrybut | Wartość |
|---|---|
| ID operacji | {OP-<Ekran>-<NazwaOperacji>} |
| Wyzwalacz w UI | {przycisk / link / shortcut} |
| Wywoływane API | {linki do dokumentów API} |
| Powiązany proces | {link do `02_procesy/`} |
| Pola wejściowe | {tabela: pole → DTO → walidacje} |
| Pola wyjściowe | {tabela: pole → DTO → wpływ na UI} |

## Możliwe wyniki

| Wynik | Warunki | Komunikat | Następna akcja UI |
|---|---|---|---|

{Blok „Wątpliwości i braki"}
{Blok rejestru zmian}
```

## H. Szablon tabeli bazy danych (`05_model_danych/01_db/<schema>/<schema>.<Tabela>.md`)

```markdown
{Blok metryki}

| Atrybut | Wartość |
|---|---|
| Pełna nazwa | {schema.Tabela} |
| Cel biznesowy | {1–2 zdania} |
| Klucz główny | {kolumny} |

## Kolumny

| Kolumna | Typ SQL | NULL | Domyślna | Klucz | Opis biznesowy |
|---|---|---|---|---|---|

## Indeksy

| Nazwa | Kolumny | Unikalny | Cel |
|---|---|---|---|

## Klucze obce

| Kolumny lokalne | Tabela docelowa | Kolumny docelowe | ON DELETE |
|---|---|---|---|

## Powiązane DTO i LINQ

## Powiązania z kodem

{Blok „Wątpliwości i braki"}
{Blok rejestru zmian}
```

## I. Szablon DTO (`05_model_danych/02_dto/.../<Dto>.md`)

```markdown
{Blok metryki}

| Atrybut | Wartość |
|---|---|
| Nazwa | {1:1 z kodu} |
| Cel | {1–2 zdania} |
| Kierunek użycia | {żądanie / odpowiedź / oba} |

## Pola

| Pole | Typ | Wymagane | Walidacje | Powiązane pole bazy | Powiązany słownik |
|---|---|---|---|---|---|

## Mapowania

## Wykorzystanie

{Blok „Wątpliwości i braki"}
{Blok rejestru zmian}
```

## J. Szablon API frontu (`04_api_i_integracje/01_api_frontend/.../<Endpoint>.md`)

```markdown
{Blok metryki}

## Charakterystyka endpointu

| Atrybut | Wartość |
|---|---|
| ID endpointu | {API-<Nazwa>} |
| Metoda HTTP | {GET/POST/PUT} |
| URL | {wzorzec} |
| Wymagana autoryzacja | {tak/nie + schemat} |
| Wymagana rola | {User / brak} |

## Żądanie

### Przykład żądania

```json
{przykład JSON}
```

## Odpowiedzi

| Kod | Znaczenie | DTO | Opis błędu |
|---|---|---|---|

## Diagram sekwencji

{Mermaid sequenceDiagram}

## Powiązania

## Powiązania z kodem

{Blok „Wątpliwości i braki"}
{Blok rejestru zmian}
```

## K. Szablon procesu technicznego (`02_procesy/.../proces.md`)

```markdown
{Blok metryki}

## Cel procesu

{1–3 zdania.}

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| ID procesu | {PROC-<Nazwa>} |
| Typ | {główny / pomocniczy} |
| Inicjator | {ekran + operacja} |
| Warunki startu | {warunki} |
| Warunki zakończenia (sukces) | {warunki} |

## Diagram sekwencji

{Mermaid sequenceDiagram}

## Kroki

{Lista numerowana.}

{Blok „Wątpliwości i braki"}
{Blok rejestru zmian}
```

## L. Szablon algorytmu (`03_algorytmy/.../<Algorytm>.md`)

```markdown
{Blok metryki}

## Cel algorytmu

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| ID algorytmu | {ALG-<Kategoria>-<Nazwa>} |
| Kategoria | {walidacji / wyliczeniowe / autoryzacyjne / ...} |
| Wejście | {parametry} |
| Wyjście | {wynik} |

## Opis krok po kroku

## Przypadki brzegowe

{Blok „Wątpliwości i braki"}
{Blok rejestru zmian}
```

## M. Szablon scenariusza testowego (`10_testy/.../<Scenariusz>.md`)

```markdown
{Blok metryki}

| Atrybut | Wartość |
|---|---|
| ID scenariusza | {TEST-<Typ>-<Nazwa>} |
| Typ | {manualny / API} |
| Priorytet | {P0 / P1 / P2} |
| Powiązany UC | {link} |

## Warunki początkowe

## Dane testowe

## Kroki

| Numer | Akcja | Oczekiwany wynik |
|---|---|---|

{Blok „Wątpliwości i braki"}
{Blok rejestru zmian}
```

## N. Szablon README katalogu

```markdown
# {Nazwa katalogu}

{Opis biznesowy — finalizowany w ostatniej fazie projektu.}

## Drzewo zawartości

{Drzewo z opisami.}

## Kluczowe dokumenty

## Powiązane katalogi

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
```

## Rejestr zmian dokumentu

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Właściciel projektu + Agent Claudiusz Sonte 4.6 max | Pierwsza wersja (skrócona — pełne szablony w pliku oryginalnym). |
