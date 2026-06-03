# wyliczeniowe — Algorytmy wyliczeniowe

Algorytmy odpowiedzialne za obliczenia finansowe i matematyczne na danych biznesowych dokumentów.

## Zawartość

| Plik | Opis |
|---|---|
| [obliczanie_ceny_pozycji.md](obliczanie_ceny_pozycji.md) | Cena brutto wiersza `UnitPrice × Qty × (1+VAT/100)` — **tylko frontend**; backend akceptuje wartość z DTO bez przeliczenia |
| [obliczanie_wartosci_dokumentu.md](obliczanie_wartosci_dokumentu.md) | Sumy dokumentu: netto (backend oblicza) i brutto (backend sumuje z DTO) |
| [aktualizacja_produktow_dokumentu.md](aktualizacja_produktow_dokumentu.md) | `UpdateDocumentProducts` — pełna podmiana pozycji, akumulacja sum, zapis snapshotów cen |

## Powiązane katalogi

- [`../../02_procesy/dokumenty/dodaj_dokument/`](../../02_procesy/dokumenty/dodaj_dokument/) — proces dodawania dokumentu
- [`../../05_model_danych/01_db/dbo/`](../../05_model_danych/01_db/dbo/) — encje Document i DocumentProduct

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
