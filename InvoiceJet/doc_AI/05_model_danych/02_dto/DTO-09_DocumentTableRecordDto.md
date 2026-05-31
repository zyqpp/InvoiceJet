# DTO: DocumentTableRecordDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-09 |
| Plik | `InvoiceJet.Application/DTOs/DocumentTableRecordDto.cs` |
| Kierunek | Response (Backend → Frontend) |
| Endpoint | [GET /api/Document/GetTableRecords](../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md) |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `Id` | `int` | NIE | ID dokumentu |
| `DocumentNumber` | `string` | TAK | Numer dokumentu (np. "FV0005") |
| `ClientName` | `string` | TAK | Nazwa klienta (z JOIN z Firm) |
| `IssueDate` | `DateTime` | NIE | Data wystawienia |
| `DueDate` | `DateTime` | NIE | Termin płatności |
| `TotalValue` | `decimal` | NIE | Suma brutto (alias dla `Document.TotalPrice`) |
| `DocumentStatus` | `string` | TAK | Nazwa statusu (z JOIN z DocumentStatus) |

## Mapowanie AutoMapper

```csharp
// DocumentProfile
CreateMap<Document, DocumentTableRecordDto>()
    .ForMember(dest => dest.ClientName,
        opt => opt.MapFrom(src => src.Client!.Name))
    .ForMember(dest => dest.TotalValue,
        opt => opt.MapFrom(src => src.TotalPrice));
```

- `Client.Name` → `ClientName` — wymaga JOINu z tabelą `Firm`
- `TotalPrice` → `TotalValue` — zmiana nazwy przez alias

## Cel

Uproszczony DTO dla widoku tabelarycznego — zawiera tylko kolumny potrzebne w liście. Nie zawiera pozycji dokumentu, danych sprzedawcy ani zagnieżdżonych obiektów.

## Przykład JSON

```json
{
  "id": 42,
  "documentNumber": "FV0015",
  "clientName": "Klient SRL",
  "issueDate": "2026-05-01",
  "dueDate": "2026-05-31",
  "totalValue": 1785.00,
  "documentStatus": "Trimisa"
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
