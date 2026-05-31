# Tabela `dbo.DocumentProduct`

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Klasa domenowa | `InvoiceJet.Domain.Models.DocumentProduct` |

## Kolumny

| Kolumna | Typ SQL | Nullable | PK/FK | Uwagi |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | NOT NULL | **PK** | Autoincrement |
| `Quantity` | `decimal(18,2)` | NOT NULL | — | Ilość (decimal — obsługa ułamkowych) |
| `UnitPrice` | `decimal(18,2)` | NOT NULL | — | Cena jednostkowa z momentu wystawienia (snapshot) |
| `TotalPrice` | `decimal(18,2)` | NOT NULL | — | Cena całkowita pozycji (z VAT lub bez) |
| `DocumentId` | `int` | **NULL** | FK → `Document.Id` | Powiązany dokument |
| `ProductId` | `int` | **NULL** | FK → `Product.Id` | Powiązany produkt |

## Indeksy

| Indeks | Kolumna | Unikalny |
|---|---|---|
| `IX_DocumentProduct_DocumentId` | `DocumentId` | NIE |
| `IX_DocumentProduct_ProductId` | `ProductId` | NIE |

## Relacje

| Kierunek | Relacja | Szczegóły |
|---|---|---|
| `DocumentProduct` → `Document` | N:0..1 nullable | bez CASCADE |
| `DocumentProduct` → `Product` | N:0..1 nullable | bez CASCADE |

## Dane seedowane

Brak.

## Uwagi

- `DocumentId` nullable — pozycja może teoretycznie istnieć bez dokumentu (anomalia)
- `ProductId` nullable — pozycja może istnieć bez produktu (jeśli produkt zostanie usunięty — brak CASCADE)
- `UnitPrice` i `TotalPrice` przechowują **ceny z momentu wystawienia** (snapshot) — niezależne od `Product.Price`; zmiana ceny produktu nie wpływa na istniejące dokumenty
- `Quantity` jako `decimal` (nie `int`) — obsługuje ułamkowe ilości
- `UpdateDocumentProducts()` przy edycji dokumentu: **usuwa WSZYSTKIE** poprzednie pozycje i dodaje nowe — brak soft-update
- Usunięcie `DocumentProduct` — w `DeleteDocuments()`: `RemoveRangeAsync(DocumentProducts)` przed usunięciem dokumentów

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Karta tabeli na podstawie ModelSnapshot. |
