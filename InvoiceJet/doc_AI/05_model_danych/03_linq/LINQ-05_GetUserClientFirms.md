# LINQ: GetUserClientFirms (lista klientów)

| Atrybut | Wartość |
|---|---|
| ID | LINQ-05 |
| Serwis | `FirmService.GetUserClientFirms()` |
| Endpoint | `GET /api/Firm/GetUserClientFirms` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Pobranie listy firm klientów dla zalogowanego użytkownika. Klienci to firmy powiązane z `UserFirm` przez tabelę pośredniczącą (relacja M:N przez `UserFirm_Firm`).

## Zapytanie LINQ (szacowane)

```csharp
var userFirm = await _context.UserFirms
    .Include(uf => uf.ClientFirms)  // Kolekcja klientów (relacja M:N)
    .FirstOrDefaultAsync(uf => uf.UserId == userId);

return _mapper.Map<List<FirmRequestDto>>(userFirm?.ClientFirms ?? new List<Firm>());
```

## Relacja w schemacie DB

```
UserFirm (1) ─── (M) [UserFirm_Firm junction table] ─── (M) Firm (klienci)
```

Tabela pośrednicząca `UserFirm_Firm` lub podobna (zależy od EF Core fluent configuration) łączy UserFirm z Firm dla klientów.

## Filtrowanie

Lista klientów zawiera tylko firmy powiązane z `UserFirm` zalogowanego użytkownika — izolacja danych zachowana.

## Anomalie

| # | Anomalia |
|---|---|
| LQ05-01 | Brak paginacji — wszystkie firmy klienta zwracane naraz |
| LQ05-02 | Brak sortowania — kolejność nieokreślona |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
