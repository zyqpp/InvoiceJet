# dashboard — Ekran startowy

Ekran startowy aplikacji InvoiceJet wyświetlany bezpośrednio po zalogowaniu. Prezentuje kluczowe statystyki firmy (liczniki dokumentów, klientów, produktów, kont bankowych) oraz wykres liniowy miesięcznych przychodów. Chroniony przez AuthGuard.

## Drzewo zawartości

```
dashboard/
├── README.md    ← Ten plik
└── ekran.md     ← DashboardComponent — statystyki i wykres przychodów
```

## Kluczowe dokumenty

- `ekran.md` — pełna dokumentacja ekranu dashboardu: elementy UI, selektory, wywołania API, anomalie

## Powiązane katalogi

- `../login/` — poprzedni ekran (po logowaniu → dashboard)
- `../register/` — poprzedni ekran (po rejestracji → dashboard)
- `../faktury/` — sekcja faktur dostępna przez sidebar

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
