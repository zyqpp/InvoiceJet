# Szablon AOS procesu backendowego

Każdy proces backendowy składa się z ośmiu plików.

---

## `00_METADANE.md`

- nazwa procesu,
- endpointy,
- kontrolery,
- serwisy,
- DTO,
- encje,
- autoryzacja,
- status dokumentu.

## `01_PRZEGLAD_PROCESU.md`

- cel procesu,
- diagram przepływu,
- warunki wejściowe,
- wynik procesu,
- zależności techniczne.

## `02_KONTRAKT_API.md`

- metoda HTTP,
- ścieżka,
- parametry trasy,
- ciało żądania,
- odpowiedź API,
- statusy HTTP.

## `03_LOGIKA_APLIKACYJNA.md`

- metoda kontrolera,
- metoda serwisu,
- kroki wykonania,
- zapisy do bazy,
- transakcje przez `IUnitOfWork`.

## `04_DANE_MODELE_MAPOWANIA.md`

- DTO wejściowe,
- DTO wyjściowe,
- encje domenowe,
- mapowania `AutoMapper`,
- tabele i relacje EF Core.

## `05_BLEDY_BEZPIECZENSTWO.md`

- autoryzacja,
- źródło użytkownika,
- wyjątki,
- mapowanie wyjątków na HTTP,
- uwagi bezpieczeństwa.

## `06_SCENARIUSZE_TESTOWE.md`

- scenariusze pozytywne,
- scenariusze negatywne,
- przypadki brzegowe,
- dane testowe JSON.

## `HISTORIA_ZMIAN.md`

- wersja,
- data,
- autor,
- opis zmiany.
