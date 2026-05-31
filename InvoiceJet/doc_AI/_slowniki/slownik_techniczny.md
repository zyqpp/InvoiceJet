# S-02. Słownik pojęć technicznych — InvoiceJet

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| ID | S-02 |
| Nazwa | Słownik pojęć technicznych |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Wersja | 0.1 |
| Data | 2026-05-31 |
| Status | Szkic |
| Plik | `doc_AI/_slowniki/slownik_techniczny.md` |

## Streszczenie

Słownik definiuje pojęcia techniczne używane w kodzie źródłowym i dokumentacji projektu InvoiceJet. Definicje odnoszą się bezpośrednio do technologii użytych w projekcie: ASP.NET Core 8, EF Core 8, Angular 16 i SQL Server. Pojęcia cytowane są w formie 1:1 z kodu źródłowego.

---

## Pojęcia techniczne

### DTO (Data Transfer Object) {#dto}

Obiekt wyłącznie do przenoszenia danych między warstwami aplikacji — bez logiki biznesowej. W projekcie InvoiceJet każdy endpoint przyjmuje i zwraca DTO, nigdy encji bazodanowych. Konwencja nazewnicza: sufiks `Dto`, np. `RegisterUserDto`, `AddDocumentDto`, `GetDocumentDto`. Mapowanie DTO ↔ encja realizowane przez AutoMapper.

### LINQ (Language Integrated Query) {#linq}

Wbudowany w C# mechanizm zapytań do kolekcji i baz danych. W projekcie używany przez EF Core do budowania zapytań SQL. Zapytania LINQ identyfikowane prefiksem `LINQ-` w dokumentacji, np. `LINQ-GetDocumentById`. Kluczowe metody: `Where()`, `Select()`, `Include()`, `ThenInclude()`, `FirstOrDefaultAsync()`, `ToListAsync()`.

### endpoint (punkt wejścia HTTP API) {#endpoint}

Konkretna trasa HTTP udostępniana przez kontroler ASP.NET Core. Składa się z: metody HTTP (GET/POST/PUT/DELETE), ścieżki URL, opcjonalnych parametrów oraz DTO żądania i odpowiedzi. W dokumentacji identyfikowany prefiksem `API-`, np. `API-PostAuthRegister`. Każdy endpoint chroniony atrybutem `[Authorize]` (z wyjątkiem endpointów autoryzacji).

### JWT (JSON Web Token) {#jwt}

Bezstanowy token uwierzytelniający generowany przez `AuthService.CreateToken()`. W projekcie podpisywany algorytmem HmacSha512, ważny 10 minut, przechowywany po stronie klienta w `localStorage`. Zawiera claimy: `userId`, `email`, `role`. Weryfikowany przez middleware ASP.NET Core; `ValidateIssuer` i `ValidateAudience` ustawione na `false` (anomalia A-WYS-03). ClockSkew ustawiony na `TimeSpan.Zero`.

### BCrypt {#bcrypt}

Adaptacyjna funkcja haszowania haseł stosowana do zabezpieczania haseł użytkowników. Biblioteka: `BCrypt.Net-Next 4.0.3`. Work factor: 11. Weryfikacja hasła: `BCrypt.Verify(password, hash)`. Brak możliwości odwrócenia hasła — przechowywany wyłącznie hash.

### AutoMapper {#automapper}

Biblioteka .NET do automatycznego mapowania obiektów (DTO ↔ Encja). W projekcie konfigurowana przez Profile: np. `UserProfile`, `DocumentProfile`, `UserFirmProfile`. Rejestrowana w DI jako singleton. Anomalia: inline LINQ projekcja w profilu AutoMapper zamiast osobnego mapowania (A-NIS-03).

### Unit of Work {#unit-of-work}

Wzorzec projektowy agregujący operacje na wielu repozytoriach w jednej transakcji. W projekcie implementowany przez interfejs `IUnitOfWork` i klasę `UnitOfWork`. Metoda `CompleteAsync()` jest aliasem dla `SaveChangesAsync()` z DbContext EF Core — zatwierdza wszystkie oczekujące zmiany w jednej operacji.

### ExceptionMiddleware {#exceptionmiddleware}

Middleware ASP.NET Core rejestrowany w `Program.cs`, przechwytujący nieobsłużone wyjątki domenowe i mapujący je na odpowiednie kody HTTP (np. `NotFoundException` → 404, `BadRequestException` → 400). Wyjątki niezidentyfikowane zwracają kod 500 z wiadomością `ex.Message` (anomalia A-WYS-06 — ujawnienie szczegółów błędów).

### QuestPDF {#questpdf}

Biblioteka .NET Community do generowania dokumentów PDF w kodzie C#. W projekcie używana do generowania faktur przez `DocumentService.GenerateInvoicePdf()`. Szablon dokumentu: `InvoiceDocument`. Fabryka: `InvoiceDocumentFactory`. Anomalia: `GenerateInvoicePdf` hardkoduje `new InvoiceDocument()` zamiast wybierać szablon na podstawie `DocumentTypeId` (A-KRIT-04).

