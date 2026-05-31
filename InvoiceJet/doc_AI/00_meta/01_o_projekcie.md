# O projekcie — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Faza | 2 — Szkielet dokumentacji |

## 1. Opis biznesowy

**InvoiceJet** to webowa aplikacja do wystawiania faktur i proform, zbudowana z myślą o firmach operujących na **rynku rumuńskim**. System umożliwia:

- Rejestrację i zarządzanie własną firmą (wystawca faktury)
- Zarządzanie klientami (odbiorcy faktur)
- Zarządzanie katalogiem produktów i usług
- Zarządzanie kontami bankowymi
- Definiowanie serii dokumentów (np. "FV0001", "PRO0001")
- Wystawianie trzech typów dokumentów:
  - **Faktura zwykła** (`Factura`) — DocumentTypeId = 1
  - **Faktura proforma** (`Factura Proforma`) — DocumentTypeId = 2
  - **Faktura storno** (`Factura Storno`) — DocumentTypeId = 3
- Generowanie i pobieranie dokumentów w formacie PDF
- Przekształcenie faktur zwykłych w storna (operacja TransformToStorno)
- Dashboard z wykresem miesięcznych przychodów i statystykami

## 2. Cel systemu

Uproszczenie procesu fakturowania dla małych firm i freelancerów z Rumunii — z integracją z ANAF (rumuński urząd skarbowy) do automatycznego uzupełniania danych firmy na podstawie numeru CUI.

## 3. Zakres funkcjonalny (MVP)

| Obszar | Funkcje |
|---|---|
| Autentykacja | Rejestracja, logowanie (JWT) |
| Firma | Zarządzanie własną firmą, integracja ANAF |
| Klienci | CRUD klientów |
| Produkty | CRUD produktów/usług |
| Konta bankowe | CRUD kont bankowych |
| Serie dokumentów | CRUD serii z autonumeracją |
| Dokumenty | Tworzenie, edycja, usuwanie, PDF |
| Raporty | Dashboard (statystyki, wykres miesięczny) |

## 4. Środowiska

| Środowisko | API URL | UI URL |
|---|---|---|
| Lokalne | `https://localhost:7229/api` | `http://localhost:4200` |
| Produkcyjne | `https://invoicejetapi.azurewebsites.net/api` | — |

## 5. Kluczowe decyzje projektowe

| Decyzja | Wybór | Uzasadnienie |
|---|---|---|
| Architektura API | Clean Architecture (4 warstwy) | Separacja odpowiedzialności |
| ORM | EF Core 8 Code First | Migracje, LINQ, silne typowanie |
| Autentykacja | JWT Bearer (HmacSha512, 10 min) | Bezstanowość API |
| PDF | QuestPDF Community 2024.3.10 | Darmowa, silna biblioteka .NET |
| Waluta | RON (Ron) i EUR | Rynek rumuński |
| Język UI | Angielski (interfejs) + rumuński (nazwy dokumentów) | Mieszany |

## 6. Znane ograniczenia i długi techniczne

| # | Ograniczenie |
|---|---|
| LT-01 | JWT wygasa po **10 minutach** — brak refresh token; użytkownik musi się zalogować ponownie |
| LT-02 | `GenerateDocumentPdf` zawsze generuje fakturę zwykłą (hardcoded `new InvoiceDocument()`) |
| LT-03 | Brak soft-delete — usunięte dokumenty i produkty są trwale kasowane |
| LT-04 | Race condition przy numerowaniu dokumentów (brak blokady `DocumentSeries.CurrentNumber`) |
| LT-05 | `TransformToStorno` nie jest atomowy — brak transakcji ogarniającej całą operację |
| LT-06 | Co najmniej 19 aktywnych `console.log` w kodzie Angular (front-end produkcyjny) |
| LT-07 | Factories do generowania PDF są zakomentowane w `Program.cs` |
| LT-08 | Wiele DTO zawiera typy domenowe zamiast dedykowanych DTO (naruszenie separacji warstw) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny na podstawie eksploracji kodu. |
