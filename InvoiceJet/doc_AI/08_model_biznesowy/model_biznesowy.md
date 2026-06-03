# Model biznesowy InvoiceJet

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis produktu

InvoiceJet to aplikacja SaaS do fakturowania dla małych firm i freelancerów działających na rynku rumuńskim. Umożliwia wystawianie faktur, proform i stoern w języku rumuńskim z integracją ANAF (rumuński urząd skarbowy).

## Segment rynku

| Cecha | Opis |
|---|---|
| Rynek | Rumunia (system podatkowy CUI/NIP rumuński, integracja ANAF) |
| Klient docelowy | Mała firma, freelancer, solo-entrepreneur |
| Waluta | RON (lej rumuński), EUR, USD |
| Język interfejsu | Angielski (etykiety), Rumuński (nazwy statusów, pola danych) |

## Typy dokumentów obsługiwane

| ID | Typ | Opis |
|---|---|---|
| 1 | Factura (Faktura) | Zwykła faktura VAT |
| 2 | Factura Proforma (Proforma) | Dokument proforma (przed fakturą) |
| 3 | Factura Storno (Storno) | Faktura korygująca/anulująca |

## Kluczowe funkcjonalności

| Funkcja | Opis |
|---|---|
| Zarządzanie firmą | Dane własnej firmy wystawiającego |
| Zarządzanie klientami | Baza klientów z autouzupełnieniem ANAF |
| Katalog produktów | Produkty/usługi z cenami i stawkami VAT |
| Serie numeracji | Konfigurowalny format numeru dokumentu |
| Konta bankowe | Wiele kont bankowych per firma |
| Wystawianie dokumentów | Faktury, proformy, storna z pozycjami |
| Generowanie PDF | Pliki PDF przez QuestPDF |
| Dashboard | Statystyki i wykres miesięcznych przychodów |
| Integracja ANAF | Autouzupełnienie danych firmy po CUI |

## Architektura techniczna (skrót)

| Warstwa | Technologia |
|---|---|
| Frontend | Angular 16 + Angular Material |
| Backend | ASP.NET Core 8 (Clean Architecture) |
| Baza danych | SQL Server (EF Core 8 Code First) |
| Hosting | Azure (Azure Web Apps) |
| PDF | QuestPDF 2024.3.10 Community |
| Auth | JWT (HmacSha512, 10 min) + BCrypt |

## Ograniczenia modelu (dług techniczny)

| # | Ograniczenie |
|---|---|
| LT-01 | Token JWT wygasa po 10 minutach — brak refresh token |
| LT-02 | Brak soft-delete — usunięte dane przepadają bezpowrotnie |
| LT-03 | CASCADE DELETE konta bankowego usuwa wszystkie faktury |
| LT-04 | UNIQUE INDEX produktu globalny — brak izolacji między użytkownikami |
| LT-05 | Race condition przy numeracji dokumentów |
| LT-06 | Brak paginacji list |
| LT-07 | CORS tylko dla localhost — brak produkcyjnego origina frontendu |
| LT-08 | `GenerateInvoicePdf` hardkoduje szablon faktury zwykłej |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
