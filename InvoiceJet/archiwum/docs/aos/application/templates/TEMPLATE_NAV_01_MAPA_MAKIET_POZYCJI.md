# [NAZWA_POZYCJI_MENU] - Mapa makiet pozycji

## 1. Diagram Mermaid

```mermaid
flowchart TD
    ITEM["Menu: [Pozycja]"] --> LIST["Ekran listy / główny widok"]
    LIST --> ADD["Dodanie"]
    LIST --> EDIT["Edycja"]
    LIST --> DETAILS["Szczegóły / podgląd"]
    LIST --> DIALOG["Dialog / akcja pomocnicza"]
```

## 2. Tabela makiet

| Element | Typ | Route / wyzwalacz | Dokument AOS aplikacyjny | Dokument AOS frontendu | Dowód |
|---|---|---|---|---|---|
| `[Nazwa elementu]` | Ekran / dialog / podgląd / akcja | `[route lub klik]` / N/D | `[link]` / N/D | `[link]` / N/D | `[link]` |

## 3. Przejscia i akcje

| Z elementu | Do elementu | Wyzwalacz | Efekt | Dowód |
|---|---|---|---|---|
| `[Element A]` | `[Element B]` | `[Przycisk / route / akcja]` | `[Opis]` / N/D | `[link]` |

## 4. Reguły wypełniania

- Diagram Mermaid jest obowiązkowy.
- Tabela makiet Markdown jest obowiązkowa.
- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Brak potwierdzenia w dokumentacji oznacz `[BRAK POTWIERDZENIA W DOKUMENTACJI]`.
- Szczegółowe markery: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
