# ManageClientFirms — Logika aplikacyjna

Proces `P-08` zawiera dwa odrębne endpointy: pobranie firm-klientów (GET) i usuwanie firm (DELETE).

---

## Endpoint 1: GET `/api/Firm/GetUserClientFirms`

### 0. Algorytm w skrócie

1. Kontroler odbiera żądanie GET bez parametrów.
2. Wywołanie `FirmService.GetUserClientFirms()`.
3. Pobranie listy relacji `UserFirm` gdzie `UserId == bieżący użytkownik && IsClient == true`.
4. Jeśli lista pusta → zwrot pustej listy (bez rzucania wyjątku).
5. Projekcja `Firm` z relacji.
6. Mapowanie `Firm[]` → `FirmDto[]`.
7. Zwrot HTTP `200 OK` z tablicą DTO.

---

### 1. Wejście do procesu

Kotwica: `FirmController.cs › FirmController.GetUserClientFirms`

```csharp
[HttpGet("GetUserClientFirms")]
public async Task<ActionResult> GetUserClientFirms()
{
    var clientFirms = await _firmService.GetUserClientFirms();
    return Ok(clientFirms);
}
```

Metoda nie przyjmuje żadnych parametrów. Identyfikator użytkownika pobrierany jest z tokenu JWT w `FirmService`.

### 2. Walidacje (faza wejściowa)

> Wymiar nie występuje w tym endpoincie. Proces jest read-only, bez walidacji wejścia. Bieżący użytkownik pobrierany automatycznie z kontekstu JWT.

### 3. Logika biznesowa

Kotwica: `FirmService.cs › FirmService.GetUserClientFirms`, linie 98-108

```csharp
public async Task<List<FirmDto>> GetUserClientFirms()
{
    var clients = await _unitOfWork.UserFirms.GetUserFirmClients(_userService.GetCurrentUserId());
    if (clients.Count == 0)
    {
        return new List<FirmDto>();
    }

    var firms = clients.Select(u => u.Firm).ToList();
    return _mapper.Map<List<FirmDto>>(firms);
}
```

**Krok 1:** Pobranie listy relacji `UserFirm`. Repozytorium `UserFirmRepository.GetUserFirmClients(userId)` zwraca listę `UserFirm`, gdzie `UserId == userId` i `IsClient == true`.

Kotwica: `IUserFirmRepository.GetUserFirmClients(Guid userId)` — metoda specjalizowana w repozytorium.

**Krok 2:** Sprawdzenie, czy lista jest pusta. Jeśli `Count == 0` → zwrot nowej pustej listy `List<FirmDto>()`. Brak wyjątku.

**Krok 3:** Projekcja powiązanych `Firm`. `Select(u => u.Firm)` pobiera obiekty `Firm` z każdej relacji `UserFirm`.

**Krok 4:** Mapowanie. AutoMapper (`_mapper.Map<List<FirmDto>>(...)`) konwertuje tablicę `Firm` na tablicę `FirmDto`.

### 4. Zapisy do bazy i transakcje

> Proces jest read-only. Brak zapisów do bazy, brak `CompleteAsync()`.

### 5. Odpowiedź

HTTP status: **200 OK**

Ciało odpowiedzi: Tablica `FirmDto[]`:

```json
[
  {
    "id": 2,
    "name": "Acme Corp",
    "cui": "12345678",
    "regCom": "J40/2020/123",
    "address": "STR. Marticel Ion Dragomir, nr. 10",
    "county": "Bihor",
    "city": "Oradea"
  }
]
```

Jeśli użytkownik nie ma firm-klientów → tablica pusta `[]`.

### 6. Uwagi techniczne

- Brak jawnej transakcji (proces read-only).
- Zwrot pustej listy zamiast `null` — bezpieczny dla klienta.

---

## Endpoint 2: PUT `/api/Firm/DeleteFirms`

### 0. Algorytm w skrócie

1. Kontroler odbiera żądanie PUT z tablicą ID firm.
2. Wywołanie `FirmService.DeleteFirms(int[] firmIds)`.
3. Pętla po każdym ID:
   - Pobranie firmy po ID.
   - Jeśli nie znaleziona → rzucenie `Exception("Product not found.")`.
   - Sprawdzenie, czy firma jest powiązana z dokumentami (`Document.ClientId == firmId`).
   - Jeśli tak → rzucenie `FirmAssociatedWithDocumentException`.
   - Jeśli nie → oznaczenie firmy do usunięcia (`RemoveAsync`).
4. Po pętli → zatwierdzenie wszystkich zmian (`CompleteAsync()`).
5. Zwrot HTTP `200 OK` (puste ciało).

---

### 1. Wejście do procesu

Kotwica: `FirmController.cs › FirmController.DeleteFirms`, linie 55-60

```csharp
[HttpPut("DeleteFirms")]
public async Task<ActionResult> DeleteFirms(int[] firmIds)
{
    await _firmService.DeleteFirms(firmIds);
    return Ok();
}
```

Parametr: `firmIds` — tablica identyfikatorów firm, przesyłana jako query string.

### 2. Walidacje (faza wejściowa)

