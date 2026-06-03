# Funkcje i obsługa

## Uruchomienie

```powershell
cd "G:\Projekty informatyczne\Gotowe aplikacje\InvoiceJet\tools\oracle_invoicejet"
.\scripts\invoke-gui.ps1 -Port 8502
```

Adres portalu:

```text
http://127.0.0.1:8502
```

Przed pierwszym użyciem trzeba mieć działającą Ollamę, pobrane modele i zbudowany indeks:

```powershell
.\scripts\invoke-setup.ps1
.\scripts\invoke-pull-models.ps1 -Models gemma3:4b,bge-m3
.\scripts\invoke-refresh-index.ps1 -ForceRebuild
```

## Zakładki portalu

### Czat

Główne miejsce pracy z Oracle. Użytkownik wybiera agenta, profil modelu, profil RAG, master prompt i zakres źródeł, a potem zadaje pytanie. Odpowiedź jest streamowana token po tokenie.

Widoczne etapy:

1. retrieval - wyszukiwanie kontekstu,
2. prompt_build - budowanie promptu,
3. generation - generowanie odpowiedzi,
4. completed - finalna odpowiedź, źródła i metryki.

Źródła są renderowane dopiero po zakończeniu generacji, żeby nie sugerować finalnego wyniku zanim odpowiedź zostanie zweryfikowana.

### Wyszukiwarka

Pozwala testować retrieval bez uruchamiania LLM. To najważniejsze narzędzie do diagnozy, gdy odpowiedź jest słaba. Jeżeli wyszukiwarka nie znajduje właściwych źródeł, model zwykle też nie odpowie dobrze.

Wyszukiwarka pokazuje:

- `source_path`,
- `heading_path`,
- `source_type`,
- `entity`,
- `table`,
- `endpoint`,
- dystans semantyczny,
- fragment tekstu.

### Źródła

Lista dokumentów, które wchodzą do bazy odpowiedzi. Ta zakładka pomaga sprawdzić, czy dokumentacja została poprawnie sklasyfikowana.

Przydatne pytania kontrolne:

- Czy plik z opisem ekranu ma `source_type=screen`?
- Czy plik tabeli ma `source_type=data_model` i ustawione `table`?
- Czy endpoint ma `source_type=api` i ustawione `endpoint`?
- Czy dokument jest w `doc_ai` albo `doc_user`, a nie poza zakresem indeksu?

### Indeks

Pokazuje stan manifestu i pozwala odświeżyć indeks.

- zwykły refresh dodaje nowe pliki, reindeksuje zmienione i usuwa brakujące,
- force rebuild usuwa lokalny stan indeksu i buduje wszystko od zera.

Force rebuild jest wymagany po zmianie:

- modelu embeddingów,
- rozmiaru chunków,
- schematu metadanych,
- logiki klasyfikacji dokumentów.

### Ewaluacja

Evaluation Lab uruchamia golden set z `eval/golden_set.json`.

Tryby:

- `retrieval` - sprawdza, czy system znajduje oczekiwane źródła.
- `answer` - uruchamia pełne generowanie odpowiedzi i sprawdza wynik końcowy.

Raport pokazuje:

- status testu,
- trafione źródła,
- brakujące źródła,
- czas,
- długość odpowiedzi,
- obecność cytowań.

### Agenci i modele

Panel pokazuje dostępne profile agentów, modeli, promptów i RAG. Można też sprawdzić lokalne modele Ollamy i pobrać modele z whitelisty.

Agent to konfiguracja pracy, nie osobny proces. Łączy:

- rolę,
- profil modelu,
- profil promptu,
- profil RAG,
- zakres źródeł,
- limity odpowiedzi.

W sidebarze agent może mieć też własną instrukcję, listę możliwości, ograniczenia i przykładowe pytania. To jest ważne szczególnie dla wyspecjalizowanych agentów, bo użytkownik od razu widzi, do czego dany profil służy.

### Agent bazodanowy: Zenon SQL

`Zenon SQL` jest profilem do pytań o model danych i podstawowe zapytania SQL. Używa profilu RAG `database_sql`, który preferuje dokumenty typu `data_model`, `mapping`, `process`, `api`, `algorithm` i `validation`.

Agent potrafi:

- wyjaśnić, które tabele i kolumny odpowiadają za dany obszar,
- wskazać relacje i klucze potrzebne do `JOIN`,
- przygotować podstawowe zapytanie `SELECT`,
- ograniczyć wynik do wskazanych kolumn,
- wskazać braki dokumentacji, gdy nie ma pewnej relacji albo kolumny.

