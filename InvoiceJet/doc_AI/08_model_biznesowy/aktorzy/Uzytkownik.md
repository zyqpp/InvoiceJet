# Aktor: Uzytkownik

| Pole | Wartość |
|---|---|
| ID dokumentu | AKTOR-Uzytkownik |
| Typ dokumentu | opis aktora |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Uzytkownik to jedyna kategoria podmiotu ludzkiego w systemie InvoiceJet. Jest to osoba fizyczna — właściciel małej firmy, freelancer lub pracownik — która rejestruje konto w systemie i wystawia dokumenty finansowe w imieniu swojej firmy na rynku rumuńskim. System nie rozróżnia ról administratorskich i użytkownicze — każde konto ma identyczne uprawnienia.

## Tabela cech aktora

| Cecha | Opis |
|---|---|
| Aktor | Uzytkownik (osoba fizyczna posiadająca konto w systemie) |
| Alternatywne nazwy | Właściciel konta, wystawca faktur, freelancer |
| Liczba aktorów | Wiele — system SaaS wielodostępny |
| Typ dostępu | Przez przeglądarkę (interfejs webowy Angular) lub API (JWT) |
| Sposób uwierzytelnienia | Adres e-mail + hasło → token JWT (ważny 10 minut) |

## Cele biznesowe

| Priorytet | Cel | Opis |
|---|---|---|
| 1 | Wystawienie faktury | Szybkie wystawienie faktury VAT dla klienta rumuńskiego |
| 2 | Zarządzanie klientami | Budowanie i utrzymywanie bazy kontrahentów |
| 3 | Zarządzanie własną firmą | Aktualizacja danych firmy, kont bankowych, serii numeracji |
| 4 | Prowadzenie katalogu produktów | Utrzymywanie katalogu powtarzalnych produktów i usług |
| 5 | Generowanie PDF faktur | Pobranie faktury w formie pliku PDF gotowego do wysłania klientowi |
| 6 | Monitorowanie płatności | Śledzenie statusu wystawionych dokumentów (Nieopłacona / Opłacona) |
| 7 | Analiza przychodów | Przegląd statystyk i wykresu miesięcznych przychodów na dashboardzie |

## Uprawnienia

| Obszar | Działania dozwolone |
|---|---|
| Konto użytkownika | Rejestracja, logowanie, przeglądanie własnych danych |
| Firma | Dodawanie, edycja i usuwanie własnej firmy |
| Klient | Dodawanie, edycja, przeglądanie i usuwanie klientów z własnej bazy |
| Konto bankowe | Dodawanie, edycja, usuwanie kont bankowych firmy |
| Produkt | Dodawanie, edycja, przeglądanie i usuwanie produktów z katalogu |
| Seria numeracji | Konfigurowanie serii numeracji dla każdego typu dokumentu |
| Dokument | Tworzenie, edycja, usuwanie i pobieranie PDF dokumentów własnej firmy |
| Dashboard | Przeglądanie statystyk i wykresów dotyczących własnych dokumentów |

## Ograniczenia

| Ograniczenie | Opis |
|---|---|
| Izolacja danych | Użytkownik widzi wyłącznie dane należące do jego konta (firmy, klientów, dokumenty) |
| Brak ról administracyjnych | Nie ma możliwości zarządzania kontami innych użytkowników ani dostępu do danych innych firm |
| Sesja | Token JWT wygasa po 10 minutach — brak automatycznego odświeżenia sesji |
| Waluta | Obsługiwane waluty kont bankowych: RON i EUR (USD nieobsługiwane mimo wzmianki w opisie produktu) |
| Numeracja dokumentów | Użytkownik nie może ręcznie ustawić numeru dokumentu — numer generowany automatycznie z serii |
| Usunięcia | Brak soft-delete — usunięte dane (dokumenty, klienci, produkty) są bezpowrotnie tracone |

## Scenariusze użycia (podsumowanie)

| Scenariusz | Opis |
|---|---|
| UC-01: Rejestracja | Nowy użytkownik zakłada konto podając imię, nazwisko, e-mail i hasło |
| UC-02: Logowanie | Użytkownik loguje się i otrzymuje token JWT |
| UC-03: Dodanie firmy | Użytkownik wprowadza dane własnej firmy (z opcją autouzupełnienia ANAF po CUI) |
| UC-04: Dodanie klienta | Użytkownik dodaje kontrahenta do bazy (z opcją autouzupełnienia ANAF po CUI) |
| UC-05: Wystawienie faktury | Użytkownik tworzy fakturę, dodaje pozycje i zapisuje dokument |
| UC-06: Pobranie PDF | Użytkownik pobiera wygenerowaną fakturę w formacie PDF |
| UC-07: Zmiana statusu | Użytkownik oznacza fakturę jako opłaconą |
| UC-08: Przeglądanie dashboardu | Użytkownik sprawdza statystyki przychodów |

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
