# Plan rozbudowy Agent AI / RAG / LLM Control Center

## 1. Cel

Obecny `Oracle InvoiceJet` ma dzialajacy lokalny RAG: Chroma jako baza wiedzy, Ollama jako zrodlo modeli LLM i embeddingow, Streamlit jako GUI na porcie `8502`, profile agentow, diagnostyke, indeks i wyszukiwarke. Kolejny etap powinien rozbudowac go w narzedzie do kontrolowania pracy LLM:

- wybor i porownywanie modeli,
- kontrola parametrow generacji,
- wlasne master prompty i presety,
- wlasni agenci do roznych zadan,
- narzedzia/funkcje wywolywane przez agenta,
- profile RAG dla roznych zrodel wiedzy,
- testy jakosci odpowiedzi i regresji,
- architektura gotowa do API/SSE i pozniejszej integracji z aplikacja.

Priorytet: najpierw kontrola, powtarzalnosc i mierzalnosc wynikow, dopiero potem automatyzacje agentowe.

## 2. Docelowe moduly

### LLM Control Center

Panel konfiguracji modelu powinien pozwalac zapisac i porownywac profile:

- model: np. lokalny model Ollama,
- parametry: `temperature`, `top_p`, `top_k`, `repeat_penalty`, `num_ctx`, `num_predict`, `seed`, `stop`,
- tryb odpowiedzi: szybki, dokladny, analityczny, techniczny reviewer,
- limity: maksymalny czas, maksymalna dlugosc, maksymalny kontekst,
- metryki: czas do pierwszego tokenu, czas generowania, token/s, liczba tokenow promptu i odpowiedzi.

Efekt: uzytkownik nie eksperymentuje przypadkowo suwakami, tylko wybiera nazwany profil modelu i moze wrocic do wynikow.

### Prompt Studio

Master prompty powinny byc zarzadzane jako wersjonowane szablony, nie jako tekst zaszyty w kodzie.

Minimalny model danych:

- `id`,
- `name`,
- `description`,
- `system_prompt`,
- `rag_instruction`,
- `answer_style`,
- `source_policy`,
- `version`,
- `is_default`.

Funkcje:

- tworzenie i edycja promptow,
- podglad finalnego promptu przed wyslaniem do modelu,
- przypisanie promptu do agenta albo profilu RAG,
- historia wersji,
- szybki rollback do poprzedniej wersji.

Zasada: prompt odpowiada za sposob myslenia i format odpowiedzi, a profil RAG za dobor kontekstu.

### Agent Builder

Agent powinien byc zapisana konfiguracja, nie osobna klasa pisana recznie dla kazdego przypadku.

Proponowane typy agentow startowych:

- `Dokumentalista`: odpowiada tylko na podstawie dokumentacji i mocno eksponuje zrodla,
- `Analityk systemowy`: laczy wymagania, procesy i luki w dokumentacji,
- `Reviewer kodu`: analizuje ryzyka, niespojnosci i brakujace testy,
- `PM / Planer`: rozbija pomysl na etapy, kryteria akceptacji i backlog,
- `Architekt`: proponuje strukture modulow, kontrakty i decyzje techniczne.

Minimalny model agenta:

- nazwa i opis,
- przypisany model/profil modelu,
- przypisany master prompt,
- domyslny profil RAG,
- lista dozwolonych narzedzi,
- limity pracy,
- tryb odpowiedzi,
- polityka zrodel i niepewnosci.

Na start agenci moga tylko odpowiadac i korzystac z RAG. Dopiero pozniej powinni dostac narzedzia wykonawcze.

### Tool / Function Calling

Narzedzia powinny byc kontrolowane i jawnie wlaczane dla agenta. W PoC lokalnym sensowne narzedzia to:

- `search_docs`: zapytanie semantyczne do Chroma,
- `read_source`: odczyt wskazanego pliku dokumentacji,
- `summarize_sources`: streszczenie znalezionych fragmentow,
- `compare_answers`: porownanie odpowiedzi kilku modeli/profili,
- `generate_plan`: wygenerowanie planu prac na podstawie pytania i zrodel.

Docelowo, dla integracji produkcyjnej, mozna dodac narzedzia z uprawnieniami:

- odczyt repozytorium,
- analiza diffow,
- tworzenie dokumentow,
- generowanie backlogu,
- tworzenie issue/PR.

Zasada bezpieczenstwa: agent nie wykonuje operacji mutujacych bez jawnej zgody uzytkownika.

### RAG Profiles

Profile RAG pozwola kontrolowac, z jakiej wiedzy i jakim sposobem agent korzysta.

Parametry profilu:

- kolekcja Chroma,
- filtr `source_path`,
- `top_k`,
- minimalny prog trafienia,
- tryb wyszukiwania: semantyczny, keyword, hybrydowy,
- reranking wlaczony/wylaczony,
- limit lacznej dlugosci kontekstu,
- strategia cytowan.

Kolejne usprawnienia RAG:

- reranker dla lepszego doboru fragmentow,
- deduplikacja podobnych chunkow,
- hybrid search dla nazw klas, endpointow i sciezek,
- grupowanie wynikow po pliku/procesie,
- wykrywanie braku odpowiedzi w dokumentacji,
- lepsze cytowania: `source_path`, naglowek, indeks chunka, zakres znakow.

### Evaluation Lab

Bez ewaluacji nie bedzie wiadomo, czy nowy model albo prompt jest lepszy.

Minimalne funkcje:

