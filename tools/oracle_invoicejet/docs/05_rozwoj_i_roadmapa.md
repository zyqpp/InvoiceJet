# Rozwój i roadmapa

Obecny Oracle InvoiceJet jest lokalnym PoC, ale architektura została ustawiona pod rozwój produkcyjny: eventowy pipeline, profile, metadane, Evaluation Lab i separacja UI od logiki RAG.

## Najbliższy priorytet

Najważniejsze nie jest dodanie kolejnych suwaków modelu, tylko poprawa jakości odpowiedzi przekrojowych.

Priorytet jakości:

1. lepsza dokumentacja źródłowa,
2. lepsze metadane,
3. lepszy retrieval,
4. golden set i regresja,
5. dopiero potem strojenie promptów i modeli.

## Kierunek 1: pełniejsze źródła wiedzy

Obecnie źródłem prawdy są `doc_AI` i `doc_user`. Następny duży krok to tryb code-aware.

Możliwe rozszerzenia:

- indeksowanie wybranych plików backendu i frontendu,
- osobna taksonomia dla kodu: controller, service, DTO, entity, migration, component, route, validator,
- mapowanie ekran -> komponent -> endpoint -> DTO -> encja -> tabela,
- ekstrakcja symboli kodu zamiast prostego dzielenia plików tekstowych,
- oznaczanie, czy źródło pochodzi z dokumentacji czy z kodu.

Warunek wejścia: obecny RAG na dokumentacji powinien być stabilny i mierzony Evaluation Lab.

## Kierunek 2: API i SSE

Pipeline `stream_answer()` jest gotowy do wystawienia przez backend.

Proponowany kontrakt:

- `POST /api/oracle/chat` - start zapytania i stream SSE,
- `GET /api/oracle/profiles` - lista profili agentów/modeli/promptów,
- `POST /api/oracle/evaluate` - uruchomienie ewaluacji,
- `GET /api/oracle/sources` - przegląd źródeł,
- `POST /api/oracle/index/refresh` - odświeżenie indeksu.

SSE jest lepszym domyślnym wyborem niż WebSocket, bo obecny przypadek to jeden kierunek: serwer wysyła statusy i tokeny do klienta.

## Kierunek 3: Agent Builder

AgentProfile 2.0 może pozwolić tworzyć własnych agentów bez edycji JSON ręcznie.

Planowane pola:

- nazwa,
- rola,
- profil modelu,
- profil promptu,
- profil RAG,
- zakres źródeł,
- limity,
- polityka niepewności,
- wymagane narzędzia read-only,
- opis przypadków użycia.

UI powinno walidować konfigurację i pokazywać podgląd finalnego promptu przed zapisem.

## Kierunek 4: Prompt Studio

Obecnie UI pokazuje profile promptów. Kolejny etap to bezpieczna edycja i porównywanie.

Funkcje:

- edycja master promptu,
- wersjonowanie profili,
- porównanie dwóch promptów na tym samym golden set,
- podgląd finalnego promptu po spakowaniu kontekstu,
- walidacja wymagań: język, fallback, zakaz wiedzy ogólnej, polityka źródeł.

Zasada: prompt nie trafia do domyślnego profilu bez wyniku ewaluacji.

## Kierunek 5: Model Lab

Model Lab powinien porównywać profile modeli na identycznych pytaniach.

Metryki:

- pass rate golden set,
- czas total,
- TTFT,
- liczba tokenów promptu,
- liczba tokenów odpowiedzi,
- obecność cytowań,
- liczba fallbacków,
- ręczna ocena jakości odpowiedzi.

To pozwoli odpowiedzieć praktycznie, czy lepszy jest np. `gemma3:4b` czy `qwen3:4b` dla dokumentacji InvoiceJet.

## Kierunek 6: lepszy retrieval

Możliwe usprawnienia:

- reranking drugim modelem po pierwszym szerokim wyszukiwaniu,
- graf źródeł: screen -> mapping -> endpoint -> table,
- graf modelu danych: tabela -> FK -> tabela -> ekran/proces/API,
- osobne indeksy dla dokumentacji użytkownika, technicznej i kodu,
- wykrywanie intencji pytania bardziej formalnym klasyfikatorem,
- normalizacja nazw ekranów, tabel, endpointów i encji,
- synonimy domenowe zarządzane w konfiguracji,
- diagnostyka "dlaczego wybrano to źródło".

## Kierunek 7: narzędzia agentowe read-only

Bezpieczny zestaw narzędzi po stabilizacji RAG:

- `search_docs` - wyszukaj źródła,
- `read_source` - przeczytaj konkretny dokument,
- `summarize_sources` - streść kilka źródeł,
- `compare_profiles` - porównaj konfiguracje,
- `run_eval_set` - uruchom golden set,
- `draft_select_sql` - przygotuj propozycję `SELECT` wyłącznie na podstawie modelu danych,
- `explain_trace` - wyjaśnij, skąd wzięła się odpowiedź.

Operacje mutujące, zapisywanie dokumentów, GitHub issue/PR i automatyzacje powinny zostać poza pierwszą wersją agentów.

## Kierunek 8: jakość dokumentacji źródłowej

RAG nie naprawi słabej dokumentacji. Największy wzrost jakości może dać standaryzacja plików `doc_AI` i `doc_user`.

Warto wprowadzić:

- stałe sekcje dla ekranów,
- stałe sekcje dla endpointów,
- jednoznaczne mapowania pole -> źródło danych,
- nazwy tabel i kolumn w przewidywalnym formacie,
- sekcje walidacji,
- sekcje ról i uprawnień,
- przykłady pytań, na które dokument ma odpowiadać.

## Kierunek 9: observability i audyt

Dla produkcyjnej wersji przydadzą się:

- historia zapytań lokalna lub serwerowa,
- zapis metryk,
- logi błędów Ollamy,
- raport pytań bez odpowiedzi,
- raport najczęściej używanych źródeł,
- wykrywanie regresji jakości po zmianie dokumentacji.

## Kierunek 10: bezpieczeństwo

Przed szerszym użyciem warto dodać:

- autoryzację użytkowników,
- limity zapytań,
- separację źródeł według uprawnień,
- blokadę dostępu do sekretów i plików spoza whitelisty,
- audyt odpowiedzi i źródeł,
- politykę retencji historii czatu.

## Proponowane kolejne etapy

1. Dodać kolejne przypadki do `golden_set.json`, szczególnie ekran -> pole -> tabela/API.
2. Poprawić dokumentację źródłową tam, gdzie golden set ujawnia braki.
3. Dodać diagnostykę grafu źródeł dla pytań przekrojowych.
4. Rozbudować Prompt Studio o podgląd finalnego promptu.
5. Dodać SSE API bez zmiany kontraktu eventów.
6. Zaprojektować code-aware indexing jako osobny profil źródeł.
