# Dokumentacja Oracle InvoiceJet RAG

Ten katalog opisuje projekt **Oracle InvoiceJet**, czyli lokalny portal RAG i warstwę agentową nad dokumentacją InvoiceJet. Nie jest to dokumentacja biznesowa samej aplikacji fakturowej. Źródłem wiedzy biznesowej pozostają pliki `InvoiceJet/doc_AI` oraz `InvoiceJet/doc_user`; tutaj opisujemy narzędzie, które tę wiedzę indeksuje, wyszukuje i przekazuje do modelu LLM.

## Dla kogo jest ta dokumentacja

- dla osoby, która pierwszy raz otwiera projekt i chce zrozumieć, jak działa RAG,
- dla developera, który ma utrzymywać `tools/oracle_invoicejet`,
- dla analityka lub PM-a, który chce wiedzieć, skąd Oracle bierze odpowiedzi,
- dla osoby testującej jakość odpowiedzi i profile agentów.

## Jak czytać

1. [Architektura i pipeline](01_architektura_i_pipeline.md) - moduły, przepływ danych, streaming, ewaluacja.
2. [Założenia, stos technologiczny i konfiguracja](02_zalozenia_stos_i_konfiguracja.md) - zakres projektu, technologie, pliki konfiguracyjne, modele.
3. [Funkcje i obsługa](03_funkcje_i_obsluga.md) - portal Streamlit, skrypty CLI, typowe scenariusze pracy.
4. [Pojęcia techniczne RAG i LLM](04_pojecia_techniczne_rag_llm.md) - chunki, embeddingi, retrieval, modele, parametry, streaming.
5. [Rozwój i roadmapa](05_rozwoj_i_roadmapa.md) - możliwe kierunki rozwoju po obecnym PoC.

## Szybki start

```powershell
cd "G:\Projekty informatyczne\Gotowe aplikacje\InvoiceJet\tools\oracle_invoicejet"
.\scripts\invoke-setup.ps1
.\scripts\invoke-pull-models.ps1 -Models gemma3:4b,bge-m3
.\scripts\invoke-refresh-index.ps1 -ForceRebuild
.\scripts\invoke-gui.ps1 -Port 8502
```

Portal działa lokalnie pod adresem:

```text
http://127.0.0.1:8502
```

## Najważniejsza zasada jakości

Oracle ma odpowiadać tylko na podstawie dokumentacji. Jeżeli dokumentacja nie zawiera odpowiedzi, poprawnym wynikiem jest fallback:

```text
Nie znalazłem tego w dokumentacji.
```

To ogranicza halucynacje modelu i wymusza pracę na źródłach. Jakość zwiększamy przez lepszą dokumentację, metadane, retrieval, profile RAG i ewaluację, a nie przez zgadywanie odpowiedzi przez model.
