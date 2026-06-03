# 06_skrypty — Skrypty inicjalizacyjne i seedery

Katalog dokumentacji skryptów inicjalizacyjnych bazy danych projektu InvoiceJet. Zawiera opis mechanizmu seedowania danych słownikowych (`DbSeeder`) wywoływanego przy starcie aplikacji. Projekt nie zawiera migracji ręcznych SQL — schemat DB zarządzany jest przez EF Core Migrations.

## Drzewo zawartości

```
06_skrypty/
├── README.md                          — ten plik
└── DbSeeder.md                        — opis komponentu DbSeeder (inicjalizacja danych słownikowych)
```

## Kluczowe dokumenty

| Dokument | Opis |
|---|---|
| [DbSeeder.md](DbSeeder.md) | Inicjalizacja tabel `DocumentType` i `DocumentStatus` przy starcie aplikacji |

## Zakres skryptów

Projekt InvoiceJet stosuje wyłącznie:
1. **EF Core Migrations** — zarządzanie schematem DB (tworzenie/modyfikacja tabel)
2. **DbSeeder** — wypełnienie tabel słownikowych danymi inicjalnymi przy starcie

Brak ręcznych skryptów SQL DDL/DML poza powyższymi mechanizmami.

## Powiązane katalogi

| Katalog | Powiązanie |
|---|---|
| [01_db/](../01_db/) | Schemat DB — tabele seedowane przez DbSeeder (`DocumentType`, `DocumentStatus`) |
| [04_zapytania_bezposrednie/](../04_zapytania_bezposrednie/) | Brak zapytań bezpośrednich — wszystko przez EF Core |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
