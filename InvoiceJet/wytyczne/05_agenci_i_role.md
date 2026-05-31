# 05. Agenci i role

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| Autor | Właściciel projektu + Agent Claudiusz Sonte 4.6 max |
| Wersja | 0.1 |
| Status | Obowiązujący |

## A. Idea

Praca nad dokumentacją projektu AOS jest wykonywana przez **wyspecjalizowanych agentów językowych**, koordynowanych przez **Agenta-Orkiestratora**. Każdy agent ma jasno zdefiniowany cel, dane wejściowe, dane wyjściowe, granice odpowiedzialności i osobowość zawodową.

W projekcie InvoiceJet wszystkie role agentów pełni **Agent Claudiusz Sonte 4.6 max**, wykonując fazy sekwencyjnie lub równolegle w granicach jednej sesji.

## B. Typy agentów

### B.1. Agent-Orkiestrator

**Cel:** zarządzanie całością wytwarzania dokumentacji. Tworzy plan, deleguje zadania, weryfikuje produkty.
**Wyjścia:** `PLAN.md`, kolejka zadań, raporty statusu.
**Granice:** nie pisze treści dokumentacji. Nie podejmuje decyzji zarezerwowanych dla właściciela projektu.

### B.2. Agent-Archiwista

**Cel:** wykonanie Fazy 0 — przeniesienie starej dokumentacji do `archiwum/`.
**Wyjścia:** `archiwum/` z plikami, `archiwum/README.md`, `archiwum/_raport_archiwizacji.md`.
**Granice:** nie otwiera plików, które przenosi. Nie analizuje ich zawartości.

### B.3. Agent-Eksplorator

**Cel:** rozpoznanie projektu — drzewo katalogów, stos technologiczny, inwentaryzacja artefaktów.
**Wyjścia:** `doc_AI/00_meta/02_stos_technologiczny.md`, `doc_AI/00_meta/05_drzewo_projektu.md`, listy inwentaryzacyjne w `doc_AI/_mapowania/inwentaryzacja_*.md`.
**Granice:** nie opisuje merytorycznie żadnego artefaktu — produkuje tylko listy i meta-informacje.

### B.4. Agent-Szablonowy

**Cel:** materializacja szablonów i szkieletu katalogów `doc_AI/`.
**Wyjścia:** kompletny szkielet `doc_AI/`, szablony w `doc_AI/_szablony/`.

### B.5. Agent-Dokumentalista-Modelu-Danych

**Cel:** opis warstwy danych — DB, DTO, LINQ, automapper.
**Wejścia:** kod modeli EF Core, migracje (`InvoiceJetDbContextModelSnapshot.cs`), DTO.
**Wyjścia:** dokumenty w `doc_AI/05_model_danych/`.

### B.6. Agent-Dokumentalista-API

**Cel:** opis endpointów frontu i integracji.
**Wejścia:** kod kontrolerów ASP.NET Core, serwisy Angular.
**Wyjścia:** dokumenty w `doc_AI/04_api_i_integracje/`.

### B.7. Agent-Dokumentalista-Ekranow

**Cel:** opis ekranów aplikacji Angular.
**Wejścia:** kod komponentów frontu, pliki routingu, gotowe dokumenty API i DTO.
**Wyjścia:** dokumenty w `doc_AI/01_ekrany/`.

### B.8. Agent-Dokumentalista-Procesow

**Cel:** opis procesów technicznych backend + frontend.
**Wyjścia:** dokumenty w `doc_AI/02_procesy/`.

### B.9. Agent-Dokumentalista-Algorytmow

**Cel:** opis algorytmów wewnętrznych (walidacja, generowanie PDF, autoryzacja).
**Wyjścia:** dokumenty w `doc_AI/03_algorytmy/`.

### B.10. Agent-Dokumentalista-Ról-i-Uprawnień

**Cel:** opis ról, uprawnień, macierzy.
**Wyjścia:** dokumenty w `doc_AI/06_role_i_uprawnienia/`.

### B.11–B.17. Pozostałe agenci

Agent-Modelarz-Biznesowy, Agent-Modelarz-BPMN, Agent-UC, Agent-Testow, Agent-Slownikowy, Agent-Mapowan, Agent-Walidator — analogicznie jak w oryginalnych wytycznych.

## C. Reguły komunikacji

Każdy agent kończący zadanie generuje **raport zamknięcia** z: listą wytworzonych plików, listą wątpliwości, propozycjami aktualizacji wytycznych.

## Rejestr zmian dokumentu

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Właściciel projektu + Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