**Walidacja 1:** Pobranie firmy po ID. Brak firmy → wyjątek `Exception` (szczegóły: plik 05, `WAL-01`).

Kotwica: `FirmService.cs › FirmService.DeleteFirms`, linie 114-115

```csharp
var firm = await _unitOfWork.Firms.GetByIdAsync(firmId) ??
              throw new Exception("Product not found.");
```

**Walidacja 2:** Sprawdzenie powiązania z dokumentami. Firma powiązana → wyjątek `FirmAssociatedWithDocumentException` (szczegóły: plik 05, `WAL-02`).

Kotwica: `FirmService.cs › FirmService.DeleteFirms`, linie 117-123

```csharp
bool isAssociatedWithDocuments = await _unitOfWork.Documents.Query()
    .AnyAsync(d => d.ClientId == firmId);

if (isAssociatedWithDocuments)
{
    throw new FirmAssociatedWithDocumentException(firm.Name);
}
```

| # | Sprawdzenie | Kotwica | Wynik negatywny |
|---|---|---|---|
| 1 | Firma istnieje (ID) | `FirmRepository.GetByIdAsync` | `Exception` (WAL-01) |
| 2 | Firma nie jest powiązana z `Document` | `DocumentRepository.Query().AnyAsync(d.ClientId)` | `FirmAssociatedWithDocumentException` (WAL-02) |

### 3. Logika biznesowa

Kotwica: `FirmService.cs › FirmService.DeleteFirms`, linie 110-129

```csharp
public async Task DeleteFirms(int[] firmIds)
{
    foreach (var firmId in firmIds)
    {
        var firm = await _unitOfWork.Firms.GetByIdAsync(firmId) ??
                      throw new Exception("Product not found.");

        bool isAssociatedWithDocuments = await _unitOfWork.Documents.Query()
            .AnyAsync(d => d.ClientId == firmId);
        
        if (isAssociatedWithDocuments)
        {
            throw new FirmAssociatedWithDocumentException(firm.Name);
        }
        
        await _unitOfWork.Firms.RemoveAsync(firm);
    }

    await _unitOfWork.CompleteAsync();
}
```

**Krok 1:** Iteracja po każdym `firmId` w tablicy.

**Krok 2:** Pobranie encji `Firm` z repozytorium (`GetByIdAsync`). Jeśli `null` → rzucenie `Exception`.

**Krok 3:** Sprawdzenie, czy istnieje jakikolwiek dokument z `ClientId == firmId` (przy użyciu `IQueryable.Query()` i `AnyAsync`).

**Krok 4:** Jeśli dokument istnieje → rzucenie `FirmAssociatedWithDocumentException` z nazwą firmy.

**Krok 5:** Jeśli brak dokumentów → oznaczenie firmy do usunięcia w serwisie (`RemoveAsync`). Nie następuje natychmiastowy zapis.

**Krok 6:** Po pętli (po oznaczeniu wszystkich firm) → zatwierdzenie zmian (`CompleteAsync()`).

### Tabela: pole encji → źródło

> Wymiar nie dotyczy tego endpointu. Nie są tworzone ani modyfikowane encje — tylko usuwane.

### 4. Zapisy do bazy i transakcje

| Krok | Operacja | Klasa/metoda | Kiedy `CompleteAsync()` |
|---|---|---|---|
| 1 | `RemoveAsync(firm)` × N (w pętli) | `FirmRepository.RemoveAsync` | Nie — zaznaczenie do usunięcia |
| 2 | `CompleteAsync()` | `UnitOfWork.CompleteAsync()` | Tak — zatwierdzenie wszystkich usunięć |

**Transakcyjność:** Brak jawnej transakcji (`BeginTransactionAsync` nie używany). Wszystkie operacje `RemoveAsync` w pętli są zbierane w EF Core tracking, a `CompleteAsync()` zapisuje je jednocześnie w jednym `SaveChangesAsync()`. EF Core i SQL Server domyślnie oplatają to automatyczną transakcją (DbTransaction).

[UWAGA: Jeśli `CompleteAsync()` ulegnie awarii przed zakończeniem (np. timeout sieciowy, SQL Server restart), część firm może być usunięta, a część nie — baza mogąc pozostać w stanie niespójnym — WYMAGA WERYFIKACJI Z ZESPOŁEM]

### 5. Odpowiedź

HTTP status: **200 OK**

Ciało odpowiedzi: Puste (brak zawartości)

Jeśli którakolwiek z walidacji się nie powiedzie (wyjątek), odpowiedź zawiera status błędu (szczegóły w pliku 05).

### 6. Uwagi techniczne

- [UWAGA: Błędny komunikat wyjątku — "Product not found." zamiast "Firm not found." — WYMAGA POPRAWY]
- [UWAGA: Generyczny typ wyjątku (`Exception`) zamiast `FirmNotFoundException` — trafia do catch-all (500) zamiast 400 — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- [UWAGA: Brak jawnej transakcji — częściowy zapis możliwy w razie awarii `CompleteAsync()` — WYMAGA WERYFIKACJI Z ZESPOŁEM]
