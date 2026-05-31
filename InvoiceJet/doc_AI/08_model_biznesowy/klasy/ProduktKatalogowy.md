# Klasa biznesowa: ProduktKatalogowy

| Pole | Wartość |
|---|---|
| ID dokumentu | KLASA-ProduktKatalogowy |
| Typ dokumentu | klasa biznesowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

ProduktKatalogowy to pozycja z katalogu produktów i usług firmy użytkownika, którą można dodać do dokumentu finansowego. Przechowuje domyślną cenę, stawkę VAT i jednostkę miary. Przy wystawianiu faktury produkt z katalogu służy jako wzorzec — rzeczywiste ceny na dokumencie są zapisywane jako migawka (snapshot) i mogą różnić się od aktualnej ceny katalogowej.

## Atrybuty biznesowe

| Nazwa atrybutu | Typ (biznesowy) | Opis | Wymagany |
|---|---|---|---|
| Identyfikator | liczba | Unikalny numer produktu w systemie | Tak |
| Nazwa | tekst | Nazwa produktu lub usługi (musi być unikalna w systemie) | Tak |
| Cena bazowa | liczba (decimal) | Domyślna cena jednostkowa produktu | Tak |
| Zawiera VAT | flaga | Określa, czy cena bazowa jest ceną brutto (z VAT) czy netto (bez VAT) | Tak |
| Stawka VAT | liczba (%) | Procent podatku VAT (np. 19%, 9%, 5%, 0%) | Tak |
| Jednostka miary | tekst | Jednostka, w której wyrażana jest ilość (szt., godz., kg, etc.) | Nie |

## Reguły biznesowe

- Nazwa produktu musi być unikalna w całym systemie — dwóch różnych użytkowników nie może mieć produktu o identycznej nazwie.
- Produkt przypisany jest do konkretnej firmy użytkownika i może być używany wyłącznie przez tę firmę.
- Zmiana ceny produktu w katalogu nie wpływa na już wystawione dokumenty — ceny na dokumentach są trwałymi migawkami.
- Przy dodawaniu pozycji do dokumentu użytkownik może wybrać produkt z katalogu lub stworzyć nowy produkt "w locie".
- Usunięcie produktu nie powoduje usunięcia pozycji dokumentów, które go zawierają.

## Powiązania z innymi klasami

| Klasa powiązana | Typ powiązania | Opis |
|---|---|---|
| Firma | N:1 | Produkt należy do katalogu konkretnej firmy |
| PozycjaDokumentu | 1:N | Produkt może być wymieniony w wielu pozycjach różnych dokumentów |

## Odpowiednik techniczny

| Element | Lokalizacja |
|---|---|
| Encja DB | `dbo.Product` |
| DTO | brak dedykowanego (dane w ProductDto) |
| Plik .cs | `InvoiceJet.Domain/Models/Product.cs` |

## Wątpliwości i braki

- Unikalność nazwy produktu jest globalna, nie per-firma — jest to prawdopodobnie niezamierzone ograniczenie.
- Powiązanie produktu z firmą (`UserFirmId`) jest opcjonalne na poziomie bazy danych — istnieje ryzyko produktów "osieroconych" (bez właściciela).
- Brak rozróżnienia między produktem katalogowym a produktem tworzonym ad hoc podczas wystawiania faktury.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
