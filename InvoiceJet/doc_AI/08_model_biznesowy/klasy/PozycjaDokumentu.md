# Klasa biznesowa: PozycjaDokumentu

| Pole | Wartość |
|---|---|
| ID dokumentu | KLASA-PozycjaDokumentu |
| Typ dokumentu | klasa biznesowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

PozycjaDokumentu to pojedyncza linia pozycji na fakturze — konkretny produkt lub usługa z określoną ilością i ceną z chwili wystawienia. Pozycja przechowuje migawkę cenową (snapshot), niezależną od aktualnej ceny w katalogu produktów. Suma wartości wszystkich pozycji dokumentu stanowi jego wartość netto i brutto.

## Atrybuty biznesowe

| Nazwa atrybutu | Typ (biznesowy) | Opis | Wymagany |
|---|---|---|---|
| Identyfikator | liczba | Unikalny numer pozycji w systemie | Tak |
| Ilość | liczba (decimal) | Ilość produktu lub usługi (może być ułamkowa, np. 2,5 godz.) | Tak |
| Cena jednostkowa | liczba (decimal) | Cena za jednostkę z chwili wystawienia dokumentu (migawka) | Tak |
| Wartość całkowita pozycji | liczba (decimal) | Cena jednostkowa × ilość (z VAT lub bez, zależnie od ustawień produktu) | Tak |
| Produkt | referencja | Produkt lub usługa z katalogu, której dotyczy pozycja | Nie |
| Dokument | referencja | Dokument finansowy, do którego należy pozycja | Tak |

## Reguły biznesowe

- Każda pozycja dokumentu jest nierozłącznie powiązana z dokumentem finansowym.
- Cena jednostkowa i wartość całkowita pozycji są zapisywane jako migawka z chwili wystawienia i nie zmieniają się przy późniejszej modyfikacji ceny katalogu produktów.
- Ilość może być ułamkowa, co umożliwia fakturowanie usług rozliczanych godzinowo lub towarów sprzedawanych na wagę.
- Przy edycji dokumentu wszystkie poprzednie pozycje są usuwane i zastępowane nowym zestawem — brak aktualizacji częściowej.
- Pozycja może odwoływać się do produktu z katalogu lub być pozycją jednorazową (ad hoc), która nie ma odpowiednika w katalogu.
- Usunięcie produktu z katalogu nie usuwa pozycji dokumentów, które go zawierają (brak kaskady).

## Powiązania z innymi klasami

| Klasa powiązana | Typ powiązania | Opis |
|---|---|---|
| Dokument | N:1 | Pozycja należy do jednego dokumentu finansowego |
| ProduktKatalogowy | N:1 | Pozycja odwołuje się do produktu z katalogu (opcjonalnie) |

## Odpowiednik techniczny

| Element | Lokalizacja |
|---|---|
| Encja DB | [dbo.DocumentProduct](../../05_model_danych/01_db/dbo/dbo.DocumentProduct.md) |
| DTO | brak dedykowanego (dane w DocumentProductDto / DocumentProductRequestDto) |
| Plik .cs | `InvoiceJet.Domain/Models/DocumentProduct.cs` |

## Wątpliwości i braki

- Pola `DocumentId` i `ProductId` są nullable na poziomie bazy danych — pozycja może technicznie istnieć bez dokumentu (anomalia).
- Brak kolumny przechowującej stawkę VAT pozycji — informacja o VAT przechowywana wyłącznie w produkcie z katalogu; jeśli produkt zostanie usunięty, stawka VAT jest tracona.
- Przy edycji dokumentu stosowane jest "usuń wszystkie i dodaj od nowa" — brak historii zmian pozycji.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
