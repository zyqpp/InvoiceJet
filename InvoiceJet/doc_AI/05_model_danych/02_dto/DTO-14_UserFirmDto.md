# DTO: UserFirmDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-14 |
| Plik | `InvoiceJet.Application/DTOs/UserFirmDto.cs` |
| Kierunek | Internal / Response |
| Kontekst | Wewnętrzny DTO dla relacji UserFirm |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `Id` | `int` | NIE | ID powiązania UserFirm |
| `UserId` | `int` | NIE | ID użytkownika |
| `FirmId` | `int` | TAK | ID firmy (null jeśli użytkownik nie ma firmy) |
| `Firm` | `FirmRequestDto` | TAK | Dane firmy (zagnieżdżone) |

## Relacja UserFirm

Tabela `UserFirm` jest tabelą pośredniczącą (powiązanie 1:1 User ↔ Firm dla własnej firmy wystawiającego). Przy rejestracji tworzony jest `UserFirm` z `FirmId=null` — użytkownik musi potem dodać firmę przez EKRAN-04.

## Mapowanie AutoMapper

| Kierunek | Profile |
|---|---|
| `UserFirm` → `UserFirmDto` | `UserFirmProfile` |
| `UserFirm` → `FirmRequestDto` (Seller) | `DocumentProfile` → `ForMember Seller MapFrom UserFirm` |

## Anomalie

| # | Anomalia |
|---|---|
| UF-01 | `FirmId` nullable — serwisy mogą rzucić `NullReferenceException` jeśli wywołane gdy użytkownik nie ma firmy |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
