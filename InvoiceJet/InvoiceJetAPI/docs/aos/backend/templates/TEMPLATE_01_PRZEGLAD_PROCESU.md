# [NAZWA PROCESU] — Przegląd procesu

## Cel

[Opis celu procesu.]

## Diagram

```mermaid
flowchart TD
  A["Żądanie HTTP"] --> B["Kontroler"]
  B --> C["Serwis aplikacyjny"]
  C --> D["Repozytoria / IUnitOfWork"]
  D --> E["Odpowiedź API"]
```

## Warunki wejściowe

| Warunek | Źródło |
|---|---|
| [Warunek] | [Kod] |

## Wynik procesu

| Wynik | Opis |
|---|---|
| Sukces | [Opis] |
| Błąd | [Opis] |
