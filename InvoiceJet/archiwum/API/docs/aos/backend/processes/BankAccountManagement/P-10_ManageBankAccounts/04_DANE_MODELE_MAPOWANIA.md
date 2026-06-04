# ManageBankAccounts — Dane, modele i mapowania

## 1. DTO

### `BankAccountDto` (wejście: AddUserFirmBankAccount, EditUserFirmBankAccount; wyjście: wszystkie 4 endpointy)

Źródło: `BankAccountDto.cs`

| Pole | Typ | Wymagane | Opis / źródło wartości |
|---|---|---|---|
| `Id` | `int` | tak (Edit/Delete), nie (Add) | Identyfikator konta; przy Add wypełniany przez DB po CompleteAsync |
| `BankName` | `string` | tak | Nazwa banku; inicjalizator `string.Empty` |
| `Iban` | `string` | tak | Numer IBAN; inicjalizator `string.Empty` |
| `Currency` | `CurrencyEnum` | tak | Waluta konta — enum: `Ron = 0`, `Euro = 1` |
| `IsActive` | `bool` | nie | Czy konto aktywne (domyślnie `false` w encji); steruje regułą jednego aktywnego konta per firma |

> Atrybuty walidacyjne DTO: brak atrybutów z przestrzeni `System.ComponentModel.DataAnnotations`. Cała walidacja (istnienie firmy, istnienie konta w bazie, powiązanie z dokumentami) realizowana w `BankAccountService`.

---

## 2. Encje i kolumny

### Encja `BankAccount` → tabela `BankAccount`

Kotwica: `BankAccount.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("InvoiceJet.Domain.Models.BankAccount", b => ...)`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `Id` | `int` IDENTITY | nie | PK | — |
| `BankName` | `nvarchar(max)` | nie | — | — |
| `Iban` | `nvarchar(max)` | nie | — | — |
| `Currency` | `int` | nie | — | — |
| `IsActive` | `bit` | nie | — | — |
| `UserFirmId` | `int` | nie | FK→`UserFirm` | tak |

Uwagi do schematu:
- `UserFirmId` jest NOT NULL w encji i snapshosie — w przeciwieństwie do `Product.UserFirmId`, tu konto zawsze jest przypisane do firmy.
- `Currency` mapowany jako `int` (wartość enum `CurrencyEnum`): `Ron = 0`, `Euro = 1`.
- Brak indeksu unikalnego na `Iban` — nie ma walidacji unikalności IBAN na poziomie DB ani serwisu.

> Pełne definicje: `../../SLOWNIK_DANYCH.md#BankAccount`.

---

## 3. Relacje i kaskady

| Z encji | Pole FK | Do encji | Kierunek | Kaskada |
|---|---|---|---|---|
| `BankAccount` | `UserFirmId` | `UserFirm` | N..1 | `OnDelete(DeleteBehavior.Cascade)` — usunięcie `UserFirm` kaskaduje usunięcie kont |
| `Document` | `BankAccountId` | `BankAccount` | N..1 | `OnDelete(DeleteBehavior.Cascade)` — usunięcie konta kaskaduje usunięcie dokumentów ⚠️ |

