# Zarządzanie seriami dokumentów — Dane, modele i mapowania

## DTO i encje

| Element | Rola |
|---|---|
| `DocumentSeriesDto` | Wejście i wyjście procesu serii dokumentów. |
| `DocumentSeries` | Encja serii dokumentów. |
| `DocumentType` | Encja typu dokumentu przypisywana do serii. |

---

## Mapowanie

| Źródło | Cel | Profil |
|---|---|---|
| `DocumentSeries` | `DocumentSeriesDto` | `DocumentSeriesProfile` |
| `DocumentSeriesDto` | `DocumentSeries` | `DocumentSeriesProfile` z regułą `DocumentTypeId <- DocumentType.Id` |
