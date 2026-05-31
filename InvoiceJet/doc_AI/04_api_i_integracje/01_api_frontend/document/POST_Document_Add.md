# POST /api/Document/AddDocument — Dodanie dokumentu

| Atrybut | Wartość |
|---|---|
| ID | API-22 |
| Metoda | POST |
| URL | `/api/Document/AddDocument` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `DocumentController.AddDocument` |
| Serwis | `IDocumentService.AddDocument` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

## Request

### Body (JSON) — `DocumentRequestDto`

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `id` | `int` | NIE | Ignorowany przy tworzeniu |
| `documentNumber` | `string?` | NIE | Ignorowany — generowany przez serwis: `SeriesName + CurrentNumber.ToString("D4")` |
| `client` | `FirmDto` | TAK | Firma klienta (musi mieć poprawne `id`) |
| `issueDate` | `DateTime` | TAK | Data wystawienia |
| `dueDate` | `DateTime?` | NIE | Termin płatności |
| `documentSeries` | `DocumentSeriesDto?` | TAK | Seria dokumentu (z `id`, `seriesName`, `currentNumber`, `documentType.id`) |
| `documentType` | `DocumentType?` | NIE | Typ (redundantny — pobierany z `documentSeries.documentType`) |
| `documentStatus` | `DocumentStatus?` | NIE | Ignorowany przy tworzeniu — zawsze `Unpaid` |
| `products` | `DocumentProductRequestDto[]` | TAK | Lista pozycji |

**Pole `products[i]`:**
| Pole | Typ | Opis |
|---|---|---|
| `id` | `int` | `0` = nowy produkt, `>0` = istniejący (lookup po `name`) |
| `name` | `string` | Nazwa produktu |
| `unitPrice` | `decimal` | Cena jednostkowa |
| `totalPrice` | `decimal` | Cena całkowita pozycji |
| `containsTva` | `bool` | Czy zawiera VAT |
| `unitOfMeasurement` | `string` | Jednostka miary |
| `tvaValue` | `int` | Procent VAT |
| `quantity` | `int` | Ilość |

**Przykład:**
```json
{
  "id": 0,
  "client": { "id": 10, "name": "Client SRL", "cui": "87654321", "regCom": "J40/1/2019", "address": "STR. 1", "county": "IASI", "city": "IASI" },
  "issueDate": "2026-05-31T00:00:00",
  "dueDate": "2026-06-14T00:00:00",
  "documentSeries": {
    "id": 1,
    "seriesName": "FV",
    "currentNumber": 5,
    "documentType": { "id": 1, "name": "Factura" }
  },
  "products": [
    {
      "id": 1,
      "name": "Consulting Services",
      "unitPrice": 100.00,
      "totalPrice": 119.00,
      "containsTva": true,
      "unitOfMeasurement": "hr",
      "tvaValue": 19,
      "quantity": 1
    }
  ]
}
```

## Response

### 200 OK — zwraca wejściowy `DocumentRequestDto` (bez modyfikacji numeru itp.)

### Błędy

| Status HTTP | Wyjątek | Warunek |
|---|---|---|
| 400 Bad Request | `UserHasNoAssociatedFirmException` | Użytkownik nie ma aktywnej firmy |
| 400 Bad Request | `NoBankAccountAddedException` | Brak aktywnego konta bankowego |
| 500 | `Exception("Product not found.")` | Produkt z `id > 0` nie znaleziony po nazwie |

## Algorytm (klucz)

1. Pobierz `userFirmId` z JWT
2. Pobierz pierwsze aktywne konto bankowe (`WHERE IsActive=true`)
3. Generuj numer: `SeriesName + CurrentNumber.ToString("D4")`
4. Nowy dokument ze statusem `Unpaid` (Id=1)
5. `UpdateDocumentProducts()`: usuń istniejące, dodaj nowe
6. Inkrementacja `DocumentSeries.CurrentNumber`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
