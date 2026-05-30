# Dodanie firmy — Logika aplikacyjna

## 1. Wejście do procesu

`FirmController.AddFirm([FromBody] FirmDto firmDto, bool isClient)` odbiera żądanie `POST /api/Firm/AddFirm/{isClient}`.

Metoda kontrolera wykonuje:

```csharp
var updatedOrNewFirm = await _firmService.AddFirm(firmDto, isClient);
return Ok(updatedOrNewFirm);
```

---

## 2. Mapowanie i zapis firmy

`FirmService.AddFirm()` mapuje DTO na encję:

```csharp
var firm = _mapper.Map<Firm>(firmDto);
```

Następnie zapisuje encję:

```csharp
await _unitOfWork.Firms.AddAsync(firm);
await _unitOfWork.CompleteAsync();
```

Pierwsze `CompleteAsync()` utrwala rekord `Firm` i nadaje mu identyfikator.

---

## 3. Utworzenie relacji użytkownik-firma

Po zapisie firmy serwis wywołuje:

```csharp
await ManageUserFirmRelation(firm.Id, isClient);
```

Metoda `ManageUserFirmRelation()` pobiera identyfikator użytkownika przez:

```csharp
_userService.GetCurrentUserId()
```

Następnie sprawdza, czy istnieje relacja:

```csharp
UserFirms.GetUserFirmById(userId, firmId)
```

---

## 4. Brak istniejącej relacji `UserFirm`

Jeżeli relacja nie istnieje, serwis tworzy:

```csharp
new UserFirm
{
    UserId = userId,
    FirmId = firmId,
    IsClient = isClient
}
```

Relacja jest dodawana przez `UserFirms.AddAsync(newUserFirm)`.

---

## 5. Ustawienie aktywnej firmy

Po dodaniu relacji serwis pobiera użytkownika przez:

```csharp
Users.GetUserByIdAsync(_userService.GetCurrentUserId())
```

Jeżeli `user.ActiveUserFirm` ma wartość `null`, serwis:

1. ustawia `user.ActiveUserFirm = newUserFirm`,
2. wywołuje `DocumentSeriesService.AddInitialDocumentSeries(newUserFirm)`.

---

## 6. Dodanie początkowych serii dokumentów

`AddInitialDocumentSeries()` tworzy trzy serie dokumentów:

| Seria | `SeriesName` | `FirstNumber` | `CurrentNumber` | `IsDefault` | Typ dokumentu |
|---|---|---:|---:|---|---|
| Faktura | Bieżący rok | `1` | `1` | `true` | `Factura` |
| Faktura storno | Bieżący rok | `1` | `1` | `true` | `Factura Storno` |
| Faktura proforma | Bieżący rok | `1` | `1` | `true` | `Factura Proforma` |

Typy dokumentów są pobierane z repozytorium `DocumentTypes` po nazwie.

---

## 7. Istniejąca relacja `UserFirm`

Jeżeli relacja istnieje, serwis aktualizuje:

```csharp
existingUserFirm.IsClient = isClient;
```

W typowym przebiegu `AddFirm()` tworzy nową encję `Firm`, więc istniejąca relacja dla tej nowej encji nie występuje. Ten wariant wynika z implementacji `ManageUserFirmRelation()`.

---

## 8. Drugi zapis do bazy

Na końcu `ManageUserFirmRelation()` wykonuje:

```csharp
await _unitOfWork.CompleteAsync();
```

Ten zapis utrwala relację `UserFirm`, zmianę `ActiveUserFirm` i serie dokumentów utworzone przez `AddInitialDocumentSeries()`.

---

## 9. Zwrócenie DTO

Po zakończeniu relacji serwis wykonuje:

```csharp
firmDto.Id = firm.Id;
return firmDto;
```

Odpowiedź API zawiera DTO z identyfikatorem utworzonej firmy.
