# Klasa biznesowa: Firma

| Pole | Wartość |
|---|---|
| ID dokumentu | KLASA-Firma |
| Typ dokumentu | klasa biznesowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Firma reprezentuje podmiot gospodarczy, w imieniu którego użytkownik wystawia dokumenty finansowe. Klasa przechowuje dane rejestrowe rumuńskiej firmy — identyfikator podatkowy CUI, numer rejestru handlowego, adres siedziby. Firma jest węzłem, do którego przypisane są konta bankowe, serie numeracji, katalog produktów oraz wystawione dokumenty.

## Atrybuty biznesowe

| Nazwa atrybutu | Typ (biznesowy) | Opis | Wymagany |
|---|---|---|---|
| Identyfikator | liczba | Unikalny numer firmy w systemie | Tak |
| Nazwa | tekst | Pełna nazwa firmy | Tak |
| CUI | tekst | Cod Unic de Înregistrare — rumuński numer identyfikacji podatkowej (odpowiednik NIP) | Tak |
| Numer rejestru handlowego | tekst | Numer wpisu w rumuńskim rejestrze handlowym (RegCom) | Nie |
| Adres | tekst | Pełny adres siedziby firmy | Tak |
| Okręg | tekst | Okręg (județ) — jednostka podziału administracyjnego Rumunii | Tak |
| Miasto | tekst | Miasto siedziby firmy | Tak |

## Reguły biznesowe

- Firma jest powiązana z użytkownikiem przez relację pośrednią — jeden użytkownik może mieć wiele firm.
- Dane firmy mogą być uzupełniane automatycznie na podstawie numeru CUI przez integrację z ANAF (rumuński urząd skarbowy).
- Firma jest rozróżniana od klienta tylko przez flagę kontekstu — fizycznie dane przechowywane są w tej samej strukturze.
- Usunięcie firmy skutkuje usunięciem wszystkich powiązanych kont bankowych i dokumentów (kaskada).

## Powiązania z innymi klasami

| Klasa powiązana | Typ powiązania | Opis |
|---|---|---|
| Uzytkownik | N:M (przez UserFirm) | Firma należy do użytkownika; jeden użytkownik może mieć wiele firm |
| KontoBankowe | 1:N | Firma posiada wiele kont bankowych |
| SeriaDokumentow | 1:N | Firma posiada wiele serii numeracji dokumentów |
| ProduktKatalogowy | 1:N | Firma posiada katalog produktów i usług |
| Dokument | 1:N | Firma jest wystawcą wielu dokumentów finansowych |
| Klient | N:M (przez UserFirm) | Firma może mieć wielu klientów (którzy sami są firmami) |

## Odpowiednik techniczny

| Element | Lokalizacja |
|---|---|
| Encja DB | [dbo.Firm](../../05_model_danych/01_db/dbo/dbo.Firm.md) |
| DTO | brak dedykowanego (dane w FirmDto) |
| Plik .cs | `InvoiceJet.Domain/Models/Firm.cs` |

## Wątpliwości i braki

- Brak indeksu na CUI — wyszukiwanie po numerze podatkowym jest nieoptymalne.
- Niespójność pola RegCom: baza danych wymaga wartości (NOT NULL), ale interfejs aplikacji traktuje je jako opcjonalne — możliwy błąd przy zapisie pustego RegCom.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