Ograniczenia:

- nie wykonuje SQL na bazie,
- nie generuje zapytań modyfikujących dane,
- nie zgaduje nieudokumentowanych nazw tabel, kolumn ani relacji,
- nie zastępuje review DBA dla zapytań produkcyjnych.

Przykłady:

```text
Przygotuj SELECT, który wyciągnie dokumenty dla kontrahenta o nazwie Abacki.
Zrób SQL dla dokumentów w statusie Paid i pokaż tylko Id, numer, datę wystawienia oraz status.
Jakie tabele łączą dokument z klientem i statusem?
```

### Diagnostyka

Zakładka do szybkiego sprawdzenia środowiska:

- czy Ollama odpowiada,
- czy modele są dostępne,
- czy indeks istnieje,
- czy embedding działa,
- czy zapytanie z dokumentacji zwraca odpowiedź,
- czy pytanie spoza dokumentacji zwraca fallback.

## Skrypty CLI

| Skrypt | Zastosowanie |
|---|---|
| `invoke-setup.ps1` | tworzy środowisko lokalne i instaluje zależności |
| `invoke-pull-models.ps1` | pobiera modele Ollama |
| `invoke-refresh-index.ps1` | buduje lub odświeża indeks |
| `invoke-gui.ps1` | uruchamia portal Streamlit |
| `invoke-query.ps1` | zadaje pytanie z CLI |
| `invoke-evaluate.ps1` | uruchamia Evaluation Lab z CLI |
| `invoke-doctor.ps1` | diagnostyka środowiska |
| `invoke-docker.ps1` | wariant kontenerowy |

Przykłady:

```powershell
.\scripts\invoke-query.ps1 -Question "Na ekranie serii dokumentów skąd pobierane są informacje i jaka tabela je przechowuje?"
.\scripts\invoke-query.ps1 -Question "Jaka będzie jutro pogoda w Warszawie?"
.\scripts\invoke-evaluate.ps1 -Mode retrieval
.\scripts\invoke-evaluate.ps1 -Mode answer -Limit 3
.\scripts\invoke-doctor.ps1 -TestEmbedding
```

## Jak zadawać dobre pytania

Oracle najlepiej działa, gdy pytanie zawiera konkretne słowa z domeny aplikacji:

- nazwa ekranu,
- nazwa pola,
- nazwa procesu,
- nazwa tabeli,
- nazwa endpointu,
- rodzaj informacji: walidacja, źródło danych, mapowanie, uprawnienia.

Przykłady:

```text
Jak wygląda proces rejestracji i logowania w InvoiceJet?
Na ekranie DocumentSeries jakie pola są pobierane z bazy?
Który endpoint obsługuje generowanie PDF i jakie źródła danych wykorzystuje?
Jakie walidacje dotyczą formularza klienta?
Która tabela przechowuje dane kont bankowych?
```

## Jak czytać metryki

- `Total` - pełny czas przebiegu od pytania do finalnego eventu.
- `Retrieval` - czas wyszukania kontekstu.
- `Generacja` - czas generowania przez LLM.
- `TTFT` - czas do pierwszego tokenu; mówi, jak szybko użytkownik zobaczy pierwszy fragment odpowiedzi.
- `prompt_eval_count` - ile tokenów promptu model przetworzył, jeżeli Ollama zwróciła tę metrykę.
- `eval_count` - ile tokenów odpowiedzi model wygenerował.
- `eval_duration_ns` - czas generacji zwrócony przez Ollamę w nanosekundach.

## Jak diagnozować słabą odpowiedź

1. Sprawdź w zakładce `Wyszukiwarka`, czy retrieval znajduje dobre źródła.
2. Jeżeli nie, sprawdź `Źródła`, czy dokument ma poprawny `source_type`.
3. Jeżeli źródła są dobre, sprawdź profil RAG i `top_k`.
4. Jeżeli retrieval jest dobry, ale odpowiedź słaba, porównaj profil promptu i modelu.
5. Dodaj przypadek do `eval/golden_set.json`, żeby problem nie wrócił po kolejnych zmianach.

## Kryteria poprawnej odpowiedzi

Poprawna odpowiedź powinna:

- odpowiadać po polsku,
- opierać się tylko na kontekście,
- wskazywać ograniczenia, jeżeli dokumentacja jest niepełna,
- zawierać cytowania lub systemowe źródła,
- zwrócić fallback, gdy brak danych w dokumentacji,
- nie pokazywać procesu rozumowania modelu.
