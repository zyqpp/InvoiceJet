# Założenia, stos technologiczny i konfiguracja

## Cel projektu

Oracle InvoiceJet ma być lokalnym asystentem wiedzy o aplikacji InvoiceJet. Najważniejszy przypadek użycia to odpowiedzi przekrojowe: ekran, pole, walidacja, API, proces i tabela danych w jednej odpowiedzi ze źródłami.

Przykład pytania docelowego:

```text
Na ekranie serii dokumentów skąd pobierane są informacje i jaka tabela je przechowuje?
```

System ma znaleźć nie tylko opis ekranu, ale również mapowania, endpointy, procesy i model danych, jeżeli dokumentacja zawiera takie informacje.

## Założenia

- Pracujemy na portalu `tools/oracle_invoicejet`.
- Portal Streamlit działa na porcie `8502`.
- Źródłem prawdy są teraz `InvoiceJet/doc_AI` i `InvoiceJet/doc_user`.
- Kod aplikacji InvoiceJet nie jest jeszcze osobnym źródłem prawdy.
- Odpowiedzi mają być po polsku i tylko na podstawie kontekstu.
- Przy braku danych zwracamy stały fallback: `Nie znalazłem tego w dokumentacji.`
- Modele działają lokalnie przez Ollama.
- Indeks Chroma, manifest, `.env` i `.venv` są lokalne i nie trafiają do repo.

## Co nie jest celem obecnej iteracji

- Nie budujemy jeszcze publicznego backendu HTTP.
- Nie dodajemy agentów wykonujących mutacje w repozytorium.
- Nie pozwalamy modelowi zgadywać brakujących informacji z wiedzy ogólnej.
- Nie traktujemy odpowiedzi LLM jako prawdy bez cytowań.
- Nie robimy automatycznego merge do `main`.

## Stos technologiczny

| Obszar | Technologia | Rola |
|---|---|---|
| Język | Python | logika narzędzia, CLI, pipeline RAG |
| UI | Streamlit | lokalny portal na `8502` |
| Vector DB | ChromaDB | lokalny indeks wektorowy dokumentacji |
| LLM runtime | Ollama | lokalne modele generacyjne i embeddingowe |
| HTTP | requests | komunikacja z API Ollamy |
| Konfiguracja | `.env`, JSON, zmienne `ORACLE_*` | profile i parametry runtime |
| Testy | unittest | testy bez nowych zależności produkcyjnych |
| Skrypty | PowerShell | uruchamianie setupu, indeksu, GUI, ewaluacji |
| Kontenery | Docker / docker-compose | opcjonalne uruchomienie izolowane |

## Modele w projekcie

Whitelistę modeli definiuje `ORACLE_ALLOWED_MODELS` w konfiguracji. Domyślnie portal dopuszcza:

- `gemma3:4b` - domyślny model generacyjny dla jakości odpowiedzi na lokalnym sprzęcie.
- `gemma3:12b` - mocniejszy lokalny model jakościowy dla trudnych pytań i porównań.
- `gemma3:1b` - lżejszy model do szybkich testów.
- `deepseek-r1:8b` - eksperymentalny model reasoningowy, używany tylko do porównań.
- `qwen3:4b` - alternatywny model generacyjny do porównań; w profilu Qwen ma wymuszone `think=false`.
- `qwen3-vl:4b` - lokalny wariant Qwen z whitelisty, na razie tylko do świadomych eksperymentów.
- `qwen3:1.7b` - lżejszy wariant Qwen do eksperymentów.
- `bge-m3` - domyślny model embeddingów.
- `nomic-embed-text` - alternatywny model embeddingów.

Model embeddingów użyty przy wyszukiwaniu musi być ten sam, którym zbudowano indeks. Po zmianie `ORACLE_EMBEDDING_MODEL` trzeba wykonać force rebuild indeksu.

## Konfiguracja runtime

Konfigurację ładuje `oracle_invoicejet/config.py`. Priorytet wartości:

1. zmienne środowiskowe `ORACLE_*`,
2. plik `.env` w `tools/oracle_invoicejet`,
3. wartości domyślne z kodu.

Najważniejsze zmienne:

