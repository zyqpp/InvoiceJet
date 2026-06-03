# 05_automapper — Profile AutoMapper

Dokumentacja profili AutoMapper projektu InvoiceJet. AutoMapper (wersja 12+) realizuje mapowania między encjami EF Core a obiektami DTO. Projekt zawiera 7 profili grupujących mapowania wg domeny biznesowej. Profile są rejestrowane w `Program.cs` przez `AddAutoMapper(assembly)`.

## Drzewo zawartości

```
05_automapper/
├── README.md                          — ten plik
├── AM-01_AuthProfile.md               — profil autentykacji (RegisterUserDto → User)
├── AM-02_FirmProfile.md               — profil firmy (FirmRequestDto ↔ Firm)
├── AM-03_BankAccountProfile.md        — profil konta bankowego (BankAccountRequestDto ↔ BankAccount)
├── AM-04_ProductProfile.md            — profil produktu (ProductRequestDto ↔ Product)
├── AM-05_DocumentSeriesProfile.md     — profil serii dokumentów (DocumentSeriesRequestDto ↔ DocumentSeries)
├── AM-06_DocumentProfile.md           — profil dokumentu (złożony — LINQ inline, aliasy)
└── AM-07_UserFirmProfile.md           — profil UserFirm (UserFirm → FirmRequestDto dla Seller)
```

## Kluczowe dokumenty

| Dokument | Opis |
|---|---|
| [AM-06_DocumentProfile.md](AM-06_DocumentProfile.md) | Najbardziej złożony profil — LINQ projekcja inline, aliasy kolumn |
| [AM-07_UserFirmProfile.md](AM-07_UserFirmProfile.md) | Mapowanie UserFirm → FirmRequestDto (Seller w dokumencie) |

## Konwencje nazewnicze

Pliki nazwane `AM-XX_NazwaProfilu.md` gdzie XX to numer porządkowy (01..07). Nazwy klas profili cytowane 1:1 z kodu C#.

## Powiązane katalogi

| Katalog | Powiązanie |
|---|---|
| [01_db/](../01_db/) | Encje EF Core — źródła i cele mapowań |
| [02_dto/](../02_dto/) | DTO — cel lub źródło mapowań AutoMapper |
| [03_linq/](../03_linq/) | Zapytania LINQ — poprzedzają mapowanie (Include wymagane przez profile) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — reorganizacja z 04_automapper/. |
