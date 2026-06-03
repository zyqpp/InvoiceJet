# POST /api/Firm/AddFirm/{isClient} — Dodanie firmy

| Atrybut | Wartość |
|---|---|
| ID | API-03 |
| Metoda | POST |
| URL | `/api/Firm/AddFirm/{isClient}` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `FirmController.AddFirm` |
| Serwis | `FirmService.AddFirm` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Path Parameters
| Parametr | Typ | Wartości | Opis |
|---|---|---|---|
| `isClient` | `bool` | `false` = własna firma, `true` = klient | Określa rolę firmy |

### Headers
| Nagłówek | Wartość |
|---|---|
| `Authorization` | `Bearer {token}` |
| `Content-Type` | `application/json` |

### Body (JSON) — `FirmDto`

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `id` | `int` | TAK (0 dla nowej) | Ignorowany przy dodawaniu — będzie nadpisany przez DB |
| `name` | `string` | TAK | Nazwa firmy |
| `cui` | `string` | TAK | Numer CUI (NIP rumuński) |
| `regCom` | `string?` | NIE | Numer rejestracji handlowej |
| `address` | `string` | TAK | Adres |
| `county` | `string` | TAK | Okręg |
| `city` | `string` | TAK | Miasto |

**Przykład (isClient=false — własna firma):**
```json
{
  "id": 0,
  "name": "My Company SRL",
  "cui": "12345678",
  "regCom": "J12/345/2020",
  "address": "STR. EXAMPLE 1",
  "county": "BUCURESTI",
  "city": "SECTOR 1"
}
```

## Response

### 200 OK

Zwraca `FirmDto` z nadanym `Id`:
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

## Algorytm (FirmService.AddFirm)

1. Mapowanie `FirmDto → Firm` przez AutoMapper
2. `AddAsync(firm)` + `CompleteAsync()` — zapis do DB
3. `firmDto.Id = firm.Id` — uzupełnienie Id w DTO
4. `ManageUserFirmRelation(firm.Id, isClient)`:
   - Szukanie istniejącej relacji `UserFirm` (userId + firmId)
   - Jeśli nie istnieje: tworzenie nowej `UserFirm {UserId, FirmId, IsClient}`
   - Jeśli użytkownik nie ma `ActiveUserFirm` → ustawienie aktywnej firmy + `AddInitialDocumentSeries`
   - Jeśli istnieje: aktualizacja `IsClient`
5. Zwrot `firmDto`

## Zachowanie po stronie frontendu

- `isClient=false`: `FirmDetailsComponent.onSubmit()` (firma wystawiająca)
- `isClient=true`: `AddEditClientDialogComponent.onSubmit()` (klient)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
