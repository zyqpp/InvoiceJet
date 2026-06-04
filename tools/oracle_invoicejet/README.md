# Oracle InvoiceJet

Lokalny portal RAG dla dokumentacji InvoiceJet. Dziala na Markdownach z repo, uzywa ChromaDB jako lokalnego indeksu i Ollamy jako zrodla modeli LLM oraz embeddingow.

Portal Streamlit dziala na porcie `8502` i jest jedynym aktualnym PoC dla Oracle InvoiceJet.

## Dokumentacja projektu Oracle RAG

Pelna dokumentacja szkoleniowa projektu RAG i warstwy agentowej jest w:

- [docs/README.md](docs/README.md) - mapa dokumentacji,
- [docs/01_architektura_i_pipeline.md](docs/01_architektura_i_pipeline.md) - architektura, pipeline ingest/query/streaming/eval,
- [docs/02_zalozenia_stos_i_konfiguracja.md](docs/02_zalozenia_stos_i_konfiguracja.md) - zalozenia, stos technologiczny i konfiguracja,
- [docs/03_funkcje_i_obsluga.md](docs/03_funkcje_i_obsluga.md) - funkcje portalu, CLI i typowe scenariusze pracy,
- [docs/04_pojecia_techniczne_rag_llm.md](docs/04_pojecia_techniczne_rag_llm.md) - wyjasnienie chunkow, embeddingow, modeli, promptow i metryk,
- [docs/05_rozwoj_i_roadmapa.md](docs/05_rozwoj_i_roadmapa.md) - dalsze mozliwosci rozwoju.

Ta dokumentacja opisuje narzedzie Oracle InvoiceJet, czyli projekt RAG + agent. Nie zastepuje dokumentacji biznesowej samego InvoiceJet.

## Co jest zrodlem odpowiedzi

Domyslna baza odpowiedzi obejmuje tylko:

- `InvoiceJet/doc_AI`
- `InvoiceJet/doc_user`

Kod aplikacji nie jest jeszcze osobnym zrodlem prawdy. Najpierw stabilizujemy jakosc odpowiedzi na dokumentacji, a dopiero potem mozna dodac tryb code-aware.

## Taksonomia wiedzy

Indeks v2 dodaje metadane do kazdego chunka:

- `source_type`: `screen`, `process`, `algorithm`, `api`, `data_model`, `validation`, `role`, `business`, `test`, `mapping`,
- `area`, `entity`, `screen`, `process`, `table`, `endpoint`,
- `knowledge_tags`.

Metadane sa wyprowadzane ze struktury `doc_AI` i `doc_user`. Dzieki temu portal lepiej odpowiada na pytania przekrojowe, np. ekran -> pole -> API/proces -> tabela.

Po aktualizacji do manifestu v2 wykonaj force rebuild:

```powershell
cd "G:\Projekty informatyczne\Gotowe aplikacje\InvoiceJet\tools\oracle_invoicejet"
.\scripts\invoke-refresh-index.ps1 -ForceRebuild
```

## Profile RAG

Dostepne profile:

- `full_app_qa` - ogolne pytania o aplikacje,
- `cross_reference` - pytania przekrojowe ekran/pole/API/tabela,
- `technical_deep_dive` - backend, API, algorytmy, model danych, role i testy,
- `database_sql` - model danych, tabele, relacje i podstawowe zapytania `SELECT`,
- `algorithm_calculation` - wyliczenia kwot, sum dokumentu, frontend/backend, model danych i ryzyka,
- `user_help` - instrukcje uzytkownika z `doc_user`.

Profil RAG decyduje, jakie typy zrodel sa preferowane przy wyszukiwaniu. `cross_reference` dogrywa kontekst z kilku klas zrodel, zeby nie odpowiadac tylko z jednego najblizszego semantycznie fragmentu.

## Agenci, modele i prompty

Konfiguracje sa w:

- `profiles/agent_profiles.json`,
- `profiles/model_profiles.json`,
- `profiles/prompt_profiles.json`.

Agent jest profilem pracy: wybiera profil modelu, prompt i profil RAG. Model profile kontroluje parametry Ollamy, m.in. `temperature`, `top_p`, `top_k`, `repeat_penalty`, `num_ctx`, `num_predict`, `seed`, `think`, `strip_thinking` i timeout. Prompt profile opisuje master prompt, polityke zrodel i styl odpowiedzi.

Wazne profile:

- `Klara - Algorytmy i wyliczenia` - agent do pytan o kwoty, sumy dokumentu, VAT, frontend/backend i ryzyka implementacyjne. Uzywa profilu RAG `algorithm_calculation` i promptu `algorithm_explainer`.
- `Quality local 12B` - mocniejszy lokalny profil `gemma3:12b` do trudnych odpowiedzi i porownan w Evaluation Lab.
- `Qwen3 no-think experimental` - profil Qwen z `think=false`; nadal traktowany jako eksperymentalny.

## Streaming odpowiedzi

Czat dziala eventowo:

1. retrieval,
2. budowanie promptu,
3. generowanie,
4. finalna odpowiedz, zrodla i metryki.

Odpowiedz dopisuje sie token po tokenie. Zrodla sa renderowane dopiero po zakonczeniu generacji. Ten kontrakt eventow jest przygotowany pod przyszle SSE/API.

Oracle pokazuje takze zrodla systemowe, gdy model nie doda wlasnej sekcji `Zrodla`. Dla `InvoiceJet/doc_AI` i `InvoiceJet/doc_user` UI buduje klikane linki do portali MkDocs na podstawie `ORACLE_DOCS_PORTAL_DOC_AI` i `ORACLE_DOCS_PORTAL_DOC_USER`.

Metryki:

