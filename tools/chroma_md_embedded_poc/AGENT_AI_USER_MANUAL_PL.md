# Agent AI - instrukcja uzytkownika

## 1. Co to jest

Zakladka `Agent AI` laczy:

1. wyszukiwanie kontekstu w dokumentacji (Chroma),
2. generowanie odpowiedzi przez lokalny model LLM (Ollama).

To jest tryb RAG:

- pytanie uzytkownika,
- znalezienie najlepszych fragmentow w dokumentacji,
- strumieniowana odpowiedz modelu na bazie tych fragmentow,
- lista zrodel (`source_path`) pod odpowiedzia, pokazywana po zakonczeniu generacji.

## 2. Wymagania

1. Musi byc uruchomiony Ollama (`ollama serve` lub Ollama Desktop).
2. Musi byc zbudowany indeks Chroma (zakladka `Wyszukiwarka` / skrypt ingest).
3. Musi byc co najmniej jeden lokalny model w Ollama.

## 3. Szybki start

1. Otworz `Agent AI`.
2. W sekcji modeli pobierz model:
   - przez Ollama (`Pobierz model przez Ollama`) albo
   - przez Hugging Face (`Pobierz GGUF...` + `Utworz model Ollama...`).
3. W czesci czatu wybierz model, ustaw `Top K` i wpisz pytanie.
4. Obserwuj etapy przetwarzania i odpowiedz dopisywana na zywo.
5. Po zakonczeniu sprawdz sekcje `Zrodla`.

## 4. Znaczenie najwazniejszych pol

- `Model`: lokalny model, ktory generuje odpowiedz.
- `Top K kontekstu`: ile fragmentow dokumentacji ma trafic do promptu.
- `num_ctx`: maksymalny rozmiar kontekstu modelu (tokeny).
- `Filtr source_path`: zaweza dokumenty do podanej czesci sciezki.
- `Temperature`: nizsza = bardziej stabilna odpowiedz, wyzsza = bardziej kreatywna.

## 5. Streaming odpowiedzi

Podczas obslugi pytania Agent AI pokazuje trzy etapy:

1. `Wyszukiwanie kontekstu w Chroma`
2. `Budowanie promptu RAG`
3. `Generowanie odpowiedzi przez model lokalny`

W trzecim etapie odpowiedz pojawia sie stopniowo token po tokenie. Zrodla sa wyswietlane dopiero po zakonczeniu odpowiedzi.

Po przebiegu widoczne sa metryki:

- `Czas retrieval`: ile trwalo wyszukiwanie kontekstu,
- `Pierwszy token`: czas od wyslania pytania do pierwszego fragmentu odpowiedzi,
- `Czas generowania`: ile trwalo generowanie odpowiedzi,
- `Czas calkowity`: calkowity czas obslugi zapytania.

## 6. Pobieranie modeli

### A) Z biblioteki Ollama

Wpisz nazwe, np.:

- `qwen2.5:3b-instruct`
- `llama3.2:3b`

Kliknij `Pobierz model przez Ollama`.

### B) Z Hugging Face (GGUF)

1. Podaj `repo_id` i `filename` GGUF.
2. Kliknij `Pobierz GGUF z Hugging Face`.
3. Podaj nazwe modelu w Ollama.
4. Kliknij `Utworz model Ollama z pobranego GGUF`.

Uwaga:

- dla prywatnych repozytoriow potrzebny jest token HF.
- modele GGUF zajmuja duzo miejsca na dysku.

## 7. Dobre praktyki

1. Zaczynaj od `Top K = 5`.
2. Przy pytaniach procesowych uzywaj `Filtr source_path`, np.:
   - `InvoiceJet/InvoiceJetAPI/docs/aos/backend/processes/P-02_LoginUser`
3. Dla precyzyjnych odpowiedzi trzymaj `Temperature` nisko (0.1-0.3).
4. Zawsze sprawdzaj `Zrodla` pod odpowiedzia.

## 8. Ograniczenia

1. Agent odpowiada na podstawie tego, co jest w indeksie.
2. Jesli dokumentacja nie zawiera odpowiedzi, wynik moze byc ogolny.
3. Jakosc zalezy od:
   - jakosci dokumentacji,
   - chunkingu,
   - doboru modelu.

## 9. Najczestsze problemy

1. `Ollama API niedostepne`:
   - uruchom `ollama serve`,
   - sprawdz czy port `11434` nie jest blokowany.
2. Brak modeli:
   - pobierz model przez sekcje zarzadzania modelami.
3. Slaba odpowiedz:
   - zwieksz `Top K`,
   - zawez `Filtr source_path`,
   - wybierz lepszy model.
