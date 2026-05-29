# Wystawienie nowej faktury — Dane, modele i mapowania

## DTO żądania

| DTO | Rola |
|---|---|
| `DocumentRequestDto` | Główne body żądania dla `POST /api/Document/AddDocument`. |
| `FirmDto` | Reprezentuje klienta w polu `Client`. |
| `DocumentSeriesDto` | Dostarcza serię dokumentu, typ dokumentu i bieżący numer. |
| `DocumentProductRequestDto` | Reprezentuje pozycję dokumentu. |

---

## Encje zapisywane lub aktualizowane

| Encja | Operacja | Źródło danych |
|---|---|---|
| `Document` | Dodanie i aktualizacja sum | `DocumentRequestDto`, aktywne konto bankowe, aktywna firma użytkownika |
| `DocumentProduct` | Dodanie pozycji dokumentu | `DocumentProductRequestDto` |
| `Product` | Dodanie, gdy pozycja ma `id <= 0` | `DocumentProductRequestDto` przez `AutoMapper` |
| `DocumentSeries` | Aktualizacja `CurrentNumber` | `DocumentSeriesDto.Id` |

---

## Mapowanie i przypisania

| Źródło | Cel | Mechanizm |
|---|---|---|
| `DocumentProductRequestDto` | `Product` | `_mapper.Map<Product>(documentProductDto)` |
| `DocumentRequestDto.Client.Id` | `Document.ClientId` | Przypisanie bezpośrednie |
| `DocumentSeries.SeriesName` + `DocumentSeries.CurrentNumber` | `Document.DocumentNumber` | Konkatenacja i format `D4` |
| Aktywne konto bankowe | `Document.BankAccount` | Zapytanie do `BankAccounts.Query()` |
| Aktywna firma użytkownika | `Document.UserFirmId` | `Users.GetUserFirmIdAsync(...)` |

---

## Wyliczenia

| Wartość | Sposób wyliczenia |
|---|---|
| `Document.UnitPrice` | Suma `UnitPrice * Quantity` dla wszystkich pozycji. |
| `Document.TotalPrice` | Suma `TotalPrice` dla wszystkich pozycji. |
| `DocumentStatusId` | Stała wartość `(int)DocumentStatusEnum.Unpaid`. |

---

## Relacje danych

| Relacja | Opis |
|---|---|
| `Document.UserFirmId` | Dokument należy do aktywnej firmy użytkownika. |
| `Document.ClientId` | Dokument wskazuje klienta jako `Firm`. |
| `Document.BankAccount` | Dokument wskazuje aktywne konto bankowe aktywnej firmy. |
| `DocumentProduct.DocumentId` | Pozycja dokumentu należy do utworzonego dokumentu. |
| `DocumentProduct.Product` | Pozycja wskazuje istniejący lub nowo utworzony produkt. |

---

## Dane niewykorzystane przez `AddDocument`

| Pole DTO | Status |
|---|---|
| `seller` | Nie jest używane przy zapisie nowego dokumentu. |
| `bankAccount` | Nie jest używane z body. Konto jest pobierane z bazy. |
| `documentType` | Nie jest używane z body. Typ pochodzi z `DocumentSeries.DocumentType`. |
| `documentStatus` | Nie jest używane z body. Status jest ustawiany na `Unpaid`. |
