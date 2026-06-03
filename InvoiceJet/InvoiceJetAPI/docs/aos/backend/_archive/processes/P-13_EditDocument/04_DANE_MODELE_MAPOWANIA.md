# Edycja dokumentu — Dane, modele i mapowania

## DTO i encje

| Element | Rola |
|---|---|
| `DocumentRequestDto` | Wejście i wyjście procesu. |
| `Document` | Encja główna aktualizowana w procesie. |
| `DocumentProduct` | Pozycje dokumentu usuwane i tworzone ponownie. |
| `Product` | Encja produktu dla pozycji dokumentu. |

---

## Mapowania

| Źródło | Cel | Mechanizm |
|---|---|---|
| `DocumentProductRequestDto` | `Product` | `_mapper.Map<Product>(documentProductDto)` |
| `Document` | `DocumentRequestDto` | `DocumentProfile` (używany w innych endpointach odczytu) |
