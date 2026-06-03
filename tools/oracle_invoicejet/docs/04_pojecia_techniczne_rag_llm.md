# Pojęcia techniczne RAG i LLM

Ten rozdział tłumaczy pojęcia używane w Oracle InvoiceJet. Ma pomóc osobie, która zna aplikacje biznesowe, ale dopiero uczy się RAG, embeddingów i lokalnych LLM.

## Czym jest RAG

RAG oznacza `Retrieval-Augmented Generation`, czyli generowanie odpowiedzi wzbogacone wyszukanym kontekstem.

Zamiast pytać model "z pamięci", system robi trzy rzeczy:

1. wyszukuje fragmenty dokumentacji pasujące do pytania,
2. buduje prompt zawierający pytanie i te fragmenty,
3. prosi LLM o odpowiedź tylko na podstawie tego kontekstu.

Dzięki temu model nie musi znać InvoiceJet z treningu. Wystarczy, że umie czytać kontekst i pisać odpowiedź.

## Dokument

Dokument to pojedynczy plik Markdown ze źródeł:

- `InvoiceJet/doc_AI`,
- `InvoiceJet/doc_user`.

Dokument może opisywać ekran, proces, endpoint, tabelę, walidację, mapowanie albo scenariusz testowy.

## Chunk

Chunk to fragment dokumentu zapisany w indeksie. Dokumenty są dzielone, bo cały plik często jest za długi, żeby efektywnie go wyszukiwać i przekazywać do modelu.

Przykład:

```text
plik: 01_ekrany/Documents/DocumentSeries.md
chunk 0: tytuł i opis ekranu
chunk 1: pola formularza
chunk 2: operacje i walidacje
```

Oracle przechowuje przy chunku:

- tekst,
- ścieżkę źródła,
- nagłówek `heading_path`,
- typ źródła,
- encję, ekran, tabelę, endpoint,
- embedding.

## Chunk size i chunk overlap

`chunk_size` to docelowa długość fragmentu. W Oracle domyślnie jest to `1800` znaków.

`chunk_overlap` to nakładka między sąsiednimi chunkami. W Oracle domyślnie jest to `250` znaków.

Nakładka jest potrzebna, bo ważna informacja może leżeć na granicy dwóch fragmentów. Bez overlapu pytanie mogłoby trafić na chunk bez pełnego kontekstu.

Zbyt małe chunki:

- są szybkie,
- ale mogą gubić sens.

Zbyt duże chunki:

- mają więcej kontekstu,
- ale pogarszają precyzję wyszukiwania i zużywają okno modelu.

## Embedding

Embedding to liczbowy opis znaczenia tekstu. Model embeddingowy zamienia tekst na wektor liczb.

Uproszczony przykład:

```text
"ekran serii dokumentów" -> [0.12, -0.44, 0.03, ...]
"tabela document series" -> [0.10, -0.39, 0.08, ...]
```

Jeżeli dwa teksty mają podobne znaczenie, ich wektory powinny być blisko siebie. Dzięki temu można znaleźć fragment dokumentacji pasujący do pytania, nawet jeśli użyto trochę innych słów.

## Model embeddingów

Model embeddingów nie generuje odpowiedzi. On tylko tworzy wektory dla pytań i dokumentacji.

W Oracle dostępne są:

- `bge-m3` - domyślny model embeddingów. W praktyce jest lepszym wyborem dla wielojęzycznych i technicznych dokumentów, dlatego jest domyślny.
- `nomic-embed-text` - alternatywa do eksperymentów. Może być lżejsza, ale jakość trzeba porównywać na Evaluation Lab.

Ważne: indeks musi być zbudowany tym samym modelem embeddingów, którego używa retrieval. Po zmianie modelu embeddingów wykonaj:

```powershell
.\scripts\invoke-refresh-index.ps1 -ForceRebuild
```

## Vector database

Vector database to baza zoptymalizowana pod wyszukiwanie podobnych wektorów. Oracle używa ChromaDB.

Chroma przechowuje:

- wektor embeddingu,
- tekst chunka,
- metadane,
- identyfikator chunka.

Gdy użytkownik zada pytanie, Oracle liczy embedding pytania i pyta Chroma o najbliższe fragmenty.

## Retrieval

Retrieval to wyszukiwanie kontekstu dla pytania. W Oracle nie jest to już tylko proste `top_k` z Chroma.

Aktualny retrieval łączy:

- wyszukiwanie semantyczne po embeddingach,
- wyszukiwanie leksykalne po ścieżkach i treści,
- profile RAG,
- preferowane typy źródeł,
- boosty dla mapowań, ekranów, API, modelu danych i walidacji.

To jest ważne dla pytań przekrojowych. Pytanie o ekran i tabelę powinno pobrać zarówno opis UI, jak i dokument modelu danych.

## top_k w retrievalu

`top_k` oznacza liczbę finalnych fragmentów kontekstu przekazanych dalej do promptu. Większy `top_k` daje modelowi więcej materiału, ale:

- wydłuża prompt,
- zwiększa koszt obliczeniowy,
- może dodać szum,
- może pogorszyć odpowiedź, jeśli kontekst jest za szeroki.

Dla pytań przekrojowych często pomaga profil `cross_reference`, bo dobiera różne typy źródeł zamiast tylko zwiększać `top_k`.

## Profil RAG

Profil RAG to strategia wyszukiwania. W Oracle są cztery profile:

