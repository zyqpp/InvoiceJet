# Klasa biznesowa: Uzytkownik

| Pole | Wartość |
|---|---|
| ID dokumentu | KLASA-Uzytkownik |
| Typ dokumentu | klasa biznesowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Uzytkownik to konto osoby fizycznej zarejestrowanej w systemie InvoiceJet. Reprezentuje podmiot, który może posiadać jedną lub więcej firm i wystawiać dokumenty finansowe w ich imieniu. Uwierzytelnienie użytkownika oparte jest na adresie e-mail i haśle, a autoryzacja odbywa się przez token JWT.

## Atrybuty biznesowe

| Nazwa atrybutu | Typ (biznesowy) | Opis | Wymagany |
|---|---|---|---|
| Identyfikator | tekst (GUID) | Unikalny identyfikator konta w systemie | Tak |
| Imię | tekst | Imię właściciela konta | Tak |
| Nazwisko | tekst | Nazwisko właściciela konta | Tak |
| Adres e-mail | tekst | Adres e-mail — służy jako login; musi być unikalny w systemie | Tak |
| Hasło | tekst (zaszyfrowany) | Hasło dostępu przechowywane w formie skrótu BCrypt | Tak |
| Rola | tekst | Uprawnienia systemowe (aktualnie zawsze: "User") | Tak |
| Aktywna firma | referencja | Wskazanie na firmę, w kontekście której użytkownik aktualnie pracuje | Nie |

## Reguły biznesowe

- Każdy użytkownik musi posiadać unikalny adres e-mail w całym systemie.
- Jeden użytkownik może być powiązany z wieloma firmami (własna firma lub klient).
- Użytkownik w danej chwili pracuje w kontekście jednej aktywnej firmy (aktywna firma może być nieokreślona, gdy użytkownik nie dodał jeszcze żadnej firmy).
- Rola użytkownika jest jednolita — system nie rozróżnia administratorów i zwykłych użytkowników na poziomie danych (brak uprawnień wielopoziomowych).
- Usunięcie użytkownika kaskadowo usuwa wszystkie jego powiązania z firmami, konta bankowe i dokumenty.

## Powiązania z innymi klasami

| Klasa powiązana | Typ powiązania | Opis |
|---|---|---|
| Firma | N:M (przez UserFirm) | Użytkownik może posiadać wiele firm; firma może należeć do wielu użytkowników |
| Klient | N:M (przez UserFirm) | Klienci użytkownika przechowywani są w tej samej strukturze co firmy własne |

## Odpowiednik techniczny

| Element | Lokalizacja |
|---|---|
| Encja DB | [dbo.User](../../05_model_danych/01_db/dbo/dbo.User.md) |
| DTO | brak wyodrębnionego DTO-Uzytkownik (dane zwracane w odpowiedzi JWT) |
| Plik .cs | `InvoiceJet.Domain/Models/User.cs` |

## Wątpliwości i braki

- Rola "User" jest hardcoded — system nie obsługuje ról administratora ani moderatora.
- Brak mechanizmu odświeżania tokenu JWT (token wygasa po 10 minutach, brak refresh token).
- Unikalność e-mail egzekwowana tylko przez kod aplikacji, brak indeksu UNIQUE na poziomie bazy danych.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