- `retrieval_sec` - czas wyszukiwania kontekstu,
- `generation_sec` - czas generacji,
- `total_sec` - caly przebieg,
- `time_to_first_token_sec` - czas do pierwszego tokenu,
- `prompt_eval_count`, `eval_count`, `eval_duration_ns` - metryki zwracane przez Ollama, jesli sa dostepne.

## Evaluation Lab

Golden set jest w:

```text
tools/oracle_invoicejet/eval/golden_set.json
```

Uruchomienie przez CLI:

```powershell
.\scripts\invoke-evaluate.ps1 -Mode retrieval
.\scripts\invoke-evaluate.ps1 -Mode answer -Limit 3
.\.venv\Scripts\oracle-evaluate.exe --mode retrieval
.\.venv\Scripts\oracle-evaluate.exe --mode answer --limit 3
```

Albo przez Python:

```powershell
python -m oracle_invoicejet.cli_evaluate --mode retrieval
```

Tryb `retrieval` sprawdza, czy profil RAG znajduje oczekiwane zrodla. Tryb `answer` uruchamia pelny model LLM i jest wolniejszy.

Quality Lab mierzy teraz rowniez jakosc odpowiedzi:

- wymagane terminy/formuly w odpowiedzi,
- zakazane fragmenty, np. fallback w odpowiedzi, ktora jednak zawiera merytoryczne ustalenia,
- wykrycie mieszanej odpowiedzi typu: tresc + `Nie znalazlem tego w dokumentacji`.

## Setup lokalny

```powershell
cd "G:\Projekty informatyczne\Gotowe aplikacje\InvoiceJet\tools\oracle_invoicejet"
.\scripts\invoke-setup.ps1
```

Jesli PowerShell blokuje skrypty:

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\invoke-setup.ps1"
```

## Modele Ollama

Portal pozwala pobierac tylko modele z whitelisty:

- `gemma3:4b`
- `gemma3:12b`
- `gemma3:1b`
- `deepseek-r1:8b`
- `qwen3:4b`
- `qwen3-vl:4b`
- `qwen3:1.7b`
- `bge-m3`
- `nomic-embed-text`

Pobranie domyslnego zestawu:

```powershell
.\scripts\invoke-pull-models.ps1 -Models gemma3:4b,bge-m3
```

## Indeksacja i refresh bazy

Pierwszy pelny build albo rebuild po zmianie embeddingu/metadanych:

```powershell
.\scripts\invoke-refresh-index.ps1 -ForceRebuild
```

Codzienne odswiezenie po zmianach w dokumentacji:

```powershell
.\scripts\invoke-refresh-index.ps1
```

Refresh dziala incremental: nowe pliki sa dodawane, zmienione pliki sa reindeksowane po hashach, usuniete pliki sa usuwane z indeksu.

## Linki do bazy wiedzy MkDocs

Oracle przechowuje w indeksie `source_path`, np.:

```text
InvoiceJet/doc_AI/04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md
```

Przy renderowaniu UI zamienia te sciezki na adresy portali:

- `InvoiceJet/doc_AI/.../plik.md` -> `ORACLE_DOCS_PORTAL_DOC_AI/.../plik.html`,
- `InvoiceJet/doc_user/.../plik.md` -> `ORACLE_DOCS_PORTAL_DOC_USER/.../plik.html`,
- `README.md` -> `index.html`.

Domyslnie:

```text
ORACLE_DOCS_PORTAL_DOC_AI=http://127.0.0.1:8001
ORACLE_DOCS_PORTAL_DOC_USER=http://127.0.0.1:8002
```

Skrypty `docs-portal/setup.ps1` i `docs-portal/start-docs.ps1` aktualizuja lokalny `.env` Oracle po zmianie portow lub hosta. Zmiana tych adresow nie wymaga przebudowy indeksu.

## Portal

```powershell
.\scripts\invoke-gui.ps1 -Port 8502
```

Adres:

```text
http://127.0.0.1:8502
```

Zakladki:

- `Czat` - streamingowa odpowiedz Oracle z wybranym agentem, profilem RAG, modelem i promptem.
- `Wyszukiwarka` - test surowego/profilowanego retrievalu z dystansem semantycznym i linkiem do portalu MkDocs.
- `Zrodla` - lista plikow w bazie odpowiedzi z metadanymi i linkami do bazy wiedzy.
- `Indeks` - status manifestu, refresh i force rebuild.
- `Ewaluacja` - golden set dla jakosci odpowiedzi przekrojowych.
- `Agenci i modele` - profile pracy, status modeli, prompt studio preview i profile RAG.
- `Diagnostyka` - doctor, test embeddingu, test RAG i test fallbacku.

## Diagnostyka i testy

```powershell
.\scripts\invoke-doctor.ps1
.\scripts\invoke-doctor.ps1 -TestEmbedding
.\scripts\invoke-query.ps1 -Question "Na ekranie serii dokumentow skad pobierane sa informacje i jaka tabela je przechowuje?"
.\scripts\invoke-query.ps1 -Question "Jaka bedzie jutro pogoda w Warszawie?"
```

Pytanie spoza dokumentacji ma zwrocic:

```text
Nie znalazłem tego w dokumentacji.
```

## Jakosc

- Odpowiedzi sa po polsku i tylko z kontekstu.
- Kazda odpowiedz ma cytowania albo staly fallback.
- Zrodla pojawiaja sie dopiero po zakonczeniu generacji i zawieraja deterministyczne linki do MkDocs, gdy `source_path` nalezy do `doc_AI` albo `doc_user`.
- UI nie zawiera logiki chunkingu, promptowania ani indeksowania poza wywolaniem serwisow.
- `.env`, `.venv`, `chroma_data`, `docker-data`, manifest i modele nie sa commitowane.
