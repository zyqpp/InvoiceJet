# Klasa biznesowa: KontoBankowe

| Pole | Wartość |
|---|---|
| ID dokumentu | KLASA-KontoBankowe |
| Typ dokumentu | klasa biznesowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

KontoBankowe to rachunek bankowy firmy użytkownika, na który klient powinien przelać należność za wystawiony dokument. Każde konto posiada numer IBAN, nazwę banku i walutę. Na fakturze drukowane jest aktywne konto bankowe firmy wystawiającej dokument. Użytkownik może posiadać wiele kont w różnych walutach i wybrać, które z nich jest aktywne.

## Atrybuty biznesowe

| Nazwa atrybutu | Typ (biznesowy) | Opis | Wymagany |
|---|---|---|---|
| Identyfikator | liczba | Unikalny numer konta w systemie | Tak |
| Nazwa banku | tekst | Nazwa instytucji bankowej prowadzącej rachunek | Tak |
| IBAN | tekst | Międzynarodowy numer rachunku bankowego | Tak |
| Waluta | tekst (słownik) | Waluta konta: RON (lej rumuński) lub EUR (euro) | Tak |
| Aktywne | flaga | Określa, czy konto jest aktualnie używane do wystawiania dokumentów | Tak |

## Reguły biznesowe

- Każde konto bankowe jest przypisane do konkretnej firmy użytkownika.
- Firma może posiadać wiele kont bankowych w różnych walutach.
- Przy wystawianiu dokumentu system automatycznie wybiera pierwsze aktywne konto bankowej firmy.
- Jeśli firma nie posiada żadnego aktywnego konta bankowego, wystawienie dokumentu jest niemożliwe.
- Usunięcie konta bankowego powoduje nieodwracalne usunięcie wszystkich dokumentów, w których to konto zostało wskazane — jest to ryzyko utraty danych.

## Powiązania z innymi klasami

| Klasa powiązana | Typ powiązania | Opis |
|---|---|---|
| Firma | N:1 | Konto należy do jednej firmy użytkownika |
| Dokument | 1:N | Konto jest wskazane jako rachunek do zapłaty na wielu dokumentach |

## Odpowiednik techniczny

| Element | Lokalizacja |
|---|---|
| Encja DB | `dbo.BankAccount` |
| DTO | brak dedykowanego (dane w BankAccountDto) |
| Plik .cs | `InvoiceJet.Domain/Models/BankAccount.cs` |

## Wątpliwości i braki

- Kaskadowe usunięcie konta bankowego likwiduje powiązane dokumenty finansowe — brak mechanizmu ochrony historycznych danych.
- Brak obsługi waluty USD pomimo wzmianki w opisie produktu (obsługiwane: RON i EUR).
- Brak możliwości wskazania konkretnego konta przy tworzeniu dokumentu — system zawsze wybiera pierwsze aktywne.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
