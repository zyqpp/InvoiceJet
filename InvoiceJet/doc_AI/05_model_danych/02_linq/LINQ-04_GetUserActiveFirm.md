# LINQ: GetUserActiveFirm (pobieranie własnej firmy)

| Atrybut | Wartość |
|---|---|
| ID | LINQ-04 |
| Serwis | `FirmService.GetUserActiveFirm()` |
| Endpoint | `GET /api/Firm/GetUserActiveFirm` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Pobranie danych własnej firmy wystawiającego (nie klienta). Wywoływane przy ładowaniu EKRAN-04.

## Zapytanie LINQ (szacowane)

```csharp
var userFirm = await _context.UserFirms
    .Include(uf => uf.Firm)
    .FirstOrDefaultAsync(uf => uf.UserId == userId);

// Jeśli UserFirm.Firm == null → użytkownik nie ma jeszcze firmy → return null
if (userFirm?.Firm == null) return null;

return _mapper.Map<FirmRequestDto>(userFirm.Firm);
```

## Przypadki

| Scenariusz | Wynik |
|---|---|
| Użytkownik ma firmę | `FirmRequestDto` z danymi |
| Użytkownik bez firmy (nowy) | `null` → frontend pokazuje formularz dodania |

## Powiązane

- EKRAN-04 — formularz danych firmy
- `FirmProfile` — mapowanie `Firm → FirmRequestDto`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
