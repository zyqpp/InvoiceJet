# Testy automatyczne — InvoiceJet

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-AUTO-INDEX |
| Typ dokumentu | informacja o stanie testów automatycznych |
| Wersja | 0.1 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Stan obecny

Projekt InvoiceJet **nie zawiera zaimplementowanych testów automatycznych** — ani po stronie backendu (ASP.NET Core 8), ani po stronie frontendu (Angular 16). Wszystkie testy są wykonywane manualnie zgodnie ze scenariuszami zawartymi w katalogu `../manualne/`.

Brak testów automatycznych jest świadomą decyzją na etapie MVP projektu. Poniżej przedstawiono propozycję zakresu i priorytetów dla przyszłej implementacji.

## Proponowany zakres testów automatycznych

### Testy jednostkowe backendu (xUnit + Moq)

| Obszar | Priorytet | Opis |
|---|---|---|
| `AuthService` (rejestracja, walidacja hasła, logowanie) | KRYTYCZNY | Weryfikacja wyrażeń regularnych hasła, unikalności e-mail, generowania JWT |
| `DocumentService` (generowanie numeru, inkrementacja serii) | KRYTYCZNY | Race condition numeracji — wymaga blokady transakcyjnej |
| `BankAccountService` (usunięcie z kaskadą) | KRYTYCZNY | Wykrycie anomalii CASCADE DELETE przed wywołaniem operacji |
| `ProductService` (unikalność nazwy) | WYSOKI | Weryfikacja zachowania przy naruszeniu UNIQUE INDEX |
| `FirmService` (integracja z ANAF) | ŚREDNI | Mock odpowiedzi ANAF, parsowanie danych |
| `DocumentPdfService` (wybór szablonu) | WYSOKI | Weryfikacja poprawnego wyboru szablonu dla każdego documentTypeId |

### Testy integracyjne API (WebApplicationFactory + xUnit)

Szczegółowe propozycje w `api/README.md`.

### Testy E2E (Cypress lub Playwright)

| Scenariusz | Priorytet | Opis |
|---|---|---|
| Rejestracja i pierwsze logowanie | WYSOKI | Pełny przepływ UI — formularz rejestracji do dashboardu |
| Pełny cykl faktury (dodanie → PDF) | WYSOKI | Od dodania firmy przez wystawienie faktury do pobrania PDF |
| Wygaśnięcie tokenu JWT | WYSOKI | TokenExpiredDialogComponent — dialog i przekierowanie |
| Dodanie klienta przez ANAF | ŚREDNI | Integracja z zewnętrznym serwisem (wymaga mockowania) |

## Rekomendowane narzędzia

| Rodzaj | Narzędzie | Uzasadnienie |
|---|---|---|
| Unit tests (backend) | xUnit + Moq | Standard dla .NET; prosta konfiguracja z WebApplicationFactory |
| Integration tests (backend) | WebApplicationFactory + EF InMemory | Testowanie endpointów bez zewnętrznej bazy danych |
| E2E tests (frontend) | Playwright | Natywna obsługa Angular; cross-browser; TypeScript |
| Testy obciążeniowe (race condition) | k6 | Symulacja równoczesnych żądań POST dla numeracji dokumentów |

## Priorytetyzacja anomalii do pokrycia automatycznego

| Anomalia | ID | Rekomendowany test |
|---|---|---|
| CASCADE DELETE kont bankowych usuwa faktury | A-KRIT-01 | xUnit integration test: weryfikacja zachowania DeleteBankAccount |
| Race condition numeracji dokumentów | A-02 | k6: 50 równoczesnych POST /Document/AddDocument |
| Hardcoded InvoiceDocument w PDF | A-KRIT-04 | xUnit unit test: DocumentPdfService.GetPdfTemplate(documentTypeId) |
| Globalny UNIQUE INDEX na nazwie produktu | A-03 | xUnit integration test: dwóch użytkowników, ta sama nazwa produktu |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
