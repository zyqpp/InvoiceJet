# [A-XX_NAZWA] - Mapa pol UI do danych

## 1. Pola formularzy i elementy makiety

| Element makiety | Frontend | Model TS | Endpoint | DTO | Backend | Encja | Tabela.kolumna | Dowod | Uwagi |
|---|---|---|---|---|---|---|---|---|---|
| `[Nazwa pola]` | `formControlName="[nazwa]"` / N/D | `[Model TS]` / N/D | `[HTTP] /api/[path]` / N/D | `[Dto.Property]` / N/D | `[Service.Method]` / N/D | `[Entity]` / N/D | `[Table.Column]` / N/D | `[link]` | N/D |

## 2. Kolumny list i gridow

| Element makiety | Frontend | Model TS | Endpoint | DTO | Backend | Encja | Tabela.kolumna | Dowod | Uwagi |
|---|---|---|---|---|---|---|---|---|---|
| `[Kolumna]` | `[matColumnDef / pole modelu]` / N/D | `[Model TS]` / N/D | `[HTTP] /api/[path]` / N/D | `[Dto.Property]` / N/D | `[Service.Method]` / N/D | `[Entity]` / N/D | `[Table.Column]` / N/D | `[link]` | N/D |

## 3. Dane pomocnicze i slowniki

| Dane | Zrodlo UI | Endpoint | DTO odpowiedzi | Backend | Encja | Tabela.kolumna | Dowod |
|---|---|---|---|---|---|---|---|
| `[Slownik / lista]` | `[Komponent / serwis]` / N/D | `[HTTP] /api/[path]` / N/D | `[Dto]` / N/D | `[Service.Method]` / N/D | `[Entity]` / N/D | `[Table.Column]` / N/D | `[link]` |

## 4. Reguly wypelniania

- Kazdy wiersz musi miec dowod w dokumentacji front/back/app.
- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Gdy brak potwierdzenia w dokumentacji zrodlowej, uzyj `[BRAK POTWIERDZENIA W DOKUMENTACJI]`.
- Gdy pole nie ma mapowania do bazy, uzyj `[BRAK MAPOWANIA DO BAZY]`.
- Szczegolowe markery: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