- zestaw testowych pytan,
- oczekiwane zrodla,
- oczekiwany typ odpowiedzi,
- uruchomienie testow dla wybranego modelu/promptu/agenta,
- porownanie odpowiedzi A/B,
- metryki: zgodnosc ze zrodlami, obecnosc cytowan, czas, dlugosc, brak halucynacji.

Pierwszy zestaw testowy powinien obejmowac:

- pytania o logowanie,
- pytania o faktury/PDF,
- pytania o serie dokumentow,
- pytania celowo bez odpowiedzi w dokumentacji,
- pytania wymagajace wskazania kilku zrodel.

## 3. Roadmapa realizacji

### Etap 1: Uporzadkowanie konfiguracji LLM

Zakres:

- dodac model `ModelProfile`,
- zapis profili w lokalnym JSON/TOML,
- panel wyboru profilu w Streamlit,
- obsluga dodatkowych parametrow Ollama: `top_p`, `top_k`, `repeat_penalty`, `seed`, `stop`,
- metryki profilu w historii odpowiedzi.

Kryteria akceptacji:

- uzytkownik moze zapisac i ponownie wybrac profil modelu,
- odpowiedz RAG korzysta z parametrow profilu,
- testy pokrywaja mapowanie profilu na payload Ollama.

### Etap 2: Prompt Studio

Zakres:

- dodac katalog/plik promptow,
- wydzielic obecny prompt RAG do szablonu,
- panel wyboru master promptu,
- podglad finalnego promptu,
- wersjonowanie promptow przez `version`.

Kryteria akceptacji:

- system nie ma promptu zaszytego w `rag.py`,
- zmiana promptu nie wymaga zmiany kodu,
- uzytkownik widzi finalny prompt przed generacja.

### Etap 3: Agent Builder MVP

Zakres:

- dodac model `AgentProfile`,
- predefiniowac 5 agentow startowych,
- panel wyboru agenta,
- agent wybiera domyslny model profile, prompt i RAG profile,
- historia czatu zapisuje, ktory agent odpowiadal.

Kryteria akceptacji:

- mozna przelaczac role agenta bez recznego zmieniania promptu,
- odpowiedzi agentow roznia sie stylem i zakresem,
- konfiguracja agentow jest zapisana poza kodem.

### Etap 4: RAG Profiles i lepsze zrodla

Zakres:

- dodac profile RAG,
- dodac filtr per profil,
- dodac minimalny prog trafienia,
- ulepszyc render zrodel,
- dodac tryb "brak pewnej odpowiedzi", gdy wyniki sa slabe.

Kryteria akceptacji:

- agent moze pracowac tylko na wybranym obszarze dokumentacji,
- slabe wyniki nie sa maskowane pewna odpowiedzia,
- zrodla sa deduplikowane i czytelne.

### Etap 5: Evaluation Lab

Zakres:

- plik z pytaniami testowymi,
- runner testow dla modelu/promptu/agenta,
- raport porownawczy,
- metryki czasu i jakosci,
- test regresji dla "brak informacji w dokumentacji".

Kryteria akceptacji:

- mozna sprawdzic, czy nowy prompt/model jest lepszy od starego,
- raport pokazuje czas, zrodla i wynik oceny,
- brak odpowiedzi w dokumentacji jest testowany jawnie.

### Etap 6: API/SSE jako warstwa produkcyjna

Zakres:

- wystawic `stream_rag_answer(...)` jako endpoint SSE,
- zachowac obecny kontrakt eventow,
- dodac endpointy konfiguracji profili,
- przygotowac klienta frontendowego pod strumien eventow.

Kryteria akceptacji:

- Streamlit i przyszly frontend moga korzystac z tego samego pipeline,
- eventy `phase`, `token`, `done`, `error` maja stabilny kontrakt,
- brak koniecznosci przepisywania logiki RAG.

## 4. Decyzje architektoniczne

- Konfiguracje modeli, promptow, agentow i RAG profiles trzymac poza kodem, na start jako pliki JSON/TOML.
- Nie dodawac bazy danych do PoC, dopoki konfiguracje plikowe wystarczaja.
- Nie dawac agentom narzedzi mutujacych w pierwszej wersji.
- Najpierw mierzyc i porownywac jakosc, potem automatyzowac dzialania.
- Utrzymac eventowy kontrakt streamingu jako fundament pod SSE.

## 5. Ryzyka i zabezpieczenia

- Zbyt duzo suwakow w UI moze pogorszyc uzytecznosc. Rozwiazanie: presety i tryb zaawansowany.
- Master prompty bez wersjonowania utrudnia regresje. Rozwiazanie: wersja i historia zmian.
- Agenci bez ograniczen moga dawac niespojne odpowiedzi. Rozwiazanie: jawne profile, limity i polityki zrodel.
- Lepszy model nie zawsze znaczy lepsza odpowiedz. Rozwiazanie: Evaluation Lab i testy porownawcze.
- RAG moze dawac pozornie pewne odpowiedzi przy slabym kontekście. Rozwiazanie: prog trafienia i tryb "brak pewnej odpowiedzi".

## 6. Rekomendowany nastepny krok

Najblizszy sprint powinien objac Etap 1 i poczatek Etapu 2:

1. `ModelProfile` z dodatkowymi parametrami Ollama.
2. Zapis/odczyt profili z pliku.
3. Panel wyboru profilu w `Agent AI`.
4. Wydzielenie master promptu z kodu do szablonu.
5. Testy payloadu Ollama i renderowania profilu.

To da realna kontrole nad modelem bez przedwczesnego komplikowania agentami.
