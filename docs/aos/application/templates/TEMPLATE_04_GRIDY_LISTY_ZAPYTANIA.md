# [A-XX_NAZWA] - Gridy, listy i zapytania

## 1. Zrodla list i gridow

| Widok/lista | Zrodlo UI | Endpoint | DTO odpowiedzi | Backend | Encje | Tabele | Filtry/sortowanie | Dowod |
|---|---|---|---|---|---|---|---|---|
| `[Nazwa widoku]` | `[DataSource / kolekcja / serwis]` / N/D | `[HTTP] /api/[path]` / N/D | `[Dto]` / N/D | `[Service.Method]` / N/D | `[Entity]` / N/D | `[Table]` / N/D | `[Filtry, sortowanie, paginacja]` / N/D | `[link]` |

## 2. Kolumny widoku

| Kolumna | Pole UI / model TS | DTO odpowiedzi | Encja | Tabela.kolumna | Dowod |
|---|---|---|---|---|---|
| `[Kolumna]` | `[property]` / N/D | `[Dto.Property]` / N/D | `[Entity]` / N/D | `[Table.Column]` / N/D | `[link]` |

## 3. Filtry, sortowanie i paginacja

| Mechanizm | Warstwa | Opis | Backend / DB | Dowod |
|---|---|---|---|---|
| Filtr | UI/API/DB | `[Opis]` / N/D | `[Service / Table]` / N/D | `[link]` |
| Sortowanie | UI/API/DB | `[Opis]` / N/D | `[Service / Table]` / N/D | `[link]` |
| Paginacja | UI/API/DB | `[Opis]` / N/D | `[Service / Table]` / N/D | `[link]` |

## 4. Reguly wypelniania

- Jezeli przeplyw nie ma gridu ani listy, wpisz: `> Sekcja nie dotyczy tego przeplywu. [powod]`.
- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Brak mapowania do tabel oznacz `[BRAK MAPOWANIA DO BAZY]`.
- Szczegolowe markery: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
