# {TYTUL_ZAPYTANIA} — zapytanie LINQ

| Pole | Wartość |
|---|---|
| ID dokumentu | {LINQ-NAZWA_ZAPYTANIA} |
| Typ dokumentu | linq |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Czym jest to zapytanie z perspektywy biznesowej. Jakie dane pobiera lub jaką operację wykonuje na bazie danych. */}
{OPIS_BIZNESOWY_ZAPYTANIA}

## Charakterystyka zapytania

| Atrybut | Wartość |
|---|---|
| ID zapytania | {LINQ-NAZWA_ZAPYTANIA} |
| Typ operacji | {SELECT / INSERT / UPDATE / DELETE / UPSERT} |
| Tabela główna | {LINK_DO_TABELI_DB} — `{schema.NazwaTabeli}` |
| Tabele dołączone (JOIN) | {LISTA_LINKOW_DO_TABEL_LUB_Brak} |
| Metoda repozytorium | `{NazwaKlasy}.{NazwaMetody}({PARAMETRY})` |
| Plik repozytorium | {LINK_DO_PLIKU_CS} |
| Stronicowanie | {tak / nie} |
| Sortowanie | {KOLUMNA + kierunek / dynamiczne / Brak} |

## Parametry wejściowe

{/* Instrukcja: Wymień parametry przekazywane do metody repozytorium wywołującej to zapytanie. */}

| Parametr | Typ C# | Wymagany | Opis |
|---|---|---|---|
| `{nazwaParametru}` | `{string / int / Guid / bool / DateTime}` | {tak / nie} | {OPIS_PARAMETRU} |

## Kod LINQ

{/* Instrukcja: Wklej fragment LINQ (nie pełną implementację — tylko kluczową część zapytania). */}

```csharp
{FRAGMENT_KODU_LINQ}
```

## Wygenerowane SQL (orientacyjnie)

{/* Instrukcja: Opcjonalnie — wklej SQL generowany przez EF Core dla tego zapytania. Usuń sekcję jeśli zbędna. */}

```sql
{FRAGMENT_SQL}
```

## Wynik zapytania

| Atrybut | Wartość |
|---|---|
| Typ zwracany | `{IQueryable<T> / IEnumerable<T> / T / int / bool}` |
| DTO / encja wynikowa | {LINK_DO_DTO_LUB_ENCJI} |
| Możliwy wynik null | {tak / nie} |

## Powiązania

- Wywoływane z serwisu: {LINK_DO_PLIKU_CS_SERWISU}
- Wywoływane przez endpoint: {LINK_DO_DOKUMENTU_API}
- Tabele bazy danych: {LINKI_DO_TABEL_DB}

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych z kodu lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
