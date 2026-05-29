# [A-XX_NAZWA] - Przeglad end-to-end

## 1. Cel przeplywu

[Opis celu z perspektywy uzytkownika. Jeden akapit. Bez zgadywania logiki, ktora nie wynika z dokumentacji.]

## 2. Diagram end-to-end

```mermaid
flowchart LR
    UI["Ekran / makieta E-XX"] --> FS["Serwis frontendu"]
    FS --> API["Endpoint API"]
    API --> BS["Serwis backendowy"]
    BS --> DB["Encja / tabela"]
```

## 3. Warunki wejscia

| Warunek | Warstwa | Dowod | Uwagi |
|---|---|---|---|
| `[Warunek]` | UI/API/DB | `[link]` | N/D |

## 4. Wynik przeplywu

| Obszar | Wynik | Dowod |
|---|---|---|
| UI | `[Komunikat, nawigacja, odswiezenie widoku]` / N/D | `[link]` |
| API | `[Status HTTP / DTO odpowiedzi]` / N/D | `[link]` |
| Backend | `[Operacja serwisu]` / N/D | `[link]` |
| Baza | `[Tabela.kolumna / rekord]` / N/D | `[link]` |

## 5. Zakres i wykluczenia

| Element | Status | Uzasadnienie |
|---|---|---|
| `[Element]` | W zakresie / Poza zakresem / N/D | `[Dowod lub marker]` |

## 6. Reguly wypelniania

- Brak danych zapisuj jako `N/D`.
- Informacje niepotwierdzone oznaczaj `[WYMAGA WERYFIKACJI]`.
- Gdy slad UI do bazy urywa sie przed baza, oznacz `[BRAK MAPOWANIA DO BAZY]`.
- Szczegolowe markery: [05_MARKERY_I_JAKOSC.md](../../../FullStackAgentAI/05_MARKERY_I_JAKOSC.md).
