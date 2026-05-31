# Rejestr długu technicznego — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Definicja

Dług techniczny = zidentyfikowane problemy w kodzie, które wymagają naprawy aby system był bezpieczny, stabilny i skalowalny. Pogrupowane według priorytetu.

---

## 🔴 KRYTYCZNE — natychmiastowa naprawa zalecana

### LT-01: CASCADE DELETE konta bankowego usuwa faktury

| Cecha | Wartość |
|---|---|
| Plik | `InvoiceJetDbContextModelSnapshot.cs` |
| Problem | FK `Document.BankAccountId NOT NULL + ON DELETE CASCADE` — usunięcie konta kasuje wszystkie faktury |
| Ryzyko | **Utrata danych produkcyjnych** |
| Naprawka | Zmień na `ON DELETE RESTRICT` (lub `SET NULL` jeśli BankAccountId staje się nullable) |
| Wysiłek | Niski (1 migracja) |

### LT-02: Race condition na numerach dokumentów

| Cecha | Wartość |
|---|---|
| Plik | `DocumentService.cs › AddDocument()` |
| Problem | `CurrentNumber` inkrementowany bez blokady — możliwe duplikaty numerów |
| Ryzyko | **Duplikaty numerów faktur — problem prawny i podatkowy** |
| Naprawka | Pessimistic lock (`UPDLOCK`/`ROWLOCK`) lub optimistic lock (`RowVersion`) lub sekwencja DB |
| Wysiłek | Średni |

### LT-03: `GenerateInvoicePdf` hardkoduje szablon

| Cecha | Wartość |
|---|---|
| Plik | `DocumentService.cs › GenerateInvoicePdf()` |
| Problem | `new InvoiceDocument()` zamiast fabryki — proformy i storna generują PDF jako faktura |
| Ryzyko | **Błędne dokumenty PDF** |
| Naprawka | Zastąpić `new InvoiceDocument()` przez `InvoiceDocumentFactory.Create(document.DocumentTypeId, data)` |
| Wysiłek | Bardzo niski (1 linia kodu) |

### LT-04: `TransformToStorno` — brak atomowości

| Cecha | Wartość |
|---|---|
| Plik | `DocumentService.cs › TransformToStorno()` |
| Problem | `CompleteAsync()` wewnątrz pętli — możliwa częściowa konwersja |
| Ryzyko | **Niespójność danych** |
| Naprawka | Przenieś `CompleteAsync()` poza pętlę |
| Wysiłek | Bardzo niski (refactor 3 linii) |

---

## 🟠 WYSOKIE — naprawa w bieżącym sprincie

### LT-05: JWT wygasa po 10 minutach — brak refresh token

| Cecha | Wartość |
|---|---|
| Plik | `AuthService.cs › CreateToken()` |
| Problem | Sesja kończy się po 10 minutach; każda przerwa = wylogowanie |
| Wpływ | **Degradacja UX — frustracja użytkowników** |
| Naprawka | Dodać refresh token endpoint lub wydłużyć czas (60-120 min) |
| Wysiłek | Średni (refresh token endpoint + Angular interceptor) |

### LT-06: `Product.Name` — globalny UNIQUE INDEX

| Cecha | Wartość |
|---|---|
| Plik | `InvoiceJetDbContextModelSnapshot.cs` |
| Problem | Indeks globalny — dwóch użytkowników nie może mieć produktu o tej samej nazwie |
| Ryzyko | **Błędy 500 dla użytkowników produktywnych** |
| Naprawka | Zmień indeks na UNIQUE per `UserFirmId` + `Name` (composite unique) |
| Wysiłek | Niski (1 migracja + EF configuration) |

### LT-07: CORS tylko dla localhost

| Cecha | Wartość |
|---|---|
| Plik | `Program.cs` |
| Problem | `WithOrigins("http://localhost:4200")` — produkcja frontendowa bez CORS |
| Ryzyko | **Aplikacja nie działa z produkcyjnego domeny frontend** |
| Naprawka | Dodać produkcyjny URL frontendu lub odczytywać z konfiguracji |
| Wysiłek | Bardzo niski |

### LT-08: Token w localStorage podatny na XSS

| Cecha | Wartość |
|---|---|
| Pliki | `JwtInterceptor`, `AuthService` (Angular) |
| Problem | JWT w localStorage dostępny przez JavaScript — ryzyko XSS |
| Naprawka | Przepisać na HttpOnly cookie (wymaga zmian backend + frontend) |
| Wysiłek | Wysoki |

---

## 🟡 ŚREDNIE — backlog

### LT-09: Brak paginacji list

| Cecha | Wartość |
|---|---|
| Problem | GetTableRecords zwraca wszystkie dokumenty — wolne przy dużej liczbie |
| Naprawka | Dodać `skip/take` parametry i metadane paginacji |
| Wysiłek | Średni |

### LT-10: Brak soft-delete

| Problem | Usunięte rekordy przepadają bezpowrotnie |
| Naprawka | Dodać `DeletedAt` / `IsDeleted` flagę + global query filter |
| Wysiłek | Wysoki |

### LT-11: `console.log` w produkcji

| Problem | `console.log(invoiceAmounts)` i `console.log(incomeAmounts)` aktywne |
| Pliki | `dashboard.component.ts` |
| Naprawka | Usunąć lub zastąpić `environment.production` guardem |
| Wysiłek | Bardzo niski |

### LT-12: Brak retry logic dla ANAF

| Problem | Jeden timeout = błąd — brak retry z backoff |
| Naprawka | `Polly` library (retry + circuit breaker) |
| Wysiłek | Niski |

### LT-13: Catch-all 500 ujawnia stack trace

| Problem | `ex.Message` w odpowiedzi 500 — ujawnia szczegóły implementacji |
| Naprawka | W produkcji zwracać generyczny komunikat; logować stack trace wewnętrznie |
| Wysiłek | Niski |

### LT-14: Dwa `CompleteAsync()` w AddDocument

| Problem | Zapis dokumentu i inkrementacja serii w oddzielnych transakcjach |
| Naprawka | Użyć jednej transakcji obejmującej oba operacje |
| Wysiłek | Niski |

---

## Podsumowanie

| Priorytet | Liczba | Suma wysiłku szac. |
|---|---|---|
| Krytyczne | 4 | ~2 dni dev |
| Wysokie | 4 | ~5 dni dev |
| Średnie | 6 | ~10 dni dev |
| **Łącznie** | **14** | ~17 dni dev |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny — skonsolidowany dług techniczny. |
