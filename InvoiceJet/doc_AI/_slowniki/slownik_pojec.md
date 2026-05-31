# Słownik pojęć — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pojęcia domenowe

| Termin | Definicja |
|---|---|
| **Factura** | Rumuńska faktura VAT (typ dokumentu 1) |
| **Factura Proforma** | Dokument proforma — oferta przed fakturą właściwą (typ 2) |
| **Factura Storno** | Faktura korygująca / anulująca (typ 3) |
| **CUI** | Cod Unic de Înregistrare — rumuński numer identyfikacyjny firmy (odpowiednik NIP) |
| **ANAF** | Agenția Națională de Administrare Fiscală — rumuński urząd skarbowy |
| **RegCom** | Numer rejestracji w rejestrze handlowym (KRS w Polsce) |
| **Județ** | Rumuski okręg administracyjny (odpowiednik województwa) — pole `County` |
| **RON** | Lej rumuński — podstawowa waluta |
| **TVA** | Taxa pe Valoare Adăugată — podatek VAT (po rumuńsku) |
| **Serie** | Seria numeracji dokumentu — prefiks + licznik (np. "FV" + 0015) |
| **UserFirm** | Encja pośrednicząca łącząca użytkownika z jego firmą wystawiającą |
| **Seller** | Sprzedawca — własna firma użytkownika wystawiającego dokument |
| **Client** | Klient — firma odbiorcy dokumentu |

## Pojęcia techniczne

| Termin | Definicja |
|---|---|
| **JWT** | JSON Web Token — bezstanowy token uwierzytelniający (10 minut) |
| **BCrypt** | Adaptacyjna funkcja haszowania haseł — BCrypt.Net-Next 4.0.3 |
| **HmacSha512** | Algorytm podpisywania JWT |
| **AuthGuard** | Angular Route Guard sprawdzający ważność JWT przed wejściem na trasę |
| **JwtInterceptor** | Angular HTTP Interceptor dodający nagłówek `Authorization: Bearer` |
| **BaseInvoiceComponent** | Abstrakcyjna klasa bazowa dla formularzy dokumentów (faktura/proforma/storno) |
| **UoW** | Unit of Work — wzorzec agregujący repozytoria; `CompleteAsync()` = `SaveChangesAsync()` |
| **Hard Delete** | Fizyczne usunięcie rekordu z bazy (brak soft-delete w projekcie) |
| **D4** | Format liczby z 4 cyframi (`ToString("D4")`): 1→`0001`, 15→`0015` |
| **QuestPDF** | Biblioteka do generowania PDF w .NET — wersja Community |
| **EF Core** | Entity Framework Core 8 — ORM dla .NET |
| **AutoMapper** | Biblioteka do mapowania obiektów (DTO↔Encja) |
| **ExceptionMiddleware** | Middleware ASP.NET Core przechwytujący wyjątki domenowe i mapujący na HTTP codes |
| **CASCADE DELETE** | Automatyczne usuwanie powiązanych rekordów przy usunięciu rekordu nadrzędnego |
| **Race condition** | Stan wyścigu — błąd gdy dwa równoległe żądania modyfikują ten sam zasób |
| **ClockSkew** | Tolerancja zegarowa przy weryfikacji JWT — ustawiona na `TimeSpan.Zero` |
| **Include/ThenInclude** | EF Core metody do ładowania powiązanych encji (eager loading) |
| **CORS** | Cross-Origin Resource Sharing — polityka dozwolonych źródeł HTTP |
| **InvoiceDocumentFactory** | Fabryka PDF tworząca właściwy szablon na podstawie `DocumentTypeId` |

## Skróty ID dokumentacyjnych

| Skrót | Pełna nazwa |
|---|---|
| EKRAN-XX | Ekran (widok) aplikacji Angular |
| DIALOG-XX | Dialog modalny Angular Material |
| LAYOUT-XX | Komponent layoutu (Navbar, Sidebar) |
| BASE-XX | Klasa bazowa (abstrakcyjna) |
| P-XX | Proces techniczny (backend) |
| ALG-XX | Algorytm / mechanizm |
| DTO-XX | Data Transfer Object |
| AM-XX | AutoMapper Profile |
| LINQ-XX | Zapytanie LINQ/EF Core |
| UC-XX | Use Case |
| API-XX | Endpoint API |
| DT-XX | Dane testowe (fixture) |
| WAL-XX | Walidacja / reguła biznesowa |
| LT-XX | Dług techniczny (Long-term issue) |
| FA-XX | Anomalia funkcjonalna |
| DA-XX | Anomalia danych |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
