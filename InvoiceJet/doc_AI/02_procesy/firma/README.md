# firma

Procesy techniczne związane z zarządzaniem firmami w systemie InvoiceJet — zarówno własną firmą wystawiającego, jak i firmami klientów.

## Drzewo zawartości

```
firma/
├── README.md                          # ten plik
├── dodaj_firme/
│   └── proces.md                      # PROC-AddFirm — dodawanie firmy (własnej lub klienta)
├── edytuj_firme/
│   └── proces.md                      # PROC-EditFirm — edycja danych firmy
├── pobierz_aktywna_firme/
│   └── proces.md                      # PROC-GetUserActiveFirm — pobranie własnej firmy
├── pobierz_firmy_klientow/
│   └── proces.md                      # PROC-GetUserClientFirms — lista firm klientów
├── usun_firme/
│   └── proces.md                      # PROC-DeleteFirms — usunięcie firmy klienta
└── pobierz_z_anaf/
    └── proces.md                      # PROC-GetFirmFromAnaf — autouzupełnienie z ANAF API
```

## Kluczowe dokumenty

- `dodaj_firme/proces.md` — POST /api/Firm/AddFirm/{isClient}
- `edytuj_firme/proces.md` — PUT /api/Firm/EditFirm/{isClient}
- `pobierz_z_anaf/proces.md` — GET /api/Firm/fromAnaf/{cui} (integracja z rumuńskim ANAF)

## Powiązane katalogi

- `../../04_api_i_integracje/01_api_frontend/firm/` — dokumentacja endpointów API firmy
- `../../04_api_i_integracje/02_systemy_dziedzinowe/anaf/` — dokumentacja integracji ANAF
- `../../01_ekrany/firma/` — ekrany zarządzania firmą
- `../../03_algorytmy/dedykowane/integracja_anaf.md` — algorytm integracji z ANAF

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — struktura podfolderów firmy (z P-03 i P-04). |
