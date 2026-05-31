# 04_zapytania_bezposrednie — Zapytania SQL bezpośrednie

Katalog dla zapytań bezpośrednich SQL (poza LINQ/EF Core). W projekcie InvoiceJet nie zidentyfikowano zapytań bezpośrednich — całość warstwy danych opiera się na EF Core 8 i LINQ.

## Status

**Brak zawartości** — projekt InvoiceJet nie stosuje zapytań SQL pisanych ręcznie (`FromSqlRaw`, `FromSqlInterpolated`, `ExecuteSqlRaw` ani ADO.NET). Cała warstwa dostępu do danych przechodzi przez EF Core 8 z LINQ.

Gdyby w przyszłości pojawiły się zapytania bezpośrednie, należy je dokumentować plikami `SQL-XX_NazwaZapytania.md` wg wzoru analogicznego do LINQ-XX.

## Powiązane katalogi

| Katalog | Powiązanie |
|---|---|
| [03_linq/](../03_linq/) | Zapytania LINQ/EF Core — aktualna warstwa danych projektu |
| [01_db/](../01_db/) | Schemat DB — tabele i relacje |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — katalog pusty (brak zapytań bezpośrednich). |
