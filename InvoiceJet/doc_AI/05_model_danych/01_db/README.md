# 01_db — Baza danych

Dokumentacja schematu bazy danych SQL Server projektu InvoiceJet. Zawiera ERD globalny i opis 10 tabel schematu dbo. Sekcja stanowi źródło prawdy o strukturze warstwy persystencji — relacjach między tabelami, kluczach głównych i obcych oraz ograniczeniach DB.

## Drzewo zawartości

```
01_db/
├── README.md                          — ten plik
├── erd_globalny.md                    — diagram ERD obejmujący cały schemat dbo
├── spis_schem_i_tabel.md              — lista wszystkich schematów i tabel z opisem
└── dbo/
    ├── erd_dbo.md                     — ERD dla schematu dbo (Mermaid erDiagram)
    ├── dbo.User.md                    — tabela użytkowników systemu
    ├── dbo.Firm.md                    — tabela firm (własnych i klientów)
    ├── dbo.UserFirm.md                — tabela powiązania użytkownik–firma (wystawiający)
    ├── dbo.UserFirm_relations.md      — opis relacji UserFirm z klientami (M:N)
    ├── dbo.BankAccount.md             — tabela kont bankowych firmy
    ├── dbo.Product.md                 — tabela produktów i usług z katalogu
    ├── dbo.DocumentType.md            — tabela typów dokumentów (słownik)
    ├── dbo.DocumentSeries.md          — tabela serii numeracji dokumentów
    ├── dbo.Document.md                — tabela dokumentów (faktury, proformy, storna)
    ├── dbo.DocumentProduct.md         — tabela pozycji dokumentu (junction)
    └── dbo.DocumentStatus.md          — tabela statusów dokumentów (słownik)
```

## Kluczowe dokumenty

| Dokument | Opis |
|---|---|
| [ERD globalny](erd_globalny.md) | Diagram ERD całego schematu dbo w formacie Mermaid |
| [ERD schematu dbo](dbo/erd_dbo.md) | Skrócony ERD z kluczowymi relacjami FK |
| [Spis schematów i tabel](spis_schem_i_tabel.md) | Tabela wszystkich obiektów DB z opisem |
| [dbo.Document](dbo/dbo.Document.md) | Centralna tabela — dokumenty finansowe |
| [dbo.UserFirm](dbo/dbo.UserFirm.md) | Kluczowe powiązanie — izolacja danych wielofirmowych |

## Konwencje nazewnicze

Tabele i kolumny nazwane w stylu PascalCase zgodnym z konwencją EF Core. Pliki dokumentacji tabel nazwane `dbo.NazwaTabeli.md`.

## Powiązane katalogi

| Katalog | Powiązanie |
|---|---|
| [02_dto/](../02_dto/) | DTO mapowane z/do encji EF Core odpowiadających tabelom |
| [03_linq/](../03_linq/) | Zapytania LINQ operujące na tabelach tego schematu |
| [05_automapper/](../05_automapper/) | Profile AutoMapper — mapowania encja ↔ DTO |
| [06_skrypty/](../06_skrypty/) | Skrypt inicjalizacyjny (DbSeeder) wypełniający tabele słownikowe |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
