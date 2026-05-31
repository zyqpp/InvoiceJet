# GET /api/Firm/GetUserActiveFirm — Aktywna firma użytkownika

| Atrybut | Wartość |
|---|---|
| ID | API-06 |
| Metoda | GET |
| URL | `/api/Firm/GetUserActiveFirm` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `FirmController.GetUserActiveFirm` |
| Serwis | `FirmService.GetUserActiveFirm` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

Brak parametrów. userId pobierany z JWT tokenu.

### Headers
| Nagłówek | Wartość |
|---|---|
| `Authorization` | `Bearer {token}` |

## Response

### 200 OK — firma znaleziona

```json
{
  "id": 42,
  "name": "My Company SRL",
  "cui": "12345678",
  "regCom": "J12/345/2020",
  "address": "STR. EXAMPLE 1",
  "county": "BUCURESTI",
  "city": "SECTOR 1"
}
```

### 200 OK — brak aktywnej firmy

Zwraca pusty `FirmDto`:
```json
{
  "id": 0,
  "name": "",
  "cui": "",
  "regCom": null,
  "address": "",
  "county": "",
  "city": ""
}
```

**Uwaga:** Endpoint nigdy nie zwraca błędu 404 — brak firmy to pusty obiekt.

## Algorytm

```csharp
var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(userId);
return activeUserFirm == null ? new FirmDto() : _mapper.Map<FirmDto>(activeUserFirm.Firm);
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
