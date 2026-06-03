# DTO: DocumentAutofillInfoDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-10 |
| Plik | `InvoiceJet.Application/DTOs/DocumentAutofillInfoDto.cs` |
| Kierunek | Response (Backend → Frontend) |
| Endpoint | `GET /api/Document/GetDocumentAutofillInfo/{documentTypeId}` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `DocumentSeries` | `List<DocumentSeriesRequestDto>` | TAK | Serie filtrowane po typie dokumentu |
| `Clients` | `List<FirmRequestDto>` | TAK | Lista klientów firmy |
| `BankAccounts` | `List<BankAccountRequestDto>` | TAK | Lista kont bankowych firmy |
| `Products` | `List<ProductRequestDto>` | TAK | Katalog produktów firmy |
| `DocumentStatuses` | `List<DocumentStatusDto>` | TAK | Dostępne statusy dokumentu |
| `Seller` | `FirmRequestDto` | TAK | Dane własnej firmy (wystawiającego) |

## Cel

Agreguje wszystkie dane potrzebne do wypełnienia selektorów formularza dokumentu w jednym żądaniu. Eliminuje konieczność wielu osobnych wywołań API przy otwieraniu formularza.

## Przykład JSON

```json
{
  "documentSeries": [
    { "id": 1, "seriesName": "FV", "currentNumber": 15, "documentTypeId": 1 }
  ],
  "clients": [
    { "id": 2, "firmName": "Klient SRL", "cuiValue": "12345678" }
  ],
  "bankAccounts": [
    { "id": 3, "bankName": "BRD", "iban": "RO49...", "currency": "RON" }
  ],
  "products": [
    { "id": 7, "name": "Programare web", "price": 150.00, "vatRate": 19.00, "measureUnit": "ore" }
  ],
  "documentStatuses": [
    { "id": 1, "name": "Trimisa" },
    { "id": 2, "name": "Platita" }
  ],
  "seller": {
    "id": 5,
    "firmName": "Moja Firma SRL",
    "cuiValue": "98765432",
    "address": "Str. Mea nr. 5",
    "county": "Ilfov",
    "city": "Bukareszt"
  }
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
