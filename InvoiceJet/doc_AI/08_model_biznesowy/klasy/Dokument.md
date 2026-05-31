# Klasa biznesowa: Dokument

| Pole | Wartość |
|---|---|
| ID dokumentu | KLASA-Dokument |
| Typ dokumentu | klasa biznesowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Dokument to centralny byt biznesowy systemu InvoiceJet — reprezentuje wystawiony dokument finansowy (fakturę, proformę lub storno). Łączy firmę wystawiającą z klientem, wskazuje konto bankowe do zapłaty, zawiera listę pozycji z produktami/usługami oraz sumy wartości netto i brutto. Dokument może być pobrany w formacie PDF i odzwierciedla stan danych z chwili wystawienia.

## Atrybuty biznesowe

| Nazwa atrybutu | Typ (biznesowy) | Opis | Wymagany |
|---|---|---|---|
| Identyfikator | liczba | Unikalny numer dokumentu w systemie | Tak |
| Numer dokumentu | tekst | Czytelny numer np. "FV0005" — generowany z serii numeracji | Tak |
| Data wystawienia | data | Data, w której dokument został wystawiony | Tak |
| Termin płatności | data | Data, do której należy uregulować należność | Nie |
| Wartość netto | liczba (decimal) | Łączna suma wartości pozycji bez podatku VAT | Tak |
| Wartość brutto | liczba (decimal) | Łączna suma wartości pozycji z podatkiem VAT | Tak |
| Typ dokumentu | tekst (słownik) | Rodzaj dokumentu: Faktura / Proforma / Storno | Tak |
| Status | tekst (słownik) | Stan płatności: Nieopłacona / Opłacona | Tak |
| Firma wystawiająca | referencja | Firma użytkownika, która wystawia dokument | Tak |
| Klient (odbiorca) | referencja | Kontrahent, dla którego wystawiono dokument | Nie |
| Konto bankowe | referencja | Rachunek bankowy wskazany jako numer do przelewu | Tak |

## Reguły biznesowe

- Każdy dokument musi być przypisany do firmy wystawiającej i posiadać wskazane aktywne konto bankowe.
- Numer dokumentu generowany jest automatycznie z domyślnej serii numeracji dla danego typu dokumentu.
- Wartość netto i brutto wyliczane są automatycznie jako suma wszystkich pozycji dokumentu.
- Dokument może być wystawiony bez wskazania klienta (pole opcjonalne).
- Statusy dokumentu: Nieopłacona (domyślny), Opłacona — zmieniany ręcznie przez użytkownika.
- Zmiana pozycji dokumentu przy edycji zastępuje kompletnie poprzedni zestaw pozycji.
- Dokument może być wygenerowany i pobrany jako plik PDF.
- Usunięcie konta bankowego przypisanego do dokumentu powoduje nieodwracalne usunięcie dokumentu.

## Powiązania z innymi klasami

| Klasa powiązana | Typ powiązania | Opis |
|---|---|---|
| Firma | N:1 | Firma wystawiająca dokument |
| Klient | N:1 | Odbiorca dokumentu (opcjonalny) |
| KontoBankowe | N:1 | Konto wskazane na dokumencie jako numer do zapłaty |
| SeriaDokumentow | N:1 (pośrednio) | Seria definiująca format numeru dokumentu |
| PozycjaDokumentu | 1:N | Pozycje (linie) dokumentu zawierające produkty/usługi |

## Odpowiednik techniczny

| Element | Lokalizacja |
|---|---|
| Encja DB | `dbo.Document` |
| DTO | brak dedykowanego (dane w DocumentDto / DocumentRequestDto) |
| Plik .cs | `InvoiceJet.Domain/Models/Document.cs` |

## Wątpliwości i braki

- Brak unikalnego ograniczenia na numerze dokumentu — zduplikowany numer jest możliwy przy race condition.
- Pola `UserFirmId` i `DocumentTypeId` są nullable na poziomie bazy, mimo że biznesowo są wymagane.
- Kaskadowe usunięcie dokumentu po usunięciu konta bankowego jest ryzykiem utraty historii finansowej.
- Brak soft-delete — usunięte dokumenty znikają bezpowrotnie.
- PDF generowany wyłącznie dla faktury zwykłej (Factura) — szablony Proforma i Storno nieobsługiwane.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
