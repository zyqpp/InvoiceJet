# [A-XX_NAZWA] - Gridy, listy i zapytania

## 1. Źródła list i gridów

| Widok/lista | Źródło UI | Endpoint | DTO odpowiedźi | Backend | Encje | Tabele | Filtry/sortowanie | Dowód |
|---|---|---|---|---|---|---|---|---|
| `[Nazwa widoku]` | `[DataSource / kolekcja / serwis]` / N/D | `[HTTP] /api/[path]` / N/D | `[Dto]` / N/D | `[Service.Method]` / N/D | `[Entity]` / N/D | `[Table]` / N/D | `[Filtry, sortowanie, paginacja]` / N/D | `[link]` |

## 2. Kolumny widoku

| Kolumna | Pole UI / model TS | DTO odpowiedźi | Encja | Tabela.kolumna | Dowód |
|---|---|---|---|---|---|
| `[Kolumna]` | `[property]` / N/D | `[Dto.Property]` / N/D | `[Entity]` / N/D | `[Table.Column]` / N/D | `[link]` |

## 3. Filtry, sortowanie i paginacja

| Mechanizm | Warstwa | Opis | Backend / DB | Dowód |
|---|---|---|---|---|
| Filtr | UI/API/DB | `[Opis]` / N/D | `[Service / Table]` / N/D | `[link]` |
| Sortowanie | UI/API/DB | `[Opis]` / N/D | `[Service / Table]` / N/D | `[link]` |
| Paginacja | UI/API/DB | `[Opis]` / N/D | `[Service / Table]` / N/D | `[link]` |

## 4. Reguły wypełniania

- Jeżeli przepływ nie ma gridu ani listy, wpisz: `> Sekcja nie dotyczy tego przepływu. [powod]`.
- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Brak mapowańia do tabel oznacz `[BRAK MAPOWANIA DO BAZY]`.
- Szczegółowe markery: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