| Zmienna | Znaczenie |
|---|---|
| `ORACLE_REPO_ROOT` | katalog główny repozytorium InvoiceJet |
| `ORACLE_CHROMA_PATH` | lokalna ścieżka bazy Chroma |
| `ORACLE_MANIFEST_PATH` | lokalna ścieżka manifestu indeksu |
| `ORACLE_COLLECTION_NAME` | nazwa kolekcji Chroma |
| `ORACLE_OLLAMA_BASE_URL` | adres API Ollamy |
| `ORACLE_LLM_MODEL` | model generacyjny |
| `ORACLE_EMBEDDING_MODEL` | model embeddingów |
| `ORACLE_TOP_K` | liczba finalnych fragmentów kontekstu |
| `ORACLE_NUM_CTX` | okno kontekstu modelu LLM |
| `ORACLE_NUM_PREDICT` | limit tokenów odpowiedzi |
| `ORACLE_TEMPERATURE` | losowość generacji |
| `ORACLE_TOP_P` | próg nucleus sampling |
| `ORACLE_LLM_TOP_K` | ograniczenie kandydatów tokenów w modelu |
| `ORACLE_REPEAT_PENALTY` | kara za powtarzanie |
| `ORACLE_SEED` | deterministyczne ziarno, jeżeli model je wspiera |
| `ORACLE_TIMEOUT_SEC` | limit czasu generacji |
| `ORACLE_THINK` | opcjonalny parametr Ollamy dla modeli thinking: `true`, `false`, `low`, `medium`, `high` albo puste `auto` |
| `ORACLE_STRIP_THINKING` | lokalne czyszczenie bloków `<think>...</think>` z odpowiedzi |
| `ORACLE_CHUNK_SIZE` | docelowy rozmiar chunka |
| `ORACLE_CHUNK_OVERLAP` | nakładka między chunkami |
| `ORACLE_MIN_HITS` | minimalna liczba trafień, aby uruchomić LLM |
| `ORACLE_DOCS_PORTAL_DOC_AI` | bazowy URL portalu MkDocs dla `InvoiceJet/doc_AI` |
| `ORACLE_DOCS_PORTAL_DOC_USER` | bazowy URL portalu MkDocs dla `InvoiceJet/doc_user` |

Adresy portali dokumentacji są używane wyłącznie do budowania linków w UI i w promptach. Zmiana tych wartości nie wymaga przebudowy indeksu, bo Chroma przechowuje `source_path` do plików Markdown, a Oracle dopiero przy renderowaniu zamienia ścieżkę na URL portalu.

## Profile konfiguracyjne

Profile są jawne i plikowe:

- `profiles/agent_profiles.json` - rola agenta, domyślny zakres, profil modelu, profil promptu, profil RAG i limity.
- `profiles/model_profiles.json` - model LLM, embedding, temperatura, `top_p`, `top_k`, `num_ctx`, `num_predict`, timeout.
- `profiles/prompt_profiles.json` - master prompt, instrukcja RAG, styl odpowiedzi i polityka źródeł.

Dzięki temu nie trzeba zmieniać kodu, żeby porównać warianty pracy modelu. Zmiany profili nadal powinny być sprawdzane przez Evaluation Lab.

## Źródła i taksonomia

Indeks obejmuje:

- `InvoiceJet/doc_AI` jako `source_group=doc_ai`,
- `InvoiceJet/doc_user` jako `source_group=doc_user`.

Taksonomia rozpoznaje typy:

- `screen`,
- `process`,
- `algorithm`,
- `api`,
- `data_model`,
- `validation`,
- `role`,
- `business`,
- `test`,
- `mapping`.

Metadane są wyprowadzane głównie ze ścieżki i nazwy pliku. Przykładowo dokument pod `05_model_danych` zwykle dostanie `source_type=data_model`, a endpoint pod `04_api_i_integracje` dostanie `source_type=api` i pole `endpoint`.

## Linkowanie do portali MkDocs

Oracle linkuje wyniki RAG do portali dokumentacji przez deterministyczne mapowanie `source_path`:

- `InvoiceJet/doc_AI/.../plik.md` trafia do `ORACLE_DOCS_PORTAL_DOC_AI/.../plik.html`,
- `InvoiceJet/doc_user/.../plik.md` trafia do `ORACLE_DOCS_PORTAL_DOC_USER/.../plik.html`,
- `README.md` trafia do `index.html`, zgodnie z generowaniem MkDocs.

Wartość `distance` w tabelach źródeł to dystans semantyczny zwrócony przez bazę wektorową. Niższa wartość oznacza bliższe dopasowanie fragmentu do pytania, ale nie jest to procent pewności ani ranking jakości finalnej odpowiedzi.

Portale MkDocs mogą działać na innych portach albo pod innym hostem, np. w sieci wewnętrznej. Wtedy trzeba zaktualizować bazowe URL-e w `.env` albo uruchomić skrypty `docs-portal`, które synchronizują te wartości automatycznie.

## Bezpieczeństwo i prywatność

- Modele działają lokalnie, więc pytania i dokumentacja nie muszą wychodzić do zewnętrznej usługi LLM.
- Nie należy logować sekretów ani zawartości `.env`.
- Operacje agentowe są obecnie read-only albo diagnostyczne.
- W przyszłym API trzeba dodać autoryzację, limity zapytań i audyt dostępu do źródeł.

## Zasady utrzymania

- Po zmianie chunkingu, embeddingu albo schematu metadanych wykonaj `ForceRebuild`.
- Po zmianie profili RAG uruchom `Evaluation Lab` w trybie `retrieval`.
- Po zmianie promptów lub modeli porównuj wyniki w trybie `answer`.
- Nie commituj `chroma_data`, `index_manifest.json`, `.env`, `.venv` ani lokalnych modeli.
