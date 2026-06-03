# 02_systemy_dziedzinowe — Integracje z systemami zewnętrznymi

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| Autor | Agent Claudiusz Sonte 4.6 max |
| Wersja | 1.0 |
| Data | 2026-05-31 |
| Status | Obowiązujący |
| Liczba integracji | 1 |

## Opis biznesowy

Dokumentacja integracji InvoiceJet z zewnętrznymi systemami dziedzinowymi. Aplikacja integruje się z publicznym API rumuńskiego urzędu skarbowego (ANAF) w celu autouzupełnienia danych firmy na podstawie numeru CUI (odpowiednik NIP).

## Drzewo zawartości

```
02_systemy_dziedzinowe/
├── README.md                          ← ten plik
└── anaf/                              ← integracja z ANAF (rumuński urząd skarbowy)
    └── pobierz_dane_firmy.md          ← GET CUI lookup — autouzupełnienie danych firmy
```

## Podkatalogi

| Katalog | System zewnętrzny | Opis | Liczba dokumentów |
|---|---|---|---|
| `anaf/` | ANAF — Agenția Națională de Administrare Fiscală | Pobieranie danych firmy rumuńskiej na podstawie numeru CUI | 1 |

## Kluczowe dokumenty

- [`anaf/pobierz_dane_firmy.md`](anaf/pobierz_dane_firmy.md) — opis integracji z ANAF API v8, format żądania/odpowiedzi, mapowanie pól na `FirmRequestDto`, anomalie.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
