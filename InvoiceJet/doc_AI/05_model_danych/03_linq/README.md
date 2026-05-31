# 03_linq — Zapytania LINQ / EF Core

Dokumentacja zapytań LINQ realizowanych przez EF Core 8 w projekcie InvoiceJet. Każdy dokument opisuje jedno zapytanie: cel biznesowy, kod LINQ (szacowany lub zweryfikowany), includowane tabele, warunki filtrowania oraz zidentyfikowane anomalie. Projekt InvoiceJet korzysta wyłącznie z EF Core 8 — brak zapytań SQL pisanych ręcznie.

## Drzewo zawartości

```
03_linq/
├── README.md                                  — ten plik
├── LINQ-01_GetDocumentById.md                 — pełny dokument z pozycjami (do edycji)
├── LINQ-02_GetTableRecords.md                 — lista dokumentów widoku tabelarycznego
├── LINQ-03_GetDashboardStats.md               — agregacja statystyk dashboardu
├── LINQ-04_GetUserActiveFirm.md               — pobieranie własnej firmy użytkownika
└── LINQ-05_GetUserClientFirms.md              — lista klientów zalogowanego użytkownika
```

## Kluczowe dokumenty

| Dokument | Opis |
|---|---|
| [LINQ-01_GetDocumentById.md](LINQ-01_GetDocumentById.md) | Najbardziej złożone zapytanie — 6 poziomów Include/ThenInclude |
| [LINQ-03_GetDashboardStats.md](LINQ-03_GetDashboardStats.md) | Agregacja danych — GroupBy, Sum, Count |

## Konwencje nazewnicze

Pliki nazwane `LINQ-XX_NazwaMetody.md` gdzie XX to numer porządkowy (01..05). Nazwy metod cytowane 1:1 z kodu C#.

## Powiązane katalogi

| Katalog | Powiązanie |
|---|---|
| [01_db/](../01_db/) | Tabele DB operowane przez zapytania LINQ |
| [02_dto/](../02_dto/) | DTO będące wynikiem mapowania po wykonaniu zapytania |
| [05_automapper/](../05_automapper/) | Profile AutoMapper — mapowanie encji na DTO po zapytaniu |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — reorganizacja z 02_linq/. |
