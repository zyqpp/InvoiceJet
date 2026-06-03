# Chroma MD Embedded POC (InvoiceJet)

Lokalny POC indeksowania dokumentacji `*.md`/`*.MD` do Chroma w trybie embedded (`PersistentClient`), bez integracji z backendem/API.

## Co robi ten modul

- automatycznie wykrywa markdowny w repo,
- pomija katalogi techniczne (`node_modules`, `bin`, `obj`, `.git`, itd.),
- czyta cale pliki i dzieli je automatycznie na chunki:
  - najpierw po naglowkach `#`, `##`, `###`,
  - potem fallback na stale okna znakow z overlapem,
- zapisuje chunki i metadata do Chroma,
- prowadzi manifest incremental (`index_manifest.json`) oparty o hash pliku,
- obsluguje usuwanie skasowanych plikow z indeksu.

## Struktura

- `chroma_md_poc/ingest.py` - indeksacja (incremental / force rebuild)
- `chroma_md_poc/query.py` - zapytania semantyczne
- `.env.example` - konfiguracja
- `requirements.txt` - zaleznosci

## Instalacja

Uruchamiaj polecenia z katalogu:

```powershell
cd G:\Projekty informatyczne\Gotowe aplikacje\InvoiceJet\tools\chroma_md_embedded_poc
```

1. Utworz venv:

```powershell
python -m venv .venv
```

2. Aktywuj venv:

```powershell
.venv\Scripts\Activate.ps1
```

3. Zainstaluj zaleznosci:

```powershell
pip install -r requirements.txt
```

4. Skopiuj konfiguracje:

```powershell
Copy-Item .env.example .env
```

## Przekierowanie wszystkiego na dysk G

Ten POC ma skrypty, ktore ustawiają cache i katalog domowy procesu na `G:` (w katalogu repo):

- `TEMP/TMP` -> `G:\...\InvoiceJet\.tmp\temp`
- `HOME/USERPROFILE` -> `G:\...\InvoiceJet\.tmp\home`
- `PIP_CACHE_DIR` -> `G:\...\InvoiceJet\.tmp\pip-cache`

Dzieki temu:

- `pip` nie zapisuje cache na `C:`,
- Chroma pobiera model ONNX do `.tmp\home\.cache\chroma` na `G:`.

## Konfiguracja

Konfiguracja przez `.env` (prefiks `CHROMA_POC_`):

- `PROJECT_ROOT` - root repo InvoiceJet
- `CHROMA_PATH` - katalog danych Chroma
- `COLLECTION_NAME` - nazwa kolekcji
- `INCLUDE_GLOBS` - wzorce plikow (`*.md,*.MD`)
- `EXCLUDE_DIRS` - katalogi pomijane
- `CHUNK_SIZE`, `CHUNK_OVERLAP`
- `TOP_K`, `BATCH_SIZE`

## Uzycie

### 1) Ingest incremental

```powershell
.\scripts\invoke-ingest.ps1
```

### 2) Pelna przebudowa indeksu

```powershell
.\scripts\invoke-ingest.ps1 -ForceRebuild
```

### 3) Zapytanie semantyczne

```powershell
.\scripts\invoke-query.ps1 -Question "Jak dziala proces logowania?"
```

Opcjonalnie:

```powershell
.\scripts\invoke-query.ps1 -Question "walidacja" -TopK 7 -SourceContains "docs/aos/backend"
```

### 4) GUI lokalne (Windows)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\invoke-gui.ps1 -Port 8501
```

Po uruchomieniu otworz przegladarke:

`http://127.0.0.1:8501`

W GUI sa teraz 2 zakladki:

- `Wyszukiwarka` - klasyczne zapytania semantyczne do Chroma.
- `Agent AI` - RAG na lokalnym modelu przez Ollama + zarzadzanie modelami.

W zakladce `Agent AI` jest przycisk `Help ?` oraz pobranie manuala (`.md`).
Pelna instrukcja jest tez w pliku:

- `AGENT_AI_USER_MANUAL_PL.md`
- `LLM_EXPANSION_PLAN_PL.md` - plan rozbudowy sterowania LLM, promptami, agentami i ewaluacja jakosci.

## Agent AI - lokalne modele

Zakladka `Agent AI` daje:

- liste lokalnych modeli Ollama,
- pobieranie modeli z biblioteki Ollama (`/api/pull`),
- pobieranie plikow `GGUF` z Hugging Face,
- tworzenie modelu Ollama bezposrednio z pobranego `GGUF`,
- chat RAG: pytanie -> kontekst z Chroma -> odpowiedz lokalnego modelu,
- strumieniowanie odpowiedzi token po tokenie w trakcie generacji.

Wymaganie: uruchomiony Ollama (`ollama serve` lub aplikacja Ollama Desktop).

## Streaming RAG

Agent AI pokazuje przebieg odpowiedzi w trzech etapach:

1. `Wyszukiwanie kontekstu w Chroma`
2. `Budowanie promptu RAG`
3. `Generowanie odpowiedzi przez model lokalny`

Podczas trzeciego etapu odpowiedz jest dopisywana na zywo token po tokenie. Zrodla (`source_path`) sa pokazywane dopiero po zakonczeniu odpowiedzi, zeby uzytkownik nie mylil czesciowego wyniku z finalnym zestawem cytowan.

Po kazdym przebiegu GUI pokazuje metryki:

- `Czas retrieval` - czas wyszukiwania fragmentow dokumentacji w Chroma,
- `Pierwszy token` - czas od startu zapytania do pierwszego tokenu odpowiedzi,
- `Czas generowania` - czas samego streamu z Ollama,
- `Czas calkowity` - caly czas obslugi zapytania.

Logika RAG jest wydzielona do `chroma_md_poc/rag.py`. Generator `stream_rag_answer(...)` emituje eventy `phase_started`, `phase_completed`, `token`, `completed` i `error`, co pozwala pozniej wystawic ten sam pipeline jako SSE bez przepisywania logiki.

## Metadata chunka

Kazdy rekord zawiera:

- `source_path`
- `file_name`
- `rel_dir`
- `heading`
- `chunk_index`
- `source_sha256`
- `char_start`
- `char_end`
- `source_mtime`

## Raport ingestu

Skrypt wypisuje m.in.:

- liczbe plikow wykrytych / pominietych,
- liczbe plikow zmienionych / bez zmian / usunietych,
- liczbe chunkow dodanych i usunietych,
- liczbe bledow odczytu,
- calkowita liczbe rekordow w kolekcji,
- czas wykonania.

## Troubleshooting

- Pierwsze uruchomienie moze pobierac model embeddingowy Chroma/ONNX z internetu.
- Brak internetu lub blokada sieci zatrzyma indeksacje na etapie embeddingu.
- Odczyt wspiera `utf-8`; pliki w innym kodowaniu sa raportowane jako warning i pomijane.
