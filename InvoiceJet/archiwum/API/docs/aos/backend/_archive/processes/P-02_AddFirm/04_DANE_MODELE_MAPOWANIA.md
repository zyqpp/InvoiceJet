# Dodanie firmy — Dane, modele i mapowania

## DTO żądania

| DTO | Rola |
|---|---|
| `FirmDto` | Body żądania i odpowiedź API po zapisie firmy. |

---

## Pola `FirmDto`

| Pole DTO | Typ | Encja / pole docelowe |
|---|---|---|
| `Id` | `int` | `Firm.Id` |
| `Name` | `string` | `Firm.Name` |
| `Cui` | `string` | `Firm.Cui` |
| `RegCom` | `string?` | `Firm.RegCom` |
| `Address` | `string` | `Firm.Address` |
| `County` | `string` | `Firm.County` |
| `City` | `string` | `Firm.City` |

---

## Encje zapisywane lub aktualizowane

| Encja | Operacja | Źródło danych |
|---|---|---|
| `Firm` | Dodanie | `FirmDto` przez `AutoMapper` |
| `UserFirm` | Dodanie lub aktualizacja `IsClient` | `firm.Id`, `currentUserId`, parametr `isClient` |
| `User` | Aktualizacja `ActiveUserFirm`, gdy jest `null` | `Users.GetUserByIdAsync(...)` |
| `DocumentSeries` | Dodanie serii początkowych dla pierwszej aktywnej firmy | `DocumentSeriesService.AddInitialDocumentSeries(newUserFirm)` |

---

## Mapowanie

| Źródło | Cel | Profil |
|---|---|---|
| `FirmDto` | `Firm` | `FirmProfile` |
| `Firm` | `FirmDto` | `FirmProfile` |

`FirmProfile` definiuje:

```csharp
CreateMap<Firm, FirmDto>().ReverseMap();
```

---

## Relacje danych

| Relacja | Opis |
|---|---|
| `UserFirm.UserId` | Wskazuje zalogowanego użytkownika. |
| `UserFirm.FirmId` | Wskazuje nowo utworzoną firmę. |
| `UserFirm.IsClient` | Przyjmuje wartość parametru trasy `isClient`. |
| `User.ActiveUserFirm` | Ustawiane na nową relację, jeżeli użytkownik nie ma aktywnej firmy. |
| `DocumentSeries.UserFirm` | Serie początkowe są przypisane do nowej relacji `UserFirm`. |

---

## Serie początkowe

| Typ dokumentu | Źródło typu | Wartości początkowe |
|---|---|---|
| `Factura` | `DocumentTypes.Query().Where(d => d.Name.Equals("Factura"))` | `SeriesName = bieżący rok`, `FirstNumber = 1`, `CurrentNumber = 1`, `IsDefault = true` |
| `Factura Storno` | `DocumentTypes.Query().Where(d => d.Name.Equals("Factura Storno"))` | `SeriesName = bieżący rok`, `FirstNumber = 1`, `CurrentNumber = 1`, `IsDefault = true` |
| `Factura Proforma` | `DocumentTypes.Query().Where(d => d.Name.Equals("Factura Proforma"))` | `SeriesName = bieżący rok`, `FirstNumber = 1`, `CurrentNumber = 1`, `IsDefault = true` |

---

## Dane bez walidacji atrybutami

`FirmDto` nie zawiera atrybutów `Required`, `StringLength`, `RegularExpression` ani innych walidatorów `DataAnnotations`.

[UWAGA: walidacja kompletności i formatu danych firmy nie jest widoczna w DTO — WYMAGA WERYFIKACJI Z ZESPOŁEM]
