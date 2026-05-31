# Klasa biznesowa: SeriaDokumentow

| Pole | Wartość |
|---|---|
| ID dokumentu | KLASA-SeriaDokumentow |
| Typ dokumentu | klasa biznesowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

SeriaDokumentow to konfiguracja numeracji dokumentów finansowych firmy. Definiuje prefiks (np. "FV", "PRO", "STORNO") oraz bieżący numer, który jest automatycznie inkrementowany po każdym wystawieniu dokumentu. Dzięki temu każdy wystawiony dokument otrzymuje unikalny, czytelny numer zgodny z wymaganiami rumuńskiego prawa podatkowego. Każda seria jest przypisana do określonego typu dokumentu.

## Atrybuty biznesowe

| Nazwa atrybutu | Typ (biznesowy) | Opis | Wymagany |
|---|---|---|---|
| Identyfikator | liczba | Unikalny numer serii w systemie | Tak |
| Prefiks serii | tekst | Część tekstowa numeru dokumentu (np. "FV", "PRO") | Tak |
| Numer startowy | liczba | Numer, od którego zaczyna się numeracja | Tak |
| Numer bieżący | liczba | Aktualny numer — inkrementowany automatycznie po każdym wystawieniu | Tak |
| Domyślna | flaga | Czy seria jest domyślna dla danego typu dokumentu | Tak |
| Typ dokumentu | referencja (słownik) | Typ dokumentu obsługiwany przez tę serię (Faktura / Proforma / Storno) | Nie |

## Reguły biznesowe

- Każda firma może posiadać wiele serii numeracji, jednak dla każdego typu dokumentu powinna być wyznaczona jedna seria domyślna.
- Format numeru dokumentu: prefiks + numer bieżący uzupełniony zerami do 4 cyfr (np. "FV0005").
- Numer bieżący jest inkrementowany natychmiast po wystawieniu dokumentu i nie cofa się przy anulowaniu.
- Seria przypisana jest do konkretnej firmy użytkownika — numeracja jest niezależna dla każdej firmy.
- Równoczesne wystawianie dokumentów przez wielu użytkowników może skutkować zduplikowanymi numerami (brak blokady współbieżnej).

## Powiązania z innymi klasami

| Klasa powiązana | Typ powiązania | Opis |
|---|---|---|
| Firma | N:1 | Seria numeracji należy do konkretnej firmy |
| Dokument | 1:N (pośrednio) | Seria definiuje format numerów wystawianych dokumentów; powiązanie przez pole DocumentNumber |

## Odpowiednik techniczny

| Element | Lokalizacja |
|---|---|
| Encja DB | `dbo.DocumentSeries` |
| DTO | brak dedykowanego (dane w DocumentSeriesDto) |
| Plik .cs | `InvoiceJet.Domain/Models/DocumentSeries.cs` |

## Wątpliwości i braki

- Brak blokady (lock/transakcja) przy inkrementacji numeru — przy równoczesnym tworzeniu dokumentów możliwe zduplikowane numery.
- Brak ograniczenia na poziomie bazy danych, że tylko jedna seria na typ dokumentu może być oznaczona jako domyślna.
- Dokument nie przechowuje odniesienia do serii (brak `SeriesId`) — jedynym śladem jest wygenerowany ciąg tekstowy `DocumentNumber`.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
