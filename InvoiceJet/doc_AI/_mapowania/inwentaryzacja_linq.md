# Inwentaryzacja LINQ — zapytania do bazy danych

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Źródło | `InvoiceJetAPI/InvoiceJet.Infrastructure/Persistence/Repositories/` |

## Lista zapytań LINQ (5)

| ID | Metoda serwisu | Endpoint | Cel | Dokument | Status |
|---|---|---|---|---|---|
| LINQ-01 | `DocumentService.GetDocumentById()` | `GET /api/Document/GetDocumentById/{id}` | Pobranie pełnego dokumentu z zagnieżdżonymi danymi (Include: Client, BankAccount, DocumentSeries, DocumentProducts, DocumentType, DocumentStatus) | [link](../05_model_danych/03_linq/LINQ-01_GetDocumentById.md) | szkic |
| LINQ-02 | `DocumentService.GetDocumentTableRecords()` | `GET /api/Document/GetTableRecords/{documentTypeId}` | Pobranie listy dokumentów w formacie tabelarycznym — tylko wybrane kolumny bez zagnieżdżeń | [link](../05_model_danych/03_linq/LINQ-02_GetTableRecords.md) | szkic |
| LINQ-03 | `DocumentService.GetDashboardStats()` | `GET /api/Document/GetDashboardStats/{year}/{documentType}` | Agregowanie danych statystycznych dla dashboardu — liczniki i miesięczne sumy | [link](../05_model_danych/03_linq/LINQ-03_GetDashboardStats.md) | szkic |
| LINQ-04 | `FirmService.GetUserActiveFirm()` | `GET /api/Firm/GetUserActiveFirm` | Pobranie danych własnej firmy wystawiającego — wywoływane przy ładowaniu ekranu danych firmy | [link](../05_model_danych/03_linq/LINQ-04_GetUserActiveFirm.md) | szkic |
| LINQ-05 | `FirmService.GetUserClientFirms()` | `GET /api/Firm/GetUserClientFirms` | Pobranie listy firm klientów zalogowanego użytkownika (relacja M:N przez UserFirm) | [link](../05_model_danych/03_linq/LINQ-05_GetUserClientFirms.md) | szkic |

## Charakterystyka zapytań

| Cecha | Opis |
|---|---|
| ORM | EF Core 8 (Code First) |
| Wzorzec | Repository + Unit of Work |
| Izolacja danych | Wszystkie zapytania filtrują przez `UserFirmId` pobranego z JWT |
| Eager loading | Include() stosowany w LINQ-01 (pełny dokument) |
| Projekcja | Select() do DTO w LINQ-02, LINQ-03 |
| Brak N+1 | Tak — dane zagnieżdżone ładowane w jednym zapytaniu |

## Uwagi

- Projekt **nie używa zapytań bezpośrednich** (raw SQL, stored procedures, views)
- `04_zapytania_bezposrednie/` jest celowo pusty
- Zapytania LINQ są hermetyczne w repozytoriach, serwisy je wywołują przez interfejsy
- Anomalia: LINQ-05 filtruje klientów przez UserFirm — ale relacja jest niejednoznaczna (patrz [dbo.UserFirm relations](../05_model_danych/01_db/dbo/dbo.UserFirm_relations.md))

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — uzupełnienie brakującego inwentarza M-01. |