- `full_app_qa` - ogólne pytania o aplikację.
- `cross_reference` - pytania ekran/pole/API/tabela/walidacja.
- `technical_deep_dive` - backend, baza, algorytmy, role, testy.
- `user_help` - instrukcje użytkownika z `doc_user`.

Profil określa:

- grupy źródeł,
- preferowane typy źródeł,
- boosty rankingowe,
- mnożnik szerokiego wyszukiwania,
- limit kontekstu.

## Prompt

Prompt to instrukcja wysłana do modelu LLM. Oracle buduje prompt z:

- master promptu,
- instrukcji RAG,
- polityki źródeł,
- pytania użytkownika,
- spakowanego kontekstu,
- ostrzeżeń audytora źródeł.

Dobry prompt mówi modelowi:

- kim jest,
- w jakim języku odpowiada,
- że ma używać tylko kontekstu,
- kiedy zwrócić fallback,
- jak cytować źródła,
- żeby nie pokazywać procesu rozumowania.

## Master prompt

Master prompt to profilowana, bazowa instrukcja zachowania modelu. W Oracle jest w `profiles/prompt_profiles.json`.

Nie jest dobrym pomysłem zmieniać master prompt "na czuja". Każdą istotną zmianę należy sprawdzać na tym samym golden set.

## LLM

LLM to model generujący tekst. W Oracle LLM dostaje prompt i zwraca odpowiedź po polsku.

Modele dostępne w projekcie:

- `gemma3:4b` - domyślny model generacyjny; lepszy balans jakości i wydajności.
- `gemma3:1b` - szybki, lżejszy model; dobry do testów, zwykle słabszy w odpowiedziach przekrojowych.
- `qwen3:4b` - alternatywa do porównań jakościowych.
- `qwen3:1.7b` - lżejsza alternatywa do szybkich eksperymentów.

Różnice między modelami należy oceniać praktycznie:

- czy cytują źródła,
- czy trzymają się kontekstu,
- czy rozumieją pytania przekrojowe,
- czy nie halucynują,
- jaki mają czas odpowiedzi,
- ile mieszczą w oknie kontekstu.

## Parametry modelu

`temperature` steruje losowością. Dla dokumentacji zwykle najlepsze są niskie wartości, np. `0.0-0.2`.

`top_p` ogranicza pulę prawdopodobnych tokenów. Niższe wartości mogą stabilizować odpowiedź, ale zbyt niskie mogą ją zubożyć.

`top_k modelu` ogranicza liczbę kandydatów tokenów rozważanych przez model. To inny parametr niż `top_k` retrievalu.

`repeat_penalty` karze powtarzanie tych samych fraz. Przydatne, gdy model wpada w pętle albo powtarza źródła.

`num_ctx` to okno kontekstu modelu. Musi pomieścić instrukcje, pytanie, kontekst i miejsce na odpowiedź.

`num_predict` to limit długości generowanej odpowiedzi.

`seed` może pomagać w powtarzalności, jeżeli model i runtime go respektują.

`timeout_sec` ogranicza maksymalny czas generacji.

## Token

Token to jednostka tekstu widziana przez model. Tokenem może być całe słowo, część słowa, znak interpunkcyjny albo fragment technicznego identyfikatora.

Modele nie liczą tekstu w znakach, tylko w tokenach. Dlatego długi prompt z wieloma źródłami może przekroczyć `num_ctx`, nawet jeśli wydaje się krótki jako tekst.

## Streaming

Streaming oznacza, że odpowiedź pojawia się stopniowo. Ollama zwraca kolejne fragmenty tekstu, a UI dopisuje je w jednym placeholderze.

Zalety:

- użytkownik widzi, że system pracuje,
- pierwsza część odpowiedzi pojawia się szybciej,
- UI może pokazywać etapy pracy.

W Oracle streaming dotyczy generacji odpowiedzi. Źródła są pokazywane dopiero po finalnym eventcie `completed`.

## TTFT

TTFT oznacza `time to first token`, czyli czas od startu przebiegu do pierwszego tokenu odpowiedzi.

Jeżeli TTFT jest wysoki, problem może leżeć w:

- wolnym retrievalu,
- dużym promptcie,
- zimnym modelu w Ollama,
- zbyt ciężkim modelu,
- przeciążonym sprzęcie.

## SSE

SSE oznacza `Server-Sent Events`. To prosty mechanizm HTTP do strumieniowania danych z serwera do klienta.

Oracle jeszcze nie wystawia osobnego API SSE, ale kontrakt eventów jest przygotowany tak, żeby później dało się go wystawić bez przepisywania pipeline.

## Halucynacja

Halucynacja to sytuacja, w której model podaje informację, której nie ma w kontekście albo która jest nieprawdziwa.

Oracle ogranicza halucynacje przez:

- retrieval z dokumentacji,
- master prompt "tylko na podstawie kontekstu",
- fallback przy braku danych,
- cytowania źródeł,
- Evaluation Lab,
- profilowanie źródeł dla pytań przekrojowych.

## Fallback no-answer

Fallback to stała odpowiedź:

```text
Nie znalazłem tego w dokumentacji.
```

To jest poprawny wynik, gdy dokumentacja nie zawiera odpowiedzi. W aplikacji RAG brak odpowiedzi jest lepszy niż pewnie brzmiąca halucynacja.

## Golden set

Golden set to zestaw testowych pytań z oczekiwanymi źródłami albo oczekiwanym fallbackiem. Służy do regresji jakości.

Jeżeli zmieniamy profile, prompt albo model, porównujemy wyniki na tych samych pytaniach. Dzięki temu nie stroimy systemu "na oko".
