# serie_dokumentow — Zarządzanie seriami numeracji dokumentów

Ekran i modal zarządzania seriami numeracji dokumentów. Serie definiują format numeru dokumentu (prefiks + licznik). Każdy typ dokumentu (faktura, proforma, storno) może mieć odrębne serie. Chroniony przez AuthGuard.

## Drzewo zawartości

```
serie_dokumentow/
├── README.md                        ← Ten plik
├── ekran.md                         ← DocumentSeriesComponent — lista serii
└── dialog_dodaj_serie/
    └── modal.md                     ← AddOrEditDocumentSeriesDialogComponent — dodaj/edytuj serię
```

## Kluczowe dokumenty

- `ekran.md` — lista serii: tabela, CRUD, wywołania API, anomalie (console.log, podwójne clear)
- `dialog_dodaj_serie/modal.md` — modal formularza serii; format numeru: `SeriesName + CurrentNumber.ToString("D4")`; anomalia race condition

## Powiązane katalogi

- `../dashboard/` — ekran startowy (sidebar: Serie dokumentów)
- `../faktury/dodaj_edytuj_fakture/` — serie wybierane w formularzu dokumentu

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
