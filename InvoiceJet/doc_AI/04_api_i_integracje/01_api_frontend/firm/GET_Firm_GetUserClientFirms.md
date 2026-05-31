# GET /api/Firm/GetUserClientFirms — Lista klientów

| Atrybut | Wartość |
|---|---|
| ID | API-07/08 |
| Metoda | GET |
| URL | `/api/Firm/GetUserClientFirms` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `FirmController.GetUserClientFirms` |
| Serwis | `FirmService.GetUserClientFirms` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

> **Uwaga anomalii A-02:** Ten endpoint ma dwie nazwy w inwentaryzacji (API-07 i API-08) — jest to jeden fizyczny endpoint.

## Request

Brak parametrów. userId pobierany z JWT tokenu.

### Headers
| Nagłówek | Wartość |
|---|---|
| `Authorization` | `Bearer {token}` |

## Response

### 200 OK — lista klientów

```json
[
  {
    "id": 10,
    "name": "Client Company SRL",
    "cui": "87654321",
    "regCom": "J40/123/2019",
    "address": "STR. CLIENTULUI 5",
    "county": "IASI",
    "city": "IASI"
  }
]
```

### 200 OK — brak klientów

```json
[]
```

## Algorytm

```csharp
// Pobierz UserFirm z IsClient=true dla aktualnego użytkownika
var clients = await _unitOfWork.UserFirms.GetUserFirmClients(userId);
if (clients.Count == 0) return new List<FirmDto>();
var firms = clients.Select(u => u.Firm).ToList();
return _mapper.Map<List<FirmDto>>(firms);
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
