# Relacje: UserFirm — powiązania i izolacja danych

| Atrybut | Wartość |
|---|---|
| Tabele | `UserFirm`, `Firm`, `User` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Dokumentacja kluczowego wzorca izolacji danych w InvoiceJet — tabel `UserFirm` i jej relacji.

## Schemat relacyjny

```
User (1) ──── (1) UserFirm (1) ──── (1) Firm [własna firma]
                              (1) ──── (N) Firm [firmy klientów]
                              (1) ──── (N) BankAccount
                              (1) ──── (N) Product  
                              (1) ──── (N) DocumentSeries
                              (1) ──── (N) Document
```

## Tabela UserFirm

| Kolumna | Typ | Nullable | Opis |
|---|---|---|---|
| `Id` | `int` | NIE | PK |
| `UserId` | `int` | NIE | FK → User.Id (UNIQUE) |
| `FirmId` | `int` | **TAK** | FK → Firm.Id (własna firma) |

**Ważne:** `FirmId` jest nullable — użytkownik może nie mieć jeszcze firmy po rejestracji.

## Klienci — relacja M:N

Firmy klientów powiązane z UserFirm przez tabelę pośredniczącą:

```sql
-- EF Core konfiguracja (fluent API)
modelBuilder.Entity<UserFirm>()
    .HasMany(uf => uf.ClientFirms)
    .WithMany()
    .UsingEntity("UserFirmClientFirm" lub nazwa wewnętrzna);
```

Tabela pośrednicząca (join table) generowana automatycznie przez EF Core dla relacji M:N.

## Cykl życia UserFirm

### Przy rejestracji
```csharp
// AuthService.RegisterUser
var userFirm = new UserFirm { UserId = user.Id, FirmId = null };
await _unitOfWork.UserFirms.AddAsync(userFirm);
```

### Przy dodaniu firmy (EKRAN-04)
```csharp
// FirmService.AddFirm (isClient=false)
var firm = _mapper.Map<Firm>(firmRequestDto);
await _unitOfWork.Firms.AddAsync(firm);
userFirm.FirmId = firm.Id;
await _unitOfWork.CompleteAsync();
```

### Przy dodaniu klienta (DIALOG-01)
```csharp
// FirmService.AddFirm (isClient=true)
var clientFirm = _mapper.Map<Firm>(firmRequestDto);
await _unitOfWork.Firms.AddAsync(clientFirm);
userFirm.ClientFirms.Add(clientFirm);
await _unitOfWork.CompleteAsync();
```

## Odczyt userFirmId w serwisach

```csharp
// Wzorzec w każdym serwisie:
var userId = int.Parse(User.FindFirst("userId")!.Value); // z JWT (w kontrolerze)
var userFirm = await _unitOfWork.UserFirms.GetByUserIdAsync(userId);
var userFirmId = userFirm.Id;
// Użyj userFirmId do filtrowania zasobów
```

## Anomalie

| # | Anomalia |
|---|---|
| UF-01 | `UserFirm.FirmId` nullable — serwisy mogą fail przy próbie pobrania danych firmy gdy FirmId=null |
| UF-02 | `UserFirm` jest 1:1 z User — UNIQUE na UserId; jeden użytkownik = jedna firma wystawiająca |
| UF-03 | Brak onboarding wizardu — użytkownik może próbować wystawiać faktury bez konfiguracji firmy |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
