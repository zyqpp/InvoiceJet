# Zarządzanie produktami — Logika aplikacyjna

## Pobranie listy

1. Serwis wywołuje `Products.GetUserFirmProductsAsync(currentUserId)`.
2. Dla pustej listy zwraca `new List<ProductDto>()`.
3. Dla niepustej listy mapuje wynik do `ICollection<ProductDto>`.

## Dodanie produktu

1. Serwis pobiera `userFirmId` użytkownika.
2. Gdy brak aktywnej firmy, rzuca `UserHasNoAssociatedFirmException`.
3. Serwis sprawdza duplikat nazwy przez `FindUserFirmProductByName(...)`.
4. Gdy duplikat istnieje, rzuca `ProductWithSameNameExistsException`.
5. Serwis mapuje `ProductDto` na `Product`, ustawia `UserFirmId` i zapisuje rekord.

## Edycja produktu

1. Serwis pobiera produkt po `Id`.
2. Gdy rekord nie istnieje, rzuca `Exception("Product not found.")`.
3. Serwis mapuje `productDto` na encję i wykonuje `CompleteAsync()`.

## Usuwanie produktów

1. Serwis iteruje po `productIds`.
2. Dla każdego rekordu sprawdza powiązania z `DocumentProducts`.
3. Gdy powiązanie istnieje, rzuca `ProductAssociatedWithInvoiceException`.
4. Gdy brak powiązań, usuwa produkt.
5. Po pętli wykonuje `CompleteAsync()`.
