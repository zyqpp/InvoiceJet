# DTO: NazwaDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-XX |
| Plik | `InvoiceJet.Application/DTOs/NazwaDto.cs` |
| Kierunek | Request / Response / Dwukierunkowy |
| Endpointy | `METHOD /api/...` |
| Ostatnia walidacja | YYYY-MM-DD |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `Id` | `int` | NIE | ID rekordu |
| `Pole1` | `string` | NIE | Opis pola |
| `Pole2` | `string` | TAK | Opis pola opcjonalnego |

## Mapowanie AutoMapper

| Kierunek | Profile |
|---|---|
| `NazwaDto` → `Encja` | `NazwaProfile` |
| `Encja` → `NazwaDto` | `NazwaProfile` |

## Przykład JSON

```json
{
  "id": 1,
  "pole1": "wartość",
  "pole2": null
}
```

## Anomalie

| # | Anomalia |
|---|---|
| XX-01 | ... |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | YYYY-MM-DD | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
