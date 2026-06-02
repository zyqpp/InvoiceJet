# Oracle InvoiceJet

Lokalny portal RAG dla dokumentacji InvoiceJet. Działa na Markdownach z repo, używa ChromaDB jako lokalnego indeksu i Ollamy jako źródła modeli LLM oraz embeddingów.

## Co jest źródłem odpowiedzi

Domyślna baza odpowiedzi obejmuje tylko:

- `InvoiceJet/doc_AI`
- `InvoiceJet/doc_user`

`archiwum/`, `InvoiceJetAPI/docs`, `InvoiceJetUI/docs`, `wytyczne/`, build outputy, `.venv`, `chroma_data`, `models` i katalogi techniczne nie są częścią bazy odpowiedzi.

## Agenci i modele

W portalu „agent” oznacza profil pracy, a nie nazwę modelu. Modele zachowują oryginalne nazwy Ollama.

Profile:

- `Mietek` — asystent ogólny, domyślny do codziennego pytania o dokumentację.
- `Stefan` — techniczny analityk do pytań o architekturę i procesy.
- `Wojtek` — przewodnik użytkownika do instrukcji krok po kroku.
- `Albercik` — szybki tryb na lekkim modelu `gemma3:1b`.
- `Hania` — testerka jakości, więcej źródeł i niska temperatura.
- `Zosia` — eksperyment z `qwen3:4b`; może wolniej odpowiadać przez tryb `thinking`.

Domyślny profil sprzętowy RTX 2060 6GB:

- LLM: `gemma3:4b`
- embedding: `bge-m3`
- `top_k=5`
- `num_ctx=8192`
- `temperature=0.1`
- `num_predict=512`

Embedding to liczbowy odcisk tekstu. Oracle zamienia pytanie i fragmenty dokumentacji na wektory, a potem szuka najbardziej podobnych fragmentów. Po zmianie modelu embeddingów trzeba przebudować indeks.

## Setup lokalny

Uruchom z katalogu repo:

```powershell
cd "G:\Projekty informatyczne\Gotowe aplikacje\InvoiceJet\tools\oracle_invoicejet"
.\scripts\invoke-setup.ps1
```

Jeśli PowerShell blokuje skrypty:

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\invoke-setup.ps1"
```

## Modele Ollama

Portal pozwala pobierać tylko modele z whitelisty:

- `gemma3:4b`
- `gemma3:1b`
- `qwen3:4b`
- `qwen3:1.7b`
- `bge-m3`
- `nomic-embed-text`

Pobranie domyślnego zestawu:

```powershell
.\scripts\invoke-pull-models.ps1 -Models gemma3:4b,bge-m3
```

## Indeksacja i refresh bazy

Pierwszy pełny build:

```powershell
.\scripts\invoke-refresh-index.ps1 -ForceRebuild
```

Codzienne odświeżenie po zmianach w dokumentacji:

```powershell
.\scripts\invoke-refresh-index.ps1
```

Refresh działa incremental: nowe pliki są dodawane, zmienione pliki są reindeksowane po hashach, usunięte pliki są usuwane z indeksu. Jeśli zmieni się kluczowe zdanie w istniejącym pliku, manifest wykryje zmianę i przebuduje chunki tylko dla tego pliku.

## Portal

```powershell
.\scripts\invoke-gui.ps1 -Port 8502
```

Adres:

```text
http://127.0.0.1:8502
```

Zakładki:

- `Czat` — pytanie do Oracle z wybranym profilem pracy.
- `Wyszukiwarka` — test surowego wyszukiwania semantycznego.
- `Źródła` — lista plików w bazie odpowiedzi.
- `Indeks` — status manifestu, refresh i force rebuild.
- `Agenci i modele` — profile pracy, status modeli i pobieranie z whitelisty.
- `Diagnostyka` — doctor, test embeddingu, test RAG i test fallbacku.

## Docker

Docker uruchamia portal. Ollama działa poza kontenerem na hoście.

Wymagania:

- Ollama działa lokalnie i odpowiada pod `http://127.0.0.1:11434`.
- Modele są pobrane na hoście, np. `gemma3:4b` i `bge-m3`.

Start:

```powershell
cd "G:\Projekty informatyczne\Gotowe aplikacje\InvoiceJet\tools\oracle_invoicejet"
docker compose up --build
```

Albo przez launcher:

```powershell
.\scripts\invoke-docker.ps1 -Build
```

Portal w kontenerze łączy się z Ollamą przez `http://host.docker.internal:11434`. Indeks kontenerowy zapisuje się w `tools/oracle_invoicejet/docker-data`.

## Diagnostyka i testy

```powershell
.\scripts\invoke-doctor.ps1
.\scripts\invoke-doctor.ps1 -TestEmbedding
.\scripts\invoke-query.ps1 -Question "Jak wygląda proces rejestracji i logowania w InvoiceJet?"
.\scripts\invoke-query.ps1 -Question "Jaka będzie jutro pogoda w Warszawie?"
```

Pytanie spoza dokumentacji ma zwrócić dokładnie:

```text
Nie znalazłem tego w dokumentacji.
```

## Jakość

- Odpowiedzi są po polsku i tylko z kontekstu.
- Każda odpowiedź ma cytowania albo stały fallback.
- UI nie zawiera logiki chunkingu, promptowania ani indeksowania poza wywołaniem serwisów.
- `.env`, `.venv`, `chroma_data`, `docker-data`, manifest i modele nie są commitowane.
