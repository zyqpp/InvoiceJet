# {SCHEMA}.{NAZWA_TABELI} — tabela bazy danych

| Pole | Wartość |
|---|---|
| ID dokumentu | {TAB-DB-SCHEMA-NAZWA_TABELI} |
| Typ dokumentu | tabela_db |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Czym jest ta tabela z perspektywy biznesowej. Jakie dane przechowuje i jaka jest jej rola w modelu danych. */}
{OPIS_BIZNESOWY_TABELI}

## Charakterystyka tabeli

| Atrybut | Wartość |
|---|---|
| Pełna nazwa | {schema.NazwaTabeli} |
| Cel biznesowy | {1–2 zdania opisujące cel przechowywania danych} |
| Klucz główny | {LISTA_KOLUMN_KLUCZA_GLOWNEGO} |
| Encja EF Core | `{NazwaKlasyEncji}` — {LINK_DO_PLIKU_CS} |

## Kolumny

{/* Instrukcja: Wymień wszystkie kolumny tabeli. Kolumna "Klucz" przyjmuje wartości: PK / FK / UQ / - */}

| Kolumna | Typ SQL | NULL | Domyślna | Klucz | Opis biznesowy |
|---|---|---|---|---|---|
| {NazwaKolumny} | {varchar(255) / int / decimal(10,2) / datetime2 / bit / ...} | {YES / NO} | {WARTOSC_LUB_NULL_LUB_-} | {PK / FK / UQ / -} | {OPIS_BIZNESOWY} |

## Indeksy

{/* Instrukcja: Wymień wszystkie indeksy — klastrowane i nieklastrowane. Jeśli brak poza PK — wpisz: "Brak". */}

| Nazwa indeksu | Kolumny | Unikalny | Cel |
|---|---|---|---|
| {IX_NAZWA_INDEKSU} | {LISTA_KOLUMN} | {tak / nie} | {CEL_INDEKSU} |

## Klucze obce

{/* Instrukcja: Wymień wszystkie FK z tej tabeli do innych tabel. Jeśli brak — wpisz: "Brak". */}

| Kolumny lokalne | Tabela docelowa | Kolumny docelowe | ON DELETE |
|---|---|---|---|
| {NazwaKolumny} | {schema.NazwaTabeliDocelowej} | {NazwaKolumnyDocelowej} | {CASCADE / SET NULL / RESTRICT / NO ACTION} |

## Relacje

{/* Instrukcja: Opisz relacje (1:1, 1:N, N:M) z innymi tabelami. */}

| Relacja | Tabela powiązana | Typ | Opis |
|---|---|---|---|
| {1:N / N:1 / 1:1 / N:M} | {LINK_DO_TABELI_POWIAZANEJ} | {rodzic / dziecko / junction} | {OPIS} |

## Powiązane DTO i LINQ

- Powiązane DTO: {LINKI_DO_DTO}
- Powiązane zapytania LINQ: {LINKI_DO_DOKUMENTOW_LINQ}

## Diagram ER

{/* Instrukcja: Opcjonalny diagram Mermaid erDiagram dla tej tabeli i jej bezpośrednich relacji. Usuń jeśli zbędny. */}

```mermaid
erDiagram
    {NAZWA_TABELI} {
        int {KluczGlowny} PK
        {TYP} {NazwaKolumny}
    }
    {NAZWA_TABELI_POWIAZANEJ} {
        int {KluczGlowny} PK
    }
    {NAZWA_TABELI} ||--o{ {NAZWA_TABELI_POWIAZANEJ} : "{OPIS_RELACJI}"
```

## Powiązania z kodem

- Encja EF Core: {LINK_DO_PLIKU_CS_ENCJI}
- Konfiguracja EF Core (Fluent API): {LINK_DO_PLIKU_CS_KONFIGURACJI}
- Migracja tworząca tabelę: {LINK_DO_PLIKU_MIGRACJI}

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych z kodu lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
