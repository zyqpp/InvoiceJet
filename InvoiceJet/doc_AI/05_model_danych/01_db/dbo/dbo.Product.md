# Tabela `dbo.Product`

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Klasa domenowa | `InvoiceJet.Domain.Models.Product` |

## Kolumny

| Kolumna | Typ SQL | Nullable | PK/FK | Uwagi |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | NOT NULL | **PK** | Autoincrement |
| `Name` | `nvarchar(450)` | NOT NULL | UNIQUE INDEX | Nazwa produktu — 450 znaków (ograniczenie indeksu) |
| `Price` | `decimal(18,2)` | NOT NULL | — | Cena bazowa |
| `ContainsTva` | `bit` | NOT NULL | — | Czy cena zawiera VAT |
| `TvaValue` | `int` | NOT NULL | — | Procent VAT (np. 19) |
| `UnitOfMeasurement` | `nvarchar(max)` | **NULL** | — | Jednostka miary (szt., kg, godz., etc.) |
| `UserFirmId` | `int` | **NULL** | FK → `UserFirm.UserFirmId` | Właściciel — nullable (anomalia) |

## Indeksy

| Indeks | Kolumna | Unikalny |
|---|---|---|
| `IX_Product_Name` | `Name` | **TAK** — globalnie! |
| `IX_Product_UserFirmId` | `UserFirmId` | NIE |

## Relacje

| Kierunek | Relacja | Szczegóły |
|---|---|---|
| `Product` → `UserFirm` | N:0..1 nullable | bez CASCADE |
| `DocumentProduct.ProductId` → `Product` | N:0..1 nullable | bez CASCADE |

## Dane seedowane

Brak.

## Uwagi

- **UNIQUE na `Name` jest globalny** — nie per UserFirm. Oznacza to, że dwóch różnych użytkowników nie może mieć produktu o tej samej nazwie. To prawdopodobnie niezamierzone zachowanie.
- `UserFirmId` nullable — produkt może istnieć bez firmy (logika aplikacji powinna temu zapobiegać, ale brak ograniczenia na DB)
- Produkty tworzone z dokumentów (gdy `DocumentProductRequestDto.Id == 0`) mają tę samą strukturę co produkty katalogowe — brak rozróżnienia
- `DocumentProduct.UnitPrice` i `TotalPrice` przechowują ceny z momentu wystawienia (snapshot) — niezależnie od `Product.Price`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Karta tabeli na podstawie ModelSnapshot. |
