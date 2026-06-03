# DTO: DocumentRequestDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-07 |
| Plik | `InvoiceJet.Application/DTOs/DocumentRequestDto.cs` |
| Kierunek | Request + Response (dwukierunkowy) |
| Endpointy | `POST /api/Document/Add`, `PUT /api/Document/Edit`, `GET /api/Document/GetDocumentById/{id}` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `Id` | `int` | NIE | ID dokumentu (0 przy dodawaniu) |
| `DocumentNumber` | `string` | TAK | Numer dokumentu (generowany przez backend) |
| `IssueDate` | `DateTime` | NIE | Data wystawienia |
| `DueDate` | `DateTime` | NIE | Termin płatności |
| `TotalPrice` | `decimal` | NIE | Suma brutto całego dokumentu |
| `DocumentTypeId` | `int` | NIE | Typ: 1=Faktura, 2=Proforma, 3=Storno |
| `DocumentStatusId` | `int` | NIE | Status dokumentu |
| `Client` | `FirmRequestDto` | TAK | Dane klienta (zagnieżdżone) |
| `Seller` | `FirmRequestDto` | TAK | Dane sprzedawcy (zagnieżdżone, z UserFirm) |
| `DocumentSeries` | `DocumentSeriesRequestDto` | TAK | Seria (zagnieżdżona, zawiera SeriesName + CurrentNumber) |
| `BankAccount` | `BankAccountRequestDto` | TAK | Konto bankowe (zagnieżdżone) |
| `Products` | `List<DocumentProductRequestDto>` | TAK | Lista pozycji dokumentu |

## Relacje zagnieżdżone

`DocumentRequestDto` zawiera pełne obiekty zagnieżdżone — nie tylko FK. Pozycja `DocumentSeries` jest przekazywana z frontendu z `CurrentNumber` używanym do generowania numeru dokumentu.

## Mapowanie AutoMapper (kluczowe)

```csharp
// DocumentProfile
CreateMap<Document, DocumentRequestDto>()
    .ForMember(dest => dest.Seller, opt => opt.MapFrom(src => src.UserFirm))
    .ForMember(dest => dest.Products, opt => opt.MapFrom(src =>
        src.DocumentProducts!.Select(dp => new DocumentProductRequestDto {
            ProductId = dp.ProductId,
            Quantity = dp.Quantity,
            Price = dp.Price,
            VatRate = dp.VatRate,
            Name = dp.Product!.Name,
            MeasureUnit = dp.Product!.MeasureUnit
        }).ToList()));
```

## Anomalie

| # | Anomalia |
|---|---|
| DTO07-01 | `DocumentSeries.CurrentNumber` w żądaniu pochodzi z frontendu — backend może generować numer na podstawie nieaktualnej wartości (race condition) |
| DTO07-02 | Brak `ClientId` jako prostego int — klient przekazywany jako pełny obiekt `FirmRequestDto` |

## Przykład JSON (fragment)

```json
{
  "id": 0,
  "issueDate": "2026-05-31",
  "dueDate": "2026-06-30",
  "totalPrice": 1785.00,
  "documentTypeId": 1,
  "documentStatusId": 1,
  "documentSeries": { "id": 1, "seriesName": "FV", "currentNumber": 5, "documentTypeId": 1 },
  "client": { "id": 2, "firmName": "Klient SRL" },
  "bankAccount": { "id": 3, "bankName": "BRD", "iban": "RO49...", "currency": "RON" },
  "products": [
    { "productId": 7, "name": "Programare web", "quantity": 10, "price": 150.00, "vatRate": 19.00, "measureUnit": "ore" }
  ]
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
