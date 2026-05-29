# Dane autouzupełniania dokumentu — Dane, modele i mapowania

## DTO odpowiedzi

| Pole `DocumentAutofillDto` | Typ |
|---|---|
| `Clients` | `List<FirmDto>` |
| `DocumentSeries` | `List<DocumentSeriesDto>` |
| `DocumentStatuses` | `List<DocumentStatusDto>` |
| `Products` | `List<ProductDto>` |

---

## Mapowania

| Źródło | Cel | Profil |
|---|---|---|
| `Firm` | `FirmDto` | `FirmProfile` |
| `DocumentSeries` | `DocumentSeriesDto` | `DocumentSeriesProfile` |
| `DocumentStatus` | `DocumentStatusDto` | `DocumentStatusProfile` |
| `Product` | `ProductDto` | `ProductProfile` |