> [UWAGA: Relacja `Document → BankAccount` ma `OnDelete(DeleteBehavior.Cascade)` — usunięcie konta bankowego skasuje powiązane dokumenty na poziomie DB. Serwis `BankAccountService.DeleteUserFirmBankAccounts` sprawdza istnienie powiązanych dokumentów (WAL-04) i blokuje usunięcie przez `BankAccountAssociatedWithDocumentsException`. Kaskada DB nigdy nie powinna być osiągnięta w normalnym przepływie — ale istnieje jako mechanizm DB. Kotwica: snapshot `Entity("InvoiceJet.Domain.Models.Document")` — `OnDelete(DeleteBehavior.Cascade)` dla `BankAccountId`. — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## 4. Mapowania AutoMapper

Źródło: `BankAccountProfile.cs › BankAccountProfile`

```csharp
public class BankAccountProfile : Profile
{
    public BankAccountProfile()
    {
        CreateMap<BankAccount, BankAccountDto>().ReverseMap();
    }
}
```

| Źródło | Cel | Profil | Uwagi |
|---|---|---|---|
| `BankAccount` | `BankAccountDto` | `BankAccountProfile` | Wszystkie pola mapowane 1:1 po nazwach; `Currency` mapowany jako wartość int ↔ enum |
| `BankAccountDto` | `BankAccount` | `BankAccountProfile` (`ReverseMap`) | `UserFirmId` **nie jest** w `BankAccountDto` — ustawiany ręcznie w serwisie po mapowaniu (`bankAccount.UserFirmId = userFirmId.Value`) |

> Uwaga do `AddUserFirmBankAccount`: mapowanie `_mapper.Map<BankAccount>(bankAccountDto)` następuje **przed** sprawdzeniem firmy (WAL-01). Dopiero po mapowaniu serwis pobiera `userFirmId` i ustawia je ręcznie: `bankAccount.UserFirmId = userFirmId.Value`. Kotwica: `BankAccountService.cs › BankAccountService.AddUserFirmBankAccount`.

> Uwaga do `EditUserFirmBankAccount`: `_mapper.Map(bankAccountDto, bankAccount)` mapuje DTO na istniejącą tracked encję. `UserFirmId` nie jest w DTO — pozostaje bez zmian po mapowaniu. Kotwica: `BankAccountService.cs › BankAccountService.EditUserFirmBankAccount`.

---

## 5. Zapytania (LINQ/SQL)

### Query 1: Pobranie kont bankowych aktywnej firmy użytkownika (`GetUserFirmBankAccounts`)

Kotwica: `BankAccountRepository.cs › BankAccountRepository.GetUserFirmBankAccountsAsync`

```csharp
return await _dbSet
    .Where(ba => ba.UserFirm.UserId == userId
              && ba.UserFirm.User.ActiveUserFirmId == ba.UserFirmId)
    .ToListAsync();
```

Semantyka: pobiera konta, gdzie powiązana `UserFirm` należy do bieżącego użytkownika i jest jego aktywną firmą.

### Query 2: Sprawdzenie powiązania konta z dokumentami (`DeleteUserFirmBankAccounts` — WAL-04)

Kotwica: `BankAccountService.cs › BankAccountService.DeleteUserFirmBankAccounts`

```csharp
bool isAssociatedWithDocuments = await _unitOfWork.Documents.Query()
    .AnyAsync(d => d.BankAccountId == bankAccountId);
```

Semantyka: sprawdza, czy istnieje choć jeden rekord `Document` z danym `BankAccountId`. Jeśli tak — konto nie może być usunięte.

### Query 3: Dezaktywacja innych kont firmy (`DeactivateOtherBankAccounts`)

Kotwica: `BankAccountService.cs › BankAccountService.DeactivateOtherBankAccounts`

```csharp
var otherAccounts = await _unitOfWork.BankAccounts.Query()
    .Where(ba => ba.UserFirmId == userFirmId && ba.Id != excludeAccountId)
    .ToListAsync();

foreach (var account in otherAccounts)
{
    account.IsActive = false;
    await _unitOfWork.BankAccounts.UpdateAsync(account);
}
```

Semantyka: pobiera wszystkie konta firmy z wyłączeniem konta o `excludeAccountId` (przy Edit) lub bez wyłączeń (przy Add), ustawia `IsActive = false` i oznacza do aktualizacji. Rzeczywisty `UPDATE` następuje w `CompleteAsync()` wywoływanym przez metodę nadrzędną.

---

## 6. Użyte enumy i lookupy

| Element | Rodzaj | Plik | Wartości |
|---|---|---|---|
| `CurrencyEnum` | enum C# | `InvoiceJet.Domain/Enums/Currency.cs` | `Ron = 0`, `Euro = 1` |

> `CurrencyEnum` przechowywany w DB jako `int` — bez konwertera wartości enum na string. Pełna definicja: `../../SLOWNIK_DANYCH.md#CurrencyEnum` (do wypełnienia).
