# [NAZWA_SEKCJI] - Diagram sekcji

## 1. Diagram Mermaid

```mermaid
flowchart TD
    MENU["Menu boczne: [Sekcja]"] --> ITEM1["[Pozycja menu 1]"]
    MENU --> ITEM2["[Pozycja menu 2]"]
    ITEM1 --> SCREEN1["[Ekran / route]"]
    ITEM2 --> SCREEN2["[Ekran / route]"]
```

## 2. Tabela linkow

| Element | Typ | Route | Dokument AOS aplikacyjny | Dokument AOS frontendu | Uwagi |
|---|---|---|---|---|---|
| `[Nazwa]` | Sekcja / pozycja / ekran / dialog / podglad | `[route]` / N/D | `[link]` / N/D | `[link]` / N/D | N/D |

## 3. Powiazane przeplywy

| Pozycja menu | Przeplyw aplikacyjny | Proces backend | Dowod |
|---|---|---|---|
| `[Nazwa]` | `[A-XX]` / N/D | `[P-XX]` / N/D | `[link]` |

## 4. Reguly wypelniania

- Diagram Mermaid jest obowiazkowy.
- Tabela linkow Markdown jest obowiazkowa i jest zrodlem nawigacji.
- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Brak potwierdzenia w dokumentacji oznacz `[BRAK POTWIERDZENIA W DOKUMENTACJI]`.
- Szczegolowe markery: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
