# [A-XX_NAZWA] - Mapa pól UI do danych

## 1. Pola formularzy i elementy makiety

| Element makiety | Frontend | Model TS | Endpoint | DTO | Backend | Encja | Tabela.kolumna | Dowód | Uwagi |
|---|---|---|---|---|---|---|---|---|---|
| `[Nazwa pola]` | `formControlName="[nazwa]"` / N/D | `[Model TS]` / N/D | `[HTTP] /api/[path]` / N/D | `[Dto.Property]` / N/D | `[Service.Method]` / N/D | `[Entity]` / N/D | `[Table.Column]` / N/D | `[link]` | N/D |

## 2. Kolumny list i gridów

| Element makiety | Frontend | Model TS | Endpoint | DTO | Backend | Encja | Tabela.kolumna | Dowód | Uwagi |
|---|---|---|---|---|---|---|---|---|---|
| `[Kolumna]` | `[matColumnDef / pole modelu]` / N/D | `[Model TS]` / N/D | `[HTTP] /api/[path]` / N/D | `[Dto.Property]` / N/D | `[Service.Method]` / N/D | `[Entity]` / N/D | `[Table.Column]` / N/D | `[link]` | N/D |

## 3. Dane pomocnicze i slowniki

| Dane | Źródło UI | Endpoint | DTO odpowiedźi | Backend | Encja | Tabela.kolumna | Dowód |
|---|---|---|---|---|---|---|---|
| `[Slownik / lista]` | `[Komponent / serwis]` / N/D | `[HTTP] /api/[path]` / N/D | `[Dto]` / N/D | `[Service.Method]` / N/D | `[Entity]` / N/D | `[Table.Column]` / N/D | `[link]` |

## 4. Reguły wypełniania

- Każdy wiersz musi mieć dowód w dokumentacji front/back/app.
- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Gdy brak potwierdzenia w dokumentacji źródłowej, użyj `[BRAK POTWIERDZENIA W DOKUMENTACJI]`.
- Gdy pole nie ma mapowańia do bazy, użyj `[BRAK MAPOWANIA DO BAZY]`.
- Szczegółowe markery: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
