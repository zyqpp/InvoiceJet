# Algorytm: Izolacja danych między użytkownikami (Data Isolation Pattern)

| Atrybut | Wartość |
|---|---|
| ID | ALG-10 |
| Nazwa | Data Isolation Pattern (UserFirm-based) |
| Kategoria | Bezpieczeństwo / Architektura |
| Pliki | Wszystkie serwisy, `UserFirmRepository.cs`, kontrolery |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Zapewnienie że każdy zalogowany użytkownik widzi i modyfikuje wyłącznie swoje dane. Realizowane przez powiązanie wszystkich zasobów z `UserFirm.Id` (nie bezpośrednio z `User.Id`).

## Model izolacji

```
User (1) ──── (1) UserFirm (1) ──── (N) BankAccount
                              (1) ──── (N) Product
                              (1) ──── (N) DocumentSeries
                              (1) ──── (N) Document (jako wystawiający)
                              (N) ──── (M) Firm (klienci, przez UserFirm_Firm)
```

## Przepływ w każdym kontrolerze

```csharp
// Krok 1: Pobierz userId z JWT
var userId = int.Parse(User.FindFirst("userId")!.Value);

// Krok 2: Pobierz UserFirmId dla userId
var userFirm = await _unitOfWork.UserFirms.GetByUserIdAsync(userId);
var userFirmId = userFirm.Id;

// Krok 3: Filtruj zasoby przez userFirmId
var products = await _unitOfWork.Products.GetAllByUserFirmIdAsync(userFirmId);
```

## Relacja UserFirm

```sql
-- UserFirm łączy User z Firm (own firm)
UserFirm:
  Id          INT PK
  UserId      INT FK → User
  FirmId      INT FK → Firm (nullable przy braku firmy)

-- Zasoby powiązane z UserFirm (nie z User):
BankAccount.UserFirmId    → UserFirm.Id
Product.UserFirmId        → UserFirm.Id
DocumentSeries.UserFirmId → UserFirm.Id
Document.UserFirmId       → UserFirm.Id
```

## Weryfikacja własności zasobów

Przy operacjach edycji i usuwania:
```csharp
// Przykład z BankAccountService
var bankAccount = await _unitOfWork.BankAccounts.GetByIdAsync(id);
if (bankAccount == null) throw new BankAccountNotFoundException();
// BRAK weryfikacji czy bankAccount.UserFirmId == userFirmId!
```

## Anomalie

| # | Anomalia |
|---|---|
| ISO-01 | **Potencjalna luka:** Przy edycji/usuwaniu zasobu brak weryfikacji czy zasób należy do zalogowanego użytkownika — wystarczy znać `id` zasobu, żeby go zmodyfikować |
| ISO-02 | `Product.Name` ma UNIQUE INDEX globalny (nie per UserFirm) — naruszenie izolacji na poziomie katalogowym |
| ISO-03 | `UserFirm.FirmId` może być `null` jeśli użytkownik nie dodał jeszcze firmy — brak guard clause w serwisach |
| ISO-04 | Brak row-level security w bazie — izolacja tylko na poziomie aplikacyjnym |

## Seeder — domyślne dane

`DbSeeder` tworzy przy starcie aplikacji (jeśli baza pusta):
- Domyślne `DocumentType` (1=Factura, 2=Proforma, 3=Storno)
- Domyślne `DocumentStatus` (wartości enum)

Nie tworzy użytkowników ani firm — dane biznesowe muszą być wprowadzone przez UI.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
