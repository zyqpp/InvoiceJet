# Szablon AOS procesu backendowego

Każdy proces backendowy składa się z **ośmiu plików**. Wzorce do skopiowania są w `docs/aos/backend/templates/`. Definicję ukończenia każdego pliku zawiera `03_MARKERY_I_WERYFIKACJA.md`.

Kolejność pracy: `00 → 01 → 04 → 03 → 02 → 05 → 06 → HISTORIA`. Najpierw rozpoznaj dane i model (`04`), bo logika (`03`) i kontrakt (`02`) się do nich odwołują.

---

## `00_METADANE.md` — wizytówka procesu
Sekcje obowiązkowe: tabela metadanych, **lista wszystkich endpointów**, komponenty (kontroler, serwis, repozytoria, DTO, encje, wyjątki, integracje), autoryzacja, status dokumentu.

## `01_PRZEGLAD_PROCESU.md` — wymiar biznesowy + przepływ
Sekcje obowiązkowe: cel biznesowy (dla analityka), diagram `mermaid` z gałęziami błędów, warunki wejściowe (ze źródłem), wynik procesu, **reguły biznesowe**, uwagi z kodu z markerami.

## `02_KONTRAKT_API.md` — wymiar API
Sekcje obowiązkowe: **osobny blok na każdy endpoint** — metoda HTTP, ścieżka, parametry, autoryzacja, **konkretny JSON żądania i odpowiedzi**, komplet statusów HTTP z warunkami.

## `03_LOGIKA_APLIKACYJNA.md` — wymiar algorytmu (kręgosłup)
Sekcje obowiązkowe: uporządkowany algorytm (walidacje → logika → zapisy → odpowiedź), **cytaty kodu z kotwicami**, tabela `pole encji → źródło`, opis `CompleteAsync()` i transakcji, uwagi techniczne z markerami.

## `04_DANE_MODELE_MAPOWANIA.md` — wymiar danych (do kolumn)
Sekcje obowiązkowe: DTO we/wy z polami, encje z **tabelą kolumn** (typ, nullability, klucze, indeksy), relacje i kaskady, profile `AutoMapper`, istotne zapytania LINQ/SQL, użyte enumy/lookupy (link do `SLOWNIK_DANYCH`).

## `05_BLEDY_BEZPIECZENSTWO.md` — wymiar walidacji i bezpieczeństwa
<!-- Nazwa zachowana dla spójności z istniejącymi procesami; treść akcentuje walidacje. -->

Sekcje obowiązkowe: **katalog walidacji `WAL-XX`** (reguła, podstawa w kodzie, warunek, wyjątek, status, komunikat), tabela błędów z mapowaniem na HTTP (w tym niemapowane → `500`), autoryzacja i źródło tożsamości, uwagi bezpieczeństwa.

## `06_SCENARIUSZE_TESTOWE.md` — wymiar danych testowych
<!-- Nazwa zachowana dla spójności; treść akcentuje REALNE DANE, nie skrypty testów. -->

Sekcje obowiązkowe: zestaw danych poprawnych (realne wartości + warunki wstępne), zestawy niepoprawne (po jednym na `WAL-XX`), wartości brzegowe, warunki wstępne/seed (link do `KATALOG_DANYCH_TESTOWYCH`), oczekiwany rezultat każdego zestawu.

## `HISTORIA_ZMIAN.md` — wersjonowanie
Sekcje obowiązkowe: tabela wersja/data/autor/opis.

---

## Katalogi przekrojowe (poza katalogiem procesu)

Oprócz ośmiu plików procesu utrzymujemy katalogi przekrojowe opisane w `05_KATALOGI_PRZEKROJOWE.md`: `KATALOG_API`, `SLOWNIK_DANYCH`, `KATALOG_WYJATKOW`, `MODEL_DOMENY`, `ZAGADNIENIA_PRZEKROJOWE`, `KATALOG_DANYCH_TESTOWYCH`, `MAPA_FULLSTACK` (odłożone).
