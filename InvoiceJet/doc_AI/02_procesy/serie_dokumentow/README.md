# serie_dokumentow

Procesy techniczne związane z zarządzaniem seriami numeracji dokumentów w systemie InvoiceJet.

## Drzewo zawartości

```
serie_dokumentow/
├── README.md                    # ten plik
├── pobierz_serie/
│   └── proces.md                # PROC-GetAllDocumentSeries — lista serii dokumentów
├── dodaj_serie/
│   └── proces.md                # PROC-AddDocumentSeries — dodanie nowej serii
├── edytuj_serie/
│   └── proces.md                # PROC-UpdateDocumentSeries — edycja serii
└── usun_serie/
    └── proces.md                # PROC-DeleteDocumentSeries — usunięcie serii
```

## Kluczowe dokumenty

- `dodaj_serie/proces.md` — POST /api/DocumentSeries/Add
- `edytuj_serie/proces.md` — PUT /api/DocumentSeries/Update (uwaga: nazwa endpointu `Update`, nie `Edit`)

## Powiązane katalogi

- `../../04_api_i_integracje/01_api_frontend/document_series/` — dokumentacja endpointów API serii
- `../../01_ekrany/serie_dokumentow/` — ekran zarządzania seriami
- `../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md` — algorytm generowania numeru dokumentu
- `../../05_model_danych/01_db/dbo/dbo.DocumentSeries.md` — tabela DocumentSeries

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — struktura podfolderów serie_dokumentow (z P-07). |
