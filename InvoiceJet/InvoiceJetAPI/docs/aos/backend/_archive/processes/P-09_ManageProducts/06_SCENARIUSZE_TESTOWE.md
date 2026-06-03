# Zarządzanie produktami — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Pobranie listy produktów | Użytkownik ma aktywną firmę. | `200 OK` i lista produktów tej firmy. |
| TC-02 | Dodanie produktu | Brak duplikatu nazwy. | `200 OK` i nowy `ProductDto`. |
| TC-03 | Edycja produktu | Produkt istnieje. | `200 OK` i zaktualizowany `ProductDto`. |
| TC-04 | Usunięcie produktu bez powiązań | Brak `DocumentProduct` dla produktu. | `200 OK` i usunięty rekord. |

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Duplikat nazwy produktu | Istnieje produkt o tej samej nazwie. | `500 Internal Server Error`, komunikat z `ProductWithSameNameExistsException`. |
| TC-N02 | Usunięcie produktu powiązanego z dokumentem | Istnieje `DocumentProduct` dla produktu. | `400 Bad Request`, komunikat z `ProductAssociatedWithInvoiceException`. |
| TC-N03 | Edycja nieistniejącego produktu | Brak rekordu o `Id`. | `500 Internal Server Error`, komunikat `Product not found.` |
