# PUT /api/Firm/EditFirm/{isClient} — Edycja firmy

| Atrybut | Wartość |
|---|---|
| ID | API-05 |
| Metoda | PUT |
| URL | `/api/Firm/EditFirm/{isClient}` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `FirmController.EditFirm` |
| Serwis | `FirmService.EditFirm` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Path Parameters
| Parametr | Typ | Wartości | Opis |
|---|---|---|---|
| `isClient` | `bool` | `false` = własna firma, `true` = klient | Określa rolę firmy |

### Body (JSON) — `FirmDto`

Takie same pola jak w `POST_Firm_AddFirm.md`. Musi zawierać poprawne `id` istniejącej firmy.

**Przykład:**
```json
{
  "id": 42,
  "name": "My Company SRL Updated",
  "cui": "12345678",
  "regCom": "J12/345/2020",
  "address": "STR. EXAMPLE 2",
  "county": "CLUJ",
  "city": "CLUJ-NAPOCA"
}
```

## Response

### 200 OK
Zwraca zaktualizowany `FirmDto`.

### Błędy

| Status HTTP | Warunek |
|---|---|
| 500 Internal Server Error | Firma o podanym `id` nie istnieje (plain `Exception("Firm not found.")` — nie domenowy wyjątek) |
| 401 Unauthorized | Brak/wygaśnięty token |

## Algorytm (FirmService.EditFirm)

1. `GetByIdAsync(firmDto.Id)` → plain `Exception` jeśli null
2. `_mapper.Map(firmDto, firm)` — aktualizacja pól encji
3. `CompleteAsync()` — zapis
4. `ManageUserFirmRelation(firm.Id, isClient)` — aktualizacja/tworzenie relacji UserFirm

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
