# ManageClientFirms — Dane, modele i mapowania

## 1. DTO

### `FirmDto` (wyjście GET `/api/Firm/GetUserClientFirms`)

| Pole | Typ | Wymagane | Opis / źródło wartości |
|---|---|---|---|
| `Id` | `int` | tak | Identyfikator firmy |
| `Name` | `string` | tak | Nazwa firmy |
| `Cui` | `string` | tak | Kod CAEN (identyfikator VAT) |
| `RegCom` | `string?` | nie | Numer rejestru handlowego |
| `Address` | `string` | tak | Adres główny |
| `County` | `string` | tak | Powiat |
| `City` | `string` | tak | Miasto |

Źródło: `FirmDto.cs › FirmDto`

Atrybuty walidacyjne: Brak. Walidacja zdefiniowana w serwisie: `GetUserClientFirms()` zwraca pustą listę, jeśli użytkownik nie ma firm-klientów.

### Parametry wejściowe DELETE `PUT /api/Firm/DeleteFirms`

| Parametr | Typ | Źródło | Opis |
|---|---|---|---|
| `firmIds` | `int[]` | query string (domyślnie) | Tablica ID firm do usunięcia |

Brak dedykowanego DTO — przesyłane jako parametr bezpośrednio w metodzie kontrolera.

## 2. Encje i kolumny

### Encja `Firm` → tabela `Firm`

Kotwica: `Firm.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("InvoiceJet.Domain.Models.Firm", b => ..., lines 213-248)`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `Id` | `int` | nie | PK | IDENTITY |
| `Name` | `nvarchar(max)` | nie | — | — |
| `Cui` | `nvarchar(max)` | nie | — | — |
| `RegCom` | `nvarchar(max)` | nie | — | — |
| `Address` | `nvarchar(max)` | nie | — | — |
| `County` | `nvarchar(max)` | nie | — | — |
| `City` | `nvarchar(max)` | nie | — | — |

Pełne definicje: `../../SLOWNIK_DANYCH.md#Firm`.

Rola w P-08:
- **GET**: Mapowana do `FirmDto` w odpowiedzi (pola zwracane w całości)
- **DELETE**: Usuwana z bazy na podstawie `Id`

### Encja `UserFirm` → tabela `UserFirm`

Kotwica: `UserFirm.cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("InvoiceJet.Domain.Models.UserFirm", lines 323-347)`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `UserFirmId` | `int` | nie | PK | IDENTITY |
| `UserId` | `uniqueidentifier` | nie | FK→User | tak |
| `FirmId` | `int` | nie | FK→Firm | tak |
| `IsClient` | `bit` | nie | — | — |

Rola w P-08:
- **GET**: Filtrowana po `IsClient = true`, używana jako kluczowa relacja do pobrania firm użytkownika
- **DELETE**: Nie dotykana bezpośrednio (kaskada usuwa automatycznie, gdy `Firm` jest usunięta, ze względu na `OnDelete(DeleteBehavior.Cascade)`)

### Encja `Document` → tabela `Document` (walidacja)

Kotwica: snapshot, linie 50-109.

Kolumna istotna dla P-08: `ClientId` (`int?`, FK→Firm)

Rola: Sprawdzenie, czy firma jest powiązana z dokumentami (przed usunięciem).

Pełne definicje: `../../SLOWNIK_DANYCH.md#Document`.

## 3. Relacje i kaskady

| Z encji | Pole FK | Do encji | Kierunek | Kaskada |
|---|---|---|---|---|
| `UserFirm` | `FirmId` | `Firm` | N..1 | Cascade |
| `Document` | `ClientId` | `Firm` | N..1 | (brak — optional) |

Szczegóły:
- Usunięcie `Firm` powoduje automatyczne usunięcie wszystkich `UserFirm` powiązanych (kaskada)
- Usunięcie `Firm` **nie** powoduje usunięcia `Document` — proces explicitnie zabrania usunięcia firmy, jeśli ma powiązane dokumenty

## 4. Mapowania AutoMapper

| Źródło | Cel | Profil | Uwagi |
|---|---|---|---|
| `Firm[]` | `FirmDto[]` | `FirmProfile` | Mapowanie dwustronne (`ReverseMap`) — w P-08 używane tylko GET |

Źródło: `FirmProfile.cs › FirmProfile`

```csharp
public class FirmProfile : Profile
{
    public FirmProfile()
    {
        CreateMap<Firm, FirmDto>().ReverseMap(); 
    }
}
```

## 5. Zapytania (LINQ)

### Query 1: Pobranie firm-klientów (GET)

Źródło: `FirmService.cs › FirmService.GetUserClientFirms`, linie 98-108

```csharp
var clients = await _unitOfWork.UserFirms.GetUserFirmClients(_userService.GetCurrentUserId());
var firms = clients.Select(u => u.Firm).ToList();
return _mapper.Map<List<FirmDto>>(firms);
```

Kroki:
1. `UserFirmRepository.GetUserFirmClients(userId)` — pobranie `UserFirm` gdzie `UserId == userId && IsClient == true`
2. Projekcja `Select(u => u.Firm)` — pobranie powiązanych `Firm`
3. `AutoMapper.Map` — konwersja `Firm[]` → `FirmDto[]`

### Query 2: Sprawdzenie powiązania z dokumentami (DELETE)

Źródło: `FirmService.cs › FirmService.DeleteFirms`, linie 117-118

```csharp
bool isAssociatedWithDocuments = await _unitOfWork.Documents.Query()
    .AnyAsync(d => d.ClientId == firmId);
```

Kroki:
1. `IDocumentRepository.Query()` — zwraca `IQueryable<Document>`
2. `AnyAsync(d => d.ClientId == firmId)` — sprawdzenie, czy istnieje dokument z `ClientId` równym danemu ID firmy

## 6. Użyte enumy i lookupy

> Wymiar nie występuje w tym procesie. Proces nie używa enumów ani tabel słownikowych.

---

## Uwagi techniczne

### [UWAGA: Błędny komunikat wyjątku w `DeleteFirms`]

Źródło: `FirmService.cs › FirmService.DeleteFirms`, linia 114-115:

```csharp
var firm = await _unitOfWork.Firms.GetByIdAsync(firmId) ??
              throw new Exception("Product not found.");
```

Komunikat mówi `"Product not found."`, ale usuwamy `Firm`. Powinno być `"Firm not found."` — WYMAGA POPRAWY.

### [UWAGA: Generyczny typ wyjątku dla firmy nie znalezionej]

Zamiast `FirmNotFoundException` rzucany jest `Exception` (generyczny). Trafia do catch-all `ExceptionMiddleware` → `500 Internal Server Error` zamiast `400 Bad Request`. — WYMAGA WERYFIKACJI Z ZESPOŁEM

### [UWAGA: `UserFirm.IsClient` domyślnie `true`]

```csharp
public bool IsClient { get; set; } = true;
```

Każde domyślnie tworzone powiązanie `UserFirm` jest klientem. Może prowadzić do błędów logicznych, jeśli kod nie zainicjalizuje jawnie. — WYMAGA WERYFIKACJI Z ZESPOŁEM