### EF Core (Entity Framework Core) {#ef-core}

ORM (Object-Relational Mapper) firmy Microsoft dla platformy .NET. Wersja używana w projekcie: EF Core 8. Mapuje encje C# (np. `Document`, `Firm`, `User`) na tabele SQL Server. Migracje zarządzane przez narzędzie `dotnet ef migrations`. Kontekst bazy danych: `InvoiceJetDbContext`. Metody eager loading: `Include()` i `ThenInclude()`.

### Repository (wzorzec repozytorium) {#repository}

Wzorzec projektowy izolujący logikę dostępu do danych. W projekcie każda encja ma swoje repozytorium (interfejs + implementacja), np. `IDocumentRepository` / `DocumentRepository`. Repozytoria korzystają z EF Core i `InvoiceJetDbContext`. Wstrzykiwane przez Dependency Injection do serwisów. Uwaga: brak `AsNoTracking()` w zapytaniach read-only (anomalia A-NIS-05).

### Clean Architecture {#clean-architecture}

Architektura warstwowa zastosowana w projekcie InvoiceJet. Warstwy i zależności: `Presentation` (kontrolery) → `Application` (serwisy, DTO, interfejsy) ← `Infrastructure` (repozytoria, DbContext, implementacje). Warstwa `Domain` zawiera encje i wyjątki. Zależności wskazują do wewnątrz — `Infrastructure` implementuje interfejsy zdefiniowane w `Application`.

### Dependency Injection (wstrzykiwanie zależności) {#di}

Mechanizm frameworka ASP.NET Core do zarządzania zależnościami między komponentami. W projekcie używany do rejestracji i wstrzykiwania: serwisów, repozytoriów, UnitOfWork, AutoMapper, DbContext, QuestPDF i pozostałych komponentów. Konfiguracja w `Program.cs`. Skrót w dokumentacji: DI.

### UserFirmId {#userfirmid}

Identyfikator izolacji danych — klucz obcy łączący zasoby z konkretną parą użytkownik-firma. Pobierany z claimu JWT (`userId`) na poziomie serwisu lub kontrolera i używany jako filtr we wszystkich zapytaniach LINQ. Każde repozytorium filtruje rekordy po `UserFirmId`, zapobiegając dostępowi do danych innych użytkowników.

### claim (roszczenie JWT) {#claim}

Jednostka informacji osadzona wewnątrz tokenu JWT. W projekcie token zawiera trzy claimy: `userId` (identyfikator powiązania użytkownik-firma, typ: `ClaimTypes.NameIdentifier`), `email` (adres e-mail, typ: `ClaimTypes.Email`), `role` (rola użytkownika, typ: `ClaimTypes.Role` — zawsze wartość `"User"`).

### race condition (wyścig w dostępie do zasobu) {#race-condition}

Stan błędu wynikający z równoczesnego dostępu dwóch lub więcej żądań HTTP do tego samego zasobu bez mechanizmu blokowania. W projekcie zidentyfikowany przy inkrementacji `DocumentSeries.CurrentNumber` w metodzie `DocumentService.AddDocument()` — dwa równoległe żądania mogą wygenerować ten sam numer dokumentu (anomalia A-KRIT-03). Brak mechanizmu optymistycznej lub pesymistycznej blokady.

### CASCADE DELETE (kaskadowe usuwanie) {#cascade-delete}

Mechanizm SQL Server (i EF Core) automatycznie usuwający rekordy potomne przy usunięciu rekordu nadrzędnego. W projekcie skonfigurowany m.in. dla relacji `BankAccount` → `Document` — usunięcie konta bankowego usuwa wszystkie powiązane dokumenty bez ostrzeżenia w UI (anomalia A-KRIT-01).

### hard delete (fizyczne usuwanie) {#hard-delete}

Strategia usuwania danych polegająca na fizycznym usunięciu rekordu z bazy danych (`DELETE FROM`). Projekt InvoiceJet stosuje wyłącznie hard delete — brak mechanizmu soft delete (flaga `IsDeleted`, `DeletedAt`). Oznacza to brak możliwości odtworzenia usuniętych danych bez kopii zapasowej.

---

## Wątpliwości i braki

| ID | Wątpliwość | Status |
|---|---|---|
| W-01 | Jakie dokładnie wyjątki domenowe obsługuje `ExceptionMiddleware`? Brak pełnej listy w kodzie. | Do_zdefiniowania |
| W-02 | Czy `IUnitOfWork` implementuje rollback? Nie znaleziono jawnego `BeginTransactionAsync()`. | Do_zdefiniowania |
| W-03 | Wersja AutoMapper — nie podano w dokumentacji. Wymaga weryfikacji z `*.csproj`. | Do_zdefiniowania |

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — 18 pojęć technicznych. |
