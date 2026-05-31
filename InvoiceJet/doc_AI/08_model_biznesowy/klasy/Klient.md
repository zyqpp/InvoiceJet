# Klasa biznesowa: Klient

| Pole | Wartość |
|---|---|
| ID dokumentu | KLASA-Klient |
| Typ dokumentu | klasa biznesowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Klient to kontrahent (odbiorca faktury) — podmiot gospodarczy, na rzecz którego użytkownik wystawia dokumenty finansowe. Z perspektywy technicznej klient jest firmą z flagą oznaczającą go jako odbiorcę, jednak z perspektywy biznesowej pełni odrębną rolę: jest stroną transakcji wpisaną na fakturze jako nabywca. Dane klienta mogą być uzupełniane automatycznie z rejestru ANAF po podaniu numeru CUI.

## Atrybuty biznesowe

| Nazwa atrybutu | Typ (biznesowy) | Opis | Wymagany |
|---|---|---|---|
| Identyfikator | liczba | Unikalny numer klienta w systemie | Tak |
| Nazwa | tekst | Pełna nazwa firmy klienta | Tak |
| CUI | tekst | Rumuński numer identyfikacji podatkowej klienta | Tak |
| Numer rejestru handlowego | tekst | Numer wpisu w rumuńskim rejestrze handlowym | Nie |
| Adres | tekst | Pełny adres siedziby klienta | Tak |
| Okręg | tekst | Okręg (județ) siedziby klienta | Tak |
| Miasto | tekst | Miasto siedziby klienta | Tak |

## Reguły biznesowe

- Klient jest przypisany do konkretnego użytkownika (przez powiązanie UserFirm z flagą IsClient).
- Jeden użytkownik może posiadać wielu klientów w swojej bazie.
- Klient może być wskazany jako odbiorca na wielu dokumentach tego samego użytkownika.
- Dane klienta mogą być autouzupełnione z ANAF po podaniu numeru CUI.
- Usunięcie klienta nie usuwa dokumentów wystawionych na jego rzecz (brak kaskady po stronie rekordu klienta w dokumencie).
- Ten sam podmiot gospodarczy (CUI) może być zarejestrowany jako klient u wielu różnych użytkowników systemu.

## Powiązania z innymi klasami

| Klasa powiązana | Typ powiązania | Opis |
|---|---|---|
| Uzytkownik | N:M (przez UserFirm) | Klient należy do bazy kontrahentów użytkownika |
| Dokument | 1:N | Klient może być wskazany jako odbiorca wielu dokumentów |

## Odpowiednik techniczny

| Element | Lokalizacja |
|---|---|
| Encja DB | `dbo.Firm` (z `UserFirm.IsClient = true`) |
| DTO | brak dedykowanego (dane w FirmDto) |
| Plik .cs | `InvoiceJet.Domain/Models/Firm.cs` |

## Wątpliwości i braki

- Klient i własna firma użytkownika przechowywane są w tej samej tabeli bazy danych — rozróżnienie wyłącznie przez flagę IsClient w tabeli UserFirm.
- Dokument przechowuje odniesienie do klienta jako `ClientId → Firm.Id` (nullable) — dokument może być wystawiony bez wskazania klienta.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
