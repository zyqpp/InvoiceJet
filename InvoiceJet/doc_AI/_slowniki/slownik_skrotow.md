# S-04. Słownik skrótów — InvoiceJet

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| ID | S-04 |
| Nazwa | Słownik skrótów |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Wersja | 0.1 |
| Data | 2026-05-31 |
| Status | Szkic |
| Plik | `doc_AI/_slowniki/slownik_skrotow.md` |

## Streszczenie

Słownik zawiera pełne rozwinięcia i krótkie objaśnienia wszystkich skrótów używanych w dokumentacji AOS projektu InvoiceJet. Skróty uporządkowane są alfabetycznie. Przy każdym skrócie podano kontekst użycia w projekcie. Skróty domenowe (rumuskie) opatrzone są tłumaczeniem na polski.

---

## Tabela skrótów

| Skrót | Rozwinięcie | Kontekst w projekcie |
|---|---|---|
| ANAF | Agenția Națională de Administrare Fiscală | Rumuński urząd skarbowy i rejestr firm. System InvoiceJet integruje się z API ANAF w celu weryfikacji CUI. Patrz: `INT-ANAF`. |
| AOS | Analiza i Opis Systemu | Typ dokumentacji tworzonej w projekcie InvoiceJet. Obejmuje opis ekranów, procesów, algorytmów, endpointów i encji. |
| API | Application Programming Interface | Interfejs HTTP backendu ASP.NET Core. Endpointy identyfikowane prefiksem `API-`. |
| BPMN | Business Process Model and Notation | Notacja diagramów procesów biznesowych. Używana do modelowania przepływów pracy w InvoiceJet. Artefakty prefiksu `BPMN-`. |
| CRUD | Create, Read, Update, Delete | Cztery podstawowe operacje na danych. Realizowane przez endpointy REST i repozytoria EF Core w projekcie. |
| CUI | Cod Unic de Identificare | Rumuński unikalny numer identyfikacyjny firmy (odpowiednik polskiego NIP). Przechowywany w polu `Firm.CUI`. |
| DI | Dependency Injection | Mechanizm wstrzykiwania zależności ASP.NET Core. Konfigurowany w `Program.cs`. Patrz: słownik techniczny. |
| DoD | Definition of Done | Kryteria ukończenia zadania dokumentacyjnego lub funkcjonalności. Stosowane w wytycznych projektu. |
| DTO | Data Transfer Object | Obiekt do przenoszenia danych między warstwami. Wszystkie endpointy używają DTO. Artefakty prefiksu `DTO-`. |
| EF | Entity Framework | Skrót od Entity Framework Core — ORM używany w projekcie. Pełna nazwa: EF Core 8. |
| ERD | Entity Relationship Diagram | Diagram związków encji bazy danych. Opisuje 10 encji projektu InvoiceJet. |
| FK | Foreign Key | Klucz obcy — pole w tabeli SQL Server odwołujące się do klucza głównego innej tabeli. Np. `Document.UserFirmId`. |
| HTTP | HyperText Transfer Protocol | Protokół komunikacyjny między Angular (frontendem) a ASP.NET Core (backendem). Metody: GET, POST, PUT, DELETE. |
| JWT | JSON Web Token | Token uwierzytelniający generowany przez backend. HmacSha512, ważność 10 minut. Patrz: słownik techniczny. |
| ORM | Object-Relational Mapper | Warstwa mapowania między obiektami C# a tabelami SQL Server. W projekcie: EF Core 8. |
| PDF | Portable Document Format | Format dokumentów generowanych w projekcie (faktury). Biblioteka: QuestPDF Community. |
| PK | Primary Key | Klucz główny — unikalny identyfikator rekordu w tabeli. Np. `Document.Id`, `Firm.Id`. |
| RAG | Retrieval-Augmented Generation | Technika uzupełniania wiedzy modelu AI danymi z zewnętrznego indeksu (tu: dokumentacją projektu). Stosowana przy pracy agenta nad dokumentacją AOS. |
| RON | — (symbol waluty ISO 4217) | Leu rumuński — waluta dokumentów wystawianych w InvoiceJet. Jedyna obsługiwana waluta. |
| SPA | Single Page Application | Architektura frontendu Angular — jedna strona HTML, przejścia bez pełnego przeładowania. |
| TVA | Taxa pe Valoarea Adăugată | Rumuński podatek VAT (odpowiednik polskiego VAT). Standardowa stawka: 19%. Przechowywana w `Product.TVA`. |
| UC | Use Case | Przypadek użycia — scenariusz interakcji użytkownika z systemem. Artefakty prefiksu `UC-`. |
| UoW | Unit of Work | Wzorzec agregujący repozytoria. `CompleteAsync()` = `SaveChangesAsync()`. Patrz: słownik techniczny. |

---

## Wątpliwości i braki

| ID | Wątpliwość | Status |
|---|---|---|
| W-01 | Skrót `RACI` wymieniony w wytycznych `07_mapowania_i_slowniki.md` (sekcja D) — nie pojawia się w dokumentacji projektu. Pominięty. | Do_zdefiniowania |
| W-02 | Skrót `BCrypt` — używany jako skrót, choć jest pełną nazwą własną biblioteki. Nie wprowadzono do tabeli jako skrót. | Do_zdefiniowania |
| W-03 | `RegCom` (numer rejestracji w rejestrze handlowym) — wspomniany w `slownik_pojec.md`, brak skrótu. Nie wprowadzono. | Do_zdefiniowania |

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — 23 skróty. |
